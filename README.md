# Pinegrow website kit

A client-ready website kit for Pinegrow 10.1 and later: a complete site, five more starter home pages, a library of 40
drag-and-drop blocks and four saved designs, all built with Tailwind CSS. Use it as it is, or as the start of your own
client sites.

## What's inside

- `website/`: the Pinegrow project. Open this folder in Pinegrow (File › Open project).
- `kit-builder/`: a skill for AI agents (Claude Code, Codex, Cursor...) that builds kits like this one for your own
  clients. See "Build your own kits" below.

### Pages

- **Northlight Interiors**, a complete site for an interior design studio: `index.html`, `about.html`, `contact.html`,
  `journal.html`, `post.html` and `404.html`.
- **Starter home pages** for other kinds of business, built from the same blocks:
  - `index-agency.html`: a web agency;
  - `index-physio.html`: a physiotherapy clinic;
  - `index-cafe.html`: a café and bakery;
  - `index-portfolio.html`: a photographer's portfolio;
  - `index-personal.html`: a personal site for a writer.
- `blank.html`: only the header and footer, to build a page from blocks.

To start a site from a starter, save it as `index.html` and delete the starters you don't need.

### Designs

Open the Design panel to switch between the four saved designs: Linen, Clear, Night and Pine. Each design changes
the colors and fonts of every page and block at once. Edit a design, or save your own, in the same panel. The default
Tailwind colors stay available in every design.

### Component styles

Buttons, headings, sections, cards and form fields use component styles (`.btn-primary`, `.section`, `.heading-lg`...).
Edit one in the Style panel and every element that uses it changes.

### Block library

The blocks are in a page library:

1. Open the Insert panel and click "+".
2. Under the project name, choose `kit-blocks.html`. Pinegrow keeps this tab from now on.
3. Click a category, then drag a block onto your page. The bar at the top of the library leads to the other
   categories and back to "All blocks".

### Content panel

Every block is a group in the Content panel, and repeated items (services, projects, people, questions, prices) can
be added, duplicated and reordered there. Your clients can edit texts and images without touching the design.

### Contact form

The contact form works on static hosting: with Netlify Forms when you publish to Netlify, or with a form service such
as Formspree or Web3Forms on any other host. `website/form/README.md` explains the setup.

### WordPress

The Northlight pages and `wp-blocks.html` define WordPress blocks, and `website/templates/` holds the block theme
templates (theme slug `northlight`). Export the project as a WordPress block theme with Pinegrow's WordPress
features, and every block can be used in the Site Editor.

### Images

The photos are in `website/images/` as WebP. Replace them with your own photos at the same names and proportions,
or change them in the Content panel.

## Build your own kits

`kit-builder/` teaches your AI agent how to build a kit like this one for your own business or clients: it asks a
few questions, picks a concept, writes the saved designs, component styles, blocks, block library and pages, gets the
photos, and checks the result. It needs Python 3 and works with Tailwind CSS static sites for now.

Copy the `kit-builder` folder into your agent's skills folder, or tell your agent:

> Read kit-builder/SKILL.md and build me a website kit for <your business>.

Open the kit it makes in Pinegrow to compile the CSS and finish it visually.
