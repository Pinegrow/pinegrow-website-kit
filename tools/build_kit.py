#!/usr/bin/env python3
"""Builds the pages of the website kit from blocks.py and the content below.

  python3 tools/build_kit.py

Writes, in website/:
- index.html (a general site for "Your Company") and its inner pages about, contact, journal, post and 404: the site
  that is exported to WordPress (these pages have wp-template). Its header and footer are Pinegrow components
  (site-header, site-footer) defined on index.html, with instances on the other pages and on index-blank.html (see
  component()). index-blank.html has only the header and footer.
- index-architecture.html, index-agency.html, index-physio.html, index-cafe.html, index-portfolio.html,
  index-personal.html: starter home pages for different businesses, built from the same blocks, with inline headers
  and footers (no wp-template, so their blocks are not exported twice).
- wp-blocks.html: defines, for WordPress, every block that the general site's pages don't use, so that each block is
  defined exactly once (check_blocks() stops the build otherwise).
- blocks/kit-blocks.html and one page per category: the block library. Only kit-blocks.html (the home page) is
  registered as a Pinegrow page library in pinegrow.json (project_resources), so the Insert panel shows one tab; the
  home page's cards and the bar on every page open the category pages (see LIB_HEAD and the comment in build_pages).
  The pages use <base href="../">, so all URLs are written as from the project root and inserted blocks keep correct
  paths.
- grey placeholder images for any image that doesn't exist yet.

Close the project in Pinegrow (or open another one) before running this, then reopen it.
"""
import json
import os
import re
import struct
import subprocess
import sys
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import blocks as B  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB = os.path.join(ROOT, "website")

LIBRARY = "blocks/kit-blocks.html"

# Undoes Pinegrow's styling of .pg-lib-hover-menu (a small absolute badge) for the library navigation, and keeps the
# library's hover effect off the links. Two classes outrank Pinegrow's one-class rules wherever they are injected.
LIB_HEAD = """<style>
.lib-pass.pg-lib-hover-menu { position: static; top: auto; right: auto; height: auto; padding: 0; background: none;
    z-index: auto; white-space: normal; font-size: inherit; text-transform: none; transform: none; cursor: auto; }
.lib-nav.lib-pass.pg-lib-hover-menu { position: sticky; top: 0; z-index: 50; }
.lib-pass.pg-lib-hover-menu a { color: inherit; text-decoration: none; }
.lib-pass.pg-lib-hover-menu a:hover, .lib-pass.pg-lib-hover-menu .lib-current { text-decoration: underline; text-underline-offset: 4px; }
html body .lib-pass.pg-lib-hover-menu, html body .lib-pass.pg-lib-hover-menu *, html body .lib-pass.pg-lib-hover-menu *:hover {
    cursor: pointer !important; transform: none !important; box-shadow: none !important; }
</style>
<script>
/* Only whole blocks can be dragged from the library. Pinegrow 10.1 lets you drag any element from a library added in
   pinegrow.json (its selector is "*"), marking the element under the mouse with pg-draggable on mouseover. This marks
   the whole block instead, and keeps clicks inside blocks from picking inner elements. Runs only in the Insert panel:
   editor pages load with pgedit=1. */
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
                if (e.target.closest && e.target.closest(".lib-pass")) {
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

VOID = {"img", "input", "br", "meta", "link", "hr", "source", "base"}


def indent(html):
    out, depth = [], 0
    for raw in html.split("\n"):
        line = raw.strip()
        if not line:
            continue
        if line.startswith("</"):
            depth = max(0, depth - 1)
            out.append("    " * depth + line)
            continue
        out.append("    " * depth + line)
        m = re.match(r"<([a-zA-Z0-9]+)", line)
        if m and not line.startswith("<!"):
            tag = m.group(1).lower()
            if tag not in VOID and not line.endswith(f"</{tag}>") and not line.endswith("/>"):
                depth += 1
    return "\n".join(out) + "\n"


def page(title, desc, body, wp=False, base=False, body_cls="bg-page font-sans text-ink antialiased", head=""):
    return f'''<!DOCTYPE html>
<html lang="en" class="scroll-pt-24"{" wp-template" if wp else ""}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{'<base href="../">' if base else ""}
<title>{title}</title>
<meta name="description" content="{desc}">
<link href="tailwind_theme/tailwind.css" rel="stylesheet" type="text/css">
<script src="form/form.js" defer></script>
{head}</head>
<body class="{body_cls}">
<a href="#main" class="skip-link">Skip to content</a>
{body}
</body>
</html>'''


def site(header, sections, footer):
    return header + "\n<main id=\"main\">\n" + "\n".join(sections) + "\n</main>\n" + footer


def component(html, cid, name, desc, define):
    """The general site's header and footer are Pinegrow components, so they stay the same on every page: defined on
    index.html, instances on the other pages. Instances also have cms-no-export, so WordPress gets each block once.
    Updating components rebuilds instances from the definition and keeps only editable fields, so cms-no-export is an
    editable attribute of the root (with no_content, the content always comes from the definition)."""
    edit = ' data-pgc-edit="WordPress[cms-no-export,no_content]"'
    if define:
        attrs = f' data-pgc-define="{cid}" data-pgc-define-name="{name}" data-pgc-define-description="{desc}"' + edit
    else:
        attrs = f' data-pgc="{cid}" data-pgc-field="WordPress" cms-no-export'
    return re.sub(r"^(<(?:header|footer))", lambda m: m.group(1) + attrs, html, count=1)


def copy_of(html):
    """A block that is also used on another WordPress page: WordPress gets the block from that page."""
    return re.sub(r"^(<[a-z]+)", lambda m: m.group(1) + " cms-no-export", html, count=1)


def no_export(html):
    """Copies of the header and footer on other pages: defined once on index.html for WordPress."""
    return re.sub(r'(<(?:header|footer) [^>]*?)( cms-block=")', r'\1 cms-no-export\2', html, count=1)


# ---------------------------------------------------------------------------------------------------------------------
# Content: Northlight Interiors (interior studio)

NL = dict(name="Northlight Interiors", mark="NL",
          nav=[("Services", "#schedule"), ("Case files", "#cases"), ("Process", "#process"), ("Questions", "#questions")],
          cta=("Request a site visit", "#contact"),
          about="Interior design for homes and small workplaces.", address="48 Alder Street<br>Portland, OR 97205",
          email="hello@northlight.studio", phone="+1 503 555 0142")

NL_HERO = dict(sheet="Sheet A-00 · Introduction", title="Rooms that work as well as they look.",
               lead="We plan homes and small workplaces down to the last shelf, hinge and lamp, then stay on site until it’s built.",
               primary=("Request a site visit", "#contact"), secondary=("Open the case files", "#cases"),
               facts=[("Practice", "Homes and small workplaces"), ("Based in", "Portland, Oregon"), ("Since", "2014 · 140+ rooms"), ("Now booking", "Spring 2027")],
               image="hero.webp", alt="A calm living room with built-in oak shelving, a linen sofa and lime-washed walls",
               spots=[(17, 36), (50, 72), (82, 28)], legend="Harbour House · living room · 24 m²",
               callouts=["Built-in oak shelving, 4.2 m wall to wall", "The client’s own sofa, re-covered in linen", "Lime-wash walls that soften the north light"])

NL_SCHEDULE = dict(id="schedule", sheet="Sheet A-01", title="Schedule of services", lead="Four ways to work with us, with the fee agreed before we start.",
                   items=[dict(ref="S-01", title="Site consultation", text="Two hours in your space with a designer and a tape measure.", includes="Walk-through, layout and colour advice, written notes the next day", time="1 day", fee="€240"),
                          dict(ref="S-02", title="Room plan", text="Everything you need to finish one room yourself.", includes="Measured plan, lighting plan, material board, shopping list with links", time="3 weeks", fee="€1,450"),
                          dict(ref="S-03", title="Full project", text="Design and site management for a whole home.", includes="Technical drawings, builder selection, weekly site visits, final styling", time="3–6 months", fee="from €9,800"),
                          dict(ref="S-04", title="Small workplace", text="Studios, practices and shops people enjoy working in.", includes="Workflow study, layout, acoustics, lighting, furniture plan", time="6–10 weeks", fee="from €4,200")])

NL_CASES = dict(id="cases", sheet="Sheet A-02", title="Case files", lead="Three recent projects, and what we changed in each.",
                items=[dict(image="work-1.webp", alt="Kitchen with sage green cabinets, brass handles and a long oak table", ref="P-12", title="The Green Kitchen", story="A dark galley kitchen opened to the garden. We moved one wall, kept the old floor and built a table long enough for the whole family.", location="Sellwood, Portland", area="31 m²", scope="Full project", year="2026"),
                       dict(image="work-2.webp", alt="Bedroom with lime-plaster walls, a low wooden bed and morning light", ref="P-09", title="Quiet Morning Suite", story="A bedroom that faced a busy street. Heavy curtains, a new window seat and plaster walls made it the quietest room in the house.", location="Pearl District", area="18 m²", scope="Room plan", year="2025"),
                       dict(image="work-3.webp", alt="Small architecture studio with long desks, plants and pinned drawings", ref="P-07", title="Atelier Brandt", story="Eight architects in a former print shop. Long shared desks, a wall of pin-up boards and acoustic panels hidden in the ceiling.", location="Central Eastside", area="140 m²", scope="Small workplace", year="2025")])

NL_TIMELINE = dict(id="process", sheet="Sheet A-03", title="How a room plan runs", lead="From the first visit to a plan your builder can follow, in about three weeks.",
                   items=[dict(when="Day 1", title="Measure", text="We visit, listen, measure every wall and photograph the light."),
                          dict(when="Week 1", title="Two directions", text="Two layouts with samples you can touch and a budget for each."),
                          dict(when="Week 2", title="Detail", text="Drawings, lighting and a shopping list with every product linked."),
                          dict(when="Week 3", title="Hand over", text="We walk you and your builder through the plan, on site.")])

NL_SAMPLES = dict(sheet="Sheet A-04", title="On our sample board", lead="Honest materials that get better with use. We order samples for every project so you can see them in your own light.",
                  items=[dict(image="sample-oak.webp", alt="Oiled oak board", name="Oiled oak", note="Floors, shelving"),
                         dict(image="sample-linen.webp", alt="Folded natural linen", name="Washed linen", note="Curtains, covers"),
                         dict(image="sample-stone.webp", alt="Honed travertine tile", name="Travertine", note="Worktops, sills"),
                         dict(image="sample-plaster.webp", alt="Lime plaster wall texture", name="Lime plaster", note="Walls, ceilings")])

NL_NOTES = dict(sheet="Sheet A-05", title="Client notes",
                items=[dict(quote="They turned our dark flat into the brightest home on the street, and told us the cost of every change before we made it.", name="Maya Lindqvist", project="Harbour House · P-14"),
                       dict(quote="Our builder said it was the clearest set of drawings he’d ever been given. The kitchen is where everyone ends up now.", name="Daniel Okafor", project="The Green Kitchen · P-12")])

NL_FAQ = dict(id="questions", sheet="Sheet A-06", title="General notes",
              items=[("Do you work outside Portland?", "Yes. For projects more than an hour away we plan site visits around the key moments and work online in between."),
                     ("Can we keep some of our furniture?", "Usually most of it. We measure what you love first and design around it."),
                     ("Do you work with our builder?", "Gladly. Our drawings are made for builders. We can also recommend builders we trust and compare quotes with you."),
                     ("What does a site visit cost?", "A site consultation is €240. If you go on to a room plan, we take it off the fee.")])

NL_CTA = dict(title="Send us a photo of the room that bothers you most.", lead="We reply within two working days with a first idea and a date for a site visit.", button=("Request a site visit", "#contact"))

NL_ABOUT = dict(sheet="Sheet B-00 · The studio", title="A small studio that measures twice.",
                lead="Three designers, one workshop table and a long list of builders we trust. We take on a few projects at a time and see each one through.",
                facts=[("Founded", "2014"), ("Team", "3 designers"), ("Rooms designed", "140+"), ("Builders we trust", "12")],
                image="about-studio.webp", alt="The Northlight studio with a long work table, material samples and tall windows")

NL_STORY = dict(sheet="Sheet B-01", title="We start with how you live, not with a mood board.", image="about-detail.webp", alt="Hands sketching a floor plan next to fabric swatches",
                text="<p>Before we draw anything, we spend time in your space. Where does the morning light fall? Where do the bags land after school? Which chair does everyone fight over?</p>\n<p>Then we measure everything, twice. Good drawings are the reason our projects finish on time: builders know exactly what to do, and you know exactly what it costs.</p>")

NL_PRINCIPLES = dict(sheet="Sheet B-02", title="What you can count on", lead="Three things we promise on every project, large or small.",
                     items=[dict(ref="N-01", title="Fees before we start", text="Every proposal has a fixed fee. If something will cost more, you hear it from us first, in writing."),
                            dict(ref="N-02", title="Drawings builders love", text="Clear, measured drawings with every detail. Fewer questions on site, fewer surprises on the invoice."),
                            dict(ref="N-03", title="One designer, start to finish", text="The person who measures your room on day one is on site on the last day.")])

NL_TEAM = dict(sheet="Sheet B-03", title="The people you will work with", lead="Small on purpose. You will know everyone by name.",
               items=[dict(image="team-1.webp", name="Ingrid Holm", role="Founder · lead designer"), dict(image="team-2.webp", name="Tomás Reyes", role="Interior architect"), dict(image="team-3.webp", name="Aiko Tanaka", role="Project manager")])

NL_CONTACT = dict(sheet="Sheet C-00 · Contact", title="Request a site visit.", lead="Tell us about the space. We reply within two working days to arrange a visit.",
                  details=[("Email", "hello@northlight.studio"), ("Phone", "+1 503 555 0142"), ("Studio hours", "Mon–Fri, 9:00–17:00"), ("Address", "48 Alder Street, Portland")],
                  image="contact.webp", alt="The green front door of the studio on Alder Street", form_label="Form F-01 · Site visit request",
                  select_label="Service", options=["Site consultation", "Room plan", "Full project", "Small workplace", "Not sure yet"],
                  message_label="Which room, and what bothers you about it?", button="Send request")

POSTS = [dict(image="post-1.webp", alt="Morning light on a reading corner with a wool armchair", cat="Living", date="Nov 12, 2026", title="Five small changes that make a living room calmer", excerpt="Before you buy anything new, try moving what you already have. Here is where we always start.", href="post.html"),
         dict(image="post-2.webp", alt="Stacked samples of oak, ash and walnut boards", cat="Materials", date="Oct 28, 2026", title="Choosing wood that ages well", excerpt="Oak, ash or walnut? How each one looks after ten years of everyday life.", href="post.html"),
         dict(image="post-3.webp", alt="A narrow hallway with a long bench and hooks on a sage green wall", cat="Small spaces", date="Oct 9, 2026", title="Making the most of a narrow hallway", excerpt="Hallways work hard. A bench, the right hooks and one good lamp change everything.", href="post.html")]

NL_JOURNAL = dict(sheet="Sheet D-00 · Journal", title="Notes from the studio", lead="Small, practical ideas from real projects. One a month, never more.", items=POSTS)

NL_POST = dict(cat="Living", title="Five small changes that make a living room calmer", date="Nov 12, 2026", author="Ingrid Holm", image="post-1.webp", alt="Morning light on a reading corner with a wool armchair",
               body="""<p>Before you buy anything new, try moving what you already have. Most rooms feel restless because there is no clear place for the eye to rest.</p>
<h2>1. Choose one quiet wall</h2>
<p>Keep one wall almost empty. A single picture or a plant is enough. It gives everything else room to breathe.</p>
<h2>2. Lower the lights</h2>
<p>Replace one ceiling light with two or three lamps at different heights. Evenings will feel completely different.</p>
<h2>3. Hide the cables</h2>
<p>It sounds small, but tidy cables make a room look finished. A box behind the sofa does wonders.</p>
<blockquote>Good rooms are not full rooms. They are rooms where everything has a reason to be there.</blockquote>
<p>Try one change a week and notice how the room feels. When you are ready for a bigger step, we are happy to help.</p>""")

NL_404 = dict(sheet="Sheet 404", title="This drawing is missing from the set.", lead="The page you are looking for has moved or never existed.")

# ---------------------------------------------------------------------------------------------------------------------
# Content: Field Office (web agency)

FO = dict(name="Field Office", nav=[("Work", "#work"), ("Services", "#services"), ("Pricing", "#pricing"), ("Studio", "#studio")], cta=("Start a project", "#contact"),
          eyebrow="Have a project in mind?", statement="Let’s make something people will actually use.", email="hello@fieldoffice.studio")
FO_HERO = dict(sheet="Field Office · Digital studio", title="We design and build websites that people actually use.",
               points=[("Strategy", "We start with your goals and your visitors, not a template."), ("Design", "Clear, accessible interfaces that look like you."), ("Build", "Fast sites your team can edit without calling us.")],
               primary=("Start a project", "#contact"))
FO_LOGOS = dict(title="Trusted by", items=["Kettle & Crane", "Northern Rail Trust", "Lumen Labs", "Fieldwork Coffee", "Oakline Books"])
FO_FEATURES = dict(id="services", sheet="What we do", title="Six things we’re good at", lead="Most projects use three or four of them. We’ll tell you which.",
                   items=[dict(ref="01", title="Research", text="Interviews, analytics and a clear picture of who your visitors are."),
                          dict(ref="02", title="Content design", text="Words and structure that answer real questions."),
                          dict(ref="03", title="Visual design", text="A look that fits your brand and works on every screen."),
                          dict(ref="04", title="Web development", text="Clean HTML and CSS, fast pages, no lock-in."),
                          dict(ref="05", title="Accessibility", text="Checked against WCAG 2.2 AA before every launch."),
                          dict(ref="06", title="Care plans", text="Updates, small changes and monthly reports.")])
FO_INDEX = dict(id="work", sheet="Selected work", title="Recent projects", lead="A few of the sites we launched in the last two years.",
                items=[dict(year="2026", title="Explaining quantum sensors to anyone", client="Lumen Labs", discipline="Design · Build", href="#"),
                       dict(year="2026", title="A timetable you can read on a bike", client="Northern Rail Trust", discipline="Research · Design", href="#"),
                       dict(year="2025", title="An online shop for small-batch coffee", client="Fieldwork Coffee", discipline="Design · Build · Care", href="#"),
                       dict(year="2025", title="Every book, every event, one calendar", client="Oakline Books", discipline="Content · Build", href="#"),
                       dict(year="2024", title="A brand new site in six weeks", client="Kettle & Crane", discipline="Design · Build", href="#")])
FO_GALLERY = dict(sheet="In detail", title="Screens we’re proud of", lead="A closer look at a few of the projects.",
                  items=[dict(image="agency-1.webp", alt="A science website shown on a laptop", title="Lumen Labs", meta="2026"),
                         dict(image="agency-2.webp", alt="A train timetable on a phone held on a bicycle", title="Northern Rail Trust", meta="2026"),
                         dict(image="agency-3.webp", alt="A coffee shop website on a tablet next to a bag of beans", title="Fieldwork Coffee", meta="2025"),
                         dict(image="agency-4.webp", alt="A bookshop events calendar on a laptop", title="Oakline Books", meta="2025"),
                         dict(image="agency-5.webp", alt="Design sketches and printed screens on a studio wall", title="Process wall", meta="Studio"),
                         dict(image="agency-6.webp", alt="A website shown on several phones side by side", title="Kettle & Crane", meta="2024")])
FO_STATS = dict(title="Field Office in numbers", items=[dict(value="12", label="years building for the web"), dict(value="80+", label="sites launched"), dict(value="98", label="average Lighthouse score"), dict(value="4", label="people, no account managers")])
FO_QUOTE = dict(sheet="Client", quote="They asked better questions in the first week than we had asked ourselves in a year. The site finally explains what we do.", name="Dr. Hannah Moore", role="Director, Lumen Labs", image="agency-client.webp")
FO_TIERS = dict(id="pricing", sheet="Pricing", title="Three ways to work with us", lead="Fixed prices for most projects. We’ll quote larger ones after a call.",
                items=[dict(name="Launch", price="€6,000", period=" once", text="A focused site of up to 8 pages.", features=["Content and design", "Built in Pinegrow, yours to edit", "Accessibility check", "Two weeks of support"], button="Start with Launch", href="#contact"),
                       dict(name="Grow", price="€12,000", period=" once", text="A larger site with research and a content plan.", features=["Everything in Launch", "Visitor interviews", "Up to 25 pages", "Analytics set-up"], button="Start with Grow", href="#contact", featured=True),
                       dict(name="Care", price="€400", period=" / month", text="We look after your site so you don’t have to.", features=["Updates and backups", "Two hours of changes", "Monthly report", "Cancel any time"], button="Ask about Care", href="#contact")])
FO_CTA = dict(id="studio", sheet="The studio", title="Four people, one room, no account managers.", lead="You talk directly to the people who design and build your site.",
              image="agency-team.webp", alt="Four people working around a large table in a bright studio", button=("Meet us for a coffee", "#contact"))

# ---------------------------------------------------------------------------------------------------------------------
# Content: Movewell Physiotherapy

MW = dict(name="Movewell Physio", nav=[("Treatments", "#treatments"), ("First visit", "#first-visit"), ("Team", "#team"), ("Find us", "#find-us")], cta=("Book an appointment", "#find-us"),
          about="Physiotherapy for sport, work and everyday life.", address="Unit 3, 12 Mill Lane<br>Bristol BS1 6QA", email="hello@movewellphysio.co.uk", phone="0117 496 0321")
MW_HERO = dict(sheet="Physiotherapy · Bristol", title="Move without thinking about it.",
               lead="Hands-on treatment and a clear plan for back pain, sports injuries and recovery after surgery.",
               primary=("Book an appointment", "#find-us"), secondary=("See treatments", "#treatments"),
               note="Same-week appointments · Direct billing with most insurers", image="physio-hero.webp", alt="A physiotherapist guiding a patient through a shoulder exercise in a bright clinic")
MW_TREATMENTS = dict(id="treatments", sheet="Treatments", title="What we treat", lead="Every appointment is one to one, with the same physio each time.",
                     items=[dict(image="physio-treat-1.webp", alt="A physio taping a runner’s knee", title="Sports injuries", text="Sprains, strains, tendon problems and a safe way back to training.", meta="45 min · £65"),
                            dict(image="physio-treat-2.webp", alt="A physio treating a patient’s lower back", title="Back and neck pain", text="Hands-on treatment and exercises that fit into a working day.", meta="45 min · £65"),
                            dict(image="physio-treat-3.webp", alt="A patient doing a supported squat after knee surgery", title="Recovery after surgery", text="A step-by-step plan after knee, hip or shoulder surgery.", meta="60 min · £80"),
                            dict(image="physio-treat-4.webp", alt="A small Pilates class on reformer machines", title="Rehab Pilates classes", text="Small classes of four, led by a physiotherapist.", meta="55 min · £22")])
MW_STEPS = dict(id="first-visit", sheet="Your first visit", title="What happens at your first appointment", lead="Wear comfortable clothes. Everything else we’ll sort out together.",
                items=[dict(number="1", title="We listen", text="What happened, what hurts and what you want to get back to."),
                       dict(number="2", title="We assess", text="Movement, strength and a clear explanation of what’s going on."),
                       dict(number="3", title="We treat", text="Hands-on treatment in the same session, so you leave feeling better."),
                       dict(number="4", title="You get a plan", text="A few exercises on your phone and a date to check progress.")])
MW_TEAM = dict(id="team", sheet="Our physios", title="Chartered physiotherapists", lead="Registered with the HCPC and the Chartered Society of Physiotherapy.",
               items=[dict(image="physio-team-1.webp", name="Priya Shah", role="Sports and running injuries"), dict(image="physio-team-2.webp", name="Owen Hughes", role="Back pain and posture"), dict(image="physio-team-3.webp", name="Clara Novak", role="Post-surgery rehab, Pilates")])
MW_QUOTE = dict(sheet="Patient story", quote="After two years of knee pain I ran my first half marathon in October. Priya explained everything and never let me rush.", name="James Whitfield", role="Runner, 41", image="physio-patient.webp")
MW_HOURS = dict(id="find-us", sheet="Find us", title="Two minutes from Temple Meads", address="Unit 3, 12 Mill Lane<br>Bristol BS1 6QA", map="https://maps.google.com/",
                hours=[("Monday–Thursday", "7:30 – 20:00"), ("Friday", "7:30 – 18:00"), ("Saturday", "8:00 – 13:00"), ("Sunday", "Closed")], note="Step-free access · Bike parking at the door")
MW_FAQ = dict(sheet="Questions", title="Before you book",
              items=[("Do I need a referral?", "No. You can book directly. If you’re claiming on insurance, check whether your insurer needs one."),
                     ("Which insurers do you work with?", "We bill Bupa, AXA Health, Vitality and Aviva directly. Others can claim back with our receipt."),
                     ("What should I wear?", "Something comfortable you can move in. Shorts for knee problems, a vest top for shoulders."),
                     ("Can I cancel?", "Yes, free of charge up to 24 hours before your appointment.")])
MW_CTA = dict(title="Book your first visit this week.", lead="Online booking takes a minute. Or call us and we’ll find a time that works.", button=("Book an appointment", "#find-us"))

# ---------------------------------------------------------------------------------------------------------------------
# Content: Ember & Oat (café)

EO = dict(name="Ember & Oat", nav=[("Menu", "#menu"), ("Our story", "#story"), ("Visit", "#visit")], cta=("Find us", "#visit"),
          about="Coffee, bread and slow mornings since 2019.", address="7 Harbour Row<br>Leith, Edinburgh EH6 6JR", email="hello@emberandoat.co.uk", phone="0131 496 0718")
EO_HERO = dict(sheet="Café & bakery · Leith", title="Bread from the oven, coffee from down the street.",
               lead="A small café by the water. Sourdough at 7, cardamom buns at 9, and a seat by the window if you’re early.",
               primary=("See the menu", "#menu"), image="cafe-hero.webp", alt="A small café counter with loaves of bread and morning light",
               card_title="Open today", card=[("Today", "7:30 – 17:00"), ("Address", "7 Harbour Row, Leith"), ("Fresh bread", "From 7:30")])
EO_STORY = dict(id="story", sheet="Our story", title="We bake everything in the room behind the counter.", image="cafe-story.webp", alt="A baker shaping loaves on a floured wooden table",
                text="<p>Ember &amp; Oat started with one oven and a sourdough starter called Morag. Five years later we still bake every loaf, bun and tart ourselves, a few metres from where you sit.</p>\n<p>Our coffee comes from Steampunk Roasters, two streets away. The milk is from a farm in East Lothian. The oats, of course, are Scottish.</p>")
EO_MENU = dict(id="menu", sheet="Menu", title="Today at the counter", lead="Prices include VAT. Ask us about allergens; we’re happy to help.",
               items=[dict(title="Coffee", items=[("Espresso", "2.60"), ("Flat white", "3.60"), ("Filter", "3.40"), ("Oat latte", "3.90"), ("Hot chocolate", "3.80")]),
                      dict(title="Breakfast", items=[("Sourdough toast & butter", "4.50"), ("Granola, yoghurt & quince", "7.50"), ("Eggs on rye", "9.80"), ("Porridge with brown sugar", "6.20")]),
                      dict(title="Bakes", items=[("Cardamom bun", "3.80"), ("Rye brownie", "3.40"), ("Seasonal tart", "4.60"), ("Loaf of sourdough", "6.50")])])
EO_BAKES = dict(sheet="From the oven", title="This week’s bakes", lead="Out of the oven at 9. They don’t usually last past lunch.",
                items=[dict(image="cafe-bake-1.webp", alt="Cardamom buns on a tray", name="Cardamom bun", note="Every day"),
                       dict(image="cafe-bake-2.webp", alt="A dark crusted sourdough loaf", name="Country sourdough", note="Every day"),
                       dict(image="cafe-bake-3.webp", alt="A plum and almond tart", name="Plum & almond tart", note="This week"),
                       dict(image="cafe-bake-4.webp", alt="Squares of rye brownie", name="Rye brownie", note="Weekends")])
EO_HOURS = dict(id="visit", sheet="Visit", title="By the water in Leith", address="7 Harbour Row<br>Leith, Edinburgh EH6 6JR", map="https://maps.google.com/",
                hours=[("Monday–Friday", "7:30 – 17:00"), ("Saturday", "8:00 – 17:00"), ("Sunday", "9:00 – 15:00")], note="Dogs welcome · Laptop-free tables at the weekend")
EO_NEWS = dict(sheet="Newsletter", title="The Thursday bake", lead="One short email a week: what’s coming out of the oven, and the odd recipe.", button="Sign up")

# ---------------------------------------------------------------------------------------------------------------------
# Content: Ana Ruiz (photographer portfolio)

AR = dict(name="Ana Ruiz", nav=[("Work", "#work"), ("Clients", "#clients"), ("Contact", "#contact")], cta=("Book a shoot", "#contact"),
          about="Editorial and portrait photography, booking autumn 2027.", address="Rua da Rosa 112<br>1200-389 Lisboa", email="studio@anaruiz.photo", phone="+351 912 345 678")
AR_HERO = dict(sheet="Photography · Lisbon", title="Light, people and places.", lead="Editorial and portrait photography for magazines, architects and brands who care about quiet, honest pictures.",
               primary=("See the work", "#work"), image="photo-1.webp", alt="A woman standing in a doorway in warm late-afternoon light")
AR_GALLERY = dict(id="work", sheet="Selected work", title="Recent commissions", lead="Portraits, interiors and a few walks around Lisbon.",
                  items=[dict(image="photo-2.webp", alt="A ceramicist at work in her studio", title="The Ceramicist", meta="Kinfolk"),
                         dict(image="photo-3.webp", alt="A white stair winding up through a house", title="Casa Branca", meta="Architect: Ala Studio"),
                         dict(image="photo-4.webp", alt="Fishermen mending nets on a beach at dawn", title="Nazaré, 6 a.m.", meta="Personal"),
                         dict(image="photo-5.webp", alt="A chef plating a dish in a small kitchen", title="Taberna do Mar", meta="Monocle"),
                         dict(image="photo-6.webp", alt="Laundry drying between old houses in Alfama", title="Alfama", meta="Personal"),
                         dict(image="photo-7.webp", alt="A portrait of an old man in a flat cap", title="Senhor Augusto", meta="The Gentlewoman")])
AR_LOGOS = dict(id="clients", title="Published in", items=["Kinfolk", "Monocle", "Cereal", "The Gentlewoman", "Apartamento"])
AR_QUOTE = dict(sheet="Kind words", quote="Ana makes people forget the camera. Every portrait she sends us feels like a conversation.", name="Lena Fischer", role="Photo editor, Cereal", image="photo-client.webp")
AR_CONTACT = dict(id="contact", sheet="Contact", title="Tell me about your story, your deadline and your budget.", email="studio@anaruiz.photo",
                  details=[("Based in", "Lisbon, Portugal"), ("Travel", "Europe and beyond"), ("Booking", "Autumn 2027"), ("Agent", "Unrepresented")])

# ---------------------------------------------------------------------------------------------------------------------
# Content: Sam Rivera (personal site)

SR = dict(name="Sam Rivera", nav=[("Writing", "#writing"), ("Projects", "#projects"), ("Newsletter", "#newsletter")], cta=("Say hello", "mailto:sam@samrivera.dev"),
          eyebrow="Get in touch", statement="Working on something interesting? I’d love to hear about it.", email="sam@samrivera.dev")
SR_HERO = dict(sheet="Writer · developer", title="Sam Rivera", lead="I write about software that respects people’s time, and I build small, useful tools on the side.",
               primary=("Read the writing", "#writing"), secondary=("Get the newsletter", "#newsletter"), image="sam-portrait.webp", alt="Portrait of Sam Rivera",
               facts=[("Now", "Writing a book about calm software"), ("Before", "Product engineer at Lantern"), ("Based in", "Montréal")])
SR_POSTS = dict(id="writing", sheet="Writing", title="Recent essays", lead="About once a month. Never about productivity hacks.",
                items=[dict(image="sam-post-1.webp", alt="A notebook and a cup of coffee on a wooden desk", cat="Essay", date="Nov 3, 2026", title="Software that leaves you alone", excerpt="Notifications, streaks and red dots: what happens when we take them away.", href="#"),
                       dict(image="sam-post-2.webp", alt="A small brass bell on a white table", cat="Essay", date="Oct 1, 2026", title="The quiet power of a good default", excerpt="Most people never change a setting. That makes defaults a moral choice.", href="#"),
                       dict(image="sam-post-3.webp", alt="A city street in Montréal in the snow", cat="Notes", date="Sep 2, 2026", title="Building tools for one person", excerpt="Why I write software for exactly one user, and what it taught me.", href="#")])
SR_PROJECTS = dict(id="projects", sheet="Projects", title="Things I’ve made", lead="Small tools and experiments, mostly open source.",
                   items=[dict(year="2026", title="Hush, a notification budget for your phone", client="Open source", discipline="App", href="#"),
                          dict(year="2025", title="Plainfeed, a reader without algorithms", client="Side project", discipline="Web app", href="#"),
                          dict(year="2024", title="Calm Patterns, a catalogue of humane design", client="Website", discipline="Writing · Design", href="#")])
SR_NEWS = dict(id="newsletter", sheet="Newsletter", title="Get the next essay", lead="One email when something new is published. No tracking, unsubscribe any time.", button="Subscribe")

# Blank starter
BLANK = dict(name="Your site", nav=[("About", "#"), ("Services", "#"), ("Contact", "#")], cta=("Get in touch", "#"),
             about="One sentence about what you do.", address="Street and number<br>Postcode and town", email="hello@example.com", phone="+1 555 0100")

# ---------------------------------------------------------------------------------------------------------------------
# Content: the general site (index.html and its inner pages). Placeholder copy that says what goes where, so users can
# turn it into their own site. This is the site that is exported to WordPress.

GEN = dict(name="Your Company", home="index.html",
           nav=[("Services", "index.html#services"), ("About", "about.html"), ("Journal", "journal.html"), ("Contact", "contact.html")],
           cta=("Get in touch", "contact.html"),
           about="One sentence about what you do and who it is for.", address="Street and number<br>Postcode and town",
           email="hello@example.com", phone="+1 555 0100")

GEN_HERO = dict(sheet="Your company · Your town", title="Say what you do in one clear sentence.",
                lead="Add two lines about who you help and how. Visitors decide in a few seconds whether they are in the right place.",
                primary=("Get in touch", "contact.html"), secondary=("See services", "#services"),
                note="Your opening hours · Where you work · A short promise", image="about-detail.webp", alt="Hands sketching a plan at a work table")
GEN_LOGOS = dict(title="Trusted by", items=["Client One", "Client Two", "Client Three", "Client Four", "Client Five"])
GEN_SERVICES = dict(id="services", sheet="Services", title="What we can do for you", lead="Three services is a good start. Add more cards when you need them.",
                    items=[dict(icon="pen", title="First service", text="What it is, who it is for and what the client gets at the end.", link="Learn more", href="contact.html"),
                           dict(icon="chart", title="Second service", text="Keep each card to two lines, so visitors can compare them at a glance.", link="Learn more", href="contact.html"),
                           dict(icon="heart", title="Third service", text="End with the result, not with the process.", link="Learn more", href="contact.html")])
GEN_STEPS = dict(id="how-it-works", sheet="How it works", title="Working with us, step by step", lead="Explain what happens after someone gets in touch.",
                 items=[dict(number="1", title="We talk", text="A short call to understand what you need."),
                        dict(number="2", title="We propose", text="A clear plan with a fixed price and a date."),
                        dict(number="3", title="We do the work", text="Regular updates, so there are no surprises."),
                        dict(number="4", title="You’re all set", text="We hand over and stay available for questions.")])
GEN_QUOTE = dict(sheet="Client", quote="Put your best client quote here. A specific result works better than general praise.", name="Client name", role="Role, company", image="team-2.webp")
GEN_CTA = dict(title="Ready to start? Tell us what you need.", lead="We reply within two working days.", button=("Get in touch", "contact.html"))

GEN_ABOUT = dict(sheet="About", title="A sentence about who you are.",
                 lead="Tell your story in two or three sentences: when you started, what you believe and why clients choose you.",
                 facts=[("Founded", "Year"), ("Team", "Number of people"), ("Projects", "Number"), ("Based in", "Town")],
                 image="about-studio.webp", alt="A bright studio with a long work table")
GEN_STORY = dict(sheet="Our story", title="How it started, and where you are going.", image="work-3.webp", alt="A small studio with long desks and plants",
                 text="<p>Write a short paragraph about how the company started. Real details make it believable: a place, a year, a first client.</p>\n<p>Then say what you do differently today, and what a client can expect when they work with you.</p>")
GEN_PRINCIPLES = dict(sheet="Promises", title="What you can count on", lead="Three things clients can rely on every time.",
                      items=[dict(ref="01", title="First promise", text="A promise you keep on every project, stated plainly."),
                             dict(ref="02", title="Second promise", text="Something clients worry about, and how you handle it."),
                             dict(ref="03", title="Third promise", text="What happens after the work is done.")])
GEN_TEAM = dict(sheet="Team", title="The people behind the work", lead="Faces build trust. Add a photo and a role for everyone clients will meet.",
                items=[dict(image="team-1.webp", name="First Name", role="Founder"), dict(image="team-2.webp", name="Second Name", role="Role"), dict(image="team-3.webp", name="Third Name", role="Role")])
GEN_CONTACT = dict(sheet="Contact", title="Get in touch.", lead="Tell us what you need. We reply within two working days.",
                   details=[("Email", "hello@example.com"), ("Phone", "+1 555 0100"), ("Hours", "Mon–Fri, 9:00–17:00"), ("Address", "Street and number, Town")],
                   image="contact.webp", alt="The front door of the office", form_label="Contact form",
                   select_label="Topic", options=["General question", "First service", "Second service", "Third service"],
                   message_label="How can we help?", button="Send message")
GEN_POSTS = [dict(image="post-1.webp", alt="Morning light on a reading corner", cat="News", date="Nov 12, 2026", title="Your first post: answer a question clients ask", excerpt="Posts that answer real questions bring visitors from search. Start with the one you hear most.", href="post.html"),
             dict(image="post-2.webp", alt="Samples on a table", cat="Guides", date="Oct 28, 2026", title="A short guide to something you know well", excerpt="Show what you know. A practical guide builds more trust than a sales page.", href="post.html"),
             dict(image="post-3.webp", alt="A tidy hallway with a bench", cat="Projects", date="Oct 9, 2026", title="A recent project, before and after", excerpt="Tell one project as a story: the problem, what you did and the result.", href="post.html")]
GEN_JOURNAL = dict(sheet="Journal", title="News and notes", lead="Short posts about your work, your field and your clients’ questions.", items=GEN_POSTS)
GEN_POST = dict(cat="News", title="Your first post: answer a question clients ask", date="Nov 12, 2026", author="Your Name", image="post-1.webp", alt="Morning light on a reading corner",
                body="""<p>Start with the question in the client’s own words, then answer it in the first paragraph. Visitors who came from search want the answer before anything else.</p>
<h2>Explain the details</h2>
<p>Use short paragraphs and a heading for each part of the answer. Add an example from your own work.</p>
<blockquote>A good post answers one question well. Save the next question for the next post.</blockquote>
<p>End with one clear next step, for example a link to the contact page.</p>""")
GEN_404 = dict(sheet="404", title="This page doesn’t exist.", lead="It may have moved. Try the menu, or go back to the home page.")

# ---------------------------------------------------------------------------------------------------------------------
# Pages

def build_pages():
    nl_head, nl_foot = B.header_drawing(NL), B.footer_titleblock(NL).replace("<footer ", '<footer id="contact" ', 1)
    gen_head, gen_foot = B.header_simple(GEN), B.footer_columns(GEN)

    def gen_site(sections, define=False):
        return site(component(gen_head, "site-header", "Site header", "Logo, menu and a button. Edit it on index.html, Pinegrow updates every page.", define),
                    sections,
                    component(gen_foot, "site-footer", "Site footer", "Contact details and links. Edit it on index.html, Pinegrow updates every page.", define))

    start_here = '''<section class="section" data-pg-name="Start here">
<div class="container-site">
<p class="sheet-label">New page</p>
<h1 class="heading-xl mt-8">Add blocks from Insert › kit-blocks.html.</h1>
<p class="lead mt-6 max-w-2xl">Then delete this section. The header and footer are components: edit them on index.html and every page follows.</p>
</div>
</section>'''
    pages = {
        "index.html": (page("Your Company | Say what you do in one sentence", "One or two sentences about what you do and who it is for. Search engines show this text.",
                            gen_site([B.hero_split(GEN_HERO), B.logos_row(GEN_LOGOS), B.services_cards(GEN_SERVICES), B.process_steps(GEN_STEPS),
                                      B.quote_large(GEN_QUOTE), B.cta_band(GEN_CTA)], define=True), wp=True)),
        "about.html": (page("About | Your Company", "Who we are, what we believe and the people behind the work.",
                            gen_site([B.about_intro(GEN_ABOUT), B.story_split(GEN_STORY), B.principles_list(GEN_PRINCIPLES), B.team_grid(GEN_TEAM), copy_of(B.cta_band(GEN_CTA))]), wp=True)),
        "contact.html": (page("Contact | Your Company", "Get in touch. We reply within two working days.",
                              gen_site([B.contact_form(GEN_CONTACT)]), wp=True)),
        "journal.html": (page("Journal | Your Company", "News and notes about our work.",
                              gen_site([B.journal_list(GEN_JOURNAL)]), wp=True)),
        "post.html": (page("Your first post | Your Company", "Start with the question in the client’s own words, then answer it.",
                           gen_site([B.post_single(GEN_POST), copy_of(B.cta_band(GEN_CTA))]), wp=True)),
        "404.html": (page("Page not found | Your Company", "The page you are looking for has moved or never existed.",
                          gen_site([B.not_found(GEN_404)]), wp=True)),
        "index-blank.html": (page("New page | Your Company", "A page with only the header and footer. Add blocks from the Insert panel.",
                                  gen_site([start_here]))),
        "index-architecture.html": (page("Northlight Interiors | Rooms that work as well as they look", "Northlight Interiors plans homes and small workplaces down to the last shelf, hinge and lamp. Portland, Oregon.",
                                         site(nl_head, [B.hero_callouts(NL_HERO), B.services_schedule(NL_SCHEDULE), B.work_case_files(NL_CASES), B.process_timeline(NL_TIMELINE),
                                                        B.samples_board(NL_SAMPLES), B.notes_columns(NL_NOTES), B.faq_list(NL_FAQ), B.cta_band(NL_CTA)], nl_foot))),
        "index-agency.html": (page("Field Office | Websites people actually use", "Field Office is a small digital studio that designs and builds websites.",
                                   site(B.header_simple(FO), [B.hero_statement(FO_HERO), B.logos_row(FO_LOGOS), B.features_grid(FO_FEATURES), B.work_index(FO_INDEX),
                                                              B.work_gallery(FO_GALLERY), B.stats_band(FO_STATS), B.quote_large(FO_QUOTE), B.pricing_tiers(FO_TIERS), B.cta_split(FO_CTA)],
                                        B.footer_big(dict(FO, name="Field Office"))).replace('id="main"', 'id="main"', 1).replace("<footer ", '<footer id="contact" ', 1))),
        "index-physio.html": (page("Movewell Physio | Physiotherapy in Bristol", "Hands-on physiotherapy for back pain, sports injuries and recovery after surgery.",
                                   site(B.header_simple(MW), [B.hero_split(MW_HERO), B.services_rows(MW_TREATMENTS), B.process_steps(MW_STEPS), B.team_grid(MW_TEAM),
                                                              B.quote_large(MW_QUOTE), B.hours_location(MW_HOURS), B.faq_list(MW_FAQ), B.cta_band(MW_CTA)], B.footer_columns(MW)))),
        "index-cafe.html": (page("Ember & Oat | Café and bakery in Leith", "Bread from the oven, coffee from down the street. A small café by the water in Leith.",
                                 site(B.header_simple(EO), [B.hero_cover(EO_HERO, True), B.story_split(EO_STORY), B.menu_list(EO_MENU), B.samples_board(EO_BAKES),
                                                            B.hours_location(EO_HOURS), B.newsletter(EO_NEWS)], B.footer_columns(EO)))),
        "index-portfolio.html": (page("Ana Ruiz | Photography", "Editorial and portrait photography from Lisbon.",
                                      site(B.header_simple(AR), [B.hero_cover(AR_HERO), B.work_gallery(AR_GALLERY), B.logos_row(dict(AR_LOGOS)), B.quote_large(AR_QUOTE),
                                                                 B.contact_simple(AR_CONTACT)], B.footer_columns(AR)))),
        "index-personal.html": (page("Sam Rivera | Writer and developer", "Essays about calm software and small, useful tools.",
                                     site(B.header_simple(SR), [B.hero_portrait(SR_HERO), B.posts_latest(SR_POSTS), B.work_index(SR_PROJECTS), B.newsletter(SR_NEWS)], B.footer_big(SR)))),
    }

    def lib_section(name, html):
        return f'<div class="pg-lib-section">\n<p class="pg-lib-section-title lib-title">{name}</p>\n{html}\n</div>'

    libs = [
        ("Headers and footers", [("Header · drawing", B.header_drawing(NL)), ("Header · simple", B.header_simple(EO)),
                                                                ("Footer · title block", B.footer_titleblock(NL)), ("Footer · columns", B.footer_columns(MW)), ("Footer · big", B.footer_big(FO))]),
        ("Heroes", [("Hero · callouts", B.hero_callouts(NL_HERO)), ("Hero · statement", B.hero_statement(FO_HERO)), ("Hero · split", B.hero_split(MW_HERO)),
                                          ("Hero · cover with card", B.hero_cover(EO_HERO, True)), ("Hero · cover", B.hero_cover(AR_HERO)), ("Hero · portrait", B.hero_portrait(SR_HERO))]),
        ("Services and pricing", [("Services · schedule", B.services_schedule(NL_SCHEDULE)), ("Services · rows with images", B.services_rows(MW_TREATMENTS)),
                                                          ("Services · cards", B.services_cards(dict(sheet="Services", title="How we can help", lead="Pick one, or combine them.",
                                                                items=[dict(icon="home", title="Full home design", text="Layouts, lighting, materials and furniture for a whole home.", link="Plan a project", href="#"),
                                                                       dict(icon="plan", title="Room plans", text="A clear plan for one room, ready in three weeks.", link="Start a room", href="#"),
                                                                       dict(icon="light", title="Lighting design", text="Layered light for evenings that feel calm.", link="Light a room", href="#")]))),
                                                          ("Features · grid", B.features_grid(FO_FEATURES)), ("Pricing · tiers", B.pricing_tiers(FO_TIERS)), ("Menu · price list", B.menu_list(EO_MENU))]),
        ("Work", [("Work · case files", B.work_case_files(NL_CASES)), ("Work · index", B.work_index(FO_INDEX)), ("Work · gallery", B.work_gallery(AR_GALLERY)),
                                      ("Logos · names", B.logos_row(FO_LOGOS))]),
        ("Story and team", [("Page intro · wide image", B.about_intro(NL_ABOUT)), ("Story · text and image", B.story_split(NL_STORY)), ("Team · grid", B.team_grid(MW_TEAM)),
                                                      ("Principles · list", B.principles_list(NL_PRINCIPLES)), ("Process · time line", B.process_timeline(NL_TIMELINE)),
                                                      ("Process · numbered steps", B.process_steps(MW_STEPS)), ("Numbers · band", B.stats_band(FO_STATS)), ("Sample board", B.samples_board(NL_SAMPLES))]),
        ("Testimonials", [("Testimonials · notes", B.notes_columns(NL_NOTES)), ("Testimonial · large", B.quote_large(MW_QUOTE))]),
        ("Contact and calls to action", [("Call to action · band", B.cta_band(NL_CTA)), ("Call to action · with image", B.cta_split(FO_CTA)),
                                                                    ("Newsletter sign-up", B.newsletter(EO_NEWS)), ("Contact · form", B.contact_form(NL_CONTACT)),
                                                                    ("Contact · simple", B.contact_simple(AR_CONTACT)), ("Opening hours and location", B.hours_location(EO_HOURS)), ("Questions · FAQ", B.faq_list(NL_FAQ))]),
        ("Posts", [("Posts · selected", B.posts_latest(SR_POSTS)), ("Posts · all (blog page)", B.journal_list(NL_JOURNAL))]),
    ]
    # The block library: a home page (registered in pinegrow.json, so it is one Insert panel tab) that links to one
    # page per category, like Pinegrow's Tailwind blocks library. Libraries added through pinegrow.json get no page
    # menu in Pinegrow 10.1, and the library view turns clicks into element picks, except inside .pg-lib-hover-menu
    # (Pinegrow's own hover menu class). So the navigation sits in a .pg-lib-hover-menu, restyled by LIB_HEAD, and its
    # links open the other pages. Every page links back to the home page, because Back only knows pages opened from
    # the jump menu.
    slugs = [(cat, re.sub(r"[^a-z]+", "-", cat.lower().replace(" and ", " ")).strip("-"), secs) for cat, secs in libs]
    home_url = LIBRARY

    def lib_nav(current):
        links = [f'<a href="{home_url}" class="font-semibold{" lib-current" if current == home_url else ""}">All blocks</a>']
        links += [f'<a href="blocks/{slug}.html"{' class="lib-current"' if current == f"blocks/{slug}.html" else ""}>{cat}</a>' for cat, slug, _ in slugs]
        return f'''<div class="pg-lib-hover-menu lib-pass lib-nav">
<nav class="flex flex-wrap gap-x-5 gap-y-1 bg-ink px-5 py-3 font-mono text-xs tracking-wider text-page uppercase" aria-label="Block library">
{chr(10).join(links)}
</nav>
</div>'''

    cards = "\n".join(f'''<a href="blocks/{slug}.html" class="lib-card block border border-ink bg-surface p-6">
<span class="font-display text-2xl font-semibold">{cat}</span>
<span class="ref mt-2 block">{len(secs)} blocks</span>
<span class="mt-4 block text-sm text-muted">{", ".join(n.split(" · ")[-1] if " · " in n else n for n, _ in secs)}</span>
</a>''' for cat, slug, secs in slugs)
    home = f'''{lib_nav(home_url)}
<div class="container-site py-12">
<h1 class="heading-lg">{sum(len(secs) for _, secs in libs)} blocks</h1>
<p class="lead mt-4 max-w-3xl">Click a category to open it, then drag a block to your page. The bar at the top takes you
to another category or back here. Blocks use the project’s design and component styles, so they match every page.</p>
<div class="pg-lib-hover-menu lib-pass mt-10">
<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
{cards}
</div>
</div>
</div>'''
    pages[home_url] = page("Blocks | Block library", "Every block of the kit by category. Click a category, then drag blocks into your pages.", home,
                           base=True, body_cls="bg-page font-sans text-ink antialiased lib-page", head=LIB_HEAD)
    lib_pages = [home_url]
    for cat, slug, secs in slugs:
        url = f"blocks/{slug}.html"
        body = lib_nav(url) + "\n" + "\n".join(lib_section(n, h) for n, h in secs)
        pages[url] = page(f"{cat} | Block library", f"Block library: {cat.lower()}. Drag blocks into your pages.", body,
                          base=True, body_cls="bg-page font-sans text-ink antialiased lib-page", head=LIB_HEAD)
        lib_pages.append(url)

    # WordPress: every block is defined once, on a page with wp-template in the project root (the exporter resolves
    # image paths from the page's folder and ignores <base>, so the library pages in blocks/ can't define them).
    # The Northlight pages define their blocks; wp-blocks.html defines all the others.
    defined = set()
    for url, html in pages.items():
        if " wp-template" in html.split("\n", 2)[1]:
            defined |= set(re.findall(r'<(?:section|header|footer|div)(?![^>]*\scms-no-export[\s>=])[^>]* cms-block="([^"]+)"(?![^>]*cms-block-parent)', html))
    extra = []
    for cat, sections in libs:
        for n, h in sections:
            bid = re.search(r' cms-block="([^"]+)"', h).group(1)
            if bid not in defined:
                extra.append(lib_section(n, h))
                defined.add(bid)
    intro = '''<div class="pg-lib-section" cms-no-export>
<p class="pg-lib-section-title lib-title">WordPress blocks</p>
<div class="container-site py-12">
<p class="lead max-w-3xl">This page defines the WordPress blocks that the Northlight pages don’t use. Edit a block here (or on the
Northlight page that has it) to change it in the exported WordPress theme. Visitors never see this page.</p>
</div>
</div>'''
    pages["wp-blocks.html"] = page("WordPress blocks", "Definitions of WordPress blocks that are not used on the Northlight pages.",
                                   intro + "\n" + "\n".join(extra), wp=True, body_cls="bg-page font-sans text-ink antialiased lib-page")
    return pages, [LIBRARY], lib_pages


def check_blocks(pages):
    """Every block id used anywhere must be defined exactly once on the WordPress pages."""
    used, defined = set(), {}
    for url, html in pages.items():
        top = re.findall(r'<(?:section|header|footer|div)(?![^>]*\scms-no-export[\s>=])[^>]* cms-block="([^"]+)"(?![^>]*cms-block-parent)', html)
        used |= set(top)
        if " wp-template" in html.split("\n", 2)[1]:
            for bid in top:
                defined.setdefault(bid, []).append(url)
    subs = {}
    for url, html in pages.items():
        if " wp-template" in html.split("\n", 2)[1]:
            for tag in re.findall(r'<[a-z]+[^>]* cms-block-parent="[^"]*"[^>]*>', html):
                if not re.search(r'\scms-no-export[\s>=]', tag):
                    subs.setdefault(re.search(r' cms-block="([^"]+)"', tag).group(1), []).append(url)
    problems = [f"{b} not exported" for b in sorted(used - set(defined))]
    problems += [f"sub-block {b} defined {len(u)} times ({', '.join(sorted(set(u)))})" for b, u in sorted(subs.items()) if len(u) > 1]
    problems += [f"{b} defined on {', '.join(u)}" for b, u in sorted(defined.items()) if len(u) > 1]
    return problems


# ---------------------------------------------------------------------------------------------------------------------
# Placeholder images

PLACEHOLDERS = {"agency-1": (1500, 1000), "agency-2": (900, 1200), "agency-3": (900, 1200), "agency-4": (900, 1200), "agency-5": (900, 1200), "agency-6": (1500, 1000),
                "agency-team": (1400, 1000), "agency-client": (400, 400),
                "physio-hero": (1200, 1400), "physio-treat-1": (600, 600), "physio-treat-2": (600, 600), "physio-treat-3": (600, 600), "physio-treat-4": (600, 600),
                "physio-team-1": (800, 1000), "physio-team-2": (800, 1000), "physio-team-3": (800, 1000), "physio-patient": (400, 400),
                "cafe-hero": (2000, 1250), "cafe-story": (1200, 1500), "cafe-bake-1": (600, 600), "cafe-bake-2": (600, 600), "cafe-bake-3": (600, 600), "cafe-bake-4": (600, 600),
                "photo-1": (2000, 1250), "photo-2": (1500, 1000), "photo-3": (900, 1200), "photo-4": (900, 1200), "photo-5": (900, 1200), "photo-6": (900, 1200), "photo-7": (1500, 1000),
                "photo-client": (400, 400), "sam-portrait": (800, 1000), "sam-post-1": (1200, 800), "sam-post-2": (1200, 800), "sam-post-3": (1200, 800)}


def png_gradient(w, h, path):
    rows = []
    for y in range(h):
        t = y / max(1, h - 1)
        c = bytes([int(196 - 50 * t), int(186 - 48 * t), int(168 - 42 * t)])
        rows.append(b"\x00" + c * w)
    raw = zlib.compress(b"".join(rows), 9)

    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff)
    open(path, "wb").write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)) + chunk(b"IDAT", raw) + chunk(b"IEND", b""))


def placeholders():
    made = []
    os.makedirs(os.path.join(ROOT, "source", "images"), exist_ok=True)
    for name, (w, h) in PLACEHOLDERS.items():
        # Originals live in source/images/; kit-builder/scripts/kit.py optimize writes the WebP files the pages use.
        out = os.path.join(ROOT, "source", "images", name + ".jpg")
        if os.path.exists(out):
            continue
        tmp = os.path.join(WEB, "images", name + ".tmp.png")
        png_gradient(max(1, w // 8), max(1, h // 8), tmp)
        subprocess.run(["sips", "-s", "format", "jpeg", "-z", str(h), str(w), tmp, "--out", out], capture_output=True)
        os.remove(tmp)
        made.append(name)
    return made


# ---------------------------------------------------------------------------------------------------------------------

def main():
    pages, libs, lib_pages = build_pages()
    problems = check_blocks(pages)
    if problems:
        sys.exit("WordPress block problems:\n  " + "\n  ".join(problems))
    os.makedirs(os.path.join(WEB, "blocks"), exist_ok=True)
    for url, html in pages.items():
        with open(os.path.join(WEB, url), "w", encoding="utf-8") as f:
            f.write(indent(html))
    for name in ["blank.html"]:
        if os.path.exists(os.path.join(WEB, name)):
            os.remove(os.path.join(WEB, name))
    for name in os.listdir(os.path.join(WEB, "blocks")):
        if "blocks/" + name not in pages:
            os.remove(os.path.join(WEB, "blocks", name))

    pj_path = os.path.join(WEB, "pinegrow.json")
    pj = json.load(open(pj_path, encoding="utf-8"))
    pj["files"] = {url: {"frameworks": ["pg.tw.lib", "tw"]} for url in pages}
    pj["project_resources"] = [{"url": url, "type": "pinegrow/pagelib"} for url in libs]
    # Block libraries and WordPress templates are not part of the published static site.
    pj["publish-excludes"] = ["blocks", "templates", "wp-blocks.html", "form/README.md"]
    json.dump(pj, open(pj_path, "w", encoding="utf-8"))

    made = placeholders()
    print(f"wrote {len(pages)} pages ({len(libs)} block library); placeholders: {', '.join(made) or 'none'}")


if __name__ == "__main__":
    main()
