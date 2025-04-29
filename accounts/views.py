from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm

class SignUpView(FormView):
    template_name = 'accounts/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Registration was successful!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Please fix the existing errors!")
        return super().form_invalid(form)


class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, "Welcome!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "The username or password is incorrect.")
        return super().form_invalid(form)


class LogoutView(RedirectView):
    url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, "You have successfully logged out of your account.")
        return super().get(request, *args, **kwargs)
