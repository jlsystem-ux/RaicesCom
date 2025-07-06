from django import forms
from .models import Event

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