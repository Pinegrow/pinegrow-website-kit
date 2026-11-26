# Enquiry forms

This kit has two static HTML forms. The Visit us page uses `visit-enquiry` and the Kids and parties page uses `party-enquiry`.

In Netlify, enable form detection and deploy the published site. Check that both names appear in the Forms panel. Set up the gym’s submission notifications, then test both forms on the deployed site. [Netlify Forms setup](https://docs.netlify.com/manage/forms/setup/)

The shared script submits to the current site when the form’s `data-form-endpoint` is set to `netlify`. That setting also works on a custom domain. Each Netlify form needs a unique name and a matching hidden `form-name` value.
