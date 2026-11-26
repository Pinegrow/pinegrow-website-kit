// Promo images of the kit: real screenshots of website/ in headless Chrome, composed into images for the email,
// the gift page and the README. Needs Node 22+ (built-in WebSocket) and Google Chrome; no npm packages.
//
//   node tools/promo_shots.mjs            all images into promo/
//   node tools/promo_shots.mjs designs    only the named steps (shots, starters, designs, blocks, pages, examples, gif)
//
// The saved designs (projectdb.pgml) are colour and font variables, so other designs than the active one are shown
// by overriding --color-* and --font-* on :root, with the design's Google Fonts loaded.

import { spawn, execFileSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { pathToFileURL, fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const SITE = path.join(ROOT, "website");
const OUT = path.join(ROOT, "promo");
const SHOTS = path.join(OUT, "shots");
const CHROME = process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";

const STARTERS = [
    ["index-architecture.html", "Northlight Interiors", "Interior design studio"],
    ["index-agency.html", "Field Office", "Web agency"],
    ["index-physio.html", "Movewell Physio", "Physiotherapy clinic"],
    ["index-cafe.html", "Ember & Oat", "Café and bakery"],
    ["index-portfolio.html", "Ana Ruiz", "Photographer"],
    ["index-personal.html", "Sam Rivera", "Writer"],
];
// Kits the kit-builder skill made with an AI agent (examples/<folder>/website).
const EXAMPLES = [
    ["crux-climbing", "Crux Climbing", "Bouldering gym"],
    ["splash-swim-school", "Splash Swim School", "Swimming lessons"],
    ["willowbend-dental", "Willowbend Family Dental", "Dental practice"],
    ["still-water-yoga", "Still Water Yoga", "Yoga studio"],
];
const SITE_PAGES = ["index.html", "about.html", "contact.html", "journal.html", "post.html", "404.html"];
const BLOCK_PAGES = ["headers-footers", "heroes", "services-pricing", "work", "story-team", "testimonials",
    "contact-calls-to-action", "posts"];

// ---------- saved designs ----------

function readDesigns() {
    const pgml = fs.readFileSync(path.join(SITE, "projectdb.pgml"), "utf8");
    const designs = [];
    const re = /<dmdesign id="([^"]+)" name="([^"]+)"([^>]*)>([\s\S]*?)<\/dmdesign>/g;
    let m;
    while ((m = re.exec(pgml))) {
        const body = m[4];
        const colors = {};
        for (const c of body.matchAll(/<dmcolor key="([\w-]+)" color="([^"]+)"/g)) {
            colors[c[1]] = c[2];
        }
        const fonts = /skill="fonts"([^>]*)>/.exec(body)[1];
        const attr = (name) => (new RegExp(`${name}="([^"]+)"`).exec(fonts) || [])[1];
        designs.push({
            id: m[1], name: m[2], active: /\bactive\b/.test(m[3]), colors,
            sans: attr("family_1"), display: attr("family_3"), mono: attr("family_4"),
        });
    }
    return designs;
}

function designCss(d) {
    const families = [...new Set([d.sans, d.display, d.mono])]
        .map((f) => `family=${f.replace(/ /g, "+")}:wght@400;500;600;700;800`).join("&");
    const fallback = "system-ui, -apple-system, sans-serif";
    const vars = Object.entries(d.colors).map(([k, v]) => `--color-${k}: ${v};`).join(" ");
    return {
        fontsUrl: `https://fonts.googleapis.com/css2?${families}&display=swap`,
        css: `:root, :host { ${vars} --font-sans: '${d.sans}', ${fallback}; --font-display: '${d.display}', ${fallback};
            --font-mono: '${d.mono}', ${fallback}; }`,
    };
}

// ---------- a small DevTools protocol client ----------

async function startChrome() {
    const profile = fs.mkdtempSync(path.join(os.tmpdir(), "kit-promo-"));
    const proc = spawn(CHROME, ["--headless=new", "--remote-debugging-port=0", `--user-data-dir=${profile}`,
        "--hide-scrollbars", "--no-first-run", "--no-default-browser-check", "--allow-file-access-from-files",
        "about:blank"], { stdio: "ignore" });
    const portFile = path.join(profile, "DevToolsActivePort");
    for (let i = 0; i < 100 && !fs.existsSync(portFile); i++) {
        await sleep(100);
    }
    const [port, wsPath] = fs.readFileSync(portFile, "utf8").trim().split("\n");
    const ws = new WebSocket(`ws://127.0.0.1:${port}${wsPath}`);
    await new Promise((resolve, reject) => {
        ws.onopen = resolve;
        ws.onerror = reject;
    });
    let nextId = 1;
    const pending = new Map();
    const listeners = [];
    ws.onmessage = (ev) => {
        const msg = JSON.parse(ev.data);
        if (msg.id && pending.has(msg.id)) {
            const { resolve, reject } = pending.get(msg.id);
            pending.delete(msg.id);
            if (msg.error) {
                reject(new Error(msg.error.message));
            } else {
                resolve(msg.result);
            }
        } else if (msg.method) {
            listeners.forEach((l) => l(msg));
        }
    };
    const send = (method, params = {}, sessionId) => new Promise((resolve, reject) => {
        const id = nextId++;
        pending.set(id, { resolve, reject });
        ws.send(JSON.stringify({ id, method, params, sessionId }));
    });
    const { targetId } = await send("Target.createTarget", { url: "about:blank" });
    const { sessionId } = await send("Target.attachToTarget", { targetId, flatten: true });
    const page = (method, params) => send(method, params, sessionId);
    await page("Page.enable");
    await page("Runtime.enable");
    const waitFor = (method) => new Promise((resolve) => {
        const l = (msg) => {
            if (msg.method === method && msg.sessionId === sessionId) {
                listeners.splice(listeners.indexOf(l), 1);
                resolve(msg.params);
            }
        };
        listeners.push(l);
    });
    const close = async () => {
        ws.close();
        const exited = new Promise((r) => proc.once("exit", r));
        proc.kill();
        await exited;
        fs.rmSync(profile, { recursive: true, force: true, maxRetries: 5, retryDelay: 200 });
    };
    return { page, waitFor, close };
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function evaluate(b, expression) {
    const r = await b.page("Runtime.evaluate", { expression, awaitPromise: true, returnByValue: true });
    if (r.exceptionDetails) {
        throw new Error(r.exceptionDetails.exception?.description || r.exceptionDetails.text);
    }
    return r.result.value;
}

// Opens a page at the given viewport, optionally in a design, and waits for fonts and images.
async function open(b, file, { width = 1440, height = 900, design = null, scale = 2 } = {}) {
    await b.page("Emulation.setDeviceMetricsOverride", { width, height, deviceScaleFactor: scale, mobile: false });
    const loaded = b.waitFor("Page.loadEventFired");
    await b.page("Page.navigate", { url: pathToFileURL(file).href });
    await loaded;
    if (design) {
        const { css, fontsUrl } = designCss(design);
        await evaluate(b, `new Promise((resolve) => {
            const link = document.createElement("link");
            link.rel = "stylesheet";
            link.href = ${JSON.stringify(fontsUrl)};
            link.onload = link.onerror = resolve;
            document.head.appendChild(link);
            const style = document.createElement("style");
            style.textContent = ${JSON.stringify(css)};
            document.head.appendChild(style);
        })`);
    }
    // Hide the skip link and anything that only shows on focus; make lazy images load.
    await evaluate(b, `(async () => {
        const style = document.createElement("style");
        style.textContent = ".skip-link { display: none !important; } * { scroll-behavior: auto !important; }";
        document.head.appendChild(style);
        document.querySelectorAll("img[loading=lazy]").forEach((img) => img.loading = "eager");
        await Promise.all([...document.images].map((img) => img.complete ? null :
            new Promise((r) => { img.onload = img.onerror = r; })));
        await document.fonts.ready;
    })()`);
    await sleep(300);
}

async function screenshot(b, out, { fullPage = false, clip = null } = {}) {
    const params = { format: "png", captureBeyondViewport: fullPage || !!clip };
    if (fullPage) {
        const size = await evaluate(b, `({ w: document.documentElement.scrollWidth,
            h: document.documentElement.scrollHeight })`);
        params.clip = { x: 0, y: 0, width: size.w, height: size.h, scale: 1 };
    } else if (clip) {
        params.clip = { ...clip, scale: 1 };
    }
    const { data } = await b.page("Page.captureScreenshot", params);
    fs.mkdirSync(path.dirname(out), { recursive: true });
    fs.writeFileSync(out, Buffer.from(data, "base64"));
    return out;
}

// Renders a composed HTML page (in promo/compose/) to a PNG of the given size.
async function compose(b, name, html, width, height) {
    const dir = path.join(OUT, "compose");
    fs.mkdirSync(dir, { recursive: true });
    const file = path.join(dir, `${name}.html`);
    fs.writeFileSync(file, html);
    // Height 0: as tall as the composed page.
    await open(b, file, { width, height: height || 900, scale: 1 });
    await screenshot(b, path.join(OUT, `${name}.png`), { fullPage: !height });
    console.log(`promo/${name}.png`);
}

const shot = (name) => `../shots/${name}`;

const COMPOSE_STYLE = `
    @import url("https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;600;700;800&display=swap");
    * { box-sizing: border-box; margin: 0; }
    body { font-family: "Hanken Grotesk", system-ui, sans-serif; color: #1e1c19; }
    .frame { border-radius: 14px; overflow: hidden; background: #fff;
        box-shadow: 0 1px 2px rgba(0,0,0,.12), 0 18px 50px -12px rgba(0,0,0,.35); }
    .bar { height: 34px; background: #e9e6df; display: flex; align-items: center; gap: 8px; padding: 0 14px; }
    .bar i { width: 11px; height: 11px; border-radius: 50%; background: #cfc9bd; display: block; }
    .frame img { display: block; width: 100%; }
    .label { margin-top: 16px; font-size: 22px; font-weight: 700; }
    .label span { font-weight: 400; opacity: .65; margin-left: 8px; }
`;
const frame = (src, bar = true) => `<div class="frame">${bar ? `<div class="bar"><i></i><i></i><i></i></div>` : ""}
    <img src="${src}"></div>`;

// ---------- steps ----------

async function shots(b, designs) {
    for (const [file] of STARTERS) {
        await open(b, path.join(SITE, file));
        await screenshot(b, path.join(SHOTS, file.replace(".html", ".png")));
        await screenshot(b, path.join(SHOTS, file.replace(".html", "-full.png")), { fullPage: true });
    }
    for (const file of SITE_PAGES) {
        await open(b, path.join(SITE, file));
        await screenshot(b, path.join(SHOTS, file.replace(".html", ".png")));
        await screenshot(b, path.join(SHOTS, file.replace(".html", "-full.png")), { fullPage: true });
    }
    for (const d of designs) {
        await open(b, path.join(SITE, "index.html"), { design: d });
        await screenshot(b, path.join(SHOTS, `design-${d.id}.png`));
        await open(b, path.join(SITE, "index-cafe.html"), { design: d });
        await screenshot(b, path.join(SHOTS, `design-cafe-${d.id}.png`));
    }
    // Every block of the library, cut from its category page.
    const blocks = [];
    for (const name of BLOCK_PAGES) {
        await open(b, path.join(SITE, "blocks", `${name}.html`));
        const rects = await evaluate(b, `[...document.querySelectorAll("[cms-block]")]
            .filter((el) => !el.parentElement.closest("[cms-block]"))
            .map((el) => { const r = el.getBoundingClientRect();
                return { id: el.getAttribute("cms-block"), x: r.left, y: r.top + window.scrollY,
                    width: r.width, height: r.height }; })`);
        for (const r of rects) {
            if (r.width < 200 || r.height < 40) {
                continue;
            }
            const out = `block-${r.id}.png`;
            await screenshot(b, path.join(SHOTS, out), { clip: { x: r.x, y: r.y, width: r.width, height: r.height } });
            blocks.push({ id: r.id, page: name, file: out, width: r.width, height: r.height });
        }
    }
    fs.writeFileSync(path.join(SHOTS, "blocks.json"), JSON.stringify(blocks, null, 1));
    console.log(`${blocks.length} blocks`);
}

async function examples(b) {
    for (const [dir] of EXAMPLES) {
        const file = path.join(ROOT, "examples", dir, "website", "index.html");
        await open(b, file);
        await screenshot(b, path.join(SHOTS, `example-${dir}.png`));
        await screenshot(b, path.join(SHOTS, `example-${dir}-full.png`), { fullPage: true });
    }
    const cards = EXAMPLES.map(([dir, name, what]) => `<div>${frame(shot(`example-${dir}.png`))}
        <p class="label">${name}<span>${what}</span></p></div>`).join("");
    await compose(b, "examples-grid", `<!doctype html><style>${COMPOSE_STYLE}
        body { background: #e8e2d4; padding: 80px; }
        .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 56px 48px; }
    </style><div class="grid">${cards}</div>`, 2400, 0);
    for (const [dir] of EXAMPLES) {
        await compose(b, `page-example-${dir}`, `<!doctype html><style>${COMPOSE_STYLE}
            body { background: #e8e2d4; padding: 40px; }
            .frame img { max-height: 3200px; object-fit: cover; object-position: top; }
        </style>${frame(shot(`example-${dir}-full.png`))}`, 1520, 0);
    }
}

async function starters(b) {
    const cards = STARTERS.map(([file, name, what]) => `<div>${frame(shot(file.replace(".html", ".png")))}
        <p class="label">${name}<span>${what}</span></p></div>`).join("");
    await compose(b, "starters-grid", `<!doctype html><style>${COMPOSE_STYLE}
        body { background: #f2eee5; padding: 80px; }
        .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 56px 48px; }
    </style><div class="grid">${cards}</div>`, 2400, 0);
}

async function designsImage(b, designs) {
    const order = ["linen", "clear", "night", "pine"].map((id) => designs.find((d) => d.id === id));
    for (const [prefix, name] of [["design-", "designs"], ["design-cafe-", "designs-cafe"]]) {
        const cards = order.map((d) => `<div>${frame(shot(`${prefix}${d.id}.png`))}
            <p class="label" style="color: #fff">${d.name}<span>${[...new Set([d.display, d.sans])].join(" · ")}</span></p></div>`).join("");
        await compose(b, name, `<!doctype html><style>${COMPOSE_STYLE}
            body { background: #1e1c19; padding: 80px; }
            .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 56px 48px; }
        </style><div class="grid">${cards}</div>`, 2400, 0);
    }
}

async function blocksImage(b) {
    const blocks = JSON.parse(fs.readFileSync(path.join(SHOTS, "blocks.json"), "utf8"))
        .filter((x) => !/^(header|footer)/.test(x.id) && x.height < 1400);
    // Columns of block thumbnails, filled shortest column first, cut at the bottom.
    const columns = 5;
    const cols = Array.from({ length: columns }, () => ({ h: 0, items: [] }));
    for (const blk of blocks) {
        const col = cols.reduce((a, c) => (c.h < a.h ? c : a));
        col.items.push(blk);
        col.h += blk.height / blk.width + 0.03;
    }
    const html = cols.map((c) => `<div class="col">${c.items.map((x) => frame(shot(x.file), false)).join("")}</div>`)
        .join("");
    await compose(b, "blocks-mosaic", `<!doctype html><style>${COMPOSE_STYLE}
        body { background: #e8e2d4; padding: 48px; height: 1500px; overflow: hidden; }
        .cols { display: grid; grid-template-columns: repeat(${columns}, 1fr); gap: 28px; }
        .col { display: flex; flex-direction: column; gap: 28px; }
        .frame { border-radius: 8px; }
    </style><div class="cols">${html}</div>`, 2400, 1500);
}

async function pages(b) {
    // Tall browser-framed pages, for the README and the gift page.
    for (const file of ["index.html", ...STARTERS.map((s) => s[0])]) {
        const base = file.replace(".html", "");
        await compose(b, `page-${base}`, `<!doctype html><style>${COMPOSE_STYLE}
            body { background: #f2eee5; padding: 40px; }
            .frame img { max-height: 3200px; object-fit: cover; object-position: top; }
        </style>${frame(shot(`${base}-full.png`))}`, 1520, 0);
    }
    // Wide README banner: the general site with two starters beside it.
    await compose(b, "readme-banner", `<!doctype html><style>${COMPOSE_STYLE}
        body { background: #f2eee5; padding: 60px; height: 1000px; overflow: hidden; }
        .row { display: grid; grid-template-columns: 1.5fr 1fr 1fr; gap: 40px; align-items: start; }
        .row > div:nth-child(2) { margin-top: 90px; } .row > div:nth-child(3) { margin-top: 180px; }
    </style><div class="row">${frame(shot("index-full.png"))}${frame(shot("index-cafe-full.png"))}
        ${frame(shot("index-architecture-full.png"))}</div>`, 2400, 1000);
}

function gif(designs) {
    // The general site's hero cycling through the four designs.
    const order = ["linen", "clear", "night", "pine"];
    const list = path.join(OUT, "compose", "gif.txt");
    fs.writeFileSync(list, order.map((id) => `file '${path.join(SHOTS, `design-${id}.png`)}'\nduration 1.6`)
        .join("\n") + `\nfile '${path.join(SHOTS, `design-${order[order.length - 1]}.png`)}'\n`);
    const out = path.join(OUT, "designs.gif");
    execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", list, "-vf",
        "scale=1200:-1:flags=lanczos,split[a][b];[a]palettegen=stats_mode=full[p];[b][p]paletteuse=dither=sierra2_4a",
        "-loop", "0", out]);
    console.log("promo/designs.gif");
}

async function main() {
    const steps = process.argv.slice(2);
    const want = (s) => !steps.length || steps.includes(s);
    const designs = readDesigns();
    const b = await startChrome();
    try {
        if (want("shots")) {
            await shots(b, designs);
        }
        if (want("starters")) {
            await starters(b);
        }
        if (want("designs")) {
            await designsImage(b, designs);
        }
        if (want("blocks")) {
            await blocksImage(b);
        }
        if (want("pages")) {
            await pages(b);
        }
        if (want("examples")) {
            await examples(b);
        }
    } finally {
        await b.close();
    }
    if (want("gif")) {
        gif(designs);
    }
}

await main();
