from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from .models import Event
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