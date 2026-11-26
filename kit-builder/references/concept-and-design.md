# Concept and design

A kit is worth something only if it doesn't look like every other generated website. Decide the concept before any
code, write it into `KIT-BRIEF.md`, and let it shape the layout, the voice and the small details.

## Find an idea from the business

Look for an object, document or ritual from the business itself and borrow its form. Examples:

- Interior designer: a set of architect's drawings. Title blocks, numbered callouts on a photo, a schedule of services
  with fees, case files with spec sheets, a material sample board.
- Café: the counter. A menu board with prices, "out of the oven at 9", opening hours as a timetable, this week's bakes.
- Physiotherapist: a treatment plan. Numbered steps of the first visit, treatment rows with duration and price, the
  team with their specialties.
- Photographer: a contact sheet. A gallery that varies its rhythm, captions with place and year, publications.
- Personal site of a writer: an index of essays with dates, a short colophon.

The idea shows in details, not decoration: labels in a mono font, numbering, rules and tables, how prices and times
are set, the words on buttons ("Request a site visit", not "Get started").

## Avoid the generic AI look

Don't use these unless the brief asks for them:

- Arch-shaped or blob-shaped image masks, floating 3D shapes, glassmorphism cards, gradient text, neon glows.
- A centered hero with a big gradient headline, two buttons and a stock photo of people smiling at laptops.
- Three identical feature cards with emoji or generic line icons, "Trusted by" logo strips with invented logos.
- Purple-to-blue gradients, everything with `rounded-2xl` and `shadow-xl`.
- Filler copy: "Elevate your...", "Unlock...", "seamless", "cutting-edge", lorem ipsum.

Prefer: a clear grid, generous but deliberate spacing, real hierarchy (one strong element per section), honest
photography, specific content (names, prices, places, times), and one or two signature details carried through every
block.

## Design tokens

Every page and style uses tokens, so the saved designs can restyle the whole kit.

Colors are roles, not hues. A set that works for most kits:

| Name | Role |
|---|---|
| `page` | page background |
| `surface` | alternate section and card background |
| `ink` | main text |
| `muted` | secondary text |
| `line` | rules and borders |
| `primary` | accent: buttons, links, markers |
| `on-primary` | text on `primary` |
| `band` | strong contrast sections (footer, call to action) |
| `on-band` | text on `band` |

Add a role only when a block needs it, and give it to every design. Check contrast: `ink` on `page` and `surface`,
`on-primary` on `primary`, `on-band` on `band` should all reach WCAG AA (4.5:1 for body text).

Fonts are three roles: `sans` (text), `display` (headings, may be the same family as `sans`) and `mono` (labels,
numbers, captions; optional). Use Google Fonts families.

## Saved designs

Make the designs genuinely different, not three tints of one palette. For example:

- a warm light design (paper, dark ink, one strong accent),
- a crisp white design with a different font pairing,
- a dark design (near-black page, light ink),
- a deep colored design (forest green or ink blue `band`).

Each design keeps the same color names and the same font roles. Name designs with one word (Linen, Clear, Night,
Pine), and make the active design the one that fits the business best.

## Blocks and starters

Plan the blocks as a set before writing them: headers and footers, heroes, services or features, work or gallery,
story and team, testimonials, calls to action, contact. Give each block one clear job. Two or three variants of the
important blocks (hero, services, footer) make the library useful for other businesses.

A starter is a home page built only from library blocks, with real content for one business. If the kit is for
several businesses, make one starter per business. Every kit also gets `index-blank.html` with only the header and
footer.
