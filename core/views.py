from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.contrib import messages
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from .models import Event, ContactMessage, StaffProfile, BlogPost, BlogCategory, Testimonial
from .forms import ContactForm
from .services import TranslationService
from django.views.decorators.http import require_POST
from django.template import loader
from django.urls import reverse
from django.db.models import Q
import json
import logging
from datetime import datetime

@ensure_csrf_cookie
def home(request):
    events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    return render(request, 'core/index.html', {'events': events})

def get_events(request):
    try:
        events = Event.objects.all()
        event_list = []
        for event in events:
            event_list.append({
                'title': event.title,
                'title_en': event.title_en,
                'title_es': event.title_es,
                'start': event.date.astimezone(timezone.get_current_timezone()).strftime('%Y-%m-%d %H:%M:%S'),
                'description': event.description,
                'description_en': event.description_en,
                'description_es': event.description_es,
                'location': event.location,
                'online': event.online,
            })
        return JsonResponse(event_list, safe=False)
    except Exception as e:
        logging.error(f"Error in get_events: {e}")
        return JsonResponse({'error': 'An error occurred while fetching events'}, status=500)

@ensure_csrf_cookie
def events_list(request):
    try:
        events = Event.objects.all().order_by('-date')
        return render(request, 'core/events_template.html', {'events': events})
    except Exception as e:
        logging.error(f"Error in events_list: {e}")
        # Return template with empty events instead of JSON error
        return render(request, 'core/events_template.html', {'events': [], 'error_message': 'Unable to load events at this time.'})

def translation_page(request):
    return render(request, 'translation.html')

@csrf_exempt
@require_POST
def translate_text(request):
    try:
        data = json.loads(request.body)
        text = data.get('text', '')
        # Accept either 'target_lang' or 'target_language' for flexibility
        target_lang = data.get('target_lang') or data.get('target_language')
        source_lang = data.get('source_lang', 'auto')
        if not text or not target_lang:
            return JsonResponse({'error': 'Missing text or target_lang'}, status=400)
        translator = TranslationService()
        translated_text = translator.translate_text(text, target_lang, source_lang)
        return JsonResponse({
            'translated_text': translated_text,
            'source_lang': source_lang,
            'target_lang': target_lang
        })
    except Exception as e:
        logging.error(f"Translation error: {e}")
        return JsonResponse({'error': str(e)}, status=500)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Thank you for your message! We will get back to you soon.'))
            return redirect('core:contact')
        else:
            messages.error(request, _('Please correct the errors below.'))
    else:
        form = ContactForm()

    # Get staff profiles to display on contact page
    try:
        staff_profiles = StaffProfile.objects.filter(
            is_active=True,
            show_on_contact_page=True
        ).order_by('display_order')
    except Exception as e:
        logging.error(f"Error fetching staff profiles: {e}")
        staff_profiles = []

    context = {
        'form': form,
        'staff_profiles': staff_profiles,
    }
    return render(request, 'core/contact.html', context)

def sitemap(request):
    """Generate sitemap.xml for SEO with dynamic event URLs"""
    from django.utils import timezone
    from .models import Event

    template = loader.get_template('sitemap.xml')
    base_domain = 'https://lurba1984.pythonanywhere.com'

    # Static URLs
    static_urls = [
        {
            'location': f'{base_domain}/',
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'changefreq': 'weekly',
            'priority': '1.0'
        },
        {
            'location': f'{base_domain}/contact/',
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'changefreq': 'monthly',
            'priority': '0.8'
        },
        {
            'location': f'{base_domain}/events/',
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'changefreq': 'daily',
            'priority': '0.9'
        }
    ]

    # Add dynamic event URLs (production-safe with error handling)
    try:
        # Only include upcoming and recent events (last 30 days)
        cutoff_date = timezone.now() - timezone.timedelta(days=30)
        events = Event.objects.filter(date__gte=cutoff_date).order_by('-date')[:50]  # Limit for performance

        for event in events:
            event_lastmod = event.updated_at.strftime('%Y-%m-%d') if hasattr(event, 'updated_at') and event.updated_at else event.date.strftime('%Y-%m-%d')
            static_urls.append({
                'location': f'{base_domain}/events/{event.pk}/',
                'lastmod': event_lastmod,
                'changefreq': 'weekly',
                'priority': '0.7'
            })
    except Exception:
        # Fail silently in production to avoid breaking sitemap
        pass

    # Add multilingual versions
    multilingual_urls = []
    for url in static_urls:
        # Add English version
        en_url = url.copy()
        en_url['location'] = url['location'].replace(base_domain, f'{base_domain}/en')
        multilingual_urls.append(en_url)

        # Add Spanish version
        es_url = url.copy()
        es_url['location'] = url['location'].replace(base_domain, f'{base_domain}/es')
        multilingual_urls.append(es_url)

    all_urls = static_urls + multilingual_urls

    context = {'urls': all_urls}
    return HttpResponse(template.render(context, request), content_type='application/xml')

def robots_txt(request):
    """Generate robots.txt for SEO"""
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /api/",
        "",
        "Sitemap: https://lurba1984.pythonanywhere.com/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

# Blog Views
def blog_list(request):
    """Display list of published blog posts with filtering and pagination"""
    posts = BlogPost.objects.filter(is_published=True)

    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    # Filter by post type
    post_type = request.GET.get('type')
    if post_type:
        posts = posts.filter(post_type=post_type)

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(title_en__icontains=search_query) |
            Q(title_es__icontains=search_query) |
            Q(summary__icontains=search_query) |
            Q(summary_en__icontains=search_query) |
            Q(summary_es__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(posts, 6)  # 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get categories for filter dropdown
    categories = BlogCategory.objects.all()

    # Get featured posts for sidebar
    featured_posts = BlogPost.objects.filter(is_published=True, is_featured=True)[:3]

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'featured_posts': featured_posts,
        'current_category': category_slug,
        'current_type': post_type,
        'search_query': search_query,
        'post_types': BlogPost.POST_TYPES,
    }
    return render(request, 'core/blog_list.html', context)

def blog_detail(request, slug):
    """Display individual blog post"""
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)

    # Get related posts (same category, exclude current post)
    related_posts = BlogPost.objects.filter(
        category=post.category,
        is_published=True
    ).exclude(id=post.id)[:3]

    # If no related posts in same category, get recent posts
    if not related_posts:
        related_posts = BlogPost.objects.filter(
            is_published=True
        ).exclude(id=post.id)[:3]

    context = {
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'core/blog_detail.html', context)

def testimonials_list(request):
    """Display list of published testimonials"""
    testimonials = Testimonial.objects.filter(is_published=True, consent_given=True)

    # Get featured testimonials first
    featured_testimonials = testimonials.filter(is_featured=True)
    regular_testimonials = testimonials.filter(is_featured=False)

    context = {
        'featured_testimonials': featured_testimonials,
        'regular_testimonials': regular_testimonials,
    }
    return render(request, 'core/testimonials.html', context)