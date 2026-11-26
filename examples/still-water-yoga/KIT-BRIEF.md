# Kit brief

Purpose: one client's site (Still Water Yoga, a small yoga studio in Ljubljana)
Businesses and pages: Still Water Yoga; home, classes and timetable, about (with the teachers), contact
CSS: Tailwind CSS
WordPress: no
Designs: 3
Block library: yes
Publishing: Netlify (contact form through Netlify Forms)
Images: Unsplash (free photos, credits in source/image-credits.md)
Concept: The class register. Every class has twelve mats and a page in the studio's register; the site is set like that register.

## Notes

Request: "Build me a website kit for my yoga studio, Still Water Yoga in Ljubljana. We teach small classes (max 12
people): vinyasa, slow flow, yin and a prenatal class, plus private sessions. I want a home page, a classes and
timetable page, an about page with the teachers, and a contact page. Make it look calm but not the usual pastel yoga
cliché."

Answers (given up front, the user was not available for the interview):

1. One business, the four pages above.
2. Tailwind CSS.
3. No WordPress, a static site.
4. Three saved designs and a block library.
5. Publishing on Netlify.

## Concept

**The class register.** Still Water keeps classes at twelve people. That number is the studio's promise, so the site
is set like the paper register at the front desk: a ledger of classes and times, ruled lines, mats numbered 01 to 12.
Calm comes from order and space, not from pastel colors, lotus icons or watercolor washes.

- Layout: long horizontal lines (still water, a horizon). Sections are separated by hairline rules, content sits in a
  12-column grid, headings are large and quiet, one strong element per section.
- Signature details carried through every block:
  - a "mat count": a row of twelve small marks next to class info (`.mat-count`), the visual sign of "max 12";
  - mono labels for times, durations, mat numbers and prices (`07:00`, `75 min`, `MAT 01-12`, `€18`);
  - numbered ledger rows for classes, steps and FAQs.
- Voice: plain, warm, specific. Times, prices, names, the street. Buttons say what happens: "Book a mat",
  "See the timetable", "Ask about a private session", "Send the message".
- Photography: honest, natural light, real bodies of different ages, the studio room with wooden floor and a window
  to the river. No sunsets, no beaches, no lotus, no silhouettes against the sky.

## Color roles

`page`, `surface`, `ink`, `muted`, `line`, `primary`, `on-primary`, `band`, `on-band` (the standard set).

## Fonts

| Design | sans | display | mono |
|---|---|---|---|
| River (active) | Instrument Sans | Newsreader | IBM Plex Mono |
| Oxide | Manrope | Manrope | DM Mono |
| Lamp | Figtree | Cormorant Garamond | IBM Plex Mono |

## Saved designs

- **River** (active): pale stone page, deep river-green accent, near-black band. A serif display face for calm.
- **Oxide**: crisp warm white, terracotta oxide accent, ink-blue band; one sans family for a sharper, modern feel.
- **Lamp**: dark evening studio, warm lamp-amber accent and band; for evening yin and the slower side of the studio.

## Blocks

- Headers and footers: header bar (sticky, mobile menu), footer register (columns), footer simple.
- Heroes: hero horizon (home), page title (inner pages), hero split (photo + intro).
- Classes: classes ledger, class feature (photo + text), mat count (the twelve-mat promise).
- Timetable and prices: week timetable, prices.
- Story and team: story split, teachers, first class steps.
- Quotes and calls to action: quote, call to action band.
- Contact: contact form, FAQ, getting here.

## Pages

`index.html`, `classes.html`, `about.html`, `contact.html`.
