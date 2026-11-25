# Content panel annotations

Pinegrow's Content panel lists the texts, links and images of a page so the user (or their client) can edit content
without touching the design. Four attributes organize it. They only label and group: they don't make anything
editable and don't change how the page looks.

- `data-pg-content-group="Treatments"`: a named group. Fields inside belong to it. Put one on every block's root
  element, with the block's name.
- `data-pg-content-label="Title"`: a clear name for one field. Use short editorial names: `Title`, `Introduction`,
  `Price`, `Primary button`, `Photo`.
- `data-pg-content-collection="Treatments"`: the parent of a list of repeated items (plural name).
- `data-pg-content-item="Treatment"`: every repeated item (singular name), each a direct child of the collection.

Don't invent other `data-pg-content-*` attributes.

```html
<section class="section" data-pg-name="Treatments (rows)" data-pg-content-group="Treatments">
    <div class="container-site">
        <h2 class="heading-lg" data-pg-content-label="Title">What we treat</h2>
        <div class="treatment-list" data-pg-content-collection="Treatments">
            <article class="treatment-row" data-pg-content-item="Treatment">
                <img src="images/physio-treat-1.webp" alt="A physio taping a runner's knee" width="240" height="240"
                     class="treatment-image" data-pg-content-label="Photo">
                <h3 class="treatment-title" data-pg-content-label="Name">Sports injuries</h3>
                <p data-pg-content-label="Description">Sprains, strains and a safe way back to training.</p>
                <p class="treatment-meta" data-pg-content-label="Duration and price">45 min · £65</p>
            </article>
            <article class="treatment-row" data-pg-content-item="Treatment">
                ...
            </article>
        </div>
    </div>
</section>
```

## Rules

- Every block root has `data-pg-name` (the name in Pinegrow's tree and the library) and `data-pg-content-group`.
- Label the fields where the tag alone says little: titles, descriptions, prices, buttons, photos, small labels.
- Mark a collection only for real repetition: at least two items with the same structure and role, every item a direct
  child of the collection, every child an item. Don't mark a grid of different things as a collection.
- No nested or overlapping collections. Don't put a form's fields in a collection. When items repeat at two levels
  (days of a timetable, each with classes), make the level the user edits most the collection (usually the inner
  one, the classes of a day) and only label the other level (`data-pg-content-label="Monday"` on the day's heading).
- `kit.py check` reports collections with fewer than two items, children that aren't items, and items outside a
  collection.
