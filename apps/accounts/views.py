"""
Accounts app views - Authentication.
"""

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy


class CustomLoginView(LoginView):
    """Custom login view with admin dashboard template."""
    template_name = 'admin_html/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('admin_dashboard:index')


class ProfileView(LoginRequiredMixin, TemplateView):
    """User profile view."""
    template_name = 'accounts/profile.html'
