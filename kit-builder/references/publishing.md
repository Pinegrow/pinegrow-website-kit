# Publishing and handover

## Publish excludes

Pinegrow publishes the whole project folder except what `pinegrow.json` lists in `publish-excludes` (and its own
files). `kit.py library` adds `blocks`. Add anything else that is not part of the live site, for example
`form/README.md`, or starters the user won't use:

```json
"publish-excludes": ["blocks", "form/README.md"]
```

Edit `pinegrow.json` yourself for this (keep every other key; `kit.py library` keeps your entries).

Starter pages are pages like any other. Tell the user in the README to save the starter they choose as `index.html`
and delete the others (or add them to `publish-excludes`).

## Images

See `images.md`. Before handover, `kit.py check` lists the placeholder images that are left and, for Unsplash or
generated images, the ones missing from `source/image-credits.md`. Tell the user which images to replace, above all
team portraits and testimonial photos that aren't of the real people.

## Before handover

1. `kit.py check` shows no errors.
2. The user opened every page in Pinegrow, so `tailwind.css` is compiled; `kit.py check` then shows no missing
   classes.
3. Every saved design looks right on every page (the user switches them in the Design panel).
4. Every page works at phone width.
5. `README.md` in the kit folder explains: what's in the kit, the starters, the designs, the block library (Insert
   panel, "+" menu, `kit-blocks.html`), the contact form setup, where the images came from and which to replace,
   and the publish excludes.
