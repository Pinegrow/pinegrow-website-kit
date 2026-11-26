# Willowbend Family Dental

A Tailwind CSS 4 website kit for Pinegrow 10.1 and later. Willowbend is a fictional family dental practice in Maplewood, Minnesota. The project opens with the Willow design and a compiled stylesheet.

## Open and edit

Open the [website folder](website/) with **File → Open project**. Start on [index.html](website/index.html).

- **Design panel** — Switch between Willow (warm ivory and moss), Harbor (cool white and marine teal), and Dusk (plum and rose). Each design changes the project’s shared colors and type.
- **Style panel** — Select a button, heading, form field or other element and edit its component style to update matching elements across the project.
- **Content panel** — Edit the labeled text, links and photos. Care options, first-visit steps, questions and office hours are editable collections.
- **Insert panel** — Open the **kit-blocks.html** tab. If it is hidden, use **+** and select it under the project name. Choose a category and drag a block onto a page. Use **All blocks** to return to the index. The 17 blocks include alternate introductions, a compact footer, a care index, and appointment and contact sections.
- **Shared navigation and footer** — Edit the definitions on the home page, then use **Components → Update the whole project** and **File → Save all** to propagate the changes.

## Starter pages

| Page | Includes |
| --- | --- |
| [Home](website/index.html) | Appointment action, care index, first-visit steps and common questions |
| [Our practice](website/about.html) | Reception photo and the practice’s approach to patient comfort |
| [Dental care](website/services.html) | Checkups, children’s dentistry and restorative care |
| [New patients](website/new-patients.html) | What to bring, what to expect and questions families often ask |
| [Visit & contact](website/contact.html) | Address, phone, office hours and an appointment request form |
| [Blank starter](website/index-blank.html) | Shared header and footer with an empty main area |

Save a copy of the blank starter to make another page. Update its title and description and remove the starter’s `noindex` meta tag. When editing Tailwind classes, open the pages and library categories you use so Pinegrow includes their utilities when it recompiles.

## Set up a practice

Replace the sample name, location, telephone links, hours and services. Check the header, footer, home information strip, services call banner and contact page for repeated details.

Replace the three generated WebP photos in [website/images](website/images/) or choose new files in the Content panel. Update alt text to match the new scenes. Editable originals and the [image generation prompts](source/image-prompts.md) are under `source/`.

## Connect appointment requests

The form is ready for a practice-approved delivery service. It collects contact and scheduling preferences only. Follow the [form setup guide](website/form/README.md), then send a sample request through the configured site and confirm receipt. If you drag the appointment form onto another page, add `form/form.js` to that page’s head, point the form at the chosen endpoint, and keep only one copy of the form on a page.

## Publish

Publish the site from the `website` folder. Pinegrow’s publish exclusions omit the block library, the blank starter and the form setup guide. If uploading the HTML directly to another host, omit those files and Pinegrow’s editor data (`pinegrow.json`, `projectdb.pgml` and `_pginfo/`). The `source` folder sits outside the publish root.
