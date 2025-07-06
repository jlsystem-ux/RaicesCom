from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.conf import settings
import os

class Category(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    name_en = models.CharField(_('Name (English)'), max_length=100)
    name_es = models.CharField(_('Name (Spanish)'), max_length=100)
    description = models.TextField(_('Description'), blank=True)
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
    
    def __str__(self):
        return self.name

class Resource(models.Model):
    title = models.CharField(_('Title'), max_length=200)
    title_en = models.CharField(_('Title (English)'), max_length=200)
    title_es = models.CharField(_('Title (Spanish)'), max_length=200)
    description = models.TextField(_('Description'))
    description_en = models.TextField(_('Description (English)'))
    description_es = models.TextField(_('Description (Spanish)'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='resources')
    link = models.URLField(_('External Link'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Resource')
        verbose_name_plural = _('Resources')
    
    def __str__(self):
        return self.title

def event_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.title.lower().replace(' ', '_')}_{instance.id}.{ext}"
    return os.path.join('events', filename)

class Event(models.Model):
    title = models.CharField(_('Title'), max_length=200)
    title_en = models.CharField(_('Title (English)'), max_length=200)
    title_es = models.CharField(_('Title (Spanish)'), max_length=200)
    description = models.TextField(_('Description'))
    description_en = models.TextField(_('Description (English)'))
    description_es = models.TextField(_('Description (Spanish)'))
    date = models.DateTimeField(_('Date'))
    location = models.CharField(_('Location'), max_length=200)
    online = models.BooleanField(_('Online Event'), default=False)
    meeting_link = models.URLField(_('Meeting Link'), blank=True, null=True)
    image = models.ImageField(
        _('Image'),
        upload_to=event_image_path,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])],
        null=True,
        blank=True,
        help_text=_('Recommended size: 800x600 pixels')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def clean(self):
        if self.online and not self.meeting_link:
            raise ValidationError(_('Meeting link is required for online events.'))
        if not self.online and self.meeting_link:
            raise ValidationError(_('Meeting link should not be provided for in-person events.'))
    
    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        ordering = ['-date']
    
    def __str__(self):
        return self.title

    def get_image_url(self):
        if self.image and hasattr(self.image, 'url') and os.path.exists(self.image.path):
            return self.image.url
        return settings.STATIC_URL + 'img/default-event.jpg'

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_instance = Event.objects.get(pk=self.pk)
                if old_instance.image and old_instance.image != self.image:
                    if os.path.isfile(old_instance.image.path):
                        os.remove(old_instance.image.path)
            except Event.DoesNotExist:
                pass
        super().save(*args, **kwargs)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_language = models.CharField(
        _('Preferred Language'),
        max_length=2,
        choices=[('en', 'English'), ('es', 'Español')],
        default='es'
    )
    country_of_origin = models.CharField(_('Country of Origin'), max_length=100, blank=True)
    phone = models.CharField(_('Phone Number'), max_length=20, blank=True)
    
    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
