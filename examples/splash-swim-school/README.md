# Splash Swim School website kit

Open the `website` folder as a project in Pinegrow 10.1 or later. The kit uses Tailwind CSS 4 and ships with the Lido stylesheet compiled for browser preview.

## Pages

| Page | File |
| --- | --- |
| Home | `index.html` |
| Lessons for babies, kids and adults | `lessons.html` |
| Prices and timetable | `prices.html` |
| About us | `about.html` |
| Contact | `contact.html` |
| Blank starter | `index-blank.html` |

## Edit the kit

1. Open each page once so Pinegrow registers its Tailwind classes.
2. Use the **Design** panel to switch among **Lido** (aqua, warm yellow and rounded type), **Deep** (pool blue, mint and compact type) and **Tide** (cream, violet and serif headlines).
3. Use the **Content** panel for headlines, photos, links, lesson rows and questions. Use the **Style** panel for shared component styles such as `btn-primary`, `heading-section` and `board-value`.
4. Open **Insert → kit-blocks.html** and pick a category. Drag any of the 18 blocks onto a page. The library includes optional lesson pricing, gift vouchers and a private lesson enquiry form. Use **All blocks** to go back to the category list.
5. Edit the shared header and footer on `index.html`, then use **Components → Update the whole project**.

The [brief](KIT-BRIEF.md) records the concept and design choices. The `source` folder holds the design recipes, component styles, block templates and six generated image originals. See the [photo prompts](source/image-prompts.md) and [image credits](source/image-credits.md) for their subjects and placements. Use confirmed venue photos where you describe the real pool or its facilities.

## Before publishing

- Confirm the sample fees, lesson lengths, age ranges, term dates and weekly timetable. Add the school’s verified contact and pool details, including access and arrival instructions.
- Enable form detection in Netlify before deploying the Pinegrow publish output. Configure the notification recipient and test `lesson-enquiry` on the deployed site. The [form notes](website/form/README.md) cover the optional private lesson form.
- The Pinegrow publish output excludes the library, blank starter and form setup notes. Use that output for manual upload.
