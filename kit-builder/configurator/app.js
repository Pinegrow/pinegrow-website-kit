(() => {
  "use strict";

  const root = document.getElementById("pinegrow-kit-studio");
  // The kit-builder skill opens the page with ?agent=1. The skill is then installed, so the prompt needs no setup.
  const agentMode = new URLSearchParams(location.search).has("agent");
  root.classList.toggle("is-agent", agentMode);
  const skillZip = "https://github.com/Pinegrow/pinegrow-website-kit/releases/latest/download/kit-builder-skill.zip";
  const field = (id) => root.querySelector(`#pk-${id}`);
  const write = (id, text) => { field(id).textContent = text; };
  const value = (id) => field(id).value.trim();
  const selected = (id) => Array.from(field(id).querySelectorAll("input:checked"), (input) => input.value);
  const list = (items) => items.join(", ");

  // Each direction has Google Fonts for headings (display), text (sans) and optionally labels (mono), and three
  // palettes. The chosen palette becomes the kit's active saved design and the other two its variations. Palette
  // colours follow the kit-builder color roles: page, ink, primary, band, on-band, on-primary.
  const colorRoles = ["page", "ink", "primary", "band", "on-band", "on-primary"];
  const looks = {
    bold: {
      name: "Action poster",
      fonts: { display: "Barlow Condensed", sans: "Barlow" }, weight: 800, tracking: "-.01em",
      palettes: [["Signal", "#fff7db #1f211a #fbd13b #1f241c #fff5d5 #1f1a0c"],
        ["Chalk", "#f4f4f0 #16181d #ff5a36 #16181d #f4f4f0 #160a05"],
        ["Floodlight", "#10140f #f2f5ea #b8f23a #1c2418 #f2f5ea #10140f"]],
      summary: "A poster-like colour block, huge condensed capitals and a diagonal photo cut.",
      brief: "Treat the home page as an event poster. Put an oversized condensed uppercase headline on a strong primary-colored field, cut the hero photo with a decisive diagonal, and use direct high-contrast calls to action. Number the services boldly and close with a full-width primary-colored call to action.",
    },
    editorial: {
      name: "Sunday edition",
      fonts: { display: "Fraunces", sans: "Libre Franklin" }, weight: 600, tracking: "-.02em",
      palettes: [["Newsprint", "#f7f1e7 #33261f #9a4b3d #482e34 #fff1ed #fff8f6"],
        ["Morning", "#fbfaf7 #1c2330 #2f5d8a #1c2330 #f4f1ea #ffffff"],
        ["Evening", "#1d1a17 #efe6d8 #e0a274 #2c2621 #efe6d8 #1d1a17"]],
      summary: "A newspaper masthead, a serif headline with a standfirst, and a panoramic photo.",
      brief: "Compose it like the opening page of a weekend magazine: a centered masthead between fine and double rules, a focused serif headline with an italic standfirst above a panoramic image, and columns divided by hairlines. Use quiet paper tones, a large italic pull quote and underlined text links instead of heavy buttons.",
    },
    coastal: {
      name: "Open house",
      fonts: { display: "Manrope", sans: "Manrope" }, weight: 800, tracking: "-.035em",
      palettes: [["Mint", "#eef8f1 #153d3c #1d7a5f #153d3c #ecfff6 #ffffff"],
        ["Sand", "#fbf6ee #2e3a3f #b65a2e #2e5560 #f6f1e8 #ffffff"],
        ["Lagoon", "#e8f4f8 #0f3446 #0e7383 #0f3446 #e8f4f8 #ffffff"]],
      summary: "A round photo with bubbles, soft rounded cards and friendly pill buttons.",
      brief: "Make the page welcoming with a soft asymmetric hero: short clear copy beside a large circular photo with a few soft bubble shapes around it. Use pill-shaped buttons, rounded cards on a lightly tinted band with numbered circles, a friendly pull quote and a rounded call-to-action panel. Keep plenty of open space.",
    },
    clinic: {
      name: "Clear care",
      fonts: { display: "Plus Jakarta Sans", sans: "Plus Jakarta Sans" }, weight: 700, tracking: "-.03em",
      palettes: [["Sky", "#f7fafc #11283d #1f66c2 #0f2a44 #e8f1fa #ffffff"],
        ["Sage", "#f6f8f5 #1d2b24 #2f7a5b #1d3a2e #eef5f0 #ffffff"],
        ["Coral", "#fffaf7 #2b1f1c #b8432f #3a2622 #fbeee9 #ffffff"]],
      summary: "A calm, trustworthy layout with a visit card, icon cards and star ratings.",
      brief: "Keep it calm and trustworthy: a clear headline with a pill-shaped label beside a large rounded photo, and a floating white card that invites a first visit with the address. Show services as bordered cards with tinted check icons and “Learn more” links, a quote under a row of stars, a soft tinted call-to-action panel and a dark footer.",
    },
    architectural: {
      name: "Studio index",
      fonts: { display: "Space Grotesk", sans: "Inter", mono: "JetBrains Mono" }, weight: 500, tracking: "-.045em",
      palettes: [["Graphite", "#f7f6f1 #22292f #2b5f86 #232b33 #f1f3f2 #ffffff"],
        ["Concrete", "#ecebe7 #1b1b1b #b5452f #2b2b2b #ecebe7 #ffffff"],
        ["Blueprint", "#f3f6fa #10233f #1f5fbf #10233f #e9eef6 #ffffff"]],
      summary: "A side navigation rail, a framed image and an index of entries on a strict grid.",
      brief: "Use a project-index layout: navigation in a dark side rail with numbered links on wide screens and a compact top bar on phones. Lead with a precisely framed wide image, then align the headline, description and action on a strict two-column grid. List services as index rows with monospaced numbers, hairlines and arrows.",
    },
    playful: {
      name: "Playroom",
      fonts: { display: "Bricolage Grotesque", sans: "Nunito" }, weight: 800, tracking: "-.03em",
      palettes: [["Sunny", "#fff1a8 #2e1a47 #7136b0 #3b1d5c #fff1a8 #fff9ef"],
        ["Bubblegum", "#ffe4ec #2a1630 #c8285c #2a1630 #ffe4ec #ffffff"],
        ["Mint pop", "#dcf7ea #102e2a #ff6b3d #123b34 #dcf7ea #1a0d06"]],
      summary: "Chunky outlined tiles, a sticker and slightly tilted cards.",
      brief: "Build a modular composition from chunky, irregularly rounded tiles with thick outlines. Separate the photo and the message into two strong tiles, add a round tilted sticker, and mix one filled card with outlined, slightly rotated cards. Put the quote in a speech bubble. Keep the type big and friendly.",
    },
    atelier: {
      name: "Night cinema",
      fonts: { display: "Cormorant Garamond", sans: "Jost" }, weight: 600, tracking: "-.01em",
      palettes: [["Bronze", "#14171d #f6efe3 #e3bb84 #0c1016 #efe2cc #1a140d"],
        ["Velvet", "#1a1014 #f5e9ea #e28a9a #120a0d #f5e9ea #1a0a0e"],
        ["Silver", "#121416 #eef0f2 #b8c4cf #0b0c0e #e6e9ec #121416"]],
      summary: "A full-bleed photo under the navigation, with a low-set serif headline.",
      brief: "Open like a film title: one edge-to-edge photograph behind slim overlaid navigation, with a large serif headline and an outlined action anchored low over a readable gradient. Use dark sections, italic serif numerals and a large italic pull quote in the primary color, hairline frames and restrained uppercase labels.",
    },
    fieldnotes: {
      name: "Field guide",
      fonts: { display: "Source Serif 4", sans: "Source Sans 3", mono: "IBM Plex Mono" }, weight: 700, tracking: "-.02em",
      palettes: [["Forest", "#f0ebd9 #263c2e #406842 #2f4835 #f7f1df #fff9e9"],
        ["Ochre", "#f4ecd8 #3a2a17 #95561a #4a3520 #f6ecd6 #fff8ec"],
        ["Slate", "#e9ece9 #1f2a30 #3f6274 #26343c #eef1ef #ffffff"]],
      summary: "Ruled bands, a framed photo plate and a numbered contents list.",
      brief: "Borrow from a printed field guide: a header over a double rule, monospaced labels such as “No. 01” and “Plate I”, a framed photographic plate beside bookish serif copy, and a numbered contents list on a deep band. Put the quote on a ruled field-note card and frame the call to action with a double line.",
    },
    retro: {
      name: "Fresh daily",
      fonts: { display: "Instrument Serif", sans: "Figtree" }, weight: 400, tracking: "-.02em",
      palettes: [["Crust", "#faf5ee #2b1d16 #b04a26 #2b1d16 #faf5ee #ffffff"],
        ["Matcha", "#f4f5ee #1f2a1f #3f6d30 #24331f #f4f5ee #ffffff"],
        ["Espresso", "#1c1512 #f5ebe0 #e0a15c #2a1f19 #f5ebe0 #1c1512"]],
      summary: "A big serif headline, a rounded photo with today’s special, and a menu-style list.",
      brief: "Make it feel like a modern neighbourhood bakery board. Pair a large, light serif headline with a tall rounded photo and a small floating “Today” card for the special. Show services as a menu list with names in serif and short italic notes, on a softly tinted rounded panel. Use a large italic quote, pill buttons and a rounded dark call-to-action panel.",
    },
  };
  const serifFonts = new Set(["Fraunces", "Cormorant Garamond", "Source Serif 4", "Instrument Serif"]);
  const monoFonts = new Set(["JetBrains Mono", "IBM Plex Mono"]);
  const fontStack = (family) => `"${family}", ${serifFonts.has(family) ? "Georgia, serif"
    : monoFonts.has(family) ? "ui-monospace, monospace" : "system-ui, sans-serif"}`;
  const paletteColors = (key, index) => looks[key].palettes[index][1].split(" ");

  const frameworks = { tailwind: "Tailwind CSS", bootstrap: "Bootstrap", plain: "Plain CSS" };
  const steps = ["business", "look", "pages", "handoff"];
  const storageKey = "pinegrow-kit-builder-v2";
  const textFields = ["website-url", "notes", "image-folder"];
  const selectFields = ["starter", "framework", "purpose", "images", "delivery"];

  const pageChoices = {
    home: "Home", services: "Services", work: "Work", prices: "Pricing", about: "About",
    contact: "Contact", faq: "FAQ", gallery: "Gallery", journal: "Journal", location: "Location",
  };

  const starters = {
    crux: {
      photo: { path: "./images/crux-climbing.webp", alt: "A boulderer in a red top climbs a steep indoor wall", position: "48% 28%" },
      name: "Crux Climbing", type: "Bouldering gym", action: "Plan your first visit", title: "Make your first move.",
      description: "Indoor bouldering for first-timers, regulars and the whole family.",
      idea: "Borrow the clarity of a climbing gym’s session board.",
      look: "bold", pages: ["home", "services", "prices", "contact", "faq"], features: ["faq", "form"],
      labels: { services: "Climbing & classes", prices: "Prices & memberships", contact: "Visit us" },
      nav: { services: "Climb", prices: "Prices", contact: "Visit us" },
      section: ["Find your next session", ["First visits", "Everything you need to start"], ["Classes", "Try a coached session"], ["Kids & parties", "Make it a family climb"]],
      secondary: "See prices", quote: ["The friendliest wall in town. I came for one session and stayed for the people.", "Maya, member since 2024"],
      cta: "Your first climb starts here.", address: "Unit 4, Harbour Works · Open daily 7–22",
    },
    splash: {
      photo: { path: "./images/splash-swim-school.webp", alt: "A swim instructor helps a child with a yellow kickboard", position: "55% 30%" },
      name: "Splash Swim School", type: "Swim school", action: "Find a lesson", title: "Find your feet in the water.",
      description: "Swimming lessons for little ones, growing swimmers and adults finding their confidence.",
      idea: "Let the pool timetable guide parents and adult learners to the right lesson.",
      look: "coastal", pages: ["home", "services", "prices", "about", "contact"], features: ["timetable", "form"],
      labels: { services: "Lessons", prices: "Prices & timetable" }, nav: { prices: "Timetable" },
      section: ["Lessons for every stage", ["Parent & baby", "First splashes together"], ["Kids", "Build skills at their own pace"], ["Adults", "Gain confidence in the pool"]],
      secondary: "See the timetable", quote: ["Our daughter went from nervous to diving in, in a single term.", "Tom, parent"],
      cta: "Book a free trial lesson.", address: "Meadow Leisure Pool · Lessons 7 days a week",
    },
    yoga: {
      detail: { path: "./images/still-water-yoga-studio-detail.webp", alt: "Hands unfolding a woven blanket on a mat next to a cork yoga block", position: "50% 55%" },
      photo: { path: "./images/still-water-yoga-class.webp", alt: "Four people doing a seated side stretch in a softly lit yoga studio", position: "50% 35%" },
      name: "Still Water Yoga", type: "Yoga studio", action: "Find a class", title: "Make space to slow down.",
      description: "Small classes and thoughtful teaching, with room for every kind of practice.",
      idea: "Use the order and rhythm of a paper class register to organize classes, times and teachers.",
      look: "editorial", pages: ["home", "services", "about", "contact"], features: ["timetable", "form"],
      labels: { services: "Classes & timetable", about: "About & teachers" }, nav: { services: "Classes", about: "Teachers" },
      section: ["Find your practice", ["Vinyasa", "Movement and breath"], ["Slow Flow", "Time to notice the details"], ["Yin", "A quiet and steady practice"]],
      secondary: "Meet the teachers", quote: ["The calmest hour of my week. The teachers notice everything.", "Ruth, student"],
      cta: "Your first class is on us.", address: "12 Mill Lane · Classes from 7am",
    },
    cafe: {
      photo: { path: "./images/ember-and-oat.webp", alt: "A bakery counter with fresh loaves and morning light", position: "60% 40%" },
      name: "Ember & Oat", type: "Café & bakery", action: "See the menu", title: "Fresh from the oven.",
      description: "Slow mornings, good coffee and small-batch baking in the heart of Leith.",
      idea: "Use the feel of a daily bakery board. Feature what is fresh and make the menu and opening hours easy to find.",
      look: "retro", pages: ["home", "services", "about", "location"], features: ["map", "menu"],
      labels: { services: "Menu", about: "Our story", location: "Find us" }, nav: {},
      section: ["On the counter", ["Sourdough", "A dark crust and soft crumb"], ["Cardamom buns", "Twisted and baked each morning"], ["House coffee", "Espresso or pour-over"]],
      secondary: "Opening hours", quote: ["The cardamom buns are worth the queue. Every single time.", "Sam, a regular since day one"],
      cta: "Come in, the kettle is on.", address: "48 Shore Road, Leith · Open 8–4",
    },
    dental: {
      photo: { path: "./images/willowbend-dental.webp", alt: "A dental professional talking with a young patient and a parent", position: "55% 28%" },
      name: "Willowbend Family Dental", type: "Dental practice", action: "Request a visit", title: "A softer start to dental care.",
      description: "Get to know the team, see what happens at a first visit and choose how to get in touch.",
      idea: "Organize the site around a calm first visit and show the practical details in a clear sequence.",
      look: "clinic", pages: ["home", "services", "about", "faq", "contact"], features: ["form", "faq", "map"],
      labels: { services: "Dental care", about: "Our practice", contact: "Visit & contact" },
      nav: { services: "Care", about: "Practice", contact: "Visit" },
      section: ["What to expect", ["Before your visit", "Know what to bring"], ["Meet the team", "Get familiar with the practice"], ["Plan your next step", "Ask about an appointment"]],
      secondary: "Your first visit", quote: ["They made my son’s first check-up feel like an adventure.", "Priya, parent"],
      cta: "New patients are welcome.", address: "3 Willowbend Road · Monday to Saturday",
    },
    architecture: {
      photo: { path: "./images/northlight-interiors.webp", alt: "Oak shelving and a linen sofa in a sunlit interior", position: "55% 62%" },
      name: "Northlight Interiors", type: "Interior design studio", action: "Explore the projects", title: "Rooms made for living.",
      description: "Considered interiors shaped around everyday rituals, honest materials and the way light changes a room.",
      idea: "Use an architectural grid and give materials and project photos room to breathe.",
      look: "architectural", pages: ["home", "work", "services", "about", "contact"], features: ["lightbox", "form"],
      labels: { work: "Projects", services: "Design services", about: "Studio" }, nav: { work: "Work", services: "Services" },
      section: ["Selected work", ["The Oak House", "A warmer family room"], ["Leith Kitchen", "Space for gathering"], ["The Studio", "A place to make things"]],
      secondary: "Our process", quote: ["They understood how we live before they drew a single line.", "The Harlow family"],
      cta: "Let’s talk about your rooms.", address: "Studio 2, Northlight Yard",
    },
    portfolio: {
      photo: { path: "./images/ana-ruiz.webp", alt: "A woman standing in a doorway in warm late-afternoon light", position: "56% 40%" },
      name: "Ana Ruiz", type: "Photographer", action: "View selected work", title: "Quiet things, closely seen.",
      description: "Portraits, stories and spaces, photographed in the light they have.",
      idea: "Let a strong photo and short captions do most of the work. Use tight editing and clear project and inquiry paths.",
      look: "atelier", pages: ["home", "work", "about", "contact"], features: ["lightbox", "form"],
      labels: { work: "Portfolio", contact: "Enquiries" }, nav: {},
      section: ["Recent stories", ["People", "Portraits at work and at home"], ["Places", "Rooms and streets in between"], ["Editorial", "Stories told in sequences"]],
      secondary: "About Ana", quote: ["Ana sees the quiet moments everyone else misses.", "A client in Lisbon"],
      cta: "Booking spring commissions now.", address: "Lisbon · Available worldwide",
    },
    agency: {
      photo: { path: "./images/field-office.webp", alt: "Four people working around a large table in a bright studio", position: "50% 32%" },
      name: "Field Office", type: "Web design agency", action: "Start a project", title: "Websites people actually use.",
      description: "A small studio for clear, fast websites with systems that teams can keep working with.",
      idea: "Lead with outcomes and put work samples near the first call to action.",
      look: "playful", pages: ["home", "services", "work", "about", "journal", "contact"], features: ["form", "newsletter"],
      labels: { work: "Case studies", about: "Studio" }, nav: { work: "Work" },
      section: ["How we can help", ["Design", "Find the clearest route"], ["Development", "Build it to last"], ["Handover", "Give your team the tools"]],
      secondary: "See our work", quote: ["The first agency that handed us a site we could actually run.", "Head of marketing, Fernwood"],
      cta: "Got a site that needs fixing?", address: "Field Office, 9 Canal Street",
    },
    blank: {
      name: "", type: "", action: "", title: "", description: "",
      idea: "", look: "bold", pages: ["home", "services", "about", "contact"], features: [],
      labels: {}, nav: {}, section: ["On this site", ["Your offer", "Show visitors what you do"], ["Your story", "Share what makes it yours"], ["Get in touch", "Give visitors a next step"]],
      secondary: "Learn more", quote: ["A short quote from a happy customer goes here.", "Customer name"],
      cta: "A clear invitation to get in touch.", address: "Your address · Opening hours",
    },
  };

  // [label, what the person sees, what the agent is asked to build]
  const featureChoices = {
    form: ["Enquiry form", "Visitors send a message from the site.", "Build an enquiry form with labelled fields and success and failure states. Place it on Contact if selected, or on Home otherwise."],
    faq: ["FAQ accordion", "Questions that open to show their answers.", "Build a keyboard-accessible FAQ accordion with editable questions and answers."],
    booking: ["External booking", "A button to your booking service.", "Link to the supplied external booking service. If its URL is missing, mark it for setup."],
    timetable: ["Timetable", "Classes or opening times you edit in Pinegrow.", "Make the timetable editable in Pinegrow. Treat it as a static schedule and label example times."],
    lightbox: ["Gallery lightbox", "Photos open large, one after another.", "Provide a keyboard-accessible lightbox with meaningful alternative text for the photos."],
    map: ["Map & directions", "How to get there, with a map link.", "Add written directions and a link to a map for the supplied address."],
    newsletter: ["Newsletter signup", "Collect emails with your mailing service.", "Connect a supplied signup provider or document that setup as pending."],
    menu: ["Menu download", "A link to a PDF menu or price list.", "Add a clearly labelled link to a user-supplied menu file. Mark the link as pending if there is no file."],
    filters: ["Category filters", "Filter a list of work or products.", "Add accessible client-side filters to the listing with visible active and empty states."],
    social: ["Social links", "Links to your social profiles.", "Add links to confirmed social profiles and keep unconfirmed links out of production navigation."],
  };

  const purposes = {
    client: "One website for me or my client. Tailor it to this business.",
    agency: "A reusable base for future client sites. Document how to replace the sample content and reuse the designs and blocks.",
    template: "A kit to distribute or sell. Include a populated example, a clean starter and buyer documentation. Record asset sources and redistribution rights.",
  };
  const deliveryOptions = {
    later: "Hosting and form provider undecided. Document how to connect and test a provider.",
    netlify: "Prepare the enquiry form for Netlify Forms. Include setup and a submission test.",
    external: "Prepare the enquiry form for a separate form service. Leave the endpoint for the user to configure and document a submission test.",
  };

  const custom = { pages: [], features: [] };
  let look = "bold";
  let palette = 0;
  let step = "business";
  let reached = 0;
  let device = "desktop";
  let pickedFolder = "";
  let promptText = "";

  const fromText = (tag, text, className) => {
    const element = document.createElement(tag);
    if (className) element.className = className;
    element.textContent = text;
    return element;
  };

  function renderPageChoices(labels, checked) {
    field("pages").replaceChildren(...Object.keys(pageChoices).map((key) => {
      const label = fromText("label", "", "choice");
      const input = document.createElement("input");
      input.type = "checkbox";
      input.value = key;
      input.checked = key === "home" || checked.includes(key);
      input.disabled = key === "home";
      label.append(input, document.createTextNode(labels[key] || pageChoices[key]));
      return label;
    }));
  }

  function renderFeatureChoices(checked) {
    field("features").replaceChildren(...Object.entries(featureChoices).map(([key, [title, help]]) => {
      const label = fromText("label", "", "choice");
      const input = document.createElement("input");
      input.type = "checkbox";
      input.value = key;
      input.checked = checked.includes(key);
      const text = fromText("span", "", "choice-text");
      text.append(fromText("strong", title), fromText("small", help));
      label.append(input, text);
      return label;
    }));
  }

  // The homepage concept, shared by the large preview and the direction cards. preview.css styles it.
  const siteMarkup = `
    <div class="s-header">
      <span class="s-brand" data-fill="name"></span>
      <span class="s-nav" data-fill="nav"></span>
      <span class="s-hcta" data-fill="action"></span>
      <span class="s-menu"><i></i><i></i><i></i></span>
    </div>
    <div class="s-hero">
      <div class="s-copy">
        <p class="s-eyebrow" data-fill="type"></p>
        <p class="s-title" data-fill="title"></p>
        <p class="s-lead" data-fill="description"></p>
        <div class="s-actions">
          <span class="s-btn"><span data-fill="action"></span><span>→</span></span>
          <span class="s-link" data-fill="secondary"></span>
        </div>
      </div>
      <div class="s-photo" data-photo="photo"><img alt="" decoding="async"></div>
      <span class="s-sticker">Say hello!</span>
      <span class="s-special"><small>Today</small><b data-fill="special"></b><span data-fill="specialDetail"></span></span>
      <span class="s-card"><b data-fill="cta"></b><span data-fill="address"></span><span class="s-card-link"><span data-fill="action"></span> →</span></span>
    </div>
    <div class="s-services">
      <p class="s-section-title" data-fill="sectionTitle"></p>
      <div class="s-items" data-fill="items"></div>
      <div class="s-photo s-detail" data-photo="detail"><img alt="" decoding="async"></div>
    </div>
    <div class="s-quote"><p data-fill="quote"></p><cite data-fill="quoteBy"></cite></div>
    <div class="s-cta">
      <p class="s-cta-title" data-fill="cta"></p>
      <span class="s-btn"><span data-fill="action"></span><span>→</span></span>
    </div>
    <div class="s-footer">
      <span class="s-brand" data-fill="name"></span>
      <span class="s-address" data-fill="address"></span>
      <span class="s-fnav" data-fill="nav"></span>
      <span class="s-copyright">© 2026 <span data-fill="name"></span></span>
    </div>`;

  function createSite(owner) {
    const site = document.createElement("div");
    site.className = "site";
    site.innerHTML = siteMarkup;
    owner.replaceChildren(site);
    return site;
  }

  function fillSite(site, content, key, paletteIndex, shownDevice) {
    const direction = looks[key];
    ["page", "ink", "accent", "band", "on-band", "on-accent"].forEach((name, i) => {
      site.style.setProperty(`--${name}`, paletteColors(key, paletteIndex)[i]);
    });
    site.style.setProperty("--display", fontStack(direction.fonts.display));
    site.style.setProperty("--text", fontStack(direction.fonts.sans));
    site.style.setProperty("--mono", fontStack(direction.fonts.mono || direction.fonts.sans));
    site.style.setProperty("--dw", direction.weight);
    site.style.setProperty("--tracking", direction.tracking);
    site.dataset.look = key;
    site.dataset.device = shownDevice;
    site.querySelectorAll("[data-fill]").forEach((element) => {
      const text = content[element.dataset.fill];
      if (element.dataset.fill === "nav") {
        element.replaceChildren(...text.map((label) => fromText("span", label)));
      } else if (element.dataset.fill === "items") {
        element.replaceChildren(...text.map(([title, detail], i) => {
          const item = fromText("div", "", "s-item");
          item.append(fromText("i", String(i + 1).padStart(2, "0"), "s-num"), fromText("b", title), fromText("span", detail));
          return item;
        }));
      } else {
        element.textContent = text;
      }
    });
    site.querySelectorAll("[data-photo]").forEach((figure) => {
      const photo = content[figure.dataset.photo];
      const image = figure.querySelector("img");
      figure.classList.toggle("is-empty", !photo);
      image.hidden = !photo;
      if (photo && image.getAttribute("src") !== photo.path) {
        image.src = photo.path;
      }
      figure.style.setProperty("--focus", photo?.position || "50% 50%");
    });
    site.querySelector(".s-services").classList.toggle("has-detail", Boolean(content.detail));
  }

  function siteContent(starter, pages) {
    const nav = pages.filter((id) => id !== "home").map((id) => starter.nav[id] || starter.labels[id] || pageChoices[id]);
    const [sectionTitle, ...items] = starter.section;
    return {
      name: starter.name || "Your business",
      type: starter.type || "Kind of business",
      title: starter.title || "Your homepage headline",
      description: starter.description || "Introduce the business and give visitors a clear next step.",
      action: starter.action || "Get in touch",
      secondary: starter.secondary,
      nav: nav.concat(custom.pages).slice(0, 4),
      sectionTitle,
      items,
      special: items[0][0],
      specialDetail: items[0][1],
      quote: starter.quote[0],
      quoteBy: starter.quote[1],
      cta: starter.cta,
      address: starter.address,
      photo: starter.photo,
      detail: starter.detail,
    };
  }

  function renderLookButtons() {
    field("looks").replaceChildren(...Object.entries(looks).map(([key, direction]) => {
      const button = fromText("button", "", "look");
      button.type = "button";
      button.dataset.look = key;
      const thumb = fromText("span", "", "look-thumb");
      thumb.setAttribute("aria-hidden", "true");
      createSite(thumb);
      const text = fromText("span", "", "look-text");
      text.append(fromText("strong", direction.name));
      button.append(thumb, text);
      return button;
    }));
  }

  function startFrom(key) {
    const starter = starters[key];
    look = starter.look;
    palette = 0;
    renderPageChoices(starter.labels, starter.pages);
    renderFeatureChoices(starter.features);
  }

  function showStep(next, moveFocus = false) {
    step = next;
    reached = Math.max(reached, steps.indexOf(step));
    root.dataset.step = step;
    root.querySelectorAll("[data-step]").forEach((button) => {
      const index = steps.indexOf(button.dataset.step);
      button.setAttribute("aria-pressed", String(button.dataset.step === step));
      button.classList.toggle("is-done", index < reached && button.dataset.step !== step);
    });
    root.querySelectorAll("[data-panel]").forEach((panel) => { panel.hidden = panel.dataset.panel !== step; });
    field("prompt-view").hidden = step !== "handoff";
    const previewView = field("preview-view");
    if (step === "handoff") {
      root.querySelector(".handoff-side").prepend(previewView);
    } else {
      root.querySelector(".studio-stage").prepend(previewView);
    }
    root.querySelector(".studio-controls").scrollTop = 0;
    if (moveFocus) {
      root.querySelector(`[data-step="${step}"]`).focus();
    }
    fitPreview();
  }

  function renderCustom(group) {
    const items = custom[group].map((label, index) => {
      const chip = fromText("span", label, "token");
      const remove = fromText("button", "×");
      remove.type = "button";
      remove.dataset.remove = group;
      remove.dataset.index = index;
      remove.setAttribute("aria-label", `Remove ${label}`);
      chip.append(remove);
      return chip;
    });
    field(`custom-${group}`).replaceChildren(...items);
  }

  // The prompt describes the example business only until the person names their own: a website or a description.
  // The preview always shows the example's content.
  const mode = () => root.querySelector('input[name="pk-mode"]:checked').value;
  const ownBusiness = () => mode() === "existing" || Boolean(value("notes"));
  const isExampleBusiness = (starter) => Boolean(starter.type) && !ownBusiness();

  function pageLabels(starter) {
    return ownBusiness() ? pageChoices : { ...pageChoices, ...starter.labels };
  }

  function renderLookStep(content) {
    const direction = looks[look];
    root.querySelectorAll("button[data-look]").forEach((button) => {
      const key = button.dataset.look;
      button.setAttribute("aria-pressed", String(key === look));
      fillSite(button.querySelector(".site"), content, key, key === look ? palette : 0, "desktop");
    });
    field("palettes").replaceChildren(...direction.palettes.map(([name], index) => {
      const button = fromText("button", "", "palette");
      button.type = "button";
      button.dataset.palette = index;
      button.setAttribute("aria-pressed", String(index === palette));
      const dots = fromText("span", "", "palette-dots");
      dots.setAttribute("aria-hidden", "true");
      dots.append(...[0, 2, 3, 1].map((i) => {
        const dot = fromText("span", "");
        dot.style.background = paletteColors(look, index)[i];
        return dot;
      }));
      button.append(dots, fromText("span", name));
      return button;
    }));
    write("look-summary", direction.summary);
    const fonts = field("fonts");
    fonts.replaceChildren(fromText("span", "Headings "), document.createTextNode(direction.fonts.display),
      fromText("span", " · Text "), document.createTextNode(direction.fonts.sans));
    if (direction.fonts.mono) {
      fonts.append(fromText("span", " · Labels "), document.createTextNode(direction.fonts.mono));
    }
  }

  function renderPreview(starter, pages) {
    const content = siteContent(starter, pages);
    const preview = field("preview");
    const site = preview.firstElementChild || createSite(preview);
    fillSite(site, content, look, palette, shownDevice());
    root.querySelectorAll("button[data-device-choice]").forEach((button) => {
      button.setAttribute("aria-pressed", String(button.dataset.deviceChoice === device));
    });
    write("look-status", `${looks[look].name} · ${looks[look].palettes[palette][0]}`);
    renderLookStep(content);
  }

  function describePhotoFolder() {
    const path = value("image-folder");
    if (!path) {
      return "Use my own photos. Ask for the local folder path if it is missing.";
    }
    const folder = JSON.stringify(path);
    if (path === pickedFolder) {
      return `Use my own photos from the selected folder ${folder}. Look for it inside the agent’s workspace. Ask for the full path if the folder is elsewhere. Map suitable images to placements and identify gaps.`;
    }
    return `Use my own photos from this local path: ${folder}. Resolve a relative path from the project workspace. Map suitable images to placements and identify gaps.`;
  }

  function makePrompt({ starter, pages, features, buildLibrary, framework, wordpress }) {
    const bundledSupport = framework === "tailwind" && !wordpress;
    const delivery = value("delivery");
    const publishing = wordpress ? "WordPress hosting to be decided." : "Static hosting to be decided.";
    const imageOptions = {
      placeholder: "Use replaceable placeholders. List the photos to replace and their intended aspect ratios.",
      local: describePhotoFolder(),
      generated: "Generate the needed images with an available image-generation tool. Keep photographic style and cropping consistent, and identify any missing assets.",
      stock: "Find suitable photographs on Unsplash. Verify usage rights and record the source URL and photographer for each selected image.",
    };
    const direction = looks[look];
    const url = value("website-url");
    const example = isExampleBusiness(starter);
    let business;
    if (mode() === "existing") {
      business = url ? `The business at ${url}` : "The business on the user’s current website (ask for its address)";
    } else if (example) {
      business = `${starter.name} (${starter.type}), a sample business`;
    } else {
      business = value("notes") ? "The business described in the notes" : "The user’s business (ask about it)";
    }
    const concept = example ? [
      `Kind of business: ${starter.type}`,
      `Main visitor action: ${starter.action}`,
      `Homepage headline: ${starter.title}`,
      `Homepage introduction: ${starter.description}`,
    ] : [
      ...(mode() === "existing" ? ["Current website: Read it first. Take the business name, offer, facts, tone and page structure from it, keep what works and improve the rest. Reuse its photos only if the user confirms they may."] : []),
      "Work out the kind of business, the main visitor action, the homepage headline and the introduction from what the user supplied. Ask only if it is unclear.",
    ];
    const featureLines = features.map((key) => `- ${featureChoices[key][0]}: ${featureChoices[key][2]}`)
      .concat(custom.features.map((feature) => `- Custom feature: ${feature}`));
    const fontLines = [
      `- display: ${direction.fonts.display}, headings at weight ${direction.weight}`,
      `- sans: ${direction.fonts.sans}`,
      ...(direction.fonts.mono ? [`- mono: ${direction.fonts.mono}`] : []),
    ];
    return [
      "Build an editable Pinegrow website kit from this brief with the pinegrow-website-kit skill. The brief answers the skill’s questions, so ask only about what is missing.",
      ...(agentMode ? [] : [
        "",
        "# Setup",
        "- If the pinegrow-website-kit skill is installed, or the workspace has a kit-builder folder with SKILL.md, use it and skip the rest of this setup.",
        "- Otherwise tell the user that this needs the free Pinegrow kit-builder skill from https://github.com/Pinegrow/pinegrow-website-kit and ask whether you may download it (about 500 KB). Wait for their answer.",
        `- If they agree, download ${skillZip} and unzip it. It holds the skill folder pinegrow-website-kit.`,
        "- Ask whether to install it for later kits by copying that folder into your skills folder (Claude Code: ~/.claude/skills, Codex: ~/.codex/skills). If they decline, use it from where you unzipped it.",
        "- Read its SKILL.md and follow it with the brief below.",
      ]),
      ...(bundledSupport ? [] : ["The bundled skill covers Tailwind CSS static kits. Check whether your Pinegrow workflow supports the build target below and use that workflow when available. If it is unavailable, explain what is missing before substituting another framework or output."]),
      "",
      "# Kit brief",
      `Purpose: ${purposes[value("purpose")]}`,
      `Businesses and pages: ${business}: ${list(pages)}`,
      `CSS: ${frameworks[framework]}`,
      `WordPress: ${wordpress ? "yes (block theme)" : "no"}`,
      "Designs: 3",
      `Block library: ${buildLibrary ? "yes" : "no"}`,
      `Publishing: ${publishing}${features.includes("form") ? ` ${deliveryOptions[delivery]}` : ""}`,
      `Images: ${imageOptions[value("images")]}`,
      "",
      "## Concept",
      ...concept,
      `Visual direction: ${direction.name}. ${direction.brief}`,
      ...(starter.idea && example ? [`Idea: ${starter.idea}`] : []),
      "",
      "## Color roles",
      `The active saved design, ${direction.palettes[palette][0]}. Add surface, muted and line to fit, and check contrast.`,
      ...colorRoles.map((role, i) => `- ${role}: ${paletteColors(look, palette)[i]}`),
      "",
      "## Fonts",
      "Google Fonts, the same in every saved design.",
      ...fontLines,
      "",
      "## Saved designs",
      `Make ${direction.palettes[palette][0]} (the colors above) the active design, and add these two:`,
      ...direction.palettes.map(([name], index) => [name, index]).filter(([, index]) => index !== palette)
        .map(([name, index]) => `- ${name}: ${colorRoles.map((role, i) => `${role} ${paletteColors(look, index)[i]}`).join(", ")}`),
      "",
      "## Pages",
      ...pages.map((page) => `- ${page}`),
      "",
      "## Page structure and block library",
      "Plan the sections and page layouts from the site goals, page list, features and visual direction. Choose the content hierarchy and composition for each page.",
      buildLibrary
        ? "For every distinct section used anywhere on the site, design the version used on the page and two genuinely different layout alternatives. Keep each version self-contained and editable in Pinegrow’s Content panel. Put all versions in named categories in the Pinegrow Insert panel, using the shared designs and styles."
        : "Create the sections directly in the pages with the appropriate Pinegrow annotations and shared components. The brief opts out of generating a separate block library, so leave the library and its source collection out of this build.",
      "",
      ...(wordpress ? [
        "## WordPress export",
        "Configure the Pinegrow project for WordPress block-theme export and provide the installable theme. Include templates and styles and make applicable content editable in the WordPress Site Editor. Document how to re-export and verify installation, the Site Editor and the front end when a WordPress test site is available. Report any remaining verification.",
        "",
      ] : []),
      "## Features and integrations",
      ...(featureLines.length ? featureLines : ["- No additional site behavior requested."]),
      ...(features.includes("form") ? [] : ["- Use contact details wherever a contact section or page is needed. Add a form only if it was explicitly requested as a custom feature."]),
      "",
      "## Notes",
      value("notes") || (example
        ? "Use the sample business above, and label its content as sample content."
        : "No notes about the business. Ask for the facts the site needs, and label sample content."),
      "",
      "Save the brief as KIT-BRIEF.md. Build shared header and footer components across the saved designs. Make text, images and repeated entries editable in Pinegrow’s Content panel.",
      "Use supplied facts and label missing production content. Run the kit checker and report deployment or form setup, asset replacement and any remaining Pinegrow compilation or editor verification. Ask only about missing information that changes the build.",
    ].join("\n");
  }

  // Shows the prompt as a document: headings, Key: value facts, lists and color chips.
  function renderBrief(text) {
    const nodes = [];
    let listElement = null;
    for (const line of text.split("\n")) {
      if (line.startsWith("- ")) {
        if (!listElement) {
          listElement = document.createElement("ul");
          nodes.push(listElement);
        }
        const item = fromText("li", "");
        const color = line.match(/^- ([a-z-]+): (#[0-9a-f]{6})$/i);
        if (color) {
          const chip = fromText("span", "", "color-chip");
          chip.style.setProperty("--chip", color[2]);
          item.append(chip, fromText("b", color[1]), document.createTextNode(` ${color[2]}`));
        } else {
          item.textContent = line.slice(2);
        }
        listElement.append(item);
        continue;
      }
      listElement = null;
      if (!line) {
        continue;
      }
      if (line.startsWith("## ")) {
        nodes.push(fromText("h4", line.slice(3)));
      } else if (line.startsWith("# ")) {
        nodes.push(fromText("h3", line.slice(2)));
      } else {
        const fact = line.match(/^([A-Z][A-Za-z ]{1,30}): (.+)$/);
        if (fact) {
          const p = fromText("p", "", "brief-fact");
          p.append(fromText("b", `${fact[1]}: `), document.createTextNode(fact[2]));
          nodes.push(p);
        } else {
          nodes.push(fromText("p", line));
        }
      }
    }
    field("brief").replaceChildren(...nodes);
  }

  function render() {
    const starter = starters[value("starter")];
    const pickedPages = selected("pages");
    const pickedFeatures = selected("features");
    const labels = pageLabels(starter);
    field("pages").querySelectorAll("input").forEach((input) => { input.nextSibling.textContent = labels[input.value]; });
    const pages = Array.from(new Set(pickedPages.map((key) => labels[key]).concat(custom.pages)));
    const existing = mode() === "existing";
    field("url-field").hidden = !existing;
    field("notes").placeholder = existing
      ? "What should change, and anything the site doesn’t say: new services, prices, tone."
      : "What the business does, who it is for, the tone, and facts like address, opening hours and prices.";
    write("notes-help", existing
      ? "The agent works out the rest from your current website."
      : starter.type
        ? `Leave it empty to build the kit for the sample business, ${starter.name}. The agent works out the rest.`
        : "The agent works out the headline, introduction and main action from it.");
    const buildLibrary = field("library").checked;
    const wordpress = field("wordpress").checked;
    const framework = value("framework");
    const format = `${wordpress ? "WordPress theme" : "Static site"} · ${frameworks[framework]}`;
    field("delivery-field").hidden = !pickedFeatures.includes("form");
    field("image-folder-field").hidden = value("images") !== "local";
    write("folder-note", pickedFolder
      ? "The chooser gives only the folder name. Paste the full path if the folder is outside the agent’s workspace."
      : "Paste a local path, or choose a folder in the agent’s workspace.");
    renderPreview(starter, pickedPages);
    const featureCount = pickedFeatures.length + custom.features.length;
    const count = `${pages.length} pages · ${featureCount} ${featureCount === 1 ? "feature" : "features"}${buildLibrary ? " · Block library" : ""}`;
    write("scope-status", count);
    write("review-business", existing ? (value("website-url") || "Current website")
      : isExampleBusiness(starter) ? `${starter.name} (sample)` : value("notes") ? "From your description" : "Not described yet");
    write("sample-status", ownBusiness() && starter.type ? `Sample content from ${starter.name}` : "");
    write("review-look", `${looks[look].name} · ${looks[look].palettes[palette][0]}`);
    write("review-format", format);
    write("review-scope", count);
    promptText = makePrompt({ starter, pages, features: pickedFeatures, buildLibrary, framework, wordpress });
    field("prompt-text").value = promptText;
    renderBrief(promptText);
  }

  // Saving: everything goes to localStorage. A shared link carries the same state, without the photo folder.
  function currentState() {
    const state = { look, palette, device, custom, mode: mode(), pages: selected("pages"), features: selected("features"),
      buildLibrary: field("library").checked, wordpress: field("wordpress").checked };
    for (const id of [...textFields, ...selectFields]) {
      state[id] = field(id).value;
    }
    return state;
  }

  function saveState() {
    try {
      localStorage.setItem(storageKey, JSON.stringify(currentState()));
    } catch {
      // Without storage the page still works for this visit.
    }
  }

  function encodeState(state) {
    const bytes = new TextEncoder().encode(JSON.stringify(state));
    return btoa(String.fromCharCode(...bytes)).replaceAll("+", "-").replaceAll("/", "_").replace(/=+$/, "");
  }

  function decodeState(text) {
    const binary = atob(text.replaceAll("-", "+").replaceAll("_", "/"));
    return JSON.parse(new TextDecoder().decode(Uint8Array.from(binary, (c) => c.charCodeAt(0))));
  }

  function loadState() {
    const shared = new URLSearchParams(location.hash.slice(1)).get("kit");
    try {
      if (shared) {
        return decodeState(shared);
      }
      return JSON.parse(localStorage.getItem(storageKey)) || {};
    } catch {
      return {};
    }
  }

  function restoreState(state) {
    const pick = (id, wanted) => {
      const option = Array.from(field(id).options).find((o) => o.value === wanted && !o.disabled);
      if (option) {
        field(id).value = wanted;
      }
    };
    pick("starter", state.starter);
    startFrom(value("starter"));
    for (const id of selectFields.slice(1)) {
      pick(id, state[id]);
    }
    for (const id of textFields) {
      if (typeof state[id] === "string") {
        field(id).value = state[id];
      }
    }
    field(state.mode === "existing" ? "mode-existing" : "mode-new").checked = true;
    if (Object.hasOwn(looks, state.look || "")) {
      look = state.look;
      palette = [0, 1, 2].includes(state.palette) ? state.palette : 0;
    }
    if (["desktop", "phone"].includes(state.device)) {
      device = state.device;
    }
    for (const id of ["pages", "features"]) {
      if (Array.isArray(state[id])) {
        field(id).querySelectorAll("input").forEach((input) => {
          input.checked = input.disabled || state[id].includes(input.value);
        });
      }
      if (Array.isArray(state.custom?.[id])) {
        custom[id] = state.custom[id].filter((item) => typeof item === "string");
        renderCustom(id);
      }
    }
    if (typeof state.buildLibrary === "boolean") {
      field("library").checked = state.buildLibrary;
    }
    if (typeof state.wordpress === "boolean" && !field("wordpress").disabled) {
      field("wordpress").checked = state.wordpress;
    }
  }

  let toastTimer = 0;
  function toast(message) {
    const status = field("copy-status");
    status.textContent = message;
    status.classList.add("is-visible");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => status.classList.remove("is-visible"), 2400);
  }

  async function copyText(text, done) {
    try {
      await navigator.clipboard.writeText(text);
      toast(done);
    } catch {
      const area = document.createElement("textarea");
      area.value = text;
      area.setAttribute("readonly", "");
      area.style.position = "fixed";
      area.style.opacity = "0";
      root.append(area);
      area.select();
      let copied = false;
      try {
        copied = document.execCommand("copy");
      } catch {
        // Reported below.
      }
      area.remove();
      toast(copied ? done : "Copying is blocked here. Open the Prompt step and select the text.");
    }
  }

  function shareLink() {
    const state = currentState();
    delete state["image-folder"];
    const url = new URL(location.href);
    url.hash = `kit=${encodeState(state)}`;
    void copyText(url.href, "Link copied. It opens this setup.");
  }

  function download() {
    const host = value("website-url").replace(/^https?:\/\/(www\.)?/, "").split("/")[0];
    const slug = (host || (isExampleBusiness(starters[value("starter")]) ? starters[value("starter")].name : "") || "website").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "website";
    const link = document.createElement("a");
    link.href = URL.createObjectURL(new Blob([promptText + "\n"], { type: "text/markdown" }));
    link.download = `${slug}-kit-prompt.md`;
    root.append(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(link.href), 1000);
  }

  // The concept is designed at a fixed width and zoomed to fit its frame. The prompt step and narrow windows show
  // only the top of the desktop concept, pinned above the settings in narrow windows.
  const designWidth = { desktop: 1100, phone: 390 };
  const heroHeight = 680;
  const narrow = matchMedia("(max-width: 860px)");
  const isCompact = () => narrow.matches || step === "handoff";
  const shownDevice = () => isCompact() ? "desktop" : device;

  function fitPreview() {
    const compact = isCompact();
    root.classList.toggle("is-compact-preview", compact);
    const frame = root.querySelector(".preview-frame");
    const site = field("preview").firstElementChild;
    if (site) {
      site.dataset.device = shownDevice();
      let zoom = Math.min(1, frame.clientWidth / designWidth[shownDevice()]);
      if (narrow.matches && step !== "handoff") {
        zoom = Math.min(zoom, innerHeight * .34 / heroHeight);
      }
      if (zoom > 0) {
        site.style.zoom = String(zoom);
        frame.style.maxHeight = compact ? `${Math.round(heroHeight * zoom)}px` : "";
      }
    }
    const thumb = field("looks").querySelector(".look-thumb");
    if (thumb?.clientWidth) {
      root.style.setProperty("--thumb-zoom", String(thumb.clientWidth / designWidth.desktop));
    }
    const stage = root.querySelector(".studio-stage");
    root.style.setProperty("--stage-height", narrow.matches && step !== "handoff" ? `${stage.offsetHeight}px` : "0px");
  }
  const resizes = new ResizeObserver(fitPreview);
  resizes.observe(root.querySelector(".preview-frame"));
  resizes.observe(field("looks"));
  narrow.addEventListener("change", fitPreview);
  addEventListener("resize", fitPreview);

  function addCustom(group) {
    const input = field(`other-${group}`);
    const entries = (group === "pages" ? input.value.split(",") : [input.value]).map((item) => item.trim()).filter(Boolean);
    if (entries.length) {
      custom[group] = Array.from(new Set([...custom[group], ...entries]));
      input.value = "";
      renderCustom(group);
      render();
      saveState();
    }
    input.focus();
  }

  root.addEventListener("click", (event) => {
    const button = event.target.closest("button");
    if (!button) {
      return;
    }
    if (button.dataset.add) {
      addCustom(button.dataset.add);
      return;
    }
    if (button.dataset.copy) {
      void copyText(promptText, "Prompt copied. Paste it into your AI agent.");
      return;
    }
    if (button === field("choose-folder")) {
      field("folder-picker").click();
      return;
    }
    if (button === field("share")) {
      shareLink();
      return;
    }
    if (button === field("download")) {
      download();
      return;
    }
    if (button.dataset.step || button.dataset.next) {
      showStep(button.dataset.step || button.dataset.next, Boolean(button.dataset.next));
      return;
    }
    if (button.dataset.look) {
      if (look !== button.dataset.look) {
        look = button.dataset.look;
        palette = 0;
      }
    } else if (button.dataset.palette) {
      palette = Number(button.dataset.palette);
    } else if (button.dataset.deviceChoice) {
      device = button.dataset.deviceChoice;
      fitPreview();
    } else if (button.dataset.remove) {
      const group = button.dataset.remove;
      custom[group].splice(Number(button.dataset.index), 1);
      renderCustom(group);
      field(`other-${group}`).focus();
    }
    render();
    saveState();
  });

  root.addEventListener("keydown", (event) => {
    if (event.key !== "Enter" || event.isComposing || !event.target.id?.startsWith("pk-other-")) {
      return;
    }
    event.preventDefault();
    addCustom(event.target.id.slice("pk-other-".length));
  });

  root.addEventListener("input", (event) => {
    const target = event.target;
    if (target === field("folder-picker") || target.id?.startsWith("pk-other-")) {
      return;
    }
    if (target === field("image-folder")) {
      pickedFolder = "";
    }
    if (target === field("starter")) {
      startFrom(value("starter"));
    }
    render();
    saveState();
  });

  field("folder-picker").addEventListener("change", (event) => {
    const picker = event.currentTarget;
    const relativePath = picker.files[0]?.webkitRelativePath || "";
    picker.value = "";
    if (!relativePath.includes("/")) {
      write("folder-note", "Paste the folder path to use it in the prompt.");
      return;
    }
    pickedFolder = relativePath.split("/", 1)[0];
    field("image-folder").value = pickedFolder;
    render();
    saveState();
  });

  renderLookButtons();
  restoreState(loadState());
  render();
  showStep("business");
})();
