# Make the contact form work

The contact form sends messages without leaving the page and shows the thank-you or error message below the
button. A static site has no server of its own, so pick one way to receive the messages:

## 1. Netlify (no setup)

Publish the site to Netlify from Pinegrow (Publish › Netlify). The form already has `data-netlify="true"`, so
Netlify Forms collects the messages. Turn on email notifications in Netlify: Site configuration › Forms ›
Form notifications.

On a `*.netlify.app` address it works right away. With your own domain, select the form in Pinegrow and set its
`data-form-endpoint` attribute to `netlify`.

## 2. A form service (any host)

For GitHub Pages, Cloudflare Pages, SFTP or any other host, use a form service such as
[Formspree](https://formspree.io) or [Web3Forms](https://web3forms.com):

1. Create a form there and copy its address, for example `https://formspree.io/f/abcdwxyz`.
2. In Pinegrow, select the form and paste the address into its `action` attribute. The form then also works for
   visitors without JavaScript.
3. For Web3Forms, also add a hidden field inside the form:
   `<input type="hidden" name="access_key" value="YOUR-ACCESS-KEY">` and use
   `https://api.web3forms.com/submit` as the address.

Until one of these is set up, sending shows the error message.

<!-- wordpress -->
## WordPress

When the site is exported as a WordPress theme, WordPress sends the messages to the site's admin email. Nothing to
set up. The form's `cms-form-*` attributes control the subject and the messages.
<!-- /wordpress -->

## Spam

A hidden field (`company_website`) catches most bots: people never see it, bots fill it in, and those messages are
quietly dropped.
