"""Blocks of the Northlight website kit.

Every block is a function that takes a content dict and returns HTML. The same function makes the block on the starter
pages and in the block library (website/blocks/), so they never drift apart.

Each block carries:
- WordPress block attributes (cms-block, cms-block-field...). Every block variant has its own block id, so blocks from
  different variants never clash in a WordPress export. Repeated items are sub-blocks inside cms-block-inner-content.
- Content panel annotations (data-pg-content-group / -label / -collection / -item).
- Only design colors (page, surface, ink, muted, line, primary, on-primary, band, on-band), the three design fonts
  (sans, display, mono) and component styles from projectdb.pgml, so every design and every style change applies.

Leaf elements are written on one line and containers open and close on their own lines; build_kit.indent() relies on
that to indent the output.
"""


# Field helpers

def fl(fid, title, extra=""):
    return (f'cms-block-field="{fid}" cms-block-field-type="content" cms-block-field-title="{title}"{extra} '
            f'data-pg-content-label="{title}"')


def rich(fid, title):
    return fl(fid, title, ' cms-block-field-control="richtext"')


def lk(fid, title):
    return (f'cms-block-field="{fid}_link" cms-block-field-type="link" cms-block-field-title="{title} link" '
            f'cms-block-field-2="{fid}_label" cms-block-field-type-2="content" cms-block-field-title-2="{title} label" '
            f'data-pg-content-label="{title}"')


def a(fid, title, href, label, cls):
    return f'<a href="{href}" class="{cls}" {lk(fid, title)}>{label}</a>'


def img(fid, title, src, alt, w, h, cls):
    return (f'<img src="images/{src}" alt="{alt}" width="{w}" height="{h}" class="{cls}" '
            f'cms-block-field="{fid}" cms-block-field-type="image" cms-block-field-title="{title}" data-pg-content-label="{title}">')


def email_link(fid, title, email, cls):
    return (f'<a href="mailto:{email}" class="{cls}" cms-block-field="{fid}" cms-block-field-type="content" '
            f'cms-block-field-title="{title}" cms-block-field-2="{fid}" cms-block-field-type-2="attr" '
            f'cms-block-field-attribute-2="href" cms-block-field-expression-2="mailto:{{{{ {fid} }}}}" data-pg-content-label="{title}">{email}</a>')


def phone_link(fid, title, phone, cls):
    tel = "".join(ch for ch in phone if ch.isdigit() or ch == "+")
    return (f'<a href="tel:{tel}" class="{cls}" cms-block-field="{fid}" cms-block-field-type="content" '
            f'cms-block-field-title="{title}" cms-block-field-2="{fid}" cms-block-field-type-2="attr" '
            f'cms-block-field-attribute-2="href" cms-block-field-expression-2="tel:{{{{ {fid} }}}}" data-pg-content-label="{title}">{phone}</a>')


def block(tag, bid, title, desc, cls, body, sid=None, extra=""):
    i = f' id="{sid}"' if sid else ""
    return (f'<{tag}{i} class="{cls}" data-pg-name="{title}" cms-block="{bid}" cms-block-title="{title}" '
            f'cms-block-description="{desc}" data-pg-content-group="{title}"{extra}>\n{body}\n</{tag}>')


def items(tag, cls, allowed, collection, parts):
    return (f'<{tag} class="{cls}" cms-block-inner-content cms-block-inner-content-allowed="{allowed}" '
            f'data-pg-content-collection="{collection}">\n' + "\n".join(parts) + f"\n</{tag}>")


def item(tag, bid, title, parent, cls, body, extra=""):
    return (f'<{tag} class="{cls}" cms-block="{bid}" cms-block-title="{title}" cms-block-parent="{parent}" '
            f'data-pg-content-item="{title}"{extra}>\n{body}\n</{tag}>')


def head(c, title_tag="h2"):
    """Section heading: sheet label, title and lead."""
    return (f'<div class="section-head">\n'
            f'<p class="sheet-label" {fl("sheet", "Sheet label")}>{c["sheet"]}</p>\n'
            f'<{title_tag} class="heading-lg" {fl("title", "Title")}>{c["title"]}</{title_tag}>\n'
            f'<p class="lead" {fl("description", "Description")}>{c["lead"]}</p>\n'
            f'</div>')


ICONS = {
    "home": '<path d="M4 20V9l8-5 8 5v11M9 20v-6h6v6"/>',
    "chair": '<path d="M6 20v-4M18 20v-4M5 16h14M7 16V6a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v10"/>',
    "plan": '<path d="M4 4h16v16H4zM4 10h7v10M11 14h9"/>',
    "light": '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-4 10.5V16h8v-2.5A6 6 0 0 0 12 3z"/>',
    "search": '<circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5"/>',
    "pen": '<path d="M4 20l4-1 11-11-3-3L5 16zM14 6l3 3"/>',
    "code": '<path d="M8 8l-4 4 4 4M16 8l4 4-4 4M13 6l-2 12"/>',
    "access": '<circle cx="12" cy="5" r="2"/><path d="M5 9h14M12 9v12M8 21l4-8 4 8"/>',
    "heart": '<path d="M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.5-7 10-7 10z"/>',
    "chart": '<path d="M4 20V4M4 20h16M8 16v-5M12 16V8M16 16v-3"/>',
}


def icon(name, fid="icon"):
    return (f'<svg class="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" cms-block-field="{fid}" '
            f'cms-block-field-type="image" cms-block-field-title="Icon">{ICONS[name]}</svg>')


# Headers and footers

def header_drawing(c):
    nav = "\n".join(f'<li><a href="{h}" class="nav-link">{l}</a></li>' for l, h in c["nav"])
    mobile = "\n".join(f'<a href="{h}" class="nav-link">{l}</a>' for l, h in c["nav"])
    body = f'''<div class="container-site flex h-16 items-center justify-between gap-6">
<a href="{c.get("home", "index.html")}" class="brand" aria-label="{c["name"]} home"><span class="brand-mark" aria-hidden="true">{c["mark"]}</span> <span cms-site-name data-pg-content-label="Site name">{c["name"]}</span></a>
<nav class="hidden lg:block" aria-label="Main">
<ul class="flex items-center gap-8" cms-menu="primary">
{nav}
</ul>
</nav>
<div class="flex items-center gap-2">
{a("header_button", "Button", c["cta"][1], c["cta"][0], "btn-primary hidden sm:inline-flex")}
<details class="mobile-menu lg:hidden">
<summary class="mobile-menu-button" aria-label="Open menu">Menu</summary>
<div class="mobile-menu-panel">
{mobile}
<a href="{c["cta"][1]}" class="btn-primary mt-2">{c["cta"][0]}</a>
</div>
</details>
</div>
</div>'''
    return block("header", "header-drawing", "Header (drawing)", "Logo mark, technical menu and a button", "site-header", body)


def header_simple(c):
    nav = "\n".join(f'<li><a href="{h}" class="nav-link-plain">{l}</a></li>' for l, h in c["nav"])
    mobile = "\n".join(f'<a href="{h}" class="nav-link-plain text-xl">{l}</a>' for l, h in c["nav"])
    body = f'''<div class="container-site flex h-20 items-center justify-between gap-6">
<a href="{c.get("home", "#")}" class="wordmark-small" aria-label="{c["name"]} home"><span cms-site-name data-pg-content-label="Site name">{c["name"]}</span></a>
<nav class="hidden lg:block" aria-label="Main">
<ul class="flex items-center gap-8" cms-menu="primary">
{nav}
</ul>
</nav>
<div class="flex items-center gap-2">
{a("header_button", "Button", c["cta"][1], c["cta"][0], "btn-primary hidden sm:inline-flex")}
<details class="mobile-menu lg:hidden">
<summary class="mobile-menu-button" aria-label="Open menu">Menu</summary>
<div class="mobile-menu-panel">
{mobile}
<a href="{c["cta"][1]}" class="btn-primary mt-2">{c["cta"][0]}</a>
</div>
</details>
</div>
</div>'''
    return block("header", "header-simple", "Header (simple)", "Wordmark, menu and a button", "site-header-simple", body)


def footer_titleblock(c):
    body = f'''<div class="container-site">
<dl class="footer-block">
<div class="md:col-span-2">
<dt>Studio</dt>
<dd><span cms-site-name class="font-display text-2xl font-semibold tracking-tight">{c["name"]}</span><span class="mt-2 block text-muted" {fl("about", "About")}>{c["about"]}</span></dd>
</div>
<div>
<dt {fl("address_label", "Address label")}>Address</dt>
<dd {rich("address", "Address")}>{c["address"]}</dd>
</div>
<div>
<dt {fl("contact_label", "Contact label")}>Contact</dt>
<dd>{email_link("email", "Email address", c["email"], "footer-link")}<br>{phone_link("phone", "Phone", c["phone"], "footer-link")}</dd>
</div>
<div>
<dt>Follow</dt>
<dd>{a("instagram", "Instagram", "https://www.instagram.com/", "Instagram", "footer-link")}<br>{a("pinterest", "Pinterest", "https://www.pinterest.com/", "Pinterest", "footer-link")}</dd>
</div>
<div>
<dt>Drawing</dt>
<dd>{c["mark"]}-<span cms-function="current_year" cms-function-type="content">2026</span> · Rev. 3</dd>
</div>
<div class="md:col-span-6">
<dt>Notes</dt>
<dd {fl("credit", "Credit")}>© {c["name"]}. Made with Pinegrow.</dd>
</div>
</dl>
</div>'''
    return block("footer", "footer-titleblock", "Footer (title block)", "Details laid out like a drawing title block", "site-footer", body)


def footer_columns(c):
    body = f'''<div class="container-site grid gap-12 md:grid-cols-12">
<div class="md:col-span-4">
<p class="wordmark-small"><span cms-site-name>{c["name"]}</span></p>
<p class="mt-4 max-w-sm text-muted" {fl("about", "About")}>{c["about"]}</p>
</div>
<div class="md:col-span-3">
<p class="ref" {fl("visit_label", "Visit label")}>Visit</p>
<p class="mt-3" {rich("address", "Address")}>{c["address"]}</p>
</div>
<div class="md:col-span-3">
<p class="ref" {fl("contact_label", "Contact label")}>Contact</p>
<p class="mt-3">{email_link("email", "Email address", c["email"], "footer-link")}<br>{phone_link("phone", "Phone", c["phone"], "footer-link")}</p>
</div>
<div class="md:col-span-2">
<p class="ref" {fl("follow_label", "Follow label")}>Follow</p>
<p class="mt-3">{a("instagram", "Instagram", "https://www.instagram.com/", "Instagram", "footer-link")}</p>
</div>
</div>
<div class="container-site mt-16 flex flex-col gap-2 border-t border-line pt-6 text-sm text-muted sm:flex-row sm:justify-between">
<p>© <span cms-function="current_year" cms-function-type="content">2026</span> <span cms-site-name>{c["name"]}</span></p>
<p {fl("credit", "Credit")}>Made with Pinegrow</p>
</div>'''
    return block("footer", "footer-columns", "Footer (columns)", "Details in columns with a bottom bar", "site-footer-columns", body)


def footer_big(c):
    body = f'''<div class="container-site">
<p class="ref" {fl("eyebrow", "Eyebrow")}>{c["eyebrow"]}</p>
<p class="footer-statement mt-6" {fl("title", "Title")}>{c["statement"]}</p>
{email_link("email", "Email address", c["email"], "footer-email mt-8")}
<div class="mt-16 flex flex-col gap-4 border-t border-line pt-6 text-sm text-muted sm:flex-row sm:items-center sm:justify-between">
<p>© <span cms-function="current_year" cms-function-type="content">2026</span> <span cms-site-name>{c["name"]}</span></p>
<p class="flex gap-6">{a("instagram", "Instagram", "https://www.instagram.com/", "Instagram", "footer-link")} {a("linkedin", "LinkedIn", "https://www.linkedin.com/", "LinkedIn", "footer-link")}</p>
<p {fl("credit", "Credit")}>Made with Pinegrow</p>
</div>
</div>'''
    return block("footer", "footer-big", "Footer (big)", "A closing line with a large email link", "site-footer-big", body)


# Heroes

def hero_callouts(c):
    tb = "\n".join(f'''<div>
<dt {fl(f"tb_{i}_label", f"Fact {i} label")}>{l}</dt>
<dd {fl(f"tb_{i}_value", f"Fact {i} value")}>{v}</dd>
</div>''' for i, (l, v) in enumerate(c["facts"], 1))
    spots = "\n".join(f'<span class="hotspot" style="left: {x}%; top: {y}%;" aria-hidden="true">{i}</span>'
                      for i, (x, y) in enumerate(c["spots"], 1))
    calls = "\n".join(f'<li><span {fl(f"callout_{i}", f"Callout {i}")}>{t}</span></li>' for i, t in enumerate(c["callouts"], 1))
    body = f'''<div class="container-site grid gap-10 lg:grid-cols-12 lg:gap-12">
<div class="flex flex-col justify-between gap-10 lg:col-span-5">
<div>
<p class="sheet-label" {fl("sheet", "Sheet label")}>{c["sheet"]}</p>
<h1 class="heading-display mt-8" {fl("title", "Title")}>{c["title"]}</h1>
<p class="lead mt-6 max-w-md" {fl("description", "Description")}>{c["lead"]}</p>
<div class="mt-8 flex flex-wrap gap-2">
{a("primary", "Primary button", c["primary"][1], c["primary"][0], "btn-primary")}
{a("secondary", "Secondary button", c["secondary"][1], c["secondary"][0], "btn-secondary")}
</div>
</div>
<dl class="title-block">
{tb}
</dl>
</div>
<figure class="lg:col-span-7">
<div class="relative">
{img("image", "Image", c["image"], c["alt"], 1600, 1100, "img-frame aspect-[16/11] w-full")}
{spots}
</div>
<figcaption class="legend">
<p class="legend-title" {fl("legend_title", "Legend title")}>{c["legend"]}</p>
<ol>
{calls}
</ol>
</figcaption>
</figure>
</div>'''
    return block("section", "hero-callouts", "Hero (callouts)", "Headline with facts and a photo with numbered callouts", "section-hero grid-paper", body)


def hero_statement(c):
    pts = "\n".join(f'''<div>
<p class="ref" {fl(f"point_{i}_label", f"Point {i} label")}>{l}</p>
<p class="mt-2 text-lg" {fl(f"point_{i}_text", f"Point {i} text")}>{t}</p>
</div>''' for i, (l, t) in enumerate(c["points"], 1))
    body = f'''<div class="container-site">
<p class="sheet-label" {fl("sheet", "Sheet label")}>{c["sheet"]}</p>
<h1 class="statement mt-10" {fl("title", "Title")}>{c["title"]}</h1>
<div class="mt-14 grid gap-10 border-t border-ink pt-8 md:grid-cols-12">
<div class="key-points md:col-span-9">
{pts}
</div>
<div class="flex flex-wrap items-start gap-2 md:col-span-3 md:justify-end">
{a("primary", "Primary button", c["primary"][1], c["primary"][0], "btn-primary")}
</div>
</div>
</div>'''
    return block("section", "hero-statement", "Hero (statement)", "A large statement with three key points", "section-hero", body)


def hero_split(c):
    body = f'''<div class="split-hero-text">
<div class="max-w-xl">
<p class="sheet-label" {fl("sheet", "Sheet label")}>{c["sheet"]}</p>
<h1 class="heading-display mt-8" {fl("title", "Title")}>{c["title"]}</h1>
<p class="lead mt-6" {fl("description", "Description")}>{c["lead"]}</p>
<div class="mt-8 flex flex-wrap gap-2">
{a("primary", "Primary button", c["primary"][1], c["primary"][0], "btn-primary")}
{a("secondary", "Secondary button", c["secondary"][1], c["secondary"][0], "btn-secondary")}
</div>
<p class="ref mt-10 border-t border-line pt-4" {fl("note", "Note")}>{c["note"]}</p>
</div>
</div>
{img("image", "Image", c["image"], c["alt"], 1200, 1400, "split-hero-image")}'''
    return block("section", "hero-split", "Hero (split)", "Text on one side and a tall photo on the other", "split-hero", body)


def hero_cover(c, with_card=False):
    card = ""
    if with_card:
        rows = "\n".join(f'''<div>
<dt {fl(f"card_{i}_label", f"Card row {i} label")}>{l}</dt>
<dd {fl(f"card_{i}_value", f"Card row {i} value")}>{v}</dd>
</div>''' for i, (l, v) in enumerate(c["card"], 1))
        card = f'''<div class="info-card lg:col-span-4 lg:col-start-9">
<p class="ref" {fl("card_title", "Card title")}>{c["card_title"]}</p>
<dl class="mt-4 grid gap-3">
{rows}
</dl>
</div>'''
    body = f'''{img("image", "Background image", c["image"], c["alt"], 2000, 1250, "cover-image")}
<div class="cover-shade" aria-hidden="true"></div>
<div class="container-site relative grid w-full gap-10 lg:grid-cols-12 lg:items-end">
<div class="lg:col-span-8">
<p class="cover-label" {fl("sheet", "Label")}>{c["sheet"]}</p>
<h1 class="cover-title mt-6" {fl("title", "Title")}>{c["title"]}</h1>
<p class="mt-6 max-w-xl text-lg opacity-90" {fl("description", "Description")}>{c["lead"]}</p>
<div class="mt-8 flex flex-wrap gap-2">
{a("primary", "Primary button", c["primary"][1], c["primary"][0], "btn-on-band")}
</div>
</div>
{card}
</div>'''
    bid, title = ("hero-cover-card", "Hero (cover with card)") if with_card else ("hero-cover", "Hero (cover)")
    desc = "Full-width photo with the headline and an information card" if with_card else "Full-width photo with the headline over it"
    return block("section", bid, title, desc, "cover-hero", body)


def hero_portrait(c):
    rows = "\n".join(f'''<div>
<dt {fl(f"fact_{i}_label", f"Fact {i} label")}>{l}</dt>
<dd {fl(f"fact_{i}_value", f"Fact {i} value")}>{v}</dd>
</div>''' for i, (l, v) in enumerate(c["facts"], 1))
    body = f'''<div class="container-site grid gap-12 lg:grid-cols-12 lg:items-end">
<div class="lg:col-span-8">
<p class="sheet-label" {fl("sheet", "Sheet label")}>{c["sheet"]}</p>
<h1 class="statement mt-8" {fl("title", "Name")}>{c["title"]}</h1>
<p class="lead mt-8 max-w-2xl" {fl("description", "Introduction")}>{c["lead"]}</p>
<div class="mt-8 flex flex-wrap gap-2">
{a("primary", "Primary button", c["primary"][1], c["primary"][0], "btn-primary")}
{a("secondary", "Secondary button", c["secondary"][1], c["secondary"][0], "btn-secondary")}
</div>
</div>
<div class="lg:col-span-4">
{img("image", "Portrait", c["image"], c["alt"], 800, 1000, "portrait max-w-80")}
<dl class="spec mt-6">
{rows}
</dl>
</div>
</div>'''
    return block("section", "hero-portrait", "Hero (portrait)", "Your name, a short introduction, a portrait and a few facts", "section-hero", body)


# Services and pricing

def services_schedule(c):
    rows = []
    for s in c["items"]:
        rows.append(item("article", "service-row", "Service", "services-schedule", "schedule-row", f'''<p class="ref" {fl("ref", "Ref")}>{s["ref"]}</p>
<div>
<h3 class="heading-md" {fl("title", "Title")}>{s["title"]}</h3>
<p class="mt-2 text-muted" {fl("description", "Description")}>{s["text"]}</p>
</div>
<p class="text-sm" {fl("includes", "Includes")}>{s["includes"]}</p>
<p class="cell-time" {fl("time", "Time")}>{s["time"]}</p>
<p class="cell-fee" {fl("fee", "Fee")}>{s["fee"]}</p>'''))
    body = f'''<div class="container-site">
{head(c)}
<div class="schedule-head" aria-hidden="true"><span>Ref</span><span>Service</span><span>Includes</span><span>Time</span><span>Fee</span></div>
{items("div", "", "service-row", "Services", rows)}
</div>'''
    return block("section", "services-schedule", "Services (schedule)", "Services with what is included, time and fee", "section", body, sid=c.get("id"))


def services_cards(c):
    cards = [item("article", "service-card", "Service", "services-cards", "service-card", f'''<span class="icon-tile">{icon(s["icon"])}</span>
<h3 class="heading-md mt-8" {fl("title", "Title")}>{s["title"]}</h3>
<p class="mt-3 flex-1 text-muted" {fl("description", "Description")}>{s["text"]}</p>
{a("link", "Link", s["href"], s["link"], "link-arrow mt-8 self-start")}''') for s in c["items"]]
    body = f'''<div class="container-site">
{head(c)}
{items("div", "grid gap-px border border-ink bg-ink md:grid-cols-3", "service-card", "Services", cards)}
</div>'''
    return block("section", "services-cards", "Services (cards)", "Section heading with service cards and icons", "section", body, sid=c.get("id"))


def services_rows(c):
    rows = [item("article", "treatment-row", "Treatment", "services-rows", "treatment-row", f'''{img("image", "Image", s["image"], s["alt"], 240, 240, "treatment-image")}
<div>
<h3 class="heading-md" {fl("title", "Title")}>{s["title"]}</h3>
<p class="mt-2 text-muted" {fl("description", "Description")}>{s["text"]}</p>
</div>
<p class="treatment-meta" {fl("meta", "Duration and price")}>{s["meta"]}</p>''') for s in c["items"]]
    body = f'''<div class="container-site grid gap-12 lg:grid-cols-12">
<div class="lg:col-span-4">
<div class="lg:sticky lg:top-28">
<p class="sheet-label" {fl("sheet", "Sheet label")}>{c["sheet"]}</p>
<h2 class="heading-lg mt-8" {fl("title", "Title")}>{c["title"]}</h2>
<p class="lead mt-6" {fl("description", "Description")}>{c["lead"]}</p>
</div>
</div>
{items("div", "border-t border-ink lg:col-span-8", "treatment-row", "Treatments", rows)}
</div>'''
    return block("section", "services-rows", "Services (rows with images)", "A list of services with small images, duration and price", "section", body, sid=c.get("id"))


def features_grid(c):
    cells = [item("div", "feature-cell", "Feature", "features-grid", "feature-cell", f'''<p class="ref" {fl("ref", "Ref")}>{f["ref"]}</p>
<h3 class="heading-md mt-6" {fl("title", "Title")}>{f["title"]}</h3>
<p class="mt-3 text-muted" {fl("description", "Description")}>{f["text"]}</p>''') for f in c["items"]]
    body = f'''<div class="container-site">
{head(c)}
{items("div", "feature-grid", "feature-cell", "Features", cells)}
</div>'''
    return block("section", "features-grid", "Features (grid)", "Six short features in a ruled grid", "section", body, sid=c.get("id"))


def pricing_tiers(c):
    tiers = []
    for t in c["items"]:
        cls = "tier tier-featured" if t.get("featured") else "tier"
        tiers.append(item("div", "pricing-tier", "Plan", "pricing-tiers", cls, f'''<p class="ref" {fl("name", "Name")}>{t["name"]}</p>
<p class="tier-price mt-6"><span {fl("price", "Price")}>{t["price"]}</span><span class="tier-period" {fl("period", "Period")}>{t["period"]}</span></p>
<p class="mt-4 text-muted" {fl("summary", "Summary")}>{t["text"]}</p>
<ul class="check-list mt-8" {rich("features", "Features")}>
{"".join(f"<li>{x}</li>" for x in t["features"])}
</ul>
{a("button", "Button", t["href"], t["button"], "btn-secondary mt-10 w-full")}''',
            extra=' cms-block-field="featured" cms-block-field-type="class" cms-block-field-title="Featured" cms-block-field-control="toggle" cms-block-field-checkbox-value="tier-featured"'))
    body = f'''<div class="container-site">
{head(c)}
{items("div", "tiers", "pricing-tier", "Plans", tiers)}
</div>'''
    return block("section", "pricing-tiers", "Pricing (tiers)", "Three plans with a featured one", "section", body, sid=c.get("id"))


# Work

def work_case_files(c):
    cases = []
    for p in c["items"]:
        spec = "\n".join(f'''<div>
<dt>{l}</dt>
<dd {fl(k, l)}>{v}</dd>
</div>''' for k, l, v in (("location", "Location", p["location"]), ("area", "Area", p["area"]), ("scope", "Scope", p["scope"]), ("year", "Completed", p["year"])))
        cases.append(item("article", "case-file", "Case file", "work-case-files", "case", f'''{img("image", "Image", p["image"], p["alt"], 1500, 1000, "case-image")}
<div class="case-body">
<p class="ref" {fl("ref", "Ref")}>{p["ref"]}</p>
<h3 class="heading-lg mt-3" {fl("title", "Title")}>{p["title"]}</h3>
<p class="mt-4 text-muted" {fl("story", "Story")}>{p["story"]}</p>
<dl class="spec mt-8">
{spec}
</dl>
</div>'''))
    body = f'''<div class="container-site">
{head(c)}
{items("div", "cases", "case-file", "Projects", cases)}
</div>'''
    return block("section", "work-case-files", "Work (case files)", "Projects with a photo, a short story and a spec sheet", "section bg-surface", body, sid=c.get("id"))


def work_gallery(c):
    # The gallery shows the 1st and 6th image of every six wide (3:2) and the others tall (3:4).
    sizes = [(1500, 1000) if i % 6 in (0, 5) else (900, 1200) for i in range(len(c["items"]))]
    figs = [item("figure", "gallery-item", "Gallery image", "work-gallery", "gallery-item", f'''{img("image", "Image", g["image"], g["alt"], *sizes[i], "gallery-image")}
<figcaption class="mt-3 flex justify-between gap-4"><span {fl("title", "Title")}>{g["title"]}</span><span class="ref" {fl("meta", "Meta")}>{g["meta"]}</span></figcaption>''') for i, g in enumerate(c["items"])]
    body = f'''<div class="container-site">
{head(c)}
{items("div", "gallery", "gallery-item", "Images", figs)}
</div>'''
    return block("section", "work-gallery", "Work (gallery)", "An image gallery with a varied grid and captions", "section", body, sid=c.get("id"))


def work_index(c):
    rows = [item("a", "project-row", "Project", "work-index", "project-row", f'''<span class="ref" {fl("year", "Year")}>{p["year"]}</span>
<span class="project-title" {fl("title", "Title")}>{p["title"]}</span>
<span class="text-muted" {fl("client", "Client")}>{p["client"]}</span>
<span class="ref md:text-right" {fl("discipline", "Discipline")}>{p["discipline"]}</span>''',
        extra=f' href="{p["href"]}" cms-block-field="link" cms-block-field-type="attr" cms-block-field-attribute="href" cms-block-field-title="Link"') for p in c["items"]]
    body = f'''<div class="container-site">
{head(c)}
<div class="project-head" aria-hidden="true"><span>Year</span><span>Project</span><span>Client</span><span>Discipline</span></div>
{items("div", "", "project-row", "Projects", rows)}
</div>'''
    return block("section", "work-index", "Work (index)", "A list of projects with year, client and discipline", "section", body, sid=c.get("id"))


def logos_row(c):
    names = [item("li", "logo-name", "Name", "logos-row", "logo-word", f'<span {fl("name", "Name")}>{n}</span>') for n in c["items"]]
    body = f'''<div class="container-site">
<div class="flex flex-col gap-6 border-y border-ink py-8 md:flex-row md:items-baseline md:gap-12">
<p class="ref shrink-0" {fl("title", "Title")}>{c["title"]}</p>
{items("ul", "flex flex-wrap items-baseline gap-x-10 gap-y-3", "logo-name", "Names", names)}
</div>
</div>'''
    return block("section", "logos-row", "Logos (names)", "A row of client or publication names", "bg-page py-10", body, sid=c.get("id"))


# Process, story, team, numbers

def process_timeline(c):
    steps = [item("li", "timeline-step", "Step", "process-timeline", "milestone", f'''<span class="milestone-mark" {fl("when", "When")}>{s["when"]}</span>
<h3 class="heading-md mt-6" {fl("title", "Title")}>{s["title"]}</h3>
<p class="mt-2 text-muted" {fl("description", "Description")}>{s["text"]}</p>''') for s in c["items"]]
    body = f'''<div class="container-site">
{head(c)}
{items("ol", "timeline", "timeline-step", "Steps", steps)}
</div>'''
    return block("section", "process-timeline", "Process (time line)", "Steps along a time line", "section", body, sid=c.get("id"))


def process_steps(c):
    steps = [item("li", "process-step", "Step", "process-steps", "big-step", f'''<span class="big-step-number" {fl("number", "Number")}>{s["number"]}</span>
<div>
<h3 class="heading-md" {fl("title", "Title")}>{s["title"]}</h3>
<p class="mt-2 text-muted" {fl("description", "Description")}>{s["text"]}</p>
</div>''') for s in c["items"]]
    body = f'''<div class="container-site grid gap-12 lg:grid-cols-12">
<div class="lg:col-span-5">
<p class="sheet-label" {fl("sheet", "Sheet label")}>{c["sheet"]}</p>
<h2 class="heading-lg mt-8" {fl("title", "Title")}>{c["title"]}</h2>
<p class="lead mt-6" {fl("description", "Description")}>{c["lead"]}</p>
</div>
{items("ol", "border-t border-ink lg:col-span-7", "process-step", "Steps", steps)}
</div>'''
    return block("section", "process-steps", "Process (numbered steps)", "Heading with large numbered steps", "section bg-surface", body, sid=c.get("id"))


def story_split(c):
    body = f'''<div class="container-site grid items-start gap-12 lg:grid-cols-12">
{img("image", "Image", c["image"], c["alt"], 1200, 1500, "img-frame aspect-[4/5] w-full lg:col-span-5")}
<div class="lg:col-span-6 lg:col-start-7">
<p class="sheet-label" {fl("sheet", "Sheet label")}>{c["sheet"]}</p>
<h2 class="heading-lg mt-8" {fl("title", "Title")}>{c["title"]}</h2>
<div class="mt-6 space-y-4 text-lg leading-relaxed text-muted" {rich("text", "Text")}>
{c["text"]}
</div>
</div>
</div>'''
    return block("section", "story-split", "Story (text and image)", "A short story next to a tall image", "section", body, sid=c.get("id"))


def team_grid(c):
    people = [item("figure", "team-member", "Person", "team-grid", "", f'''{img("photo", "Photo", p["image"], "Portrait of " + p["name"], 800, 1000, "portrait")}
<figcaption class="mt-4 border-t border-ink pt-3"><span class="heading-md block" {fl("name", "Name")}>{p["name"]}</span><span class="ref mt-1 block" {fl("role", "Role")}>{p["role"]}</span></figcaption>''') for p in c["items"]]
    body = f'''<div class="container-site">
{head(c)}
{items("div", "grid gap-8 sm:grid-cols-2 lg:grid-cols-3", "team-member", "People", people)}
</div>'''
    return block("section", "team-grid", "Team (grid)", "People with portraits, names and roles", "section", body, sid=c.get("id"))


def principles_list(c):
    rows = [item("div", "principle", "Principle", "principles-list", "principle-row", f'''<p class="ref" {fl("ref", "Ref")}>{p["ref"]}</p>
<h3 class="heading-md" {fl("title", "Title")}>{p["title"]}</h3>
<p class="text-muted" {fl("description", "Description")}>{p["text"]}</p>''') for p in c["items"]]
    body = f'''<div class="container-site">
{head(c)}
{items("div", "", "principle", "Principles", rows)}
</div>'''
    return block("section", "principles-list", "Principles (list)", "Numbered principles or promises", "section bg-surface", body, sid=c.get("id"))


def stats_band(c):
    stats = [item("div", "stat", "Number", "stats-band", "stat", f'''<p class="stat-value" {fl("value", "Value")}>{s["value"]}</p>
<p class="mt-3 opacity-80" {fl("label", "Label")}>{s["label"]}</p>''') for s in c["items"]]
    body = f'''<div class="container-site">
<p class="ref text-on-band/70" {fl("title", "Title")}>{c["title"]}</p>
{items("div", "stats", "stat", "Numbers", stats)}
</div>'''
    return block("section", "stats-band", "Numbers (band)", "Key numbers on the band color", "section-band", body)


def samples_board(c):
    s = [item("li", "sample", "Sample", "samples-board", "sample", f'''{img("image", "Image", x["image"], x["alt"], 400, 400, "sample-image")}
<p class="mt-3 font-semibold" {fl("name", "Name")}>{x["name"]}</p>
<p class="ref mt-1" {fl("note", "Note")}>{x["note"]}</p>''') for x in c["items"]]
    body = f'''<div class="container-site grid gap-12 lg:grid-cols-12">
<div class="lg:col-span-4">
<p class="sheet-label" {fl("sheet", "Sheet label")}>{c["sheet"]}</p>
<h2 class="heading-lg mt-8" {fl("title", "Title")}>{c["title"]}</h2>
<p class="lead mt-6" {fl("description", "Description")}>{c["lead"]}</p>
</div>
{items("ul", "sample-board lg:col-span-8", "sample", "Samples", s)}
</div>'''
    return block("section", "samples-board", "Sample board", "A board of materials or products with names", "section bg-surface", body, sid=c.get("id"))


def menu_list(c):
    groups = [item("div", "menu-group", "Menu group", "menu-list", "menu-group", f'''<h3 class="ref text-ink" {fl("title", "Title")}>{g["title"]}</h3>
<ul class="menu-items mt-4" {rich("items", "Items")}>
{"".join(f'<li><span>{n}</span><span>{p}</span></li>' for n, p in g["items"])}
</ul>''') for g in c["items"]]
    body = f'''<div class="container-site">
{head(c)}
{items("div", "grid gap-x-16 gap-y-12 md:grid-cols-3", "menu-group", "Menu", groups)}
</div>'''
    return block("section", "menu-list", "Menu (price list)", "A menu or price list in groups", "section", body, sid=c.get("id"))


def hours_location(c):
    rows = "\n".join(f'''<div>
<dt {fl(f"day_{i}", f"Days {i}")}>{d}</dt>
<dd {fl(f"hours_{i}", f"Hours {i}")}>{h}</dd>
</div>''' for i, (d, h) in enumerate(c["hours"], 1))
    body = f'''<div class="container-site grid gap-12 lg:grid-cols-12">
<div class="lg:col-span-5">
<p class="sheet-label" {fl("sheet", "Sheet label")}>{c["sheet"]}</p>
<h2 class="heading-lg mt-8" {fl("title", "Title")}>{c["title"]}</h2>
<p class="mt-6 text-lg" {rich("address", "Address")}>{c["address"]}</p>
{a("map", "Map link", c["map"], "Open in maps", "link-arrow mt-6")}
</div>
<div class="lg:col-span-6 lg:col-start-7">
<dl class="hours">
{rows}
</dl>
<p class="ref mt-4" {fl("note", "Note")}>{c["note"]}</p>
</div>
</div>'''
    return block("section", "hours-location", "Opening hours and location", "Opening hours with the address and a map link", "section", body, sid=c.get("id"))


def quote_large(c):
    body = f'''<div class="container-site grid gap-10 lg:grid-cols-12">
<p class="sheet-label lg:col-span-3" {fl("sheet", "Sheet label")}>{c["sheet"]}</p>
<figure class="lg:col-span-9">
<blockquote class="quote-xl" {fl("quote", "Quote")}>{c["quote"]}</blockquote>
<figcaption class="mt-10 flex items-center gap-4">{img("photo", "Photo", c["image"], "Portrait of " + c["name"], 160, 160, "h-14 w-14 object-cover")}<span><span class="block font-semibold" {fl("name", "Name")}>{c["name"]}</span><span class="ref mt-1 block" {fl("role", "Role")}>{c["role"]}</span></span></figcaption>
</figure>
</div>'''
    return block("section", "quote-large", "Testimonial (large)", "One large quote with a name and photo", "section", body)


def notes_columns(c):
    notes = [item("figure", "client-note", "Note", "notes-columns", "client-note", f'''<blockquote class="quote" {fl("quote", "Quote")}>{n["quote"]}</blockquote>
<figcaption class="mt-6"><span class="block font-semibold" {fl("name", "Name")}>{n["name"]}</span><span class="ref mt-1 block" {fl("project", "Project")}>{n["project"]}</span></figcaption>''') for n in c["items"]]
    body = f'''<div class="container-site grid gap-12 lg:grid-cols-12">
<div class="lg:col-span-4">
<p class="sheet-label" {fl("sheet", "Sheet label")}>{c["sheet"]}</p>
<h2 class="heading-lg mt-8" {fl("title", "Title")}>{c["title"]}</h2>
</div>
{items("div", "grid gap-x-10 gap-y-14 md:grid-cols-2 lg:col-span-8", "client-note", "Notes", notes)}
</div>'''
    return block("section", "notes-columns", "Testimonials (notes)", "Short client notes in two columns", "section", body, sid=c.get("id"))


def faq_list(c):
    qs = [item("details", "faq-item", "Question", "faq-list", "faq-item", f'''<summary {fl("question", "Question")}>{q}</summary>
<p class="faq-answer" {rich("answer", "Answer")}>{ans}</p>''') for q, ans in c["items"]]
    body = f'''<div class="container-site grid gap-12 lg:grid-cols-12">
<div class="lg:col-span-4">
<p class="sheet-label" {fl("sheet", "Sheet label")}>{c["sheet"]}</p>
<h2 class="heading-lg mt-8" {fl("title", "Title")}>{c["title"]}</h2>
</div>
{items("div", "border-t border-ink lg:col-span-8", "faq-item", "Questions", qs)}
</div>'''
    return block("section", "faq-list", "Questions (FAQ)", "Frequently asked questions", "section bg-surface", body, sid=c.get("id"))


# Calls to action and contact

def cta_band(c):
    body = f'''<div class="container-site grid gap-10 lg:grid-cols-12 lg:items-end">
<h2 class="cta-title lg:col-span-8" {fl("title", "Title")}>{c["title"]}</h2>
<div class="lg:col-span-4">
<p class="opacity-80" {fl("description", "Description")}>{c["lead"]}</p>
{a("button", "Button", c["button"][1], c["button"][0], "btn-on-band mt-6")}
</div>
</div>'''
    return block("section", "cta-band", "Call to action (band)", "A closing invitation on the band color", "section-cta", body, sid=c.get("id"))


def cta_split(c):
    body = f'''<div class="container-site grid items-center gap-10 lg:grid-cols-2">
{img("image", "Image", c["image"], c["alt"], 1400, 1000, "img-frame aspect-[7/5] w-full")}
<div>
<p class="sheet-label" {fl("sheet", "Sheet label")}>{c["sheet"]}</p>
<h2 class="heading-lg mt-8" {fl("title", "Title")}>{c["title"]}</h2>
<p class="lead mt-6" {fl("description", "Description")}>{c["lead"]}</p>
{a("button", "Button", c["button"][1], c["button"][0], "btn-primary mt-8")}
</div>
</div>'''
    return block("section", "cta-split", "Call to action (with image)", "An image next to a heading and a button", "section bg-surface", body, sid=c.get("id"))


def newsletter(c):
    body = f'''<div class="container-site">
<div class="newsletter-box">
<div>
<p class="sheet-label" {fl("sheet", "Sheet label")}>{c["sheet"]}</p>
<h2 class="heading-lg mt-6" {fl("title", "Title")}>{c["title"]}</h2>
<p class="mt-4 text-muted" {fl("description", "Description")}>{c["lead"]}</p>
</div>
<form class="flex w-full flex-col gap-2 sm:flex-row" name="newsletter" method="POST" data-form data-form-endpoint="" data-netlify="true" netlify-honeypot="company_website" cms-form="newsletter_form" cms-form-send-email="true" cms-form-subject="New newsletter sign-up" cms-form-success-element="[data-form-success]" cms-form-error-element="[data-form-error]">
<input type="hidden" name="form-name" value="newsletter">
<p class="hidden" aria-hidden="true"><label>Leave this field empty <input type="text" name="company_website" tabindex="-1" autocomplete="off"></label></p>
<label class="sr-only" for="newsletter-email">Email address</label>
<input id="newsletter-email" class="field mt-0 flex-1" type="email" name="email" placeholder="you@example.com" autocomplete="email" required>
<button type="submit" class="btn-primary" data-pg-content-label="Button">{c["button"]}</button>
<p class="form-message hidden sm:basis-full" role="status" data-form-success data-pg-content-label="Thank you message">Thanks, you are on the list.</p>
<p class="form-message hidden sm:basis-full" role="alert" data-form-error data-pg-content-label="Error message">Sorry, that didn’t work. Please try again later.</p>
</form>
</div>
</div>'''
    return block("section", "newsletter", "Newsletter sign-up", "An email sign-up form", "section", body, sid=c.get("id"))


def contact_form(c):
    rows = "\n".join(f'''<div>
<dt {fl(f"detail_{i}_label", f"Detail {i} label")}>{l}</dt>
<dd {fl(f"detail_{i}_value", f"Detail {i} value")}>{v}</dd>
</div>''' for i, (l, v) in enumerate(c["details"], 1))
    opts = "\n".join(f"<option>{o}</option>" for o in c["options"])
    body = f'''<div class="container-site grid gap-12 lg:grid-cols-12">
<div class="lg:col-span-5">
<p class="sheet-label" {fl("sheet", "Sheet label")}>{c["sheet"]}</p>
<h1 class="heading-xl mt-8" {fl("title", "Title")}>{c["title"]}</h1>
<p class="lead mt-6" {fl("description", "Description")}>{c["lead"]}</p>
<dl class="title-block mt-10">
{rows}
</dl>
{img("image", "Image", c["image"], c["alt"], 1200, 900, "img-frame mt-10 aspect-[4/3] w-full")}
</div>
<div class="lg:col-span-6 lg:col-start-7">
<form class="grid gap-6 border border-ink bg-page p-6 sm:grid-cols-2 md:p-8" name="contact" method="POST" action="contact.html" data-form data-form-endpoint="" data-netlify="true" netlify-honeypot="company_website" cms-form="contact_form" cms-form-send-email="true" cms-form-subject="New message from your website" cms-form-success-element="[data-form-success]" cms-form-error-element="[data-form-error]" data-pg-name="Contact form">
<p class="ref sm:col-span-2" data-pg-content-label="Form label">{c["form_label"]}</p>
<input type="hidden" name="form-name" value="contact">
<p class="hidden" aria-hidden="true"><label>Leave this field empty <input type="text" name="company_website" tabindex="-1" autocomplete="off"></label></p>
<label class="field-label">Your name <input class="field" type="text" name="name" autocomplete="name" required></label>
<label class="field-label">Email <input class="field" type="email" name="email" autocomplete="email" required></label>
<label class="field-label">Phone (optional) <input class="field" type="tel" name="phone" autocomplete="tel"></label>
<label class="field-label">{c["select_label"]}
<select class="field" name="service">
{opts}
</select>
</label>
<label class="field-label sm:col-span-2">{c["message_label"]} <textarea class="field min-h-36" name="message" rows="5" required></textarea></label>
<div class="flex flex-col gap-4 sm:col-span-2 sm:flex-row sm:items-center sm:justify-between">
<p class="caption" data-pg-content-label="Privacy note">We only use your details to reply to you.</p>
<button type="submit" class="btn-primary" data-pg-content-label="Send button">{c["button"]}</button>
</div>
<p class="form-message hidden sm:col-span-2" role="status" data-form-success data-pg-content-label="Thank you message">Thank you. Your message is on its way; we will reply within two working days.</p>
<p class="form-message hidden sm:col-span-2" role="alert" data-form-error data-pg-content-label="Error message">Sorry, the message could not be sent. Please email us instead.</p>
</form>
</div>
</div>'''
    return block("section", "contact-form", "Contact (form)", "Contact details with a contact form", "section-hero grid-paper", body, sid=c.get("id"))


def contact_simple(c):
    rows = "\n".join(f'''<div>
<dt {fl(f"detail_{i}_label", f"Detail {i} label")}>{l}</dt>
<dd {fl(f"detail_{i}_value", f"Detail {i} value")}>{v}</dd>
</div>''' for i, (l, v) in enumerate(c["details"], 1))
    body = f'''<div class="container-site">
<p class="sheet-label" {fl("sheet", "Sheet label")}>{c["sheet"]}</p>
<h2 class="heading-lg mt-8 max-w-3xl" {fl("title", "Title")}>{c["title"]}</h2>
{email_link("email", "Email address", c["email"], "footer-email mt-8")}
<dl class="title-block mt-12 md:grid-cols-4">
{rows}
</dl>
</div>'''
    return block("section", "contact-simple", "Contact (simple)", "A large email address with a few details", "section", body, sid=c.get("id"))


# Posts and pages

def posts_latest(c):
    cards = []
    for i, p in enumerate(c["items"]):
        if i == 0:
            cards.append(f'''<article class="post-card" cms-post="block" cms-post-loop-block-attribute="posts" cms-post-loop-block-attribute-title="Posts" cms-post-loop-block-attribute-type="post">
<p class="ref"><span cms-tags="category" cms-tags-display="this">{p["cat"]}</span> · <span cms-post-date>{p["date"]}</span></p>
<a href="{p["href"]}" class="mt-4 block" cms-post-link><img src="images/{p["image"]}" alt="{p["alt"]}" width="1200" height="800" class="img-frame aspect-[3/2] w-full" cms-post-image="large"></a>
<h3 class="heading-md mt-5"><a href="{p["href"]}" cms-post-title cms-post-link>{p["title"]}</a></h3>
<p class="mt-3 text-muted" cms-post-excerpt>{p["excerpt"]}</p>
</article>''')
        else:
            cards.append(f'''<article class="post-card" cms-no-export>
<p class="ref"><span>{p["cat"]}</span> · <span>{p["date"]}</span></p>
<a href="{p["href"]}" class="mt-4 block"><img src="images/{p["image"]}" alt="{p["alt"]}" width="1200" height="800" class="img-frame aspect-[3/2] w-full"></a>
<h3 class="heading-md mt-5"><a href="{p["href"]}">{p["title"]}</a></h3>
<p class="mt-3 text-muted">{p["excerpt"]}</p>
</article>''')
    body = f'''<div class="container-site">
{head(c)}
<div class="grid gap-x-8 gap-y-14 md:grid-cols-3">
{chr(10).join(cards)}
</div>
</div>'''
    return block("section", "posts-latest", "Posts (selected)", "Three selected posts", "section", body, sid=c.get("id"))


def journal_list(c):
    cards = []
    for i, p in enumerate(c["items"]):
        if i == 0:
            cards.append(f'''<article class="post-card" cms-post="loop" data-pg-content-item="Post">
<p class="ref"><span cms-tags="category" cms-tags-display="this">{p["cat"]}</span> · <span cms-post-date>{p["date"]}</span></p>
<a href="{p["href"]}" class="mt-4 block" cms-post-link><img src="images/{p["image"]}" alt="{p["alt"]}" width="1200" height="800" class="img-frame aspect-[3/2] w-full" cms-post-image="large"></a>
<h2 class="heading-md mt-5"><a href="{p["href"]}" cms-post-title cms-post-link>{p["title"]}</a></h2>
<p class="mt-3 text-muted" cms-post-excerpt>{p["excerpt"]}</p>
<a href="{p["href"]}" class="link-arrow mt-5 self-start" cms-post-link>Read the note</a>
</article>''')
        else:
            cards.append(f'''<article class="post-card" cms-no-export data-pg-content-item="Post">
<p class="ref"><span>{p["cat"]}</span> · <span>{p["date"]}</span></p>
<a href="{p["href"]}" class="mt-4 block"><img src="images/{p["image"]}" alt="{p["alt"]}" width="1200" height="800" class="img-frame aspect-[3/2] w-full"></a>
<h2 class="heading-md mt-5"><a href="{p["href"]}">{p["title"]}</a></h2>
<p class="mt-3 text-muted">{p["excerpt"]}</p>
<a href="{p["href"]}" class="link-arrow mt-5 self-start">Read the note</a>
</article>''')
    body = f'''<div class="container-site">
{head(c, "h1")}
<div class="grid gap-x-8 gap-y-14 md:grid-cols-2 lg:grid-cols-3" data-pg-content-collection="Posts">
{chr(10).join(cards)}
</div>
</div>'''
    return block("section", "journal-list", "Posts (all, for the blog page)", "The list of posts for a blog or archive page", "section-hero", body)


def about_intro(c):
    rows = "\n".join(f'''<div>
<dt {fl(f"fact_{i}_label", f"Fact {i} label")}>{l}</dt>
<dd {fl(f"fact_{i}_value", f"Fact {i} value")}>{v}</dd>
</div>''' for i, (l, v) in enumerate(c["facts"], 1))
    body = f'''<div class="container-site">
<div class="grid gap-10 lg:grid-cols-12 lg:items-end">
<div class="lg:col-span-7">
<p class="sheet-label" {fl("sheet", "Sheet label")}>{c["sheet"]}</p>
<h1 class="heading-xl mt-8" {fl("title", "Title")}>{c["title"]}</h1>
<p class="lead mt-6 max-w-xl" {fl("description", "Description")}>{c["lead"]}</p>
</div>
<dl class="title-block lg:col-span-5">
{rows}
</dl>
</div>
{img("image", "Image", c["image"], c["alt"], 2400, 1029, "img-frame mt-12 aspect-[21/9] w-full")}
</div>'''
    return block("section", "page-intro", "Page intro (wide image)", "Page title with facts and a wide image", "section-hero grid-paper", body)


def post_single(c):
    return f'''<article class="section-hero" data-pg-name="Post" cms-block="post-single" cms-block-title="Post" cms-block-description="A single post with its image and text">
<div class="container-site max-w-3xl" cms-post="loop">
<p class="sheet-label"><span cms-tags="category" cms-tags-display="this">{c["cat"]}</span></p>
<h1 class="heading-xl mt-8" cms-post-title>{c["title"]}</h1>
<p class="ref mt-6"><span cms-post-date>{c["date"]}</span> · <span cms-author-field="display_name" cms-author-field-type="content">{c["author"]}</span></p>
<img src="images/{c["image"]}" alt="{c["alt"]}" width="1200" height="800" class="img-frame mt-10 aspect-[3/2] w-full" cms-post-image="large">
<div class="post-content mt-10" cms-post-content data-pg-content-label="Post text">
{c["body"]}
</div>
<a href="journal.html" class="link-arrow mt-12" cms-no-export>Back to the journal</a>
</div>
</article>'''


def not_found(c):
    body = f'''<div class="container-site max-w-3xl py-16">
<p class="sheet-label" {fl("sheet", "Sheet label")}>{c["sheet"]}</p>
<h1 class="heading-xl mt-8" {fl("title", "Title")}>{c["title"]}</h1>
<p class="lead mt-6" {fl("description", "Description")}>{c["lead"]}</p>
{a("button", "Button", "index.html", "Back to the home page", "btn-primary mt-9")}
</div>'''
    return block("section", "not-found", "Page not found", "Message for pages that don’t exist", "section-hero grid-paper", body)
