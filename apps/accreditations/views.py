from django.views.generic import ListView
from .models import Accreditation


class AccreditationListView(ListView):
    """Public accreditations page."""
    model = Accreditation
    template_name = 'frontend/accreditations/list.html'
    context_object_name = 'accreditations'
    paginate_by = 12

    def get_queryset(self):
        return Accreditation.objects.filter(is_active=True).order_by('display_order')
