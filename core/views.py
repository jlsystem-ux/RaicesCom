from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import Event, ContactMessage, StaffProfile
from .forms import ContactForm
from .services import TranslationService
from django.views.decorators.http import require_POST
from django.template import loader
from django.urls import reverse
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
        return JsonResponse({'error': 'An error occurred while fetching events'}, status=500)

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
    staff_profiles = StaffProfile.objects.filter(
        is_active=True,
        show_on_contact_page=True
    ).order_by('display_order')

    context = {
        'form': form,
        'staff_profiles': staff_profiles,
    }
    return render(request, 'core/contact.html', context)

def sitemap(request):
    """Generate sitemap.xml for SEO"""
    template = loader.get_template('sitemap.xml')

    # Static URLs
    static_urls = [
        {
            'location': 'https://lurba1984.pythonanywhere.com/',
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'changefreq': 'weekly',
            'priority': '1.0'
        },
        {
            'location': 'https://lurba1984.pythonanywhere.com/contact/',
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'changefreq': 'monthly',
            'priority': '0.8'
        },
        {
            'location': 'https://lurba1984.pythonanywhere.com/events/',
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'changefreq': 'weekly',
            'priority': '0.9'
        }
    ]

    # Add multilingual versions
    multilingual_urls = []
    for url in static_urls:
        # Add English version
        en_url = url.copy()
        en_url['location'] = url['location'].replace('https://lurba1984.pythonanywhere.com/', 'https://lurba1984.pythonanywhere.com/en/')
        multilingual_urls.append(en_url)

        # Add Spanish version
        es_url = url.copy()
        es_url['location'] = url['location'].replace('https://lurba1984.pythonanywhere.com/', 'https://lurba1984.pythonanywhere.com/es/')
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