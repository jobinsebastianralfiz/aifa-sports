from django.views.generic import ListView
from .models import Achievement


class AchievementListView(ListView):
    """Public achievements page."""
    model = Achievement
    template_name = 'frontend/achievements/list.html'
    context_object_name = 'achievements'
    paginate_by = 12

    def get_queryset(self):
        return Achievement.objects.filter(is_active=True).order_by('display_order', '-year')
