# Splash enquiry forms

Contact uses the `lesson-enquiry` form. In Netlify, enable form detection and deploy the Pinegrow publish output. Check that the form appears in the Forms panel, set up the school's submission notifications and test a submission on the deployed site. [Netlify Forms setup](https://docs.netlify.com/manage/forms/setup/)

The optional **Private lesson enquiry form** in Insert is named `private-lesson-enquiry`. If you drop it onto a new page, include the shared `form/form.js` script as on Contact. Check that the form is detected and test it after deployment.

The `data-form-endpoint="netlify"` setting works on a Netlify subdomain and on a custom domain. Give each form a unique name and a matching hidden `form-name` value. Once the school has a confirmed email address or phone number, add that as a fallback in the form error message.
