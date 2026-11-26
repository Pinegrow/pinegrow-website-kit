# Still Water Yoga website kit

A Tailwind CSS website kit for Still Water Yoga, built to be opened and finished in Pinegrow (10.1 or later).
Open the `website` folder as the project.

## What's inside

- **Pages:** `index.html` (home), `classes.html` (classes, timetable, prices, your first class), `about.html`
  (the studio and the teachers) and `contact.html` (form, directions, questions).
- **Three saved designs** (Design panel): **River** (active; pale stone, river green, Instrument Sans + Newsreader +
  IBM Plex Mono), **Oxide** (warm white, terracotta, ink-blue band; Manrope + DM Mono) and **Lamp** (dark evening
  studio, lamp amber; Figtree + Cormorant Garamond + IBM Plex Mono). Switching the design restyles every page.
- **53 component styles** (Style panel): containers, sections, headings, buttons, the ledger rows, the timetable, form
  fields, the FAQ and the "mat count" (twelve small marks, the studio's sign for "max 12").
- **Block library** with 19 blocks in 7 categories, ready to drag onto new pages.
- **Content panel** labels on every block, so texts, prices, times and photos can be edited without touching the design.

## First steps in Pinegrow

1. Open the `website` folder in Pinegrow.
2. Open every page once (`index.html`, `classes.html`, `about.html`, `contact.html`). Pinegrow compiles the Tailwind CSS
   for the classes on the pages it has opened; until then the pages look unstyled in a browser.
3. Try the saved designs in the Design panel.

## The block library

In the Insert panel, open the "+" menu and choose `kit-blocks.html` under the project name. Click a category, then
drag a whole block onto your page. The dark bar at the top leads to the other categories and back to All blocks.
The library lives in `website/blocks/` and is not published.

## Editing the timetable and prices

The timetable is on `classes.html` (block "Timetable (week)"): one row per day, one line per class with time, class,
teacher and length. Prices are in "Prices (passes)" and in the class rows. The home page hero lists the drop-in price
and the morning times, so update those too.

## Contact form (Netlify)

The form on `contact.html` is ready for Netlify Forms. Publish the site to Netlify (Publish › Netlify), then turn on
email notifications in Netlify: Site configuration › Forms › Form notifications. On a `*.netlify.app` address it works
right away. With your own domain, select the form in Pinegrow and set its `data-form-endpoint` attribute to `netlify`.
Other hosts need a form service; the steps are in `website/form/README.md`.

## Images to replace

The photos in `website/images/` are free Unsplash photos (Unsplash License, no attribution required);
`source/image-credits.md` lists the photographer and photo page of each. They show models and other studios, not
Still Water, so replace at least the teacher portraits (`teacher-*.jpg`), the founder photo (`story-maja.jpg`), the
studio rooms (`hero-studio.jpg`, `about-room.jpg`) and the street (`studio-entrance.jpg`) with your own photos before
the site goes live. `source/image-prompts.md` lists every image with its size and ratio. Replace each file with a JPG
of the same name and size, and update its `alt` text in Pinegrow to describe the new photo.

## Placeholder details to check

The address (Trnovski pristan 14), phone (+386 40 123 456), email (hello@stillwateryoga.si), teacher names and bios,
the timetable, prices, the quotes and the directions are written as realistic examples. Replace them with the real ones.

## Publishing

`pinegrow.json` excludes `blocks` (the library) and `form/README.md` from publishing.

## For later changes

`source/` holds what the kit was built from: `designs.json`, `styles.txt`, the blocks and the image prompts.
`KIT-BRIEF.md` has the concept and decisions.
