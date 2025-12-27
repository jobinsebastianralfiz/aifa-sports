"""
Custom context processors for the core app.
"""

from django.urls import reverse, NoReverseMatch


def navigation(request):
    """
    Provide consistent navigation items across all pages.
    """
    from apps.programs.models import Program

    # Define main navigation items
    nav_items = [
        {
            'name': 'Home',
            'url_name': 'frontend:home',
            'url': '/',
            'match_path': None,
            'match_url_name': 'home',
        },
        {
            'name': 'About',
            'url_name': 'frontend:about',
            'url': '/about/',
            'match_path': None,
            'match_url_name': 'about',
            'has_children': True,
            'children': [
                {'name': 'Our Story', 'url': '/about/#story', 'anchor': True},
                {'name': 'Mission & Vision', 'url': '/about/#mission-vision', 'anchor': True},
                {'name': 'Board of Directors', 'url': '/about/#board', 'anchor': True},
                {'name': 'Core Values', 'url': '/about/#values', 'anchor': True},
            ]
        },
        {
            'name': 'Community',
            'url_name': 'frontend:community',
            'url': '/community/',
            'match_path': None,
            'match_url_name': 'community',
        },
        {
            'name': 'Programs',
            'url_name': 'programs:list',
            'url': '/programs/',
            'match_path': 'programs',
            'match_url_name': None,
        },
        {
            'name': 'Our Team',
            'url_name': 'coaches:list',
            'url': '/coaches/',
            'match_path': 'coaches',
            'match_url_name': None,
        },
        {
            'name': 'Facilities',
            'url_name': 'facilities:list',
            'url': '/facilities/',
            'match_path': 'facilities',
            'match_url_name': None,
        },
        {
            'name': 'Achievements',
            'url_name': 'achievements:list',
            'url': '/achievements/',
            'match_path': 'achievements',
            'match_url_name': None,
        },
        {
            'name': 'Gallery',
            'url_name': 'gallery:list',
            'url': '/gallery/',
            'match_path': 'gallery',
            'match_url_name': None,
        },
        {
            'name': 'Contact',
            'url_name': 'frontend:contact',
            'url': '/contact/',
            'match_path': None,
            'match_url_name': 'contact',
        },
    ]

    # Resolve URLs and determine active state
    current_path = request.path
    current_url_name = None
    if request.resolver_match:
        current_url_name = request.resolver_match.url_name

    for item in nav_items:
        # Try to resolve URL
        try:
            item['url'] = reverse(item['url_name'])
        except NoReverseMatch:
            pass  # Keep default URL

        # Determine if this item is active
        item['is_active'] = False
        if item['match_url_name'] and current_url_name == item['match_url_name']:
            item['is_active'] = True
        elif item['match_path'] and item['match_path'] in current_path:
            item['is_active'] = True

    # Footer quick links (subset of main nav)
    footer_quick_links = [
        {'name': 'About Us', 'url_name': 'frontend:about'},
        {'name': 'Community', 'url_name': 'frontend:community'},
        {'name': 'Programs', 'url_name': 'programs:list'},
        {'name': 'Our Team', 'url_name': 'coaches:list'},
        {'name': 'Facilities', 'url_name': 'facilities:list'},
        {'name': 'Achievements', 'url_name': 'achievements:list'},
        {'name': 'Gallery', 'url_name': 'gallery:list'},
        {'name': 'Contact', 'url_name': 'frontend:contact'},
    ]

    for link in footer_quick_links:
        try:
            link['url'] = reverse(link['url_name'])
        except NoReverseMatch:
            link['url'] = '#'

    # Get programs for footer
    try:
        footer_programs = Program.objects.filter(status='active')[:5]
    except Exception:
        footer_programs = []

    return {
        'nav_items': nav_items,
        'footer_quick_links': footer_quick_links,
        'footer_programs': footer_programs,
    }


def site_settings(request):
    """
    Add site settings to template context.
    """
    from apps.core.models import SiteSettings

    try:
        settings = SiteSettings.get_settings()
    except Exception:
        settings = None

    return {
        'site_settings': settings,
    }


def page_content(request):
    """
    Add page-specific content to template context based on the current URL.
    """
    from apps.core.models import PageSettings, AboutPageContent, HomepageContent

    context = {}

    # Determine current page type from URL
    path = request.path.strip('/')
    page_type_map = {
        '': 'home',
        'about': 'about',
        'contact': 'contact',
        'programs': 'programs',
        'coaches': 'coaches',
        'events': 'events',
        'news': 'news',
        'gallery': 'gallery',
    }

    # Get the first path segment
    first_segment = path.split('/')[0] if path else ''
    current_page = page_type_map.get(first_segment)

    if current_page:
        try:
            context['page_settings'] = PageSettings.get_for_page(current_page)
        except Exception:
            context['page_settings'] = None

    # Add homepage content if on homepage
    if first_segment == '' or first_segment == 'home':
        try:
            context['homepage_content'] = HomepageContent.get_content()
            context['about_content'] = AboutPageContent.get_content()
        except Exception:
            context['homepage_content'] = None
            context['about_content'] = None

    # Add about page content if on about page
    if first_segment == 'about':
        try:
            context['about_content'] = AboutPageContent.get_content()
        except Exception:
            context['about_content'] = None

    return context
