/* Contact form: sends the message without leaving the page and shows the thank-you or error message.

   Choose how messages reach you (see form/README.md):

   1. Netlify: publish the site to Netlify. Netlify Forms receives the messages (the form has data-netlify="true").
      On a *.netlify.app address nothing needs to be set up. With your own domain, set the form's
      data-form-endpoint attribute to "netlify".
   2. A form service, for any host (GitHub Pages, Cloudflare Pages, SFTP...): create a form at Formspree, Web3Forms
      or a similar service and paste its address into the form's action attribute.

   On WordPress, the theme's own form handling (cms-form) sends the messages and this script stays out of the way. */

(function () {
    "use strict";

    function onNetlify(form) {
        return /\.netlify\.app$/.test(location.hostname)
            || (form.getAttribute("data-form-endpoint") || "").trim().toLowerCase() === "netlify";
    }

    // A form service address in the form's action (or, as before, in data-form-endpoint).
    function serviceAddress(form) {
        var endpoint = (form.getAttribute("data-form-endpoint") || "").trim();
        if (/^https:\/\//i.test(endpoint)) {
            return endpoint;
        }
        var action = (form.getAttribute("action") || "").trim();
        return /^https:\/\//i.test(action) ? action : "";
    }

    function show(form, selector, visible) {
        var element = form.querySelector(selector);
        if (element) {
            element.classList.toggle("hidden", !visible);
        }
    }

    function send(form, data) {
        if (onNetlify(form)) {
            return fetch("/", {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: new URLSearchParams(data).toString()
            });
        }
        var address = serviceAddress(form);
        if (!address) {
            console.warn("Contact form: no form service is set up. See form/README.md.");
            return Promise.reject(new Error("No form service"));
        }
        return fetch(address, { method: "POST", body: data, headers: { Accept: "application/json" } });
    }

    function init(form) {
        form.addEventListener("submit", function (event) {
            event.preventDefault();
            show(form, "[data-form-success]", false);
            show(form, "[data-form-error]", false);

            var data = new FormData(form);
            // A filled-in hidden field means a bot; act as if it worked.
            if (data.get("company_website")) {
                form.reset();
                show(form, "[data-form-success]", true);
                return;
            }

            var button = form.querySelector('[type="submit"]');
            if (button) {
                button.disabled = true;
            }
            send(form, data)
                .then(function (response) {
                    if (!response.ok) {
                        throw new Error("The form could not be sent: " + response.status);
                    }
                    form.reset();
                    show(form, "[data-form-success]", true);
                })
                .catch(function () {
                    show(form, "[data-form-error]", true);
                })
                .then(function () {
                    if (button) {
                        button.disabled = false;
                    }
                });
        });
    }

    document.addEventListener("DOMContentLoaded", function () {
        // In a WordPress block theme the form is handled by WordPress.
        if (document.querySelector(".wp-site-blocks")) {
            return;
        }
        document.querySelectorAll("form[data-form]").forEach(init);
    });
})();
