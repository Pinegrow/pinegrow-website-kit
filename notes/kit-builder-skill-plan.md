# Plan: a skill that lets users build website kits with their own AI agent

Goal: give Pinegrow users a skill that their own agent (Claude Code, Codex, Cursor...) follows to build a client-ready
website kit like the Black Friday 2026 gift, for their own purpose and with Tailwind CSS, Bootstrap or plain CSS.

## How it reaches users

- A `kit-builder/` folder next to `website/` in the gift download, and later on its own (docs page, GitHub).
- Plain Markdown in the Agent Skills format (`SKILL.md` plus reference files), so any agent can use it: copy it to
  the agent's skills folder, or tell the agent "Read kit-builder/SKILL.md and build a kit for ...".
- Works with Pinegrow 10.1: the agent edits files while the project is closed in Pinegrow, the user opens it to
  compile and check. Where 10.2 brings the `pinegrow` command, a short optional section uses it instead.
- The gift kit is the worked example: the references point at its files ("annotate like `hero-split` in
  `blocks/heroes.html`") instead of repeating them.
- Announce it in its own email after the gift ("Make your own kits with your AI agent"), not on Black Friday.

## The interview

The agent asks at most five questions, each with a default, and skips what the user's prompt already answers. It
writes the answers to `KIT-BRIEF.md` in the project and rereads that file when the user comes back later.

1. Purpose: one client site, a reusable agency base, or a template to sell? Which businesses or pages (for example
   "physio clinic: home, treatments, team, contact")? Default: one business, home plus 3 pages.
2. CSS: Tailwind CSS, Bootstrap 5 or plain CSS? Default: Tailwind CSS.
3. WordPress block theme as well, or a static site only? Default: static only.
4. Design variants (saved designs) and a block library? Default: 3 designs, library yes.
5. Where it will be published: Netlify or another host? This picks the contact form (Netlify Forms or a form
   service; no server-side mailer, it's a security risk).
   Default: ask later, when the form is built.

## Files of the skill

```
kit-builder/
  SKILL.md                 workflow, the interview, rules for every kit, which reference to read for each answer
  references/
    concept-and-design.md  a distinctive concept, not the usual AI look; color roles; saved designs; blocks
    project-files.md       kit folder layout, pinegrow.json, projectdb.pgml, _pginfo/fonts.json, opening and closing
    tailwind.md            designs.json, styles.txt, page template, Tailwind traps
    content-panel.md       data-pg-content-* groups, collections, labels
    block-library.md       source/blocks layout, what kit.py library makes, how it behaves in Pinegrow
    forms.md               the contact form for Netlify and form services
    publishing.md          publish excludes, images, handover checklist
    wordpress.md, bootstrap.md, plain-css.md   "not in this version yet" notes
  scripts/
    kit.py                 init, designs, styles, images, library, check
    tw-default-colors.json the 22 default Tailwind colors written into every saved design
  form/                    form.js and README (copied into the project by kit.py init)
```

The kit the skill builds keeps its sources next to the Pinegrow project: `KIT-BRIEF.md`, `source/designs.json`,
`source/styles.txt`, `source/blocks/<NN-category>/<NN-block>.html` and `source/image-prompts.md`, with the project in
`website/`. `kit.py` writes the parts of the project that are easy to get wrong (saved designs with the default
Tailwind colors, font activation, component styles with raw `&`, the library pages with their navigation and drag
script, `project_resources`, `publish-excludes`).

`SKILL.md` tells the agent to read only the references that match the brief.

## What each CSS choice means in Pinegrow

Checked in the 10.2 source, and the Bootstrap rows confirmed by Matjaž (Nov 25): Bootstrap needs no "Customize & update
Bootstrap Theme", and its colors can be redefined but not added. Everything marked "test" still needs a test build.

| | Tailwind CSS | Bootstrap 5 | Plain CSS |
|---|---|---|---|
| Design panel provider | `tw` | `bs5` | `plainhtml` |
| Colors | any names (`tw.colors`), default Tailwind colors kept | Bootstrap's fixed set (`primary`, `secondary`, ..., `light`, `dark`); names can't be added (`colors.can_edit` is off) | any names (`plainhtml.colors`), written as CSS variables |
| Fonts | sans, display, mono (`fonts`) | text and headings (`fonts`, `headings`) | text and headings (`fonts`, `headings`) |
| Other design options | Tailwind options | text size, grid spacing, roundness, button roundness | plain HTML options |
| Where the design goes | compiled `tailwind_theme/tailwind.css` | Bootstrap's own color and font variables, no theme customization needed | `css/theme.css`, generated and locked by the Design panel |
| Saved designs (`<dmdesign>` in projectdb.pgml) | yes, tested in the gift kit | stored the same way, test | stored the same way, test |
| Reusable styles | component styles (Tailwind only: `show_class_styles` is set only by the Tailwind framework) | Bootstrap utility and component classes, plus classes in a project stylesheet (`css/style.css`) that use `var(--bs-*)` | classes in `css/style.css` that use the Design panel's CSS variables |
| Compile step | Pinegrow compiles when pages change; open every page once | none for the kit | none |
| Traps | no `group`, `peer` or `not-prose` in component styles; activate fonts in `_pginfo/fonts.json` | only Bootstrap's color names exist: design with roles mapped onto them | don't hand-edit `css/theme.css` |

The same in all three: Content panel annotations, WordPress blocks (`cms-*` attributes), the block library, the
contact form, publish excludes.

## Rules for every kit (in SKILL.md)

- Use only design tokens (design colors and fonts), never fixed colors, so every saved design works.
- Every block sets its own background (WordPress blocks don't inherit page styles).
- Blocks are self-contained sections with Content panel groups; repeated items are collections.
- Starters are home pages built only from library blocks.
- Hand-written pages are fine; a generator script (like `tools/build_kit.py`) is optional and only worth it for
  large kits.
- Close the project in Pinegrow before editing its files, then reopen it and open every page.
- Finish with `kit.py check` and fix everything it reports.

## The checker (`kit.py check`)

Always:
- links inside the kit resolve, images exist, every page has a title and description;
- no fixed colors where tokens belong (hex colors in classes and in project CSS outside the design files);
- every block has a Content panel group, every repeated item list is a collection;
- block library: home page registered in `project_resources`, every library page has `<base href="../">` and the
  library head, every block is a direct child of `.pg-lib-section`;
- publish excludes include the library and WordPress-only files.

Tailwind: component styles contain no `group`, `peer` or `not-prose`; every font used in a saved design is activated
in `_pginfo/fonts.json`; every class used in the pages is in the compiled CSS (after the user opened the project).

Bootstrap: pages and project CSS use only Bootstrap's color names and `var(--bs-*)`.

Plain CSS: project CSS uses only `var(--...)` colors; `css/theme.css` is not edited by hand.

WordPress: every block id is defined exactly once on root-level `wp-template` pages; ids use lowercase and `-`,
field ids `_`; repeated items are sub-blocks with `cms-block-parent`; every block in `templates/*.html` exists.

## Test plan

For each CSS choice, a fresh agent gets only the skill and a new brief, and builds a kit without help:

1. Tailwind, static, "yoga studio". Pass: checker clean, opens in Pinegrow, saved designs switch, library drags whole
   blocks, Content panel shows every field.
2. Tailwind with WordPress, "bakery". Pass: the above, plus export to a local WordPress site, blocks appear in the
   Site Editor and the contact form sends.
3. Bootstrap, static, "law firm". Pass: as test 1, and the pages use only Bootstrap's color names.
4. Plain CSS, static, "architect". Pass: as test 1.

Each test also gets a design review against the "not the usual AI look" rules. Only ship a CSS choice after its test
passes; until then `SKILL.md` says it is coming.

## Bootstrap colors

Bootstrap has a fixed set of colors (`primary`, `secondary`, `success`, `info`, `warning`, `danger`, `light`, `dark`).
The Design panel redefines them; it can't add new ones. So `bootstrap.md` has the agent design with color roles mapped
onto those names, for example:

| Role in the kit | Bootstrap color | Used as |
|---|---|---|
| accent, buttons | `primary` | `btn-primary`, `text-primary`, `bg-primary` |
| second accent | `secondary` | `btn-secondary`, badges |
| light sections | `light` | `bg-light` |
| dark bands, text | `dark` | `bg-dark text-white`, `text-dark` |

Page background and body text come from Bootstrap's body colors. Saved designs change the values, so every design
keeps working as long as the pages use only these names. The checker flags any other color.

## Open questions

- Plain CSS and Bootstrap: confirm that several saved designs switch correctly (test builds 3 and 4).
- Should the skill also be built into Pinegrow (Pine Cone skill, `pinegrow` command) in 10.2, or stay a download?
- Licence and wording for users who sell kits built with it.

## Order of work

1. Write `SKILL.md`, the shared references and `kit.py` with the Tailwind checks; test 1. (Done Nov 25, test running.)
2. WordPress reference and checks; test 2.
3. Write `bootstrap.md` and its checks; test 3.
4. Same for plain CSS; test 4.
5. Package with the gift kit, write the docs page and the follow-up email.
