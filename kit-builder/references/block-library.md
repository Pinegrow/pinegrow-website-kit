# Block library

The block library lets the user drag whole blocks from Pinegrow's Insert panel onto any page. `kit.py library` builds
it from `source/blocks/`.

## Source files

```
source/blocks/
  01-headers-and-footers/
    01-header-simple.html
    02-footer-columns.html
  02-heroes/
    01-hero-split.html
    02-hero-cover.html
  03-services/
    ...
```

- One folder per category. The number sets the order; the rest becomes the name ("Headers and footers").
- One file per block, with exactly one root element: the block (`section`, `header` or `footer`).
- The root has `data-pg-name` (the block's name in the library, for example "Hero (split)") and
  `data-pg-content-group`.
- Write URLs as from the `website/` folder: `images/hero.webp`, `contact.html`. The library pages use
  `<base href="../">`, so the same URLs work in the library and on the pages the block is dropped into.
- Use placeholder content that shows what the block is for, ideally the content of one of the starters.
- Every block a starter uses should be in the library, so the user can build more pages from it.

## What `kit.py library` makes

- `website/blocks/kit-blocks.html`: the library home, with one card per category.
- `website/blocks/<category>.html`: one page per category with its blocks, each under a small title bar.
- A navigation bar on every library page (All blocks and every category).
- `pinegrow.json`: registers `blocks/kit-blocks.html` as a page library (`project_resources`) and excludes `blocks`
  from publishing.

Run it again after every change to `source/blocks/`, and after changing the body class of `index.html`. `kit.py check`
tells you when the library is older than its sources. Never edit `website/blocks/` by hand.

## How it behaves in Pinegrow (10.1)

- The user opens the library once from the Insert panel's "+" menu (under the project name: `kit-blocks.html`).
  Pinegrow keeps the tab.
- Clicking a category card or a link in the bar opens that page in the library. The library's Back button and jump
  menu don't follow these pages, which is why every page links back to All blocks.
- Hovering anywhere in a block marks the whole block, so only whole blocks can be dragged. A script in the library
  pages does this, because Pinegrow 10.1 otherwise lets any element of a project library be dragged (a single
  button or half a section) and ignores the `pg-lib-item` class there.
- The links work because they sit in an element with Pinegrow's `pg-lib-hover-menu` class, the one place where the
  library lets clicks through. The library pages restyle that class.

Tell the user how to open the library in the kit's README.
