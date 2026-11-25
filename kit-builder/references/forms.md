# Contact form

A static site has no server, so the form needs somewhere to send messages: Netlify Forms or a form service.
`kit.py init` copies `form/` into the project: `form.js` sends the form without leaving the page and shows a
thank-you or error message, and `form/README.md` explains the setup to the user; link to it in the kit's README.

Don't add a server-side mailer (a PHP script or similar) to the kit. It would be a security risk on the user's
hosting (spam relay, header injection) and it isn't needed.

## The form

```html
<form class="contact-form" name="contact" method="POST" action="contact.html"
      data-form data-form-endpoint="" data-netlify="true" netlify-honeypot="company_website">
    <input type="hidden" name="form-name" value="contact">
    <p class="hidden" aria-hidden="true"><label>Leave this field empty
        <input type="text" name="company_website" tabindex="-1" autocomplete="off"></label></p>
    <label class="field-label">Your name <input class="field" type="text" name="name" autocomplete="name" required></label>
    <label class="field-label">Email <input class="field" type="email" name="email" autocomplete="email" required></label>
    <label class="field-label">Message <textarea class="field" name="message" rows="5" required></textarea></label>
    <button type="submit" class="btn-primary" data-pg-content-label="Send button">Send</button>
    <p class="form-message hidden" role="status" data-form-success data-pg-content-label="Thank you message">Thank you. We'll reply within two working days.</p>
    <p class="form-message hidden" role="alert" data-form-error data-pg-content-label="Error message">Sorry, the message couldn't be sent. Please email us at hello@example.com.</p>
</form>
```

Keep:

- `data-form`: `form.js` handles only forms with it.
- `action`: the page itself until the user sets up a form service; then the service's address (Formspree,
  Web3Forms), which also makes the form work without JavaScript.
- `data-form-endpoint`: empty, or `netlify` for Netlify with a custom domain.
- `data-netlify="true"`, `netlify-honeypot` and the hidden `form-name` field: Netlify Forms.
- The `company_website` field: a hidden honeypot that drops spam from bots.
- `data-form-success` and `data-form-error`: the messages `form.js` shows. They start `hidden`.
- `<script src="form/form.js" defer></script>` in the head of the page.

Field names can change (`phone`, `service`, `date`...). Netlify and the form services receive every field.

## Which way to receive messages

From the brief's publishing answer:

- Netlify: works on `*.netlify.app` without setup. With a custom domain, set `data-form-endpoint="netlify"`.
- Any other host (GitHub Pages, Cloudflare Pages, SFTP...): a form service. The user creates a form there and pastes
  its address into the form's `action`.

Until one is set up, sending shows the error message, so write the error message to include another way to get in
touch (an email address or phone number).

Write the matching steps into the kit's README.
