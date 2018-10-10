from django.urls import reverse_lazy
from django.views import generic
from accounts import forms


class SignUp(generic.CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("accounts:login")
    template_name = 'accounts/signup.html'
