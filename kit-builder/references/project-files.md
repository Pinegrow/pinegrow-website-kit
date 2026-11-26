# Pinegrow project files

The kit folder:

```
<kit>/
  KIT-BRIEF.md          the brief (questions, concept, decisions)
  README.md             handover notes for the user (you write it at the end)
  source/
    designs.json        saved designs, written into the project by kit.py designs
    styles.txt          component styles, written into the project by kit.py styles
    blocks/             one file per block, built into the library by kit.py library
    images/             original images (any size and format), never published
    image-prompts.md    a prompt for every image
  website/              the Pinegrow project: the folder the user opens in Pinegrow
    pinegrow.json       project settings
    projectdb.pgml      saved designs and component styles
    _pginfo/fonts.json  activated fonts
    tailwind_theme/tailwind.css   compiled by Pinegrow, never edit it
    images/             WebP images written by kit.py optimize
    form/               contact form script and its setup notes
    blocks/             the block library pages (generated)
    index.html ...      the pages
```

## Opening and closing

Pinegrow keeps open pages and project data in memory and saves them back. Before you change files in `website/` or
run `kit.py`, the project must be closed in Pinegrow (or another project opened). Ask the user to do it, or do it
with the `pinegrow` command if you have it. After your changes, the user opens the project again.

Pinegrow compiles `tailwind_theme/tailwind.css` from the classes on the pages it has opened and from the component
styles. So after opening the project, every page must be opened once. Until then, pages look unstyled in a browser.

## Components

On a site with several pages, the header and footer are Pinegrow components. The user edits them once on
`index.html`, and Components › Update the whole project copies them to every page.

- The definition, on `index.html`, gets `data-pgc-define="site-header"`, `data-pgc-define-name="Site header"` and
  `data-pgc-define-description` (one sentence: what it is, and that it is edited on index.html) on its root element.
- Every other page, `index-blank.html` included, has an instance: the same markup, character for character, with
  `data-pgc="site-header"` on the root instead of the three `data-pgc-define` attributes.
- The footer works the same way (`site-footer`, "Site footer").
- Starter home pages for other businesses keep their own header and footer, without component attributes.
- After changing the definition yourself, copy it to every instance the same way, so the pages agree before the
  user opens them.

## pinegrow.json

`kit.py init` writes a Tailwind CSS 4 project:

```json
{
 "files": {},
 "breakpoints": [],
 "frameworks": ["pg.tw.lib", "tw"],
 "template_framework_id": "tailwind",
 "active-design-provider": "tw",
 "design-settings": {"mode": "jit4", "external_source_url": null, "custom_source_url": null}
}
```

`kit.py library` adds the block library (`project_resources`) and `publish-excludes`. Pinegrow adds more keys while
the user works (open pages, view sizes). Keep them.

## projectdb.pgml

An XML file with the saved designs (`<dmdesigns>`), the component styles (`<classstyles>`) and which default Tailwind
colors are collapsed in the Design panel (`<dmlocked>`). Write it only through `kit.py designs` and `kit.py styles`,
which take care of the details:

- every design repeats the 22 default Tailwind colors, so they stay available in every design;
- custom colors follow as `<dmcolor key="ink" color="#1e1c19">`;
- fonts are a `fonts` skill: `family_1` is sans, `name_3="display" family_3` and `name_4="mono" family_4`;
- the active design has the `active` attribute;
- component styles are `<classstyle name=".btn" key=".btn" class="..." component>`, with `&` and `>` stored raw
  (Pinegrow writes them that way; escaping them breaks arbitrary variants such as `[&>li]:mt-2`).

## _pginfo/fonts.json

Pinegrow imports a Google font only when it is in the `activated` list. `kit.py designs` adds every font of every
design with weights 400 to 700 (400 and 500 for mono). If a family needs other weights, add
`"font_weights": {"Family Name": ["300", "400", "700"]}` to the design in `designs.json` and run `kit.py designs`
again (it only adds fonts that aren't activated yet, so remove the old entry from `fonts.json` first).
