from django.forms import Form
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.contrib import messages
from django import forms
from django.utils.translation import gettext as _


class clientdetailsform(Form):
    first_name = forms.CharField(label=_('Your Name'), max_length=100)
    email = forms.EmailField(label=_('Your Email'))


class UpdateClientDetailsFormView(LoginRequiredMixin, FormView):
    template_name = 'my_enhanced_template.html'
    form_class = clientdetailsform
    success_url = '/successs/'

    def form_valid(self, form:clientdetailsform):
        # Get the name and email from the form
        name = self.request.POST.get('name', None)
        email = self.request.POST.get('email', None)

        # Create and save a new Client object with the name and email
        if name:
            Client.objects.create(name=name, email=email)

            # Set a success message
            messages.success(self.request, "Your details were saved successfully!")
        else:
            messages.warning(self.request, "You did not fill in any information!")
        # Redirect to the specified success URL
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = {}
        context['user_greeting'] = _(f'Hello, {self.request.user.username}!')
        return context

    def form_invalid(self, form):
        return super().form_invalid(form)