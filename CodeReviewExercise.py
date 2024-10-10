from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect


class FormView:
    """Render a form on GET and processes it on POST."""

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_form(self):
        """Return an instance of the form to be used in this view."""
        return self.form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""

        if self.request.method in ("POST", "PUT"):
            return {
                "data": self.request.POST,
                "files": self.request.FILES,
            }

        return {}

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")
        return str(self.success_url)  # success_url may be lazy

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if "form" not in kwargs:
            kwargs["form"] = self.get_form()
        return super().get_context_data(**kwargs)
