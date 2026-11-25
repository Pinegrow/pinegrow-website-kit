#!/usr/bin/env python3
"""Helper for building Pinegrow website kits (Tailwind CSS projects, Pinegrow 10.1 and later).

  python3 kit.py init KIT        create the kit folders and an empty Pinegrow Tailwind CSS project
  python3 kit.py designs KIT     write the saved designs from source/designs.json and activate their Google fonts
  python3 kit.py styles KIT      write the component styles from source/styles.txt
  python3 kit.py images KIT      make grey placeholders for images the pages and blocks use but don't exist
  python3 kit.py optimize KIT    write every image the pages use from its original in source/images/, at the size
                                 the page asks for, as WebP when the src ends in .webp
  python3 kit.py fit SRC OUT WxH  resize and center-crop one image to exactly W x H (.webp or .jpg)
  python3 kit.py library KIT     build the block library (website/blocks/) from source/blocks/
  python3 kit.py check KIT       check the kit and list what to fix

KIT is the kit folder: it holds KIT-BRIEF.md, source/ and website/ (the Pinegrow project).
Close the project in Pinegrow before running designs, styles or library, then open it again.
Only the Python standard library is used.
"""
import html
import html.parser
import json
import os
import re
import shutil
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)

FORBIDDEN_IN_STYLES = ("group", "peer", "not-prose")
LIBRARY_HOME = "blocks/kit-blocks.html"


# ---------------------------------------------------------------------------------------------------------------------
# Small helpers

def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def write_new(path, text):
    """Writes only if the file doesn't exist yet."""
    if not os.path.exists(path):
        write(path, text)
        return True
    return False


def load_json(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    write(path, json.dumps(data, indent=1, ensure_ascii=False) + "\n")


def attr(value):
    """Attribute value for projectdb.pgml. Pinegrow stores & and > raw, so only quotes are escaped."""
    return value.replace('"', "&quot;")


def replace_block(text, tag, new, after=None):
    """Replaces <tag>...</tag> (or a self-closing <tag .../>) in text, or inserts new after `after`."""
    m = re.search(rf"[ \t]*<{tag}\b[^>]*?(/>|>.*?</{tag}>)\n?", text, re.S)
    if m:
        return text[:m.start()] + new + text[m.end():]
    if after and after in text:
        i = text.index(after) + len(after)
        return text[:i] + "\n" + new + text[i:]
    i = text.rindex("</project>")
    return text[:i] + new + text[i:]


def paths(kit):
    kit = os.path.abspath(kit)
    return {
        "kit": kit,
        "brief": os.path.join(kit, "KIT-BRIEF.md"),
        "source": os.path.join(kit, "source"),
        "designs": os.path.join(kit, "source", "designs.json"),
        "styles": os.path.join(kit, "source", "styles.txt"),
        "blocks": os.path.join(kit, "source", "blocks"),
        "web": os.path.join(kit, "website"),
        "pj": os.path.join(kit, "website", "pinegrow.json"),
        "db": os.path.join(kit, "website", "projectdb.pgml"),
        "fonts": os.path.join(kit, "website", "_pginfo", "fonts.json"),
        "css": os.path.join(kit, "website", "tailwind_theme", "tailwind.css"),
    }


# ---------------------------------------------------------------------------------------------------------------------
# init

BRIEF = """# Kit brief

Purpose:
Businesses and pages:
CSS: Tailwind CSS
WordPress: no
Designs: 3
Block library: yes
Publishing:
Images:

## Concept

## Color roles

## Fonts

## Saved designs

## Notes
"""

DESIGNS_EXAMPLE = {
    "active": "first",
    "designs": [
        {"id": "first", "name": "First", "colors": {
            "page": "#f4f1ea", "surface": "#e9e4d8", "ink": "#1d1b18", "muted": "#6b655b", "line": "#d6cfbf",
            "primary": "#b4432a", "on-primary": "#fff8f1", "band": "#1d1b18", "on-band": "#f4f1ea"},
         "fonts": {"sans": "Hanken Grotesk", "display": "Hanken Grotesk", "mono": "IBM Plex Mono"}},
    ],
}

STYLES_EXAMPLE = """# Component styles: one per line, ".class-name: utility classes". Lines starting with a space continue the
# previous style. Use only design colors and fonts. Never use group, peer or not-prose here; put them on the element.

.container-site: mx-auto w-full max-w-7xl px-5 md:px-10
.section: bg-page py-20 md:py-28
.btn-primary: inline-flex items-center justify-center gap-2 bg-primary px-5 py-3 text-sm font-semibold text-on-primary
 hover:opacity-90
"""

PINEGROW_JSON = {
    "files": {},
    "breakpoints": [],
    "frameworks": ["pg.tw.lib", "tw"],
    "template_framework_id": "tailwind",
    "active-design-provider": "tw",
    "design-settings": {"mode": "jit4", "external_source_url": None, "custom_source_url": None},
}


def cmd_init(kit):
    p = paths(kit)
    made = []
    for path, text in [(p["brief"], BRIEF), (p["styles"], STYLES_EXAMPLE),
                       (p["designs"], json.dumps(DESIGNS_EXAMPLE, indent=1) + "\n"),
                       (p["db"], "<project>\n    <documents></documents>\n</project>\n"),
                       (p["css"], "/* Pinegrow compiles this file. Open every page in Pinegrow to fill it. */\n")]:
        if write_new(path, text):
            made.append(os.path.relpath(path, p["kit"]))
    if not os.path.exists(p["pj"]):
        save_json(p["pj"], PINEGROW_JSON)
        made.append("website/pinegrow.json")
    if not os.path.exists(p["fonts"]):
        save_json(p["fonts"], {"activated": []})
        made.append("website/_pginfo/fonts.json")
    os.makedirs(os.path.join(p["blocks"]), exist_ok=True)
    os.makedirs(os.path.join(p["web"], "images"), exist_ok=True)
    form_src = os.path.join(SKILL, "form")
    form_dst = os.path.join(p["web"], "form")
    if os.path.isdir(form_src) and not os.path.exists(form_dst):
        shutil.copytree(form_src, form_dst)
        made.append("website/form/")
    print("Created: " + (", ".join(made) if made else "nothing, everything exists already"))


# ---------------------------------------------------------------------------------------------------------------------
# designs

FONT_SLOTS = {"sans": 1, "display": 3, "mono": 4}
FONT_DEFAULT_CATEGORY = {"sans": "sans", "display": "sans", "mono": "monospace"}
FONT_CATEGORIES = ("sans", "serif", "display", "handwriting", "monospace")
FONT_FALLBACK = {"sans": "system-ui, -apple-system, sans-serif", "display": "system-ui, -apple-system, sans-serif",
                 "handwriting": "cursive", "serif": 'Georgia, Cambria, "Times New Roman", serif',
                 "monospace": 'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace'}


def font_family(value):
    """A font in designs.json is a family name, or {"family": ..., "category": "serif", "weights": [...]}."""
    return value.get("family", "") if isinstance(value, dict) else value
BACKGROUND = ('<dmdesignskill skill="background" image_for_colors="true" advanced="true" filter_blur="0" '
              'filter_brightness="100" filter_contrast="100" filter_grayscale="0" filter_hue-rotate="0" '
              'filter_invert="0" filter_opacity="100" filter_saturate="100" filter_sepia="0"></dmdesignskill>')
COLOR_NAME = re.compile(r"^[a-z][a-z0-9-]*$")
COLOR_VALUE = re.compile(r"^(#[0-9a-fA-F]{3,8}|oklch\([^)]*\))$")


def design_problems(data):
    problems = []
    designs = data.get("designs") or []
    if not designs:
        return ["designs.json has no designs"]
    defaults = load_json(os.path.join(HERE, "tw-default-colors.json"), {})
    names = None
    for d in designs:
        did = d.get("id", "?")
        if not re.match(r"^[a-z0-9-]+$", did):
            problems.append(f"design id '{did}' must be lowercase letters, digits and -")
        cols = d.get("colors") or {}
        for k, v in cols.items():
            if not COLOR_NAME.match(k):
                problems.append(f"{did}: color name '{k}' must be lowercase letters, digits and -")
            if k in defaults:
                problems.append(f"{did}: color name '{k}' would replace a default Tailwind color; pick another name")
            if not COLOR_VALUE.match(str(v)):
                problems.append(f"{did}: color '{k}' has an unsupported value '{v}' (use #hex or oklch())")
        if names is None:
            names = list(cols)
        elif sorted(names) != sorted(cols):
            problems.append(f"{did}: colors differ from the first design ({sorted(set(names) ^ set(cols))}); "
                            "every design needs the same color names")
        fonts = d.get("fonts") or {}
        for k, v in fonts.items():
            if k not in FONT_SLOTS:
                problems.append(f"{did}: font '{k}' is not one of sans, display, mono")
            if not font_family(v):
                problems.append(f"{did}: font '{k}' has no family")
            if isinstance(v, dict) and v.get("category", "sans") not in FONT_CATEGORIES:
                problems.append(f"{did}: font '{k}' category must be one of {', '.join(FONT_CATEGORIES)}")
        if "sans" not in fonts:
            problems.append(f"{did}: set fonts.sans")
    if data.get("active") not in [d.get("id") for d in designs]:
        problems.append("'active' must be the id of one of the designs")
    return problems


def cmd_designs(kit):
    p = paths(kit)
    data = load_json(p["designs"])
    if data is None:
        sys.exit(f"Missing {p['designs']}")
    problems = design_problems(data)
    if problems:
        sys.exit("designs.json:\n  " + "\n  ".join(problems))
    defaults = load_json(os.path.join(HERE, "tw-default-colors.json"))

    out = ["    <dmdesigns>"]
    for d in data["designs"]:
        active = " active" if d["id"] == data["active"] else ""
        out.append(f'        <dmdesign id="{attr(d["id"])}" name="{attr(d.get("name", d["id"]))}"{active}>')
        out.append('            <dmdesignskill skill="tw.colors">')
        for key, a in defaults.items():
            shades = " ".join(f'{k}="{v}"' for k, v in a.items())
            out.append(f'                <dmcolor key="{key}" {shades}/>')
        for key, value in d["colors"].items():
            out.append(f'                <dmcolor key="{attr(key)}" color="{attr(value)}"></dmcolor>')
        out.append("            </dmdesignskill>")
        f = d.get("fonts", {})
        fa = [f'family_1="{attr(font_family(f["sans"]))}"']
        for slot in ("display", "mono"):
            if f.get(slot):
                n = FONT_SLOTS[slot]
                fa.append(f'name_{n}="{slot}" family_{n}="{attr(font_family(f[slot]))}"')
        out.append(f'            <dmdesignskill skill="fonts" {" ".join(fa)}></dmdesignskill>')
        out.append('            <dmdesignskill skill="tailwind"></dmdesignskill>')
        out.append("            " + BACKGROUND)
        out.append("        </dmdesign>")
    out.append("    </dmdesigns>\n")

    db = read(p["db"]) if os.path.exists(p["db"]) else "<project>\n    <documents></documents>\n</project>\n"
    db = replace_block(db, "dmdesigns", "\n".join(out), after="<documents></documents>")
    locked = " ".join(f'tw-colors-{k}="true"' for k in defaults)
    db = replace_block(db, "dmlocked", f"    <dmlocked {locked}></dmlocked>\n")
    write(p["db"], db)

    # Google fonts must be activated, otherwise Pinegrow doesn't import them.
    fonts = load_json(p["fonts"], {"activated": []})
    have = {x.get("family") for x in fonts.get("activated", [])}
    added = []
    for d in data["designs"]:
        for slot, value in (d.get("fonts") or {}).items():
            family = font_family(value)
            if family in have:
                continue
            spec = value if isinstance(value, dict) else {}
            category = spec.get("category") or FONT_DEFAULT_CATEGORY[slot]
            weights = [str(w) for w in (spec.get("weights") or d.get("font_weights", {}).get(family)
                                        or (["400", "500"] if slot == "mono" else ["400", "500", "600", "700"]))]
            fonts.setdefault("activated", []).append({
                "type": "google", "family": family, "weights": weights,
                "styles": [{"weight": w} for w in weights], "category": category,
                "url": "https://fonts.googleapis.com/css?family=" + family.replace(" ", "+") + ":" + ",".join(weights),
                "usage": "all", "fallback": FONT_FALLBACK.get(category, FONT_FALLBACK["sans"])})
            have.add(family)
            added.append(family)
    save_json(p["fonts"], fonts)
    print(f"Wrote {len(data['designs'])} designs (active: {data['active']}). "
          f"Activated fonts: {', '.join(added) if added else 'none new'}.")


# ---------------------------------------------------------------------------------------------------------------------
# styles

def parse_styles(text):
    styles, problems = [], []
    for n, line in enumerate(text.split("\n"), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[0] in " \t":
            if not styles:
                problems.append(f"line {n}: continuation without a style")
            else:
                styles[-1][1] += " " + line.strip()
            continue
        m = re.match(r"^(\.[A-Za-z][\w-]*)\s*:\s*(.*)$", line.strip())
        if not m:
            problems.append(f"line {n}: expected '.class-name: utilities'")
            continue
        styles.append([m.group(1), m.group(2).strip(), n])
    seen = set()
    for key, classes, n in styles:
        if key in seen:
            problems.append(f"line {n}: {key} is defined twice")
        seen.add(key)
        problems += style_problems(key, classes, f"line {n}: ")
    return [(k, " ".join(c.split())) for k, c, _ in styles], problems


def style_problems(key, classes, where=""):
    problems = []
    for c in classes.split():
        base = c.split(":")[-1].lstrip("!")
        if base.split("/")[0] in FORBIDDEN_IN_STYLES:
            problems.append(f"{where}{key} uses '{c}', which can't be in a component style (Tailwind fails and "
                            "Pinegrow keeps the old CSS). Put it on the element instead.")
        if re.search(r"#[0-9a-fA-F]{3,8}\b", c):
            problems.append(f"{where}{key} uses a fixed color in '{c}'. Use a design color.")
    return problems


def cmd_styles(kit):
    p = paths(kit)
    styles, problems = parse_styles(read(p["styles"]))
    if problems:
        sys.exit("styles.txt:\n  " + "\n  ".join(problems))
    out = ["    <classstyles>"]
    for key, classes in styles:
        out.append(f'        <classstyle name="{key}" key="{key}" class="{attr(classes)}" component></classstyle>')
    out.append("    </classstyles>\n")
    db = read(p["db"])
    db = replace_block(db, "classstyles", "\n".join(out), after="</dmdesigns>")
    write(p["db"], db)
    print(f"Wrote {len(styles)} component styles.")


# ---------------------------------------------------------------------------------------------------------------------
# images

def placeholder_png(w, h):
    """A grey gradient PNG. Browsers and Pinegrow show it whatever the file extension is."""
    rows = []
    for y in range(h):
        t = y / max(1, h - 1)
        rows.append(b"\x00" + bytes([int(200 - 50 * t), int(196 - 50 * t), int(188 - 46 * t)]) * w)

    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + chunk(b"tEXt", b"Comment\x00kit-placeholder")
            + chunk(b"IDAT", zlib.compress(b"".join(rows), 9)) + chunk(b"IEND", b""))


def to_int(value, default):
    m = re.match(r"^\s*(\d+)\s*$", value or "")
    return int(m.group(1)) if m else default


def is_placeholder(path):
    """A placeholder made by kit.py images (marked PNG), or an older one (PNG data in a .jpg file)."""
    with open(path, "rb") as f:
        head = f.read(64)
    return (b"kit-placeholder" in head
            or (path.lower().endswith((".jpg", ".jpeg", ".webp")) and head[:8] == b"\x89PNG\r\n\x1a\n"))


def image_size(path):
    """(width, height) of a JPEG or PNG file, or None."""
    try:
        with open(path, "rb") as f:
            data = f.read(256 * 1024)
    except OSError:
        return None
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        chunk = data[12:16]
        if chunk == b"VP8X":
            return 1 + int.from_bytes(data[24:27], "little"), 1 + int.from_bytes(data[27:30], "little")
        if chunk == b"VP8 ":
            return (struct.unpack("<H", data[26:28])[0] & 0x3FFF, struct.unpack("<H", data[28:30])[0] & 0x3FFF)
        if chunk == b"VP8L":
            b = data[21:25]
            return 1 + (b[0] | (b[1] & 0x3F) << 8), 1 + (b[1] >> 6 | b[2] << 2 | (b[3] & 0x0F) << 10)
        return None
    if data[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                h, w = struct.unpack(">HH", data[i + 5:i + 9])
                return w, h
            if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
                i += 2
                continue
            i += 2 + struct.unpack(">H", data[i + 2:i + 4])[0]
    return None


def convert(src, out, W, H, quality=80):
    """Scales src to cover W x H, crops the center and writes out (.webp or .jpg). Uses ImageMagick, ffmpeg, or
    sips (macOS) with cwebp for WebP. Returns the tool used."""
    import subprocess
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    webp = out.lower().endswith(".webp")
    if shutil.which("magick"):
        subprocess.run(["magick", src, "-auto-orient", "-resize", f"{W}x{H}^", "-gravity", "center", "-extent",
                        f"{W}x{H}", "-strip", "-quality", str(quality), out], check=True, capture_output=True)
        return "magick"
    if shutil.which("ffmpeg"):
        codec = ["-c:v", "libwebp", "-quality", str(quality)] if webp else ["-q:v", "3"]
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-vf",
                        f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}", "-frames:v", "1"]
                       + codec + [out], check=True, capture_output=True)
        return "ffmpeg"
    if shutil.which("sips") and (not webp or shutil.which("cwebp")):
        w, h = image_size(src)
        scale = max(W / w, H / h)
        tmp = out + ".tmp." + ("png" if webp else "jpg")
        subprocess.run(["sips", "-s", "format", "png" if webp else "jpeg", "-z", str(max(H, round(h * scale))),
                        str(max(W, round(w * scale))), src, "--out", tmp], check=True, capture_output=True)
        if webp:
            subprocess.run(["sips", "-c", str(H), str(W), tmp, "--out", tmp], check=True, capture_output=True)
            subprocess.run(["cwebp", "-quiet", "-q", str(quality), tmp, "-o", out], check=True, capture_output=True)
            os.remove(tmp)
        else:
            subprocess.run(["sips", "-c", str(H), str(W), tmp, "--out", out], check=True, capture_output=True)
            os.remove(tmp)
        return "sips"
    sys.exit("No image tool found for this format. WebP needs ImageMagick (magick), ffmpeg, or cwebp with sips. "
             "Ask the user before installing one, or write .jpg files instead.")


def cmd_fit(src, out, size):
    m = re.match(r"^(\d+)x(\d+)$", size)
    if not m:
        sys.exit("Size must be WxH, for example 1600x900")
    if not image_size(src):
        sys.exit(f"{src} is not a JPEG, PNG or WebP image")
    W, H = int(m.group(1)), int(m.group(2))
    tool = convert(src, out, W, H)
    print(f"{out}: {image_size(out)[0]}x{image_size(out)[1]} ({tool})")


def page_images(p):
    """{src: (width, height)} for every images/... <img> on the pages, the library and the block sources."""
    files = [os.path.join(p["web"], f) for f in os.listdir(p["web"]) if f.endswith(".html")]
    for d in (os.path.join(p["web"], "blocks"), p["blocks"]):
        for dp, _, fs in os.walk(d):
            files += [os.path.join(dp, f) for f in fs if f.endswith(".html")]
    wanted = {}
    for f in files:
        for m in re.finditer(r"<img\b[^>]*>", read(f)):
            tag = m.group(0)
            src = get_attr(tag[4:], "src")
            if src and src.startswith("images/"):
                wanted.setdefault(src, (to_int(get_attr(tag[4:], "width"), 0), to_int(get_attr(tag[4:], "height"), 0)))
    return wanted


def cmd_optimize(kit):
    """Writes every image the pages use from its original in source/images/ (any name.png/.jpg/.jpeg/.webp with the
    same base name), at the width and height the <img> asks for, in the format of the src (WebP for .webp)."""
    p = paths(kit)
    originals = os.path.join(p["source"], "images")
    made, missing, kept = [], [], []
    for src, (w, h) in sorted(page_images(p).items()):
        base = os.path.splitext(os.path.basename(src))[0]
        orig = None
        for ext in (".png", ".jpg", ".jpeg", ".webp", ".PNG", ".JPG", ".JPEG"):
            cand = os.path.join(originals, os.path.dirname(src)[len("images/"):], base + ext)
            if os.path.exists(cand):
                orig = cand
                break
        out = os.path.join(p["web"], src)
        if not orig:
            (kept if os.path.exists(out) else missing).append(src)
            continue
        if not (w and h):
            w, h = image_size(orig)
        if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(orig) and image_size(out) == (w, h):
            kept.append(src)
            continue
        convert(orig, out, w, h)
        made.append(f"{src} {w}x{h} {os.path.getsize(out) // 1024} KB")
    for line in made:
        print("wrote " + line)
    if missing:
        print("no original in source/images for: " + ", ".join(missing))
    print(f"{len(made)} written, {len(kept)} up to date or without an original, {len(missing)} missing")


def cmd_images(kit):
    """Grey placeholder originals in source/images/ for every image without one, then optimize."""
    p = paths(kit)
    originals = os.path.join(p["source"], "images")
    made = []
    for src, (w, h) in sorted(page_images(p).items()):
        base = os.path.splitext(src[len("images/"):])[0]
        if any(os.path.exists(os.path.join(originals, base + ext)) for ext in (".png", ".jpg", ".jpeg", ".webp")):
            continue
        if os.path.exists(os.path.join(p["web"], src)) and not is_placeholder(os.path.join(p["web"], src)):
            continue
        w, h = w or 1200, h or 800
        scale = max(1, max(w, h) // 400)
        out = os.path.join(originals, base + ".png")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "wb") as fh:
            fh.write(placeholder_png(max(1, w // scale), max(1, h // scale)))
        made.append(f"{src} ({w}x{h})")
    print("Placeholders: " + (", ".join(made) if made else "none needed"))
    cmd_optimize(kit)


# ---------------------------------------------------------------------------------------------------------------------
# library

LIB_HEAD = """<style>
/* Library chrome: plain CSS, so it works with every design. */
.kit-lib-bar { position: sticky; top: 0; z-index: 50; display: flex; flex-wrap: wrap; gap: 4px 20px;
    padding: 12px 20px; background: #111; color: #fff; font: 600 12px/1.4 system-ui, sans-serif;
    letter-spacing: .06em; text-transform: uppercase; }
.kit-lib-title { margin: 0; padding: 8px 20px; background: #222; color: #ddd; font: 500 12px/1.4 system-ui, sans-serif;
    letter-spacing: .06em; text-transform: uppercase; }
.kit-lib-home { padding: 40px 20px; font: 16px/1.5 system-ui, sans-serif; color: #111; background: #fff; }
.kit-lib-home h1 { margin: 0 0 8px; font-size: 32px; }
.kit-lib-cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; margin-top: 24px; }
.kit-lib-card { display: block; padding: 20px; border: 1px solid #ccc; background: #fafafa; }
.kit-lib-card strong { display: block; font-size: 20px; }
.kit-lib-card span { display: block; margin-top: 6px; color: #555; font-size: 14px; }
/* Pinegrow styles .pg-lib-hover-menu as a small badge. Two classes outrank its one-class rules. */
.kit-lib-pass.pg-lib-hover-menu { position: static; top: auto; right: auto; height: auto; padding: 0; background: none;
    z-index: auto; white-space: normal; font-size: inherit; text-transform: none; transform: none; cursor: auto; }
.kit-lib-bar.kit-lib-pass.pg-lib-hover-menu { position: sticky; top: 0; z-index: 50; padding: 12px 20px; background: #111;
    font-size: 12px; text-transform: uppercase; }
.kit-lib-pass.pg-lib-hover-menu a { color: inherit; text-decoration: none; }
.kit-lib-pass.pg-lib-hover-menu a:hover, .kit-lib-pass.pg-lib-hover-menu .kit-lib-current { text-decoration: underline;
    text-underline-offset: 4px; }
html body .kit-lib-pass.pg-lib-hover-menu, html body .kit-lib-pass.pg-lib-hover-menu *,
html body .kit-lib-pass.pg-lib-hover-menu *:hover { cursor: pointer !important; transform: none !important;
    box-shadow: none !important; }
</style>
<script>
/* Only whole blocks can be dragged from the library. Pinegrow 10.1 lets you drag any element from a library added in
   pinegrow.json (its selector is "*"), marking the element under the mouse with pg-draggable on mouseover. This marks
   the whole block instead, and keeps clicks inside blocks from picking inner elements. Links in .kit-lib-pass (the
   bar and the cards) still open pages: Pinegrow lets clicks inside .pg-lib-hover-menu through. Runs only in the
   Insert panel: pages open in the editor load with pgedit=1. */
if (!/[?&]pgedit=1/.test(location.search)) {
    (function() {
        var blockOf = function(el) {
            return el && el.closest ? el.closest(".pg-lib-section > :not(.pg-lib-section-title)") : null;
        };
        document.addEventListener("mouseover", function(e) {
            e.stopImmediatePropagation();
            var block = blockOf(e.target);
            if (block && block.hasAttribute("pg-draggable")) {
                return;
            }
            document.querySelectorAll("[pg-draggable]").forEach(function(el) {
                el.removeAttribute("pg-draggable");
                el.removeAttribute("draggable");
                el.classList.remove("pg-lib-item");
            });
            if (block) {
                block.setAttribute("pg-draggable", "true");
                block.setAttribute("draggable", "true");
                block.classList.add("pg-lib-item");
            }
        }, true);
        ["click", "dblclick"].forEach(function(type) {
            document.addEventListener(type, function(e) {
                if (e.target.closest && e.target.closest(".kit-lib-pass")) {
                    return;
                }
                e.stopImmediatePropagation();
                e.preventDefault();
            }, true);
        });
    })();
}
</script>
"""


def nice(name):
    name = re.sub(r"^\d+[-_ ]*", "", name)
    name = re.sub(r"\.html$", "", name).replace("-", " ").replace("_", " ").strip()
    return name[:1].upper() + name[1:]


def first_element(text):
    m = re.search(r"<([a-zA-Z][\w-]*)\b([^>]*)>", text)
    return (m.group(1).lower(), m.group(2)) if m else (None, "")


def get_attr(attrs, name):
    m = re.search(rf'\s{name}="([^"]*)"', " " + attrs)
    return html.unescape(m.group(1)) if m else None


def library_sources(p):
    cats = []
    if not os.path.isdir(p["blocks"]):
        return cats
    for d in sorted(os.listdir(p["blocks"])):
        full = os.path.join(p["blocks"], d)
        if not os.path.isdir(full):
            continue
        blocks = []
        for f in sorted(os.listdir(full)):
            if f.endswith(".html"):
                code = read(os.path.join(full, f)).strip()
                tag, attrs = first_element(code)
                title = get_attr(attrs, "data-pg-name") or get_attr(attrs, "data-pg-content-group") or nice(f)
                blocks.append({"file": os.path.join("source", "blocks", d, f), "title": title, "code": code})
        if blocks:
            slug = re.sub(r"^\d+[-_ ]*", "", d).lower()
            cats.append({"name": nice(d), "slug": slug, "blocks": blocks})
    return cats


def body_class(p):
    idx = os.path.join(p["web"], "index.html")
    if os.path.exists(idx):
        m = re.search(r'<body[^>]*class="([^"]*)"', read(idx))
        if m:
            return m.group(1)
    return "bg-page text-ink font-sans antialiased"


def lib_page(title, body, bcls):
    return f"""<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <base href="../">
        <title>{html.escape(title)} | Block library</title>
        <link href="tailwind_theme/tailwind.css" rel="stylesheet" type="text/css">
{LIB_HEAD}    </head>
    <body class="{bcls}">
{body}
    </body>
</html>
"""


def library_fingerprint(p, cats):
    import hashlib
    h = hashlib.sha1(" ".join(sorted(body_class(p).split())).encode())
    for c in cats:
        for b in c["blocks"]:
            h.update(b["file"].encode() + b"\0" + b["code"].encode() + b"\0")
    return h.hexdigest()[:16]


def cmd_library(kit):
    p = paths(kit)
    cats = library_sources(p)
    if not cats:
        sys.exit("No blocks: put them in source/blocks/<NN-category>/<NN-block>.html")
    bcls = body_class(p)
    total = sum(len(c["blocks"]) for c in cats)

    def bar(current):
        home_cur = ' class="kit-lib-current"' if current == LIBRARY_HOME else ""
        links = [f'<a href="{LIBRARY_HOME}"{home_cur}>All blocks</a>']
        for c in cats:
            url = f"blocks/{c['slug']}.html"
            cur = ' class="kit-lib-current"' if current == url else ""
            links.append(f'<a href="{url}"{cur}>{html.escape(c["name"])}</a>')
        return '<nav class="pg-lib-hover-menu kit-lib-pass kit-lib-bar" aria-label="Block library">\n' + "\n".join(links) + "\n</nav>"

    cards = "\n".join(
        f'<a class="kit-lib-card" href="blocks/{c["slug"]}.html"><strong>{html.escape(c["name"])}</strong>'
        f'<span>{len(c["blocks"])} blocks: {html.escape(", ".join(b["title"] for b in c["blocks"]))}</span></a>'
        for c in cats)
    home = f"""<!-- kit-library {library_fingerprint(p, cats)} -->
{bar(LIBRARY_HOME)}
<div class="kit-lib-home">
<h1>{total} blocks</h1>
<p>Click a category, then drag a block to your page. The bar at the top leads to the other categories and back here.</p>
<div class="pg-lib-hover-menu kit-lib-pass kit-lib-cards">
{cards}
</div>
</div>"""
    out_dir = os.path.join(p["web"], "blocks")
    os.makedirs(out_dir, exist_ok=True)
    written = {LIBRARY_HOME}
    write(os.path.join(p["web"], LIBRARY_HOME), lib_page("Blocks", home, bcls + " kit-lib-page"))
    for c in cats:
        url = f"blocks/{c['slug']}.html"
        sections = "\n".join(
            f'<div class="pg-lib-section">\n<p class="pg-lib-section-title kit-lib-title">{html.escape(b["title"])}</p>\n'
            f'{b["code"]}\n</div>' for b in c["blocks"])
        write(os.path.join(p["web"], url), lib_page(c["name"], bar(url) + "\n" + sections, bcls + " kit-lib-page"))
        written.add(url)
    for f in os.listdir(out_dir):
        if f.endswith(".html") and f"blocks/{f}" not in written:
            os.remove(os.path.join(out_dir, f))

    pj = load_json(p["pj"], dict(PINEGROW_JSON))
    pj["project_resources"] = [{"url": LIBRARY_HOME, "type": "pinegrow/pagelib"}]
    ex = pj.get("publish-excludes") or []
    if "blocks" not in ex:
        ex.append("blocks")
    pj["publish-excludes"] = ex
    save_json(p["pj"], pj)
    print(f"Wrote the block library: {total} blocks in {len(cats)} categories ({', '.join(c['name'] for c in cats)}).")


# ---------------------------------------------------------------------------------------------------------------------
# check

class Tree(html.parser.HTMLParser):
    """Minimal element tree for checks."""
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = {"tag": "#root", "attrs": {}, "children": [], "parent": None, "line": 0}
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        node = {"tag": tag, "attrs": {k: (v if v is not None else "") for k, v in attrs}, "children": [],
                "parent": self.cur, "line": self.getpos()[0]}
        self.cur["children"].append(node)
        if tag not in self.VOID:
            self.cur = node

    def handle_startendtag(self, tag, attrs):
        node = {"tag": tag, "attrs": {k: (v if v is not None else "") for k, v in attrs}, "children": [],
                "parent": self.cur, "line": self.getpos()[0]}
        self.cur["children"].append(node)

    def handle_endtag(self, tag):
        n = self.cur
        while n is not self.root and n["tag"] != tag:
            n = n["parent"]
        if n is not self.root:
            self.cur = n["parent"]


def parse(text):
    t = Tree()
    t.feed(text)
    return t.root


def walk(node):
    for c in node["children"]:
        yield c
        yield from walk(c)


def brief_value(p, key):
    if not os.path.exists(p["brief"]):
        return ""
    m = re.search(rf"^{key}:\s*(.*)$", read(p["brief"]), re.M | re.I)
    return m.group(1).strip() if m else ""


def cmd_check(kit):
    p = paths(kit)
    errors, warnings = [], []

    def err(msg):
        errors.append(msg)

    def warn(msg):
        warnings.append(msg)

    if not os.path.exists(p["brief"]):
        warn("KIT-BRIEF.md is missing")
    css_choice = brief_value(p, "CSS").lower()
    if css_choice and "tailwind" not in css_choice:
        warn(f"CSS in the brief is '{css_choice}'; only the Tailwind CSS checks exist so far")
    if brief_value(p, "WordPress").lower().startswith("y"):
        warn("WordPress is in the brief; the WordPress checks are not written yet")

    # Designs
    designs = load_json(p["designs"])
    color_names, font_families = set(), set()
    if designs is None:
        err("source/designs.json is missing")
    else:
        for prob in design_problems(designs):
            err("designs.json: " + prob)
        for d in designs.get("designs", []):
            color_names |= set((d.get("colors") or {}).keys())
            font_families |= {font_family(v) for v in (d.get("fonts") or {}).values()}
    db = read(p["db"]) if os.path.exists(p["db"]) else ""
    if "<dmdesigns>" not in db:
        err("projectdb.pgml has no saved designs: run kit.py designs")
    elif designs:
        for d in designs.get("designs", []):
            if f'<dmdesign id="{d.get("id")}"' not in db:
                err(f"design '{d.get('id')}' is in designs.json but not in projectdb.pgml: run kit.py designs")
    fonts = load_json(p["fonts"], {"activated": []})
    active_fonts = {x.get("family") for x in fonts.get("activated", [])}
    for fam in sorted(font_families - active_fonts):
        err(f"font '{fam}' is not activated in _pginfo/fonts.json: run kit.py designs")

    # Component styles
    style_keys = set()
    if os.path.exists(p["styles"]):
        styles, probs = parse_styles(read(p["styles"]))
        for prob in probs:
            err("styles.txt " + prob)
        style_keys = {k[1:] for k, _ in styles}
        for k in style_keys:
            if f'key=".{k}"' not in db:
                err(f"component style .{k} is in styles.txt but not in projectdb.pgml: run kit.py styles")
    for m in re.finditer(r'<classstyle [^>]*key="([^"]+)"[^>]*class="([^"]*)"', db):
        for prob in style_problems(m.group(1), html.unescape(m.group(2))):
            err("projectdb.pgml: " + prob)

    # Pages
    pages = sorted(f for f in os.listdir(p["web"]) if f.endswith(".html")) if os.path.isdir(p["web"]) else []
    lib_pages = sorted("blocks/" + f for f in os.listdir(os.path.join(p["web"], "blocks"))
                       if f.endswith(".html")) if os.path.isdir(os.path.join(p["web"], "blocks")) else []
    if not pages:
        err("website/ has no pages")
    used_classes = set()
    tw_default = set(load_json(os.path.join(HERE, "tw-default-colors.json"), {}).keys())
    def where(url, node):
        if url.startswith("blocks/"):
            return f"{url}:{node['line']} (generated: fix it in source/blocks, then run kit.py library)"
        return f"{url}:{node['line']}"

    for url in pages + lib_pages:
        text = read(os.path.join(p["web"], url))
        root = parse(text)
        is_lib = url.startswith("blocks/")
        base_dir = p["web"] if is_lib else os.path.dirname(os.path.join(p["web"], url))
        if not is_lib:
            if not re.search(r"<title>[^<]+</title>", text):
                err(f"{url}: missing <title>")
            if not re.search(r'<meta name="description" content="[^"]+"', text):
                warn(f"{url}: missing meta description")
            if 'href="tailwind_theme/tailwind.css"' not in text:
                err(f"{url}: doesn't link tailwind_theme/tailwind.css")
        for n in walk(root):
            a = n["attrs"]
            for name in ("href", "src"):
                v = a.get(name)
                if not v or n["tag"] == "base" or re.match(r"^(https?:|mailto:|tel:|#|data:|javascript:|//)", v):
                    continue
                target = os.path.normpath(os.path.join(base_dir, v.split("#")[0].split("?")[0]))
                if v.split("#")[0] and not os.path.exists(target):
                    err(f"{where(url, n)}: {name}=\"{v}\" doesn't exist")
            if n["tag"] == "img" and "alt" not in a:
                err(f"{where(url, n)}: <img> without alt")
            if n["tag"] == "img" and not (a.get("width") and a.get("height")):
                warn(f"{where(url, n)}: <img> without width and height")
            elif n["tag"] == "img" and a.get("src", "").startswith("images/"):
                real = image_size(os.path.join(p["web"], a["src"]))
                w, h = to_int(a.get("width"), 0), to_int(a.get("height"), 0)
                if real and w and h and not is_placeholder(os.path.join(p["web"], a["src"])) \
                        and abs(real[0] / real[1] - w / h) > 0.03 * (w / h):
                    warn(f"{where(url, n)}: {a['src']} is {real[0]}x{real[1]} but width/height say {w}x{h}")
            cls = a.get("class", "")
            for c in cls.split():
                used_classes.add(c)
                if re.search(r"#[0-9a-fA-F]{3,8}\b", c):
                    err(f"{where(url, n)}: fixed color in class '{c}'. Use a design color.")
                m = re.match(r"^(?:[\w-]+:)*(?:bg|text|border|ring|outline|fill|stroke|from|via|to|decoration|divide|accent|caret|shadow)-([a-z]+)-\d{2,3}(?:/\d+)?$", c)
                if m and m.group(1) in tw_default and not is_lib:
                    warn(f"{where(url, n)}: '{c}' uses a default Tailwind color; designs can't change it")
            st = a.get("style", "")
            if re.search(r"#[0-9a-fA-F]{3,8}\b|rgb\(", st):
                err(f"{where(url, n)}: fixed color in style=\"{st}\"")
            if "data-pg-content-collection" in a:
                items = [c for c in n["children"] if "data-pg-content-item" in c["attrs"]]
                if len(items) < 2:
                    warn(f"{where(url, n)}: collection '{a['data-pg-content-collection']}' has fewer than 2 items")
                if len(items) != len(n["children"]):
                    warn(f"{where(url, n)}: not every child of collection '{a['data-pg-content-collection']}' "
                         "is a data-pg-content-item")
            if "data-pg-content-item" in a and "data-pg-content-collection" not in n["parent"]["attrs"]:
                err(f"{where(url, n)}: item '{a['data-pg-content-item']}' is not a direct child of a collection")
        if is_lib and url != LIBRARY_HOME:
            for n in walk(root):
                if "pg-lib-section" in n["attrs"].get("class", "").split():
                    kids = [c for c in n["children"] if "pg-lib-section-title" not in c["attrs"].get("class", "")]
                    if len(kids) != 1:
                        err(f"{where(url, n)}: a .pg-lib-section must hold one title and one block")
                    elif "data-pg-content-group" not in kids[0]["attrs"]:
                        err(f"{where(url, n)}: block '{kids[0]['attrs'].get('data-pg-name', kids[0]['tag'])}' "
                            "has no data-pg-content-group")

    # Block library
    pj = load_json(p["pj"], {})
    if os.path.isdir(p["blocks"]) and library_sources(p):
        if LIBRARY_HOME not in lib_pages:
            err("the block library is not built: run kit.py library")
        if {"url": LIBRARY_HOME, "type": "pinegrow/pagelib"} not in (pj.get("project_resources") or []):
            err("pinegrow.json doesn't register the library: run kit.py library")
        if "blocks" not in (pj.get("publish-excludes") or []):
            err("pinegrow.json publish-excludes doesn't include blocks: run kit.py library")
        home = os.path.join(p["web"], LIBRARY_HOME)
        if os.path.exists(home):
            m = re.search(r"<!-- kit-library (\w+) -->", read(home))
            if not m or m.group(1) != library_fingerprint(p, library_sources(p)):
                err("source/blocks or the body class of index.html changed since the library was built: "
                    "run kit.py library")
        for c in library_sources(p):
            for b in c["blocks"]:
                tag, attrs = first_element(b["code"])
                if tag not in ("section", "header", "footer"):
                    warn(f"{b['file']}: the block's root is <{tag}>; use section, header or footer")
                if get_attr(attrs, "data-pg-name") is None:
                    err(f"{b['file']}: the block's root has no data-pg-name")
                if get_attr(attrs, "data-pg-content-group") is None:
                    err(f"{b['file']}: the block's root has no data-pg-content-group")

    # Classes without a definition (typos, or component styles that don't exist)
    if os.path.exists(p["css"]) and os.path.getsize(p["css"]) > 2000:
        css = read(p["css"])
        missing = sorted(c for c in used_classes
                         if not c.startswith(("pg-", "kit-lib")) and "." + css_escape(c) not in css)
        if missing:
            warn(f"{len(missing)} classes are not in the compiled CSS (typos, or pages not opened in Pinegrow "
                 f"since they changed): {' '.join(missing[:40])}")
    else:
        warn("tailwind_theme/tailwind.css is not compiled yet: open the project in Pinegrow and open every page")

    # No server-side scripts: a kit is a static site, and a mailer script is a security risk on shared hosting.
    for dp, _, fs in os.walk(p["web"]):
        for f in fs:
            if f.lower().endswith((".php", ".phtml", ".cgi", ".pl", ".asp", ".aspx", ".jsp")):
                err(f"{os.path.relpath(os.path.join(dp, f), p['web'])}: server-side script in the kit; remove it "
                    "(use Netlify Forms or a form service for the contact form)")

    # Images
    img_dir = os.path.join(p["web"], "images")
    orig_dir = os.path.join(p["source"], "images")
    if os.path.isdir(img_dir):
        files = sorted(f for f in os.listdir(img_dir) if not f.startswith("."))
        holders = [f for f in files if is_placeholder(os.path.join(img_dir, f))]
        if os.path.isdir(orig_dir):
            for f in sorted(os.listdir(orig_dir)):
                if not f.startswith(".") and is_placeholder(os.path.join(orig_dir, f)):
                    holders.append(os.path.splitext(f)[0])
        for f in files:
            if not f.lower().endswith((".webp", ".svg")):
                warn(f"images/{f} is not WebP: keep the original in source/images, use a .webp src and run "
                     "kit.py optimize")
        if holders:
            warn(f"{len(holders)} placeholder images left (tell the user, or replace them): {', '.join(holders)}")
        source = brief_value(p, "Images").lower()
        credits = os.path.join(p["source"], "image-credits.md")
        if ("unsplash" in source or "generat" in source) and files:
            listed = read(credits) if os.path.exists(credits) else ""
            missing = [f for f in files if f not in holders and os.path.splitext(f)[0] not in holders
                       and os.path.splitext(f)[0] not in listed]
            if missing:
                warn(f"images not in source/image-credits.md: {', '.join(missing)}")

    for w in warnings:
        print("warning: " + w)
    for e in errors:
        print("error: " + e)
    print(f"{len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


def css_escape(c):
    return re.sub(r"([^a-zA-Z0-9_-])", r"\\\1", c)


# ---------------------------------------------------------------------------------------------------------------------

def main():
    if len(sys.argv) == 5 and sys.argv[1] == "fit":
        cmd_fit(sys.argv[2], sys.argv[3], sys.argv[4])
        return
    if len(sys.argv) != 3 or sys.argv[1] not in ("init", "designs", "styles", "images", "optimize", "library",
                                                  "check"):
        sys.exit(__doc__)
    cmd, kit = sys.argv[1], sys.argv[2]
    if cmd != "init" and not os.path.isdir(os.path.join(kit, "website")):
        sys.exit(f"{kit} has no website/ folder. Run: python3 kit.py init {kit}")
    result = {"init": cmd_init, "designs": cmd_designs, "styles": cmd_styles, "images": cmd_images, "optimize": cmd_optimize, "library": cmd_library,
              "check": cmd_check}[cmd](kit)
    sys.exit(result or 0)


if __name__ == "__main__":
    main()
