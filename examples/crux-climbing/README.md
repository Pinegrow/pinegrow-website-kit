# Crux Climbing website kit

Open the **website** folder as a project in Pinegrow 10.1 or later. The kit uses Tailwind CSS 4 and ships with the Chalk stylesheet compiled for browser preview.

## Get started in Pinegrow

1. Choose **Open Project** and select **website**. Open each of the seven HTML files below so Pinegrow can register their Tailwind classes. If a utility drops out after the first compile, make a small edit and undo it with all seven pages open to trigger another compile.
2. Switch among **Chalk**, **Night** and **Tape** in the **Design** panel. Chalk is the default with warm white and bright yellow. Night uses charcoal and coral. Tape pairs pale lilac and vivid blue. The designs also switch the heading and body fonts.
3. Use the **Content** panel for headlines, photos, links, table rows and questions. Use the **Style** panel for shared classes such as `btn-primary`, `heading-section` and `board-value`.
4. In the **Insert** panel, open the **kit-blocks.html** tab. Choose a category and drag a whole block into a page. The 18 blocks include photo and text heroes, visitor links, steps, photo sections, tables, questions, gift vouchers, and two types of enquiry form. Find **Gift vouchers** under **Visit and enquiry**. Its button opens the visit enquiry form. Use **All blocks** to return to the category list.
5. Edit the shared header and footer on `index.html`, then use **Components → Update the whole project** to update the other pages.

| Page | File |
| --- | --- |
| Home | `index.html` |
| Climbing and classes | `climbing.html` |
| Prices and memberships | `prices.html` |
| Kids and parties | `kids.html` |
| Visit us | `visit.html` |
| Frequently asked questions | `faq.html` |
| Blank starter with shared header and footer | `index-blank.html` |

## Before going live

- Replace the clearly marked sample entry fees, membership prices and terms, class lengths, and opening hours. Fill in the street address, directions and access details on Visit us. Add the confirmed age limits and adult supervision rules on Kids and parties.
- Crux supplied the photos in the Home introduction, the family climbing section on Kids and parties, and Getting here on Visit us. Three generated photos remain in the Home, Climbing and classes, and Kids and parties heroes. See the [image credits](source/image-credits.md) for the filenames and Insert library placements.
- Publish the six visitor pages and their assets. Pinegrow excludes the Insert library, the blank starter and the form setup notes from its publish output. For a manual Netlify upload, upload that publish output so the library’s example forms stay out of the deployment.

## Netlify enquiries

Visit us and Kids and parties have separate forms named `visit-enquiry` and `party-enquiry`. In the Netlify project, turn on **Forms → Enable form detection**, then deploy or redeploy the publish output. Set the gym’s notification address in Netlify and submit a test of each form on the deployed site. Both forms use the same-origin Netlify endpoint on a Netlify subdomain or a custom domain. [Netlify Forms setup](https://docs.netlify.com/manage/forms/setup/)

The project has been checked as a static site. Live submissions can be verified once the site is deployed.

The `source` folder holds the editable design recipes, component style definitions and block sources used to assemble the kit. Use Pinegrow for day-to-day edits to the pages.
