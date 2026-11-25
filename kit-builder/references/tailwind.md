# Tailwind CSS kits

Pinegrow compiles Tailwind CSS 4 itself. There is no config file and no build step for you: the design colors and
fonts come from the saved designs in `projectdb.pgml`, and the reusable styles are component styles.

## Saved designs: `source/designs.json`

```json
{
 "active": "linen",
 "designs": [
  {"id": "linen", "name": "Linen",
   "colors": {"page": "#f2eee5", "surface": "#e8e2d4", "ink": "#1e1c19", "muted": "#6a645a", "line": "#d5cdbb",
              "primary": "#c2462b", "on-primary": "#fff8f1", "band": "#1e1c19", "on-band": "#f2eee5"},
   "fonts": {"sans": "Hanken Grotesk", "display": "Hanken Grotesk", "mono": "IBM Plex Mono"}},
  {"id": "night", "name": "Night",
   "colors": {"page": "#111110", "surface": "#1b1a18", "ink": "#ecebe6", "muted": "#a19e95", "line": "#33312d",
              "primary": "#ef7a3c", "on-primary": "#111110", "band": "#ef7a3c", "on-band": "#111110"},
   "fonts": {"sans": "Inter", "display": "Space Grotesk", "mono": "Space Mono"}}
 ]
}
```

Rules, all checked by `kit.py designs`:

- every design has the same color names;
- names are lowercase with `-` and don't reuse a default Tailwind color name (`red`, `stone`...);
- values are `#hex` or `oklch(...)`;
- fonts are `sans` (required), `display` and `mono`, Google Fonts family names. For a serif, handwriting or other
  non-sans family, give the category so Pinegrow picks the right fallback:
  `"display": {"family": "Newsreader", "category": "serif", "weights": ["400", "500", "600"]}`.
- only upright styles are activated. Don't design with the italics of a Google font yet.

Run `kit.py designs <kit>` after every change. It writes the designs, keeps the default Tailwind colors in every
design and activates the fonts.

Each color becomes the usual utilities: `bg-page`, `text-ink`, `border-line`, `bg-primary/10`, `ring-primary`... In
arbitrary values use the variable: `bg-[color-mix(in_oklab,var(--color-line)_50%,transparent)]`. Fonts become
`font-sans`, `font-display` and `font-mono`.

## Component styles: `source/styles.txt`

One style per line, `.class-name: utilities`. A line starting with a space continues the previous style.

```
.container-site: mx-auto w-full max-w-7xl px-5 md:px-10
.section: border-t border-line bg-page py-20 md:py-28
.heading-xl: font-display text-5xl leading-[0.95] font-semibold tracking-tight text-ink md:text-7xl
.btn-primary: inline-flex items-center justify-center gap-2 bg-primary px-5 py-3 text-sm font-semibold
 text-on-primary transition hover:opacity-90 focus-visible:outline-2 focus-visible:outline-offset-2
 focus-visible:outline-primary
.price-list: divide-y divide-line border-y border-line [&>li]:flex [&>li]:justify-between [&>li]:py-3
```

Run `kit.py styles <kit>` after every change. Then use the class on elements: `<a class="btn-primary">`.

- Make a style for anything that repeats: containers, sections, headings, labels, buttons, cards, form fields, lists.
  Name it by purpose (`.btn-primary`, `.card-service`, `.eyebrow`), not by looks (`.green-button`).
- Keep layout placement inline (`md:col-span-7`, `order-2`, a one-off `mt-10`).
- One style can style its children with arbitrary variants: `[&_svg]:size-4`, `[&>li]:py-3`,
  `md:[&>*:nth-child(3n+1)]:col-span-2`.
- Never put `group`, `group/name`, `peer`, `peer/name` or `not-prose` in a style. Tailwind can't `@apply` them: the
  compile fails and Pinegrow quietly keeps the old CSS. Put them on the element (`class="card-service group"`).
- No fixed colors in styles. `kit.py styles` refuses them.
- A utility on the element always wins over the same property in a component style: Pinegrow compiles component
  styles into Tailwind's `components` layer, which comes before `utilities`. So `class="card-service text-on-band"`
  works for a card on a dark band. Check that the colors still contrast in every design.

## Pages

Every page in `website/` uses the same head and body classes:

```html
<!DOCTYPE html>
<html lang="en" class="scroll-pt-24">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Treatments | Movewell Physio</title>
    <meta name="description" content="Hands-on physiotherapy for back pain, sports injuries and recovery after surgery.">
    <link href="tailwind_theme/tailwind.css" rel="stylesheet" type="text/css">
    <script src="form/form.js" defer></script>
</head>
<body class="bg-page font-sans text-ink antialiased">
    <a href="#main" class="skip-link">Skip to content</a>
    <!-- header block -->
    <main id="main">
        <!-- blocks -->
    </main>
    <!-- footer block -->
</body>
</html>
```

The page examples use classes such as `.skip-link`, `.mobile-menu`, `.mobile-menu-button`, `.mobile-menu-panel`,
`.field`, `.field-label` and `.form-message`. They are component styles you define in `styles.txt` like any other
(`.skip-link: sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-50 focus:bg-primary ...`).

Include `form/form.js` only on pages with a form. `scroll-pt-24` keeps a sticky header from covering the target of
in-page links. `kit.py library` copies the body class of `index.html` to the library pages, so write `index.html`
before building the library.

A mobile menu without JavaScript:

```html
<details class="mobile-menu lg:hidden">
    <summary class="mobile-menu-button">Menu</summary>
    <nav class="mobile-menu-panel" aria-label="Main">...</nav>
</details>
```

Style `summary` with `list-none [&::-webkit-details-marker]:hidden` to hide the triangle.

## Checking the CSS

Until the user opens the project in Pinegrow and opens every page, `tailwind.css` is empty and pages look unstyled in
a browser. Pinegrow may compile once before all pages are open; if `kit.py check` then lists common utilities as
missing (`flex-col`, `gap-4`), ask the user to make any small change in Pinegrow (edit a word and change it back)
so it compiles again with every page. After that, `kit.py check` lists classes that are missing from the compiled CSS: usually a typo, a class
from Tailwind 3 that changed in 4 (`bg-opacity-50` is now `bg-black/50`, `flex-shrink-0` is `shrink-0`), or a page
that changed since Pinegrow last opened it.
