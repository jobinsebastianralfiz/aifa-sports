"""
Custom decorators for permission checking.
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    """Require Super Admin or Staff login."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Please login to access this page.")
            return redirect('accounts:login')
        if not hasattr(request.user, 'profile'):
            messages.error(request, "Access denied.")
            return redirect('frontend:home')
        return view_func(request, *args, **kwargs)
    return wrapper


def super_admin_required(view_func):
    """Require Super Admin login."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not hasattr(request.user, 'profile') or not request.user.profile.is_super_admin():
            messages.error(request, "Super Admin access required.")
            return redirect('admin_dashboard:index')
        return view_func(request, *args, **kwargs)
    return wrapper


class AdminRequiredMixin:
    """Mixin for class-based views requiring admin access."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Please login to access this page.")
            return redirect('accounts:login')
        if not request.user.is_staff and not hasattr(request.user, 'profile'):
            messages.error(request, "Access denied.")
            return redirect('frontend:home')
        return super().dispatch(request, *args, **kwargs)


class SuperAdminRequiredMixin:
    """Mixin for class-based views requiring super admin access."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not hasattr(request.user, 'profile') or not request.user.profile.is_super_admin():
            messages.error(request, "Super Admin access required.")
            return redirect('admin_dashboard:index')
        return super().dispatch(request, *args, **kwargs)
