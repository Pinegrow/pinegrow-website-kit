# Images

The brief's `Images:` line says where the photos come from: the user's own photos, Unsplash, or generated.

## How images flow

1. Plan every image the pages and blocks need in `source/image-prompts.md`: file name, what it shows, size in pixels
   (about twice the size it is shown at on a desktop screen, so it stays sharp on retina screens) and aspect ratio.
2. In the pages and blocks, use WebP: `<img src="images/hero-studio.webp" width="1600" height="1000" alt="...">`.
   `width` and `height` are the size the file should have.
3. Put the originals, at any size and in any format (PNG, JPG, WebP), in `source/images/` with the same base name
   (`source/images/hero-studio.png`). They stay outside the Pinegrow project, so they are never published.
4. Run `kit.py optimize <kit>`. It writes `website/images/<name>.webp` from each original, scaled to cover the
   `width` and `height` and cropped from the center, at a quality that keeps files small. Run it again after
   replacing an original. When the subject isn't centered, crop the original first.
5. `kit.py images <kit>` makes grey placeholder originals for images that don't have one yet, and optimizes them.
   `kit.py check` lists the placeholders that are left; tell the user which images still need replacing.

`kit.py optimize` uses ImageMagick (`magick`), `ffmpeg`, or `sips` with `cwebp` on macOS (`sips` alone can't write
WebP). If none is installed, ask the user whether to install one; until then use `.jpg` in the `src` and `optimize`
writes JPG with `sips`. `kit.py fit SRC OUT WxH` converts a single image the same way.

Every `<img>` has an `alt` text that describes what the actual photo shows. Keep one look across the kit (similar
light, color and framing) and avoid the clichés in `concept-and-design.md`.

## The user's own photos

Ask for the folder. Copy the photos you use into `source/images/` under the planned names; never change the
originals. Look at them if you can view images and pick what fits each place; otherwise ask the user which photo goes
where.

## Free photos from Unsplash

Unsplash is for good stand-in photos, so the kit doesn't ship with grey boxes. Keep it simple:

- Search the real site in a browser (`https://unsplash.com/s/photos/<words-with-dashes>`). Never write a photo URL,
  id or photographer from memory. A plain page fetch or `curl` gets a bot check; without a browser tool, use
  placeholders and tell the user.
- Use only free photos: skip Unsplash+ ones (their images come from `plus.unsplash.com`).
- Download from the photo's page (its download link, `https://unsplash.com/photos/<id>/download?force=true`) into
  `source/images/`, then run `kit.py optimize`.
- List each photo in `source/image-credits.md`: file name, photographer, page URL.
- Photos of people are strangers, not the user's team: describe them in `alt` without real names, and tell the user to
  replace team and testimonial photos with their own.

## Generated images

Offer this only if you can actually create images. Write the prompts in `source/image-prompts.md` first, with one
shared style line used in every prompt, generate at the planned aspect ratio, save the results in `source/images/`
and run `kit.py optimize`. Look at each result and regenerate garbled text, extra fingers or warped buildings. Note in
`source/image-credits.md` that they are generated.

If you can't generate images but the user wants generated ones, write the prompts and use placeholders. The user
generates the images with their own tool, saves them in `source/images/` under the same names, and runs
`kit.py optimize` (or asks you to).
