from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('api/events/', csrf_exempt(views.get_events), name='get_events'),
    path('events/', views.events_list, name='events_list'),
    path('api/translate/', views.translate_text, name='translate_text'),
]
