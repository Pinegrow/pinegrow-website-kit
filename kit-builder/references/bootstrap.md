# Bootstrap kits

Not in this version of the skill yet. Tell the user, and offer a Tailwind CSS kit instead, or wait for the version
with Bootstrap support.

What it will cover: Bootstrap has a fixed set of colors (`primary`, `secondary`, `success`, `info`, `warning`,
`danger`, `light`, `dark`). Pinegrow's Design panel redefines them but can't add new names, so the kit maps its color
roles onto those names (accent on `primary`, light sections on `light`, dark bands on `dark`). Reusable styles are
Bootstrap classes plus a project stylesheet that uses `var(--bs-*)`, because component styles are a Tailwind CSS
feature.
