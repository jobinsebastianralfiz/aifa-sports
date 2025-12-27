"""
Core app frontend views - Public pages.
"""

from django.views.generic import TemplateView, FormView
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from apps.programs.models import Program, Batch
from apps.coaches.models import Coach
from apps.hero.models import HeroSlide
from apps.testimonials.models import Testimonial
from apps.news.models import News
from apps.events.models import Event
from apps.blog.models import BlogPost
from apps.gallery.models import GalleryImage
from apps.contact.models import ContactMessage
from apps.contact.forms import ContactForm
from apps.core.models import AboutPageContent, HomepageContent, SiteSettings, BoardMember, CommunityActivity, CommunityPageContent
from apps.achievements.models import Achievement
from apps.accreditations.models import Accreditation
from apps.facilities.models import Facility


class HomeView(TemplateView):
    """Homepage view."""
    template_name = 'frontend/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hero_slides'] = HeroSlide.objects.filter(is_active=True).order_by('display_order')
        context['programs'] = Program.objects.filter(status='active', is_featured=True)[:6]
        context['coaches'] = Coach.objects.filter(status='active', show_on_website=True)[:4]
        context['testimonials'] = Testimonial.objects.filter(is_active=True, is_featured=True)[:6]
        context['gallery_images'] = GalleryImage.objects.filter(is_active=True)[:8]
        context['news'] = News.objects.filter(status='published', show_on_homepage=True)[:3]
        context['upcoming_events'] = Event.objects.filter(status='upcoming', show_on_homepage=True)[:3]
        context['recent_posts'] = BlogPost.objects.filter(status='published')[:3]
        # Add page content
        context['homepage_content'] = HomepageContent.get_content()
        context['about_content'] = AboutPageContent.get_content()
        # Add achievements and accreditations
        context['achievements'] = Achievement.objects.filter(is_active=True, show_on_homepage=True).order_by('display_order')[:6]
        context['accreditations'] = Accreditation.objects.filter(is_active=True, show_on_homepage=True).order_by('display_order')[:8]
        # Add facilities
        context['facilities'] = Facility.objects.filter(is_active=True, show_on_homepage=True).select_related('category').order_by('display_order')[:6]
        return context


class AboutView(TemplateView):
    """About page view."""
    template_name = 'frontend/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board_members'] = BoardMember.objects.filter(show_on_website=True)
        context['testimonials'] = Testimonial.objects.filter(is_active=True)[:6]
        # Add page content
        context['about_content'] = AboutPageContent.get_content()
        return context


class CommunityView(TemplateView):
    """Community Outreach & Charity page view."""
    template_name = 'frontend/community.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activities'] = CommunityActivity.objects.filter(show_on_website=True)
        context['featured_activities'] = CommunityActivity.objects.filter(show_on_website=True, is_featured=True)[:3]
        context['page_content'] = CommunityPageContent.get_content()
        return context


class ContactView(FormView):
    """Contact page with form."""
    template_name = 'frontend/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('frontend:contact')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Thank you for your message! We will get back to you soon.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


@method_decorator(csrf_exempt, name='dispatch')
class ChatbotAPIView(View):
    """API endpoint for chatbot responses using database data."""

    def get(self, request):
        topic = request.GET.get('topic', '').lower()
        query = request.GET.get('query', '').lower()

        # Determine topic from query if not specified
        if not topic and query:
            topic = self._detect_topic(query)

        response_data = self._get_response(topic, query)
        return JsonResponse(response_data)

    def post(self, request):
        import json
        try:
            data = json.loads(request.body)
            topic = data.get('topic', '').lower()
            query = data.get('query', '').lower()
        except json.JSONDecodeError:
            topic = request.POST.get('topic', '').lower()
            query = request.POST.get('query', '').lower()

        if not topic and query:
            topic = self._detect_topic(query)

        response_data = self._get_response(topic, query)
        return JsonResponse(response_data)

    def _detect_topic(self, query):
        """Detect topic from user query."""
        topic_keywords = {
            'programs': ['program', 'course', 'training', 'class', 'learn', 'academy'],
            'fees': ['fee', 'cost', 'price', 'payment', 'charge', 'amount', 'money'],
            'timings': ['time', 'timing', 'schedule', 'hour', 'when', 'batch', 'slot'],
            'contact': ['contact', 'phone', 'email', 'address', 'location', 'reach', 'call', 'where'],
            'trial': ['trial', 'demo', 'free', 'try', 'book', 'register', 'join', 'admission', 'enroll'],
            'coaches': ['coach', 'trainer', 'staff', 'instructor', 'team', 'teacher'],
            'facilities': ['facility', 'ground', 'field', 'equipment', 'infrastructure', 'turf', 'gym'],
            'events': ['event', 'tournament', 'match', 'competition', 'upcoming'],
            'achievements': ['achievement', 'trophy', 'award', 'won', 'champion', 'success'],
            'greeting': ['hi', 'hello', 'hey', 'good morning', 'good evening', 'namaste', 'hii'],
            'thanks': ['thank', 'thanks', 'thx', 'appreciate'],
        }

        for topic, keywords in topic_keywords.items():
            if any(keyword in query for keyword in keywords):
                return topic

        return 'default'

    def _get_response(self, topic, query):
        """Get response based on topic."""
        site_settings = SiteSettings.get_settings()

        handlers = {
            'programs': self._get_programs_response,
            'fees': self._get_fees_response,
            'timings': self._get_timings_response,
            'contact': self._get_contact_response,
            'trial': self._get_trial_response,
            'coaches': self._get_coaches_response,
            'facilities': self._get_facilities_response,
            'events': self._get_events_response,
            'achievements': self._get_achievements_response,
            'greeting': self._get_greeting_response,
            'thanks': self._get_thanks_response,
        }

        handler = handlers.get(topic, self._get_default_response)
        return handler(site_settings)

    def _get_programs_response(self, site_settings):
        """Get programs information."""
        programs = Program.objects.filter(status='active').order_by('display_order')[:6]

        if not programs.exists():
            return {
                'success': True,
                'message': "We offer various football training programs for all age groups. Please contact us for the latest program details!",
                'topic': 'programs'
            }

        program_list = []
        for p in programs:
            program_list.append(f"⚽ <b>{p.name}</b> ({p.age_group}) - {p.short_description}")

        message = "We offer the following training programs:\n\n"
        message += "\n".join(program_list)
        message += "\n\nWould you like to know more about any specific program?"

        return {
            'success': True,
            'message': message,
            'topic': 'programs',
            'data': [{'name': p.name, 'age_group': p.age_group, 'slug': p.slug} for p in programs]
        }

    def _get_fees_response(self, site_settings):
        """Get fee structure."""
        programs = Program.objects.filter(status='active').order_by('display_order')[:6]

        if not programs.exists():
            return {
                'success': True,
                'message': "Please contact us for our current fee structure and any available discounts!",
                'topic': 'fees'
            }

        fee_list = []
        for p in programs:
            fee_list.append(f"💰 <b>{p.name}:</b> ₹{p.fee_amount:,.0f}/{p.fee_period}")

        message = "Our fee structure:\n\n"
        message += "\n".join(fee_list)
        message += "\n\n✨ Contact us for family discounts and payment plans!"

        return {
            'success': True,
            'message': message,
            'topic': 'fees'
        }

    def _get_timings_response(self, site_settings):
        """Get training timings."""
        batches = Batch.objects.filter(status='active').select_related('program')[:8]

        if not batches.exists():
            message = """Our training schedule:\n
🕐 <b>Morning Batch:</b> 6:00 AM - 8:00 AM
🕐 <b>Evening Batch:</b> 4:00 PM - 6:00 PM
🕐 <b>Weekend Special:</b> 7:00 AM - 10:00 AM

📅 Training days: Monday to Saturday

Contact us for specific batch timings!"""
        else:
            timing_list = []
            for b in batches:
                timing_list.append(f"🕐 <b>{b.program.name} - {b.name}:</b> {b.schedule}")

            message = "Our current training batches:\n\n"
            message += "\n".join(timing_list)
            message += "\n\nWhich batch timing suits you best?"

        return {
            'success': True,
            'message': message,
            'topic': 'timings'
        }

    def _get_contact_response(self, site_settings):
        """Get contact information."""
        message = "You can reach us at:\n\n"

        if site_settings.phone:
            message += f"📞 <b>Phone:</b> {site_settings.phone}\n"
        if site_settings.email:
            message += f"📧 <b>Email:</b> {site_settings.email}\n"
        if site_settings.address:
            message += f"📍 <b>Location:</b> {site_settings.address}\n"
        if site_settings.whatsapp:
            message += f"💬 <b>WhatsApp:</b> {site_settings.whatsapp}\n"

        message += "\n🕐 <b>Office Hours:</b>\nMon-Sat: 9 AM - 7 PM\nSunday: 9 AM - 1 PM"
        message += '\n\nOr visit our <a href="/contact/" style="color: var(--primary)">Contact Page</a>!'

        return {
            'success': True,
            'message': message,
            'topic': 'contact',
            'data': {
                'phone': site_settings.phone,
                'email': site_settings.email,
                'address': site_settings.address,
                'whatsapp': site_settings.whatsapp
            }
        }

    def _get_trial_response(self, site_settings):
        """Get trial booking information."""
        message = """Great choice! We offer FREE trial sessions! 🎉

To book your trial:

1️⃣ Fill our contact form
2️⃣ Choose your preferred date
3️⃣ Bring comfortable sports wear
4️⃣ Arrive 15 mins early

<a href="/contact/" style="color: var(--primary); font-weight: bold;">👉 Book Your Free Trial Now!</a>"""

        if site_settings.phone:
            message += f"\n\nOr call us directly at {site_settings.phone}"

        return {
            'success': True,
            'message': message,
            'topic': 'trial'
        }

    def _get_coaches_response(self, site_settings):
        """Get coaches information."""
        coaches = Coach.objects.filter(status='active', show_on_website=True).order_by('display_order')[:6]

        if not coaches.exists():
            message = """Our coaching team includes:

🏆 UEFA Licensed coaches
🏆 Former professional players
🏆 Sports science specialists
🏆 Certified fitness trainers

All coaches undergo regular training and background verification."""
        else:
            coach_list = []
            for c in coaches:
                coach_list.append(f"🏆 <b>{c.full_name}</b> - {c.designation} ({c.experience_years} yrs exp)")

            message = "Meet our expert coaching team:\n\n"
            message += "\n".join(coach_list)

        message += '\n\n<a href="/our-team/" style="color: var(--primary);">View Full Team →</a>'

        return {
            'success': True,
            'message': message,
            'topic': 'coaches',
            'data': [{'name': c.full_name, 'designation': c.designation} for c in coaches] if coaches.exists() else []
        }

    def _get_facilities_response(self, site_settings):
        """Get facilities information."""
        facilities = Facility.objects.filter(is_active=True).order_by('display_order')[:6]

        if not facilities.exists():
            message = """Our world-class facilities include:

🏟️ FIFA-standard football turf
🏋️ Modern gym & fitness center
🎥 Video analysis room
🚿 Changing rooms & showers
☕ Cafeteria
🅿️ Ample parking space"""
        else:
            facility_list = []
            for f in facilities:
                desc = f.short_description or f.name
                facility_list.append(f"🏟️ <b>{f.name}</b> - {desc}")

            message = "Our facilities:\n\n"
            message += "\n".join(facility_list)

        message += '\n\n<a href="/facilities/" style="color: var(--primary);">View All Facilities →</a>'

        return {
            'success': True,
            'message': message,
            'topic': 'facilities'
        }

    def _get_events_response(self, site_settings):
        """Get upcoming events."""
        events = Event.objects.filter(status='upcoming').order_by('start_date')[:5]

        if not events.exists():
            message = "No upcoming events at the moment. Stay tuned for exciting tournaments and competitions!"
        else:
            event_list = []
            for e in events:
                date_str = e.start_date.strftime('%d %b %Y') if e.start_date else ''
                event_list.append(f"📅 <b>{e.title}</b> - {date_str}")

            message = "Upcoming events:\n\n"
            message += "\n".join(event_list)

        message += '\n\n<a href="/events/" style="color: var(--primary);">View All Events →</a>'

        return {
            'success': True,
            'message': message,
            'topic': 'events'
        }

    def _get_achievements_response(self, site_settings):
        """Get achievements information."""
        achievements = Achievement.objects.filter(is_active=True).order_by('-year', 'display_order')[:6]

        if not achievements.exists():
            message = """Our academy has a proud history of achievements:

🏆 Multiple district championships
🏆 State-level tournament winners
🏆 Players selected for professional teams
🏆 Youth development excellence awards"""
        else:
            achievement_list = []
            for a in achievements:
                achievement_list.append(f"🏆 <b>{a.title}</b> ({a.year})")

            message = "Our achievements:\n\n"
            message += "\n".join(achievement_list)

        message += '\n\n<a href="/achievements/" style="color: var(--primary);">View All Achievements →</a>'

        return {
            'success': True,
            'message': message,
            'topic': 'achievements'
        }

    def _get_greeting_response(self, site_settings):
        """Get greeting response."""
        site_name = site_settings.site_name or "AIFA Football Academy"
        message = f"""Hello! 👋 Welcome to {site_name}!

I'm here to help you with information about:
• Our training programs
• Fee structure
• Training timings
• Booking a free trial

How can I assist you today?"""

        return {
            'success': True,
            'message': message,
            'topic': 'greeting'
        }

    def _get_thanks_response(self, site_settings):
        """Get thanks response."""
        return {
            'success': True,
            'message': """You're welcome! 😊

Is there anything else I can help you with?

Feel free to ask about our programs, fees, or book a free trial session!""",
            'topic': 'thanks'
        }

    def _get_default_response(self, site_settings):
        """Get default response."""
        return {
            'success': True,
            'message': """I'm not sure I understood that. 🤔

I can help you with:
• Training programs
• Fee structure
• Training timings
• Contact information
• Booking a free trial
• Our coaches & facilities

Please try asking about one of these topics!""",
            'topic': 'default'
        }
