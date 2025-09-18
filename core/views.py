from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import Event, ContactMessage, StaffProfile
from .forms import ContactForm
from .services import TranslationService
from django.views.decorators.http import require_POST
import json
import logging

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