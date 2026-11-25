# Image prompts: website kit (version 4, block library and starters)

Save each generated image in `source/images/` (next to `website/`) under the base name given, as PNG or JPG at any
size, at the aspect ratio given (for example `source/images/cafe-hero.png`). Then run
`python3 kit-builder/scripts/kit.py optimize .` in the BlackFriday2026Gift folder: it writes
`website/images/<name>.webp` at the size the pages use. Close the project in Pinegrow first. Until an image is
generated, a grey gradient placeholder stands in. (The `.jpg` names below are the base names; the pages use `.webp`.)

**Status (Nov 25, 15:30):** all 52 images are generated and in `source/images/`; the pages use them as WebP.
Nothing left to generate.

**Rules for every image** (add to every prompt):

> Realistic documentary photograph, natural light, real textures and slightly imperfect real places, not staged stock
> photography. No text, no logos, no readable screens, no watermarks. Muted natural colours that look right on a warm
> paper, a white, a near-black and a forest green website.

Things to avoid: arches and arched windows, glossy "AI" skin, everyone smiling at the camera, perfectly symmetrical
rooms, floating devices, lens flare, teal-and-orange grading.

**Gallery images** (agency and portfolio): on wide screens the 1st and 6th image of each gallery are shown wide (3:2)
and the others tall (3:4); on phones all are cropped to 3:4. Keep the subject in the centre third.

**Cover heroes** (`cafe-hero`, `photo-1`): the headline sits over the lower left on a dark fade, and phones crop to a
tall centre strip. Put the subject in the centre to right, keep the lower left quiet.

## Field Office (web agency, `index-agency.html`)

Shared style: a small, calm digital studio. Show real screens only as soft, unreadable shapes of layout and colour.

| File | Size | Ratio | Prompt |
|---|---|---|---|
| `agency-1.jpg` | 1500×1000 | 3:2 | A laptop on a lab bench next to a microscope and sample trays; the screen shows a calm science website with a large diagram, out of focus. Cool daylight from a big window. |
| `agency-2.jpg` | 900×1200 | 3:4 | Close-up of a hand holding a phone mounted on a bicycle handlebar at a rainy railway platform; the screen shows a simple timetable layout, unreadable. Wet steel, overcast light. |
| `agency-3.jpg` | 900×1200 | 3:4 | A tablet leaning against a kraft paper bag of coffee beans on a roastery counter, a scoop and spilled beans beside it; the screen shows a shop page with product photos, out of focus. |
| `agency-4.jpg` | 900×1200 | 3:4 | An open laptop on a bookshop counter between stacks of new hardbacks and a paper events poster; the screen shows a calendar grid, unreadable. Warm evening lamp light. |
| `agency-5.jpg` | 900×1200 | 3:4 | A studio wall covered in printed website screens, pencil sketches and sticky notes, with a strip of masking tape and a hand pinning up one more print. |
| `agency-6.jpg` | 1500×1000 | 3:2 | Six phones lying side by side on a pale wooden table, each showing a different page of the same simple website in muted green and cream, seen from above, slightly off-axis. |
| `agency-team.jpg` | 1400×1000 | 7:5 | Four people of different ages and backgrounds working around one long table in a bright converted workshop, laptops, paper sketches and mugs, mid-conversation, nobody looking at the camera. |
| `agency-client.jpg` | 400×400 | 1:1 | Head-and-shoulders portrait of a woman in her late forties, a physicist, short grey hair, plain dark sweater, in front of a softly blurred lab corridor, calm expression. |

## Movewell Physio (physiotherapy clinic, `index-physio.html`)

Shared style: a bright, practical clinic with pale wood, white walls and plants; real bodies and real effort, no
spa clichés (no candles, stones or orchids).

| File | Size | Ratio | Prompt |
|---|---|---|---|
| `physio-hero.jpg` | 1200×1400 | 6:7 | A physiotherapist in a plain navy polo guiding a middle-aged man through a shoulder exercise with a resistance band, her hand on his shoulder blade, in a bright treatment room with a wall bar and a window. |
| `physio-treat-1.jpg` | 600×600 | 1:1 | Close-up of hands applying kinesiology tape to a runner's knee, the runner sitting on a treatment couch in running shorts. |
| `physio-treat-2.jpg` | 600×600 | 1:1 | A physiotherapist's hands working on a patient's lower back, the patient lying on a treatment couch with a white towel, side light. |
| `physio-treat-3.jpg` | 600×600 | 1:1 | An older woman doing a supported squat holding a wall bar, a fresh surgery scar visible on her knee, a physio watching beside her. |
| `physio-treat-4.jpg` | 600×600 | 1:1 | Three people on Pilates reformer machines in a small bright studio with pale wooden floors, mid-movement, seen from the side. |
| `physio-team-1.jpg` | 800×1000 | 4:5 | Portrait of a South Asian woman in her thirties, a physiotherapist, dark hair tied back, navy clinic polo, standing in a bright clinic corridor, relaxed half-smile. |
| `physio-team-2.jpg` | 800×1000 | 4:5 | Portrait of a Welsh man in his fifties, a physiotherapist who treats back pain, short beard, grey quarter-zip top, leaning against a treatment couch, arms loosely folded. |
| `physio-team-3.jpg` | 800×1000 | 4:5 | Portrait of a Czech woman in her late twenties, a physiotherapist for recovery after surgery, light brown hair, black long-sleeve top, in a studio with reformer machines blurred behind her. |
| `physio-patient.jpg` | 400×400 | 1:1 | Head-and-shoulders portrait of a man of 41, a recreational runner, short hair, running jacket, slightly out of breath, outdoors by a river on an overcast day. |

## Ember & Oat (café and bakery, `index-cafe.html`)

Shared style: a small Scottish harbour café, early morning, flour and steam, worn wood and enamel, Nordic calm.

| File | Size | Ratio | Prompt |
|---|---|---|---|
| `cafe-hero.jpg` | 2000×1250 | 16:10 | A small café counter at 7 a.m. seen from the door: wooden shelves of fresh sourdough loaves, a tray of buns, an espresso machine with steam, a window with harbour light on the right. Subject centre to right, lower left darker and quiet. |
| `cafe-story.jpg` | 1200×1500 | 4:5 | A baker with flour on her forearms shaping a loaf on a floured wooden table in a small bakehouse, proving baskets stacked behind her, light from a side window. |
| `cafe-bake-1.jpg` | 600×600 | 1:1 | Top-down: Swedish-style cardamom buns, knotted and sugar-crusted, on a dark baking tray with parchment. |
| `cafe-bake-2.jpg` | 600×600 | 1:1 | A dark, deeply crusted sourdough loaf with an ear, on a floured linen cloth, one slice cut. |
| `cafe-bake-3.jpg` | 600×600 | 1:1 | Top-down: a rustic plum and almond tart with halved plums and toasted flaked almonds, on a pale stoneware plate. |
| `cafe-bake-4.jpg` | 600×600 | 1:1 | Squares of rye brownie with a crackled top on baking paper, one square broken to show the fudgy inside. |

## Ana Ruiz (photographer, `index-portfolio.html`)

Shared style: these are the photographer's own pictures, so they must look like a real body of work: one consistent
eye, quiet and warm, film-like grain, Lisbon light.

| File | Size | Ratio | Prompt |
|---|---|---|---|
| `photo-1.jpg` | 2000×1250 | 16:10 | A woman in a linen dress standing in a tall wooden doorway of an old Lisbon house in warm late-afternoon light, shadow lines across the tiled facade. She stands centre right; lower left in shade. |
| `photo-2.jpg` | 1500×1000 | 3:2 | A ceramicist at her wheel in a cramped studio, hands grey with clay, shelves of unfired bowls behind her, light from a high window. |
| `photo-3.jpg` | 900×1200 | 3:4 | Looking up a white spiral stair winding through a modernist house, soft light from a skylight, clean shadows. |
| `photo-4.jpg` | 900×1200 | 3:4 | Two fishermen mending orange nets on the beach at Nazaré at dawn, colourful boats pulled up behind them, mist over the sea. |
| `photo-5.jpg` | 900×1200 | 3:4 | A chef plating a small dish of grilled sardines in a narrow tavern kitchen, steam, tiled wall, tight crop on hands and plate. |
| `photo-6.jpg` | 900×1200 | 3:4 | Laundry drying on lines strung between old houses in Alfama, a narrow stepped street below, morning sun on one side. |
| `photo-7.jpg` | 1500×1000 | 3:2 | Portrait of an old man in a flat cap sitting outside a café on a small stool, hands folded on a walking stick, looking just past the camera. |
| `photo-client.jpg` | 400×400 | 1:1 | Head-and-shoulders portrait of a German woman in her forties, a magazine photo editor, short dark bob, black turtleneck, in front of a pinboard of prints, out of focus. |

## Sam Rivera (personal site, `index-personal.html`)

Shared style: quiet, everyday, a writer's life in Montréal; still lifes and street scenes, nothing techy.

| File | Size | Ratio | Prompt |
|---|---|---|---|
| `sam-portrait.jpg` | 800×1000 | 4:5 | Portrait of a person in their mid thirties with short curly dark hair and round glasses, wearing a grey wool sweater, sitting by a window in a small Montréal apartment with books behind, thoughtful, not posed. |
| `sam-post-1.jpg` | 1200×800 | 3:2 | An open paper notebook with handwritten notes (unreadable) and a cup of black coffee on a worn wooden desk, a phone lying face down, morning light. |
| `sam-post-2.jpg` | 1200×800 | 3:2 | A single small brass desk bell on a plain white table against a white wall, soft shadow, lots of empty space. |
| `sam-post-3.jpg` | 1200×800 | 3:2 | A Montréal street of brick row houses with outdoor iron staircases in falling snow, one person walking with a paper bag, dusk street lights coming on. |

## Northlight Interiors (done, for reference)

Don't regenerate: `hero.jpg` 1600×1100 (living room with three callout areas), `work-1/2/3.jpg` 1500×1000,
`sample-oak/linen/stone/plaster.jpg` 600×600, `contact.jpg` 1200×900, `about-studio.jpg` 2400×1029,
`about-detail.jpg` 1200×1500, `team-1/2/3.jpg` 800×1000, `post-1/2/3.jpg` 1200×800.
