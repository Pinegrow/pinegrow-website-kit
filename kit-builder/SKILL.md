---
name: pinegrow-website-kit
description: Build a client-ready website kit as a Pinegrow project, with saved designs, component styles, Content panel annotations, a drag-and-drop block library and starter pages. Use when the user wants a website, template or kit made in or for Pinegrow (Pinegrow 10.1 or later).
---

# Pinegrow website kit

You build a website kit that the user opens and finishes in Pinegrow, the visual web editor. A kit is more than a
site: it has several saved designs the user switches in the Design panel, component styles they edit in the Style
panel, Content panel annotations so clients can edit texts safely, a block library they drag sections from, and
starter pages built from those blocks.

`scripts/kit.py` (Python 3, standard library only) writes the Pinegrow files that are easy to get wrong and checks
the kit. Run it from anywhere: `python3 <skill folder>/scripts/kit.py <command> <kit folder>`.

## 1. Ask, then write the brief

Run `kit.py init <kit folder>` (for example `~/Sites/yoga-kit`). It creates `KIT-BRIEF.md`, `source/` and
`website/` (the Pinegrow project). Then ask the user at most these six questions, in one message, each with your
default. Skip the ones their request already answers.

1. What is the kit for: one client's site, a reusable base for their agency, or a template to sell? Which business or
   businesses, and which pages? (Default: one business, a home page plus about, services and contact.)
2. Tailwind CSS, Bootstrap or plain CSS? (Default: Tailwind CSS.)
3. Should it also export to a WordPress block theme? (Default: no, a static site.)
4. How many saved designs, and should it include a block library? (Default: 3 designs and a library.)
5. Where will it be published (Netlify or another host)? (Default: decide when building the
   contact form.)
6. Images: do you have photos I should use (tell me the folder), should I find free photos on Unsplash, or should I
   generate them? Offer generating only if you can actually create images. (Default: Unsplash.)

Write the answers into `KIT-BRIEF.md`. Keep the `Key: value` lines at the top: `kit.py check` reads `CSS`,
`WordPress` and `Images`. When you come back to a kit later, read the brief first instead of asking again.

This version of the skill builds **Tailwind CSS** kits for **static sites**. If the user picks Bootstrap, plain CSS
or WordPress, read `references/bootstrap.md`, `references/plain-css.md` or `references/wordpress.md`: they say what
is supported yet and what to tell the user.

## 2. Find the concept

Read `references/concept-and-design.md`. Fill in the brief's Concept (an idea that shapes the layout, the voice and
the details), Color roles, Fonts and Saved designs sections. Show the user the concept in
a few lines and go on unless they want changes.

## 3. Build

Read `references/project-files.md` and `references/tailwind.md` first. They explain how Pinegrow stores designs and
styles and the traps that break the project.

1. **Designs.** Write `source/designs.json` and run `kit.py designs`.
2. **Component styles.** Write `source/styles.txt` and run `kit.py styles`.
3. **Blocks.** One file per block in `source/blocks/<NN-category>/<NN-block>.html`. Annotate them for the Content
   panel (`references/content-panel.md`).
4. **Images.** Reference images as `images/<name>.webp` with `width` and `height`. Get the originals the way the
   brief says (`references/images.md`): the user's photos, Unsplash or generated, into `source/images/`. Run
   `kit.py optimize` to write the WebP files at the right size, and `kit.py images` for placeholders while an
   original is still missing.
5. **Pages.** Write the pages in `website/` from the blocks (copy a block, then change its content). For one
   business these are the pages in the brief. For several businesses, each gets a starter home page
   (`index-cafe.html`...), plus `blank.html` with only the header and footer.
6. **Block library.** Run `kit.py library` (`references/block-library.md`).
7. **Contact form.** If there is a contact page, follow `references/forms.md`.
8. **Publishing.** Follow `references/publishing.md`.

Close the project in Pinegrow before you edit its files or run `kit.py`, and tell the user to open it again
afterwards. Pinegrow can otherwise save its open copy over your changes.

## 4. Check and hand over

1. Run `kit.py check <kit folder>` and fix every error. Fix warnings unless there is a good reason, and say which
   ones you left.
2. Ask the user to open the `website` folder in Pinegrow, open every page once (Pinegrow compiles the Tailwind CSS
   for the classes on the pages it has opened), switch through the saved designs, and try the block library (Insert
   panel, "+" menu, `kit-blocks.html`). If you can drive Pinegrow yourself (the `pinegrow` command from Pinegrow
   10.2), do it.
3. Run `kit.py check` again once the CSS is compiled: it then also finds classes that don't exist. If it lists common
   utilities (`flex-col`, `gap-4`), Pinegrow compiled before every page was open: ask the user to make any small
   change in Pinegrow so it compiles again.
4. If you can look at pages in a browser, serve `website/` (`python3 -m http.server`) and review every page at desktop
   and phone width. Fix overflow, cramped spacing and anything that looks unfinished.
5. Write `README.md` in the kit folder for the user: what the kit contains, the starters, the designs, how to use the
   library, how to make the contact form work, which images to replace.

## Rules for every kit

- Use only the design colors and fonts in pages and styles, never fixed colors (`#hex`, `rgb()`, `text-[#...]`), so
  every saved design works. The default Tailwind colors stay available but don't change with the design, so use them
  only for things that must not change (for example a red error message).
- Every block sets its own background and spacing. Don't rely on the page around it.
- One block is one root element (`section`, `header` or `footer`) with `data-pg-name` and `data-pg-content-group`.
- Repeat structure through component styles, not by copying long class lists.
- Write real, specific content for the business, never lorem ipsum.
- No JavaScript frameworks. Use plain HTML for interaction where possible (`<details>` for menus and questions).
- Make every page work on phones (no horizontal scrolling, readable text, tappable links).
- Don't edit `tailwind_theme/tailwind.css` or `_pginfo/` by hand, except through `kit.py`.
