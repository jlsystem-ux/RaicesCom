from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Event, ContactMessage

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 'title_en', 'title_es',
            'description', 'description_en', 'description_es',
            'date', 'location', 'online', 'meeting_link', 'image'
        ]
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Your full name')
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('your.email@example.com')
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Your phone number (optional)')
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Subject of your message')
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': _('Please describe how we can help you...')
            })
        }
        labels = {
            'name': _('Full Name'),
            'email': _('Email Address'),
            'phone': _('Phone Number'),
            'subject': _('Subject'),
            'message': _('Message')
        } 