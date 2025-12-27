"""
Core app admin dashboard views.
"""

from django.views.generic import TemplateView, UpdateView, ListView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages

from apps.accounts.decorators import AdminRequiredMixin, SuperAdminRequiredMixin
from apps.programs.models import Program, Batch
from apps.coaches.models import Coach
from apps.gallery.models import GalleryImage
from apps.hero.models import HeroSlide
from apps.testimonials.models import Testimonial
from apps.contact.models import ContactMessage, Inquiry
from apps.events.models import Event, EventRegistration
from apps.news.models import News
from .models import SiteSettings, PageSettings, AboutPageContent, HomepageContent, BoardMember, CommunityActivity, CommunityPageContent
from .forms import SiteSettingsForm, PageSettingsForm, AboutPageContentForm, HomepageContentForm, BoardMemberForm, CommunityActivityForm, CommunityPageContentForm


class DashboardView(AdminRequiredMixin, TemplateView):
    """Admin dashboard home."""
    template_name = 'admin_dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Statistics for dashboard
        context['total_programs'] = Program.objects.filter(status='active').count()
        context['total_batches'] = Batch.objects.filter(status='active').count()
        context['total_coaches'] = Coach.objects.filter(status='active').count()
        context['upcoming_events'] = Event.objects.filter(status='upcoming').count()

        # Messages and Inquiries
        context['new_messages'] = ContactMessage.objects.filter(status='new').count()
        context['new_inquiries'] = Inquiry.objects.filter(status='new').count()

        # Registrations and Content
        context['total_registrations'] = EventRegistration.objects.count()
        context['total_posts'] = 0  # Blog posts if you have them
        context['total_news'] = News.objects.filter(status='published').count()

        # Recent items
        context['recent_messages'] = ContactMessage.objects.order_by('-created_at')[:5]
        context['recent_inquiries'] = Inquiry.objects.select_related('program').order_by('-created_at')[:5]
        context['recent_registrations'] = EventRegistration.objects.select_related('event').order_by('-created_at')[:5]

        # Legacy context (for backward compatibility)
        context['hero_count'] = HeroSlide.objects.filter(is_active=True).count()
        context['program_count'] = context['total_programs']
        context['coach_count'] = context['total_coaches']
        context['gallery_count'] = GalleryImage.objects.filter(is_active=True).count()
        context['testimonial_count'] = Testimonial.objects.filter(is_active=True).count()

        return context


class SettingsView(SuperAdminRequiredMixin, UpdateView):
    """Site settings view - Super Admin only."""
    template_name = 'admin_dashboard/settings.html'
    form_class = SiteSettingsForm
    success_url = reverse_lazy('admin_dashboard:settings')

    def get_object(self):
        return SiteSettings.get_settings()

    def form_valid(self, form):
        messages.success(self.request, 'Settings updated successfully!')
        return super().form_valid(form)


# Page Content Views
class PageContentIndexView(SuperAdminRequiredMixin, TemplateView):
    """Page content management overview."""
    template_name = 'admin_dashboard/page_content/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_settings'] = PageSettings.objects.all().order_by('page_type')
        context['about_content'] = AboutPageContent.get_content()
        context['homepage_content'] = HomepageContent.get_content()
        return context


class PageSettingsListView(SuperAdminRequiredMixin, TemplateView):
    """List all page settings."""
    template_name = 'admin_dashboard/page_content/page_settings_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_settings'] = PageSettings.objects.all().order_by('page_type')
        return context


class PageSettingsCreateView(SuperAdminRequiredMixin, TemplateView):
    """Create page settings."""
    template_name = 'admin_dashboard/page_content/page_settings_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PageSettingsForm()
        context['is_edit'] = False
        return context

    def post(self, request, *args, **kwargs):
        form = PageSettingsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Page settings created successfully!')
            return redirect('admin_dashboard:page_content:page-settings-list')
        return self.render_to_response(self.get_context_data(form=form))


class PageSettingsUpdateView(SuperAdminRequiredMixin, UpdateView):
    """Update page settings."""
    model = PageSettings
    form_class = PageSettingsForm
    template_name = 'admin_dashboard/page_content/page_settings_form.html'
    success_url = reverse_lazy('admin_dashboard:page_content:page-settings-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Page settings updated successfully!')
        return super().form_valid(form)


class AboutContentView(SuperAdminRequiredMixin, UpdateView):
    """About page content editor."""
    template_name = 'admin_dashboard/page_content/about_content_form.html'
    form_class = AboutPageContentForm
    success_url = reverse_lazy('admin_dashboard:page_content:index')

    def get_object(self):
        return AboutPageContent.get_content()

    def form_valid(self, form):
        messages.success(self.request, 'About page content updated successfully!')
        return super().form_valid(form)


class HomepageContentView(SuperAdminRequiredMixin, UpdateView):
    """Homepage content editor."""
    template_name = 'admin_dashboard/page_content/homepage_content_form.html'
    form_class = HomepageContentForm
    success_url = reverse_lazy('admin_dashboard:page_content:index')

    def get_object(self):
        return HomepageContent.get_content()

    def form_valid(self, form):
        messages.success(self.request, 'Homepage content updated successfully!')
        return super().form_valid(form)


# Board Member Views
class BoardMemberListView(AdminRequiredMixin, ListView):
    """Admin board member listing."""
    model = BoardMember
    template_name = 'admin_dashboard/board_members/list.html'
    context_object_name = 'board_members'
    paginate_by = 20

    def get_queryset(self):
        return BoardMember.objects.all().order_by('display_order', 'first_name')


class BoardMemberCreateView(AdminRequiredMixin, CreateView):
    """Create new board member."""
    model = BoardMember
    form_class = BoardMemberForm
    template_name = 'admin_dashboard/board_members/form.html'
    success_url = reverse_lazy('admin_dashboard:board_members:list')

    def form_valid(self, form):
        messages.success(self.request, 'Board member created successfully!')
        return super().form_valid(form)


class BoardMemberUpdateView(AdminRequiredMixin, UpdateView):
    """Update board member."""
    model = BoardMember
    form_class = BoardMemberForm
    template_name = 'admin_dashboard/board_members/form.html'
    success_url = reverse_lazy('admin_dashboard:board_members:list')

    def form_valid(self, form):
        messages.success(self.request, 'Board member updated successfully!')
        return super().form_valid(form)


class BoardMemberDeleteView(AdminRequiredMixin, DeleteView):
    """Delete board member."""
    model = BoardMember
    template_name = 'admin_dashboard/board_members/delete.html'
    success_url = reverse_lazy('admin_dashboard:board_members:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Board member deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Community Activity Views
class CommunityActivityListView(AdminRequiredMixin, ListView):
    """Admin community activity listing."""
    model = CommunityActivity
    template_name = 'admin_dashboard/community/list.html'
    context_object_name = 'activities'
    paginate_by = 20

    def get_queryset(self):
        return CommunityActivity.objects.all().order_by('-date', 'display_order')


class CommunityActivityCreateView(AdminRequiredMixin, CreateView):
    """Create new community activity."""
    model = CommunityActivity
    form_class = CommunityActivityForm
    template_name = 'admin_dashboard/community/form.html'
    success_url = reverse_lazy('admin_dashboard:community:list')

    def form_valid(self, form):
        messages.success(self.request, 'Community activity created successfully!')
        return super().form_valid(form)


class CommunityActivityUpdateView(AdminRequiredMixin, UpdateView):
    """Update community activity."""
    model = CommunityActivity
    form_class = CommunityActivityForm
    template_name = 'admin_dashboard/community/form.html'
    success_url = reverse_lazy('admin_dashboard:community:list')

    def form_valid(self, form):
        messages.success(self.request, 'Community activity updated successfully!')
        return super().form_valid(form)


class CommunityActivityDeleteView(AdminRequiredMixin, DeleteView):
    """Delete community activity."""
    model = CommunityActivity
    template_name = 'admin_dashboard/community/delete.html'
    success_url = reverse_lazy('admin_dashboard:community:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Community activity deleted successfully!')
        return super().delete(request, *args, **kwargs)


class CommunityPageContentView(SuperAdminRequiredMixin, UpdateView):
    """Community page content editor."""
    template_name = 'admin_dashboard/community/page_content_form.html'
    form_class = CommunityPageContentForm
    success_url = reverse_lazy('admin_dashboard:community:list')

    def get_object(self):
        return CommunityPageContent.get_content()

    def form_valid(self, form):
        messages.success(self.request, 'Community page content updated successfully!')
        return super().form_valid(form)
