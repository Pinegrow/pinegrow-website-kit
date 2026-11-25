#!/usr/bin/env python3
"""Turns an exported copy of the kit into the static or the WordPress download.

  python3 tools/make_variant.py static DIR
  python3 tools/make_variant.py wordpress DIR

DIR is a copy of the download (README.md, LICENSE, website/, kit-builder/), never the repository itself.
package.sh runs this on copies made with git archive.

static:    removes the WordPress block attributes (cms-* and wp-*) from every page and library page, the WordPress
           templates (website/templates/) and wp-blocks.html, and their entries in pinegrow.json. The Pinegrow
           parts (data-pg-content-*, data-pg-name, component styles, the block library) stay.
wordpress: keeps everything.

In both, README files keep the parts between <!-- static --> and <!-- /static --> or <!-- wordpress --> and
<!-- /wordpress --> that belong to the variant and drop the others, and drop <!-- repo --> parts (only for GitHub).
"""
import json
import os
import re
import shutil
import sys

# A WordPress attribute: space, cms-... or wp-..., an optional double-quoted value, then the end of the attribute.
WP_ATTR = re.compile(r'\s(?:cms|wp)-[a-z0-9-]+(?:="[^"]*")?(?=[\s/>])')
TAG = re.compile(r"<([a-zA-Z][a-zA-Z0-9-]*)\b")


def strip_page(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    before = TAG.findall(text)
    out, n = WP_ATTR.subn("", text)
    after = TAG.findall(out)
    if before != after:
        sys.exit(f"{path}: removing attributes changed the elements; stopping")
    left = re.findall(r'\s(?:cms|wp)-[a-z0-9-]+(?:=|\s|>)', out)
    if left:
        sys.exit(f"{path}: attributes left after stripping: {left[:5]}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(out)
    return n


def readme_variant(path, variant):
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        text = f.read()
    other = "wordpress" if variant == "static" else "static"
    for drop in (other, "repo"):
        text = re.sub(rf"<!-- {drop} -->.*?<!-- /{drop} -->\n?", "", text, flags=re.S)
    text = re.sub(rf"<!-- /?{variant} -->\n?", "", text)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("static", "wordpress"):
        sys.exit(__doc__)
    variant, root = sys.argv[1], os.path.abspath(sys.argv[2])
    web = os.path.join(root, "website")
    if not os.path.isdir(web) or os.path.isdir(os.path.join(root, ".git")):
        sys.exit(f"{root} must be an exported copy with website/, not the repository")

    for path in (os.path.join(root, "README.md"), os.path.join(web, "form", "README.md")):
        readme_variant(path, variant)
    if variant == "wordpress":
        print("wordpress: kept everything")
        return

    removed = 0
    pages = 0
    for dp, _, fs in os.walk(web):
        if os.path.relpath(dp, web).split(os.sep)[0] in ("templates", "_pgbackup"):
            continue
        for f in fs:
            if f.endswith(".html"):
                removed += strip_page(os.path.join(dp, f))
                pages += 1
    shutil.rmtree(os.path.join(web, "templates"), ignore_errors=True)
    wp_blocks = os.path.join(web, "wp-blocks.html")
    if os.path.exists(wp_blocks):
        os.remove(wp_blocks)
        pages -= 1

    pj_path = os.path.join(web, "pinegrow.json")
    with open(pj_path, encoding="utf-8") as f:
        pj = json.load(f)
    for key in ("files", "urls"):
        pj.get(key, {}).pop("wp-blocks.html", None)
    pj["open-pages"] = [u for u in pj.get("open-pages", []) if u != "wp-blocks.html"]
    pj["publish-excludes"] = [u for u in pj.get("publish-excludes", []) if u not in ("templates", "wp-blocks.html")]
    with open(pj_path, "w", encoding="utf-8") as f:
        json.dump(pj, f)
    print(f"static: removed {removed} WordPress attributes from {pages} pages, templates/ and wp-blocks.html")


if __name__ == "__main__":
    main()
