"""
Programs app frontend views.
"""

from django.views.generic import ListView, DetailView
from .models import Program, Batch


class ProgramListView(ListView):
    """Public program listing."""
    model = Program
    template_name = 'frontend/programs/list.html'
    context_object_name = 'programs'
    paginate_by = 12

    def get_queryset(self):
        return Program.objects.filter(status='active').order_by('display_order', 'name')


class ProgramDetailView(DetailView):
    """Public program detail page."""
    model = Program
    template_name = 'frontend/programs/detail.html'
    context_object_name = 'program'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Program.objects.filter(status='active')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['batches'] = Batch.objects.filter(
            program=self.object,
            status='active'
        ).order_by('name')
        context['related_programs'] = Program.objects.filter(
            status='active'
        ).exclude(pk=self.object.pk)[:3]
        return context
