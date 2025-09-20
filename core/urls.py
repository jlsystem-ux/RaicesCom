from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('api/events/', views.get_events, name='get_events'),
    path('events/', views.events_list, name='events_list'),
    path('api/translate/', views.translate_text, name='translate_text'),
    path('contact/', views.contact, name='contact'),

    # Blog URLs
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('testimonials/', views.testimonials_list, name='testimonials'),
]
