# Black Friday 2026 gift: client-ready website kit

A Pinegrow 10.1+ website kit, given away with the Black Friday 2026 email: one complete site (Northlight Interiors),
five more starter home pages and a library of 40 blocks (42 WordPress blocks with the post and 404 blocks), all styled by the same saved designs and component styles.

## Folders

This folder is its own git repository, public at https://github.com/pinegrow/pinegrow-website-kit under the MIT
license (the workspace repository ignores `lab/`). `README.md` is for users and goes
into the download; this file is for us.

- `website/`: the Pinegrow project (Tailwind CSS 4, compiled by Pinegrow). In the download.
- `kit-builder/`: the skill that lets users build kits like this one with their own AI agent (Tailwind CSS, static
  sites so far; tested with two agent runs). See `notes/kit-builder-skill-plan.md`. In the download.
- `source/images/`: the original images (generated, any size). `kit-builder/scripts/kit.py optimize .` writes them
  to `website/images/` as WebP at the size each page uses. Not in the download.
- `tools/`: the generator that writes the pages (`blocks.py` has every block, `build_kit.py` the content and pages).
  Not in the download.
- `notes/`: working notes, for example `image-prompts.md`. Not in the download.
- Later: `tutorial/` for the Cactorial project that makes the videos, `gift-page/` if needed.

## Packaging

- `.gitignore` keeps Pinegrow's backups (`website/_pgbackup/`) and logs out of the repository.
- `.gitattributes` marks `tools/`, `notes/`, `source/`, this file and the packaging files `export-ignore`, so the zip
  holds only `README.md`, `LICENSE`, `website/` and `kit-builder/`. GitHub's release "Source code (zip)" follows the same rules.
- `./package.sh 1.0` makes `~/Documents/PinegrowDist/pinegrow-website-kit-1.0.zip` from the last commit, so commit
  first. To leave the skill out of a release, add `kit-builder/ export-ignore` to `.gitattributes`.

## What is in the website project

- **Northlight Interiors** (`index.html`, `about.html`, `contact.html`, `journal.html`, `post.html`, `404.html`): the
  complete site, laid out like a set of architect's drawings (title block, photo with numbered callouts, schedule of
  services, case files, time line, material sample board). This is the site that is exported to WordPress.
- **Starter home pages**, each a different business built from the same blocks:
  - `index-agency.html`: Field Office, a web agency (statement hero, project index, gallery, numbers, pricing).
  - `index-physio.html`: Movewell Physio, a clinic (split hero, treatments, first visit steps, team, hours, FAQ).
  - `index-cafe.html`: Ember & Oat, a café (cover hero with opening hours, story, menu, this week's bakes, newsletter).
  - `index-portfolio.html`: Ana Ruiz, a photographer (cover hero, gallery, publications, contact details).
  - `index-personal.html`: Sam Rivera, a personal site (portrait hero, essays, projects, newsletter).
  - `blank.html`: only the header and footer, to build a page from blocks.
- **Block library** (`blocks/`): a home page, `kit-blocks.html`, and one page per category (Headers and footers,
  Heroes, Services and pricing, Work, Story and team, Testimonials, Contact and calls to action, Posts), 40 blocks in
  all, like Pinegrow's Tailwind blocks library. `pinegrow.json` registers only the home page (`project_resources`), so
  the Insert panel shows one tab, `KIT-BLOCKS.HTML`. Users click a category card to open it, and a sticky bar on every
  page leads to the other categories and back to "All blocks".
  - Navigation: in Pinegrow 10.1 a library page turns every click into picking an element, except inside Pinegrow's
    own `.pg-lib-hover-menu`. The bar and the cards sit in a `.pg-lib-hover-menu.lib-pass` wrapper, so their links
    open pages; a `<style>` on each library page (`LIB_STYLE` in `build_kit.py`) undoes Pinegrow's badge styling of
    that class. `a.pg-lib-link` alone does not navigate (it only makes the link non-draggable), and Alt+click on a
    link also navigates. Tested in the dev app: cards and the bar navigate, blocks dragged from a category page
    insert correctly, and pages opened this way get Pinegrow ids even when they are not open in the editor.
  - Only whole blocks can be dragged. Pinegrow 10.1 gives a library added in `pinegrow.json` the selector `*`, so any
    element could be dragged (a button, half a section), and `pg-lib-item` has no effect then. A small script on each
    library page (in `LIB_HEAD`) marks the whole block under the mouse as draggable and blocks clicks inside blocks.
    It runs only in the Insert panel, not when a library page is open in the editor (`pgedit=1`). Tested: hovering a
    heading, button or table marks the whole section, the nav bar marks nothing, and a block dragged from a button
    inserts as the whole section without library attributes.
  - The toolbar's Back button and jump menu don't follow pages opened through links, so every page links to
    "All blocks".
  - The tab is not open by default: users add it once from the Insert panel's "+" menu (under the project name,
    `kit-blocks.html`). Pinegrow then keeps it.
  - The pages use `<base href="../">` and write URLs from the project root, so inserted blocks keep working image
    paths.
- **Design panel**: four saved designs, Linen, Clear, Night and Pine (active). They share the color names (page,
  surface, ink, muted, line, primary, on-primary, band, on-band), keep the default Tailwind colors, and set three fonts
  (sans for text, display for headings, mono for labels). Switching the design restyles every page and block. The fonts
  are activated in `_pginfo/fonts.json`, so Pinegrow imports them from Google Fonts.
- **Component styles** in `projectdb.pgml` (about 110: `.btn-primary`, `.sheet-label`, `.section-head`, `.tier`,
  `.gallery`, `.field`...), editable in the Style panel. They use only the design colors and fonts.
- **Content panel**: every block is a group, repeated items (services, projects, people, questions, plans, menu items)
  are collections, fields have clear labels (`data-pg-content-*`).
- **WordPress block theme**: every block is a WordPress block (`cms-block-*`), defined exactly once. The Northlight
  pages define the blocks they use (copies of the header and footer have `cms-no-export`), and `wp-blocks.html`
  defines all the others. Library pages and starters have no `wp-template`, so they are not exported. Templates are in
  `templates/` and use the theme slug `northlight`.
- **Contact form**: works on Netlify, with a form service, and as a WordPress form (no server-side mailer: it would
  be a security risk on shared hosting). See
  `website/form/README.md`.
- **Publishing**: `pinegrow.json` excludes `blocks/`, `templates/`, `wp-blocks.html` and `form/README.md` from
  publishing (`publish-excludes`), so the static site has only real pages.

## How users work with it

1. Open the `website` folder in Pinegrow. Pick a design in the Design panel.
2. Start from the starter closest to the business: save it as `index.html` (rename or delete the others), or start
   from `blank.html`.
3. Add blocks from the Insert panel: open `kit-blocks.html` from the panel's "+" menu, click a category, and drag a
   block to the page.
   Edit texts and images in the Content panel, styles in the Style panel (component styles change every block that
   uses them).
4. Publish the static site, or export the WordPress block theme. For WordPress, build the front page in
   `templates/front-page.html` from block ids (`<!-- wp:northlight/hero-split /-->`), the `cms-block` values on
   `wp-blocks.html` and the Northlight pages. To change how a block looks in WordPress, edit it where it
   is defined (a Northlight page or `wp-blocks.html`).

## Regenerating the pages

The pages are generated. After changing `tools/blocks.py` or `tools/build_kit.py`:

1. Open another project in Pinegrow (so it doesn't hold the kit's pages), then run `python3 tools/build_kit.py`.
   It stops if a block would be exported to WordPress twice or not at all.
2. Reopen the kit, open every page once (so their classes are compiled) and let Pinegrow compile
   `tailwind_theme/tailwind.css`. Component styles may not contain `group`, `peer` or `not-prose`: Tailwind then fails
   and Pinegrow keeps the old CSS.

Hand edits to generated pages are overwritten, so make them in the generator. `projectdb.pgml` (designs and
component styles), `templates/`, `form/` and `_pginfo/` are not generated.

## Compatibility

Built with features that shipped in Pinegrow 10.1 (saved designs, component styles, Content panel annotations, page
library from `project_resources`, publish excludes, WordPress blocks). Check it in the released 10.1 before giving
it away.

## Rules for editing

- Use only the design colors (`bg-page`, `text-ink`, `bg-primary`...) and fonts (`font-sans`, `font-display`) in
  pages and component styles, never fixed colors, so all four designs keep working.
- Every block sets its own background, because WordPress blocks don't inherit page styles.
- Before giving the project away: open every page in Pinegrow so the compiled CSS has all classes, delete
  `_pgbackup/`, and replace any remaining placeholder images (`notes/image-prompts.md`).
