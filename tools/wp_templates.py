#!/usr/bin/env python3
"""Writes the items of every collection block into the WordPress block templates.

A template names a collection block on its own (`<!-- wp:PGTHEMESLUG/services-cards /-->`), but WordPress renders a block's
inner blocks only from the template, so the cards, names and steps came out empty. This reads each page that a
template is made from, takes the items of each collection with their field values, and writes them into the template:

    <!-- wp:PGTHEMESLUG/services-cards -->
    <!-- wp:PGTHEMESLUG/service-card /-->
    <!-- wp:PGTHEMESLUG/service-card {"title":"Second service",...} /-->
    <!-- /wp:PGTHEMESLUG/services-cards -->

The first item keeps the block's defaults (the block is defined from it); the others get the fields that differ.

    python3 tools/wp_templates.py [website folder]
"""
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
SLUG = "PGTHEMESLUG"  # Pinegrow fills in the theme slug when it exports the theme.
# Template file -> the page it is made from.
TEMPLATES = {"front-page.html": "index.html", "page-about.html": "about.html", "page-contact.html": "contact.html",
             "home.html": "journal.html", "single.html": "post.html", "404.html": "404.html"}


class Node:
    def __init__(self, tag, attrs, start, parent):
        self.tag, self.attrs, self.start, self.parent = tag, dict(attrs), start, parent
        self.children, self.end, self.inner_start, self.inner_end = [], None, None, None

    def walk(self):
        yield self
        for c in self.children:
            yield from c.walk()


class Tree(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=False)
        self.text = text
        self.line_starts = [0]
        for m in re.finditer("\n", text):
            self.line_starts.append(m.end())
        self.root = Node("#root", [], 0, None)
        self.cur = self.root
        self.feed(text)

    def text_offset(self):
        line, col = self.getpos()
        return self.line_starts[line - 1] + col

    def handle_starttag(self, tag, attrs):
        start = self.text_offset()
        node = Node(tag, attrs, start, self.cur)
        self.cur.children.append(node)
        tag_end = self.text.index(">", start) + 1
        if tag in VOID:
            node.end = node.inner_start = node.inner_end = tag_end
        else:
            node.inner_start = tag_end
            self.cur = node

    def handle_startendtag(self, tag, attrs):
        start = self.text_offset()
        node = Node(tag, attrs, start, self.cur)
        node.end = node.inner_start = node.inner_end = self.text.index(">", start) + 1
        self.cur.children.append(node)

    def handle_endtag(self, tag):
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is self.root:
            return
        pos = self.text_offset()
        n.inner_end = pos
        n.end = self.text.index(">", pos) + 1
        self.cur = n.parent


def inner(text, node):
    return text[node.inner_start:node.inner_end].strip()


def clean_svg(text, node):
    svg = text[node.start:node.end]
    svg = re.sub(r'\s(?:cms-block-[a-z0-9-]+|data-pg-[a-z0-9-]+)(?:="[^"]*")?', "", svg)
    return svg


def field_values(text, item):
    values = {}
    for n in item.walk():
        for suffix in ("", "-2"):
            fid = n.attrs.get("cms-block-field" + suffix)
            if not fid:
                continue
            ftype = n.attrs.get("cms-block-field-type" + suffix, "content")
            if ftype == "content":
                values[fid] = inner(text, n)
            elif ftype == "link":
                values[fid] = {"post_id": 0, "url": n.attrs.get("href", ""), "title": "", "post_type": None}
            elif ftype == "image":
                if n.tag == "svg":
                    values[fid] = {"id": 0, "url": "", "size": "", "svg": clean_svg(text, n), "alt": None}
                else:
                    values[fid] = {"id": 0, "url": n.attrs.get("src", ""), "size": "", "alt": n.attrs.get("alt")}
    return values


def block_json(attrs):
    s = json.dumps(attrs, ensure_ascii=False, separators=(",", ":"))
    # The way WordPress serializes block comment attributes.
    return (s.replace("\\\"", "\\u0022").replace("--", "\\u002d\\u002d").replace("<", "\\u003c")
             .replace(">", "\\u003e").replace("&", "\\u0026"))


def collections(page_text):
    """{parent block id: [item lines]} for the collections on a page."""
    tree = Tree(page_text)
    out = {}
    for n in tree.root.walk():
        if "cms-block-inner-content" not in n.attrs:
            continue
        p = n.parent
        while p is not None and "cms-block" not in p.attrs:
            p = p.parent
        if p is None:
            continue
        items = [c for c in n.walk() if c is not n and "cms-block" in c.attrs and c.attrs.get("cms-block-parent") == p.attrs["cms-block"]]
        if not items:
            continue
        first = field_values(page_text, items[0])
        lines = []
        for i, it in enumerate(items):
            bid = it.attrs["cms-block"]
            if i == 0:
                lines.append(f"<!-- wp:{SLUG}/{bid} /-->")
                continue
            values = field_values(page_text, it)
            diff = {k: v for k, v in values.items() if first.get(k) != v}
            lines.append(f"<!-- wp:{SLUG}/{bid} {block_json(diff)} /-->" if diff else f"<!-- wp:{SLUG}/{bid} /-->")
        out[p.attrs["cms-block"]] = lines
    return out


def main():
    website = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "website")
    tdir = os.path.join(website, "templates")
    for tname, page in TEMPLATES.items():
        tpath, ppath = os.path.join(tdir, tname), os.path.join(website, page)
        if not (os.path.exists(tpath) and os.path.exists(ppath)):
            continue
        cols = collections(open(ppath, encoding="utf-8").read())
        text = open(tpath, encoding="utf-8").read()
        changed = 0
        for parent, lines in cols.items():
            # A block written on its own, or one this script expanded before.
            pattern = re.compile(rf"<!-- wp:{SLUG}/{re.escape(parent)} /-->|<!-- wp:{SLUG}/{re.escape(parent)} -->.*?<!-- /wp:{SLUG}/{re.escape(parent)} -->", re.S)
            new = f"<!-- wp:{SLUG}/{parent} -->\n" + "\n".join(lines) + f"\n<!-- /wp:{SLUG}/{parent} -->"
            text, n = pattern.subn(lambda m: new, text)
            changed += n
        if changed:
            open(tpath, "w", encoding="utf-8").write(text)
            print(f"{tname}: {changed} collection block(s) written from {page}")


if __name__ == "__main__":
    main()
