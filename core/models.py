from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
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
    import uuid
    ext = filename.split('.')[-1]
    # Use UUID if id is None (new object), otherwise use id
    identifier = instance.id if instance.id else str(uuid.uuid4())[:8]
    safe_title = instance.title.lower().replace(' ', '_')[:30] if instance.title else 'event'
    filename = f"{safe_title}_{identifier}.{ext}"
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
        if self.image and hasattr(self.image, 'url'):
            try:
                # In production, don't check file existence as files are served by web server
                if settings.DEBUG:
                    # Only check file existence in development
                    if os.path.exists(self.image.path):
                        return self.image.url
                else:
                    # In production, trust that the file exists and return URL
                    return self.image.url
            except (ValueError, AttributeError):
                pass
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

class ContactMessage(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    email = models.EmailField(_('Email'))
    phone = models.CharField(_('Phone'), max_length=20, blank=True)
    subject = models.CharField(_('Subject'), max_length=200)
    message = models.TextField(_('Message'))
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(_('Read'), default=False)

    class Meta:
        verbose_name = _('Contact Message')
        verbose_name_plural = _('Contact Messages')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"

def staff_photo_path(instance, filename):
    """Generate path for staff photos"""
    ext = filename.split('.')[-1].lower()
    filename = f"{instance.name.lower().replace(' ', '_')}.{ext}"
    return os.path.join('staff', filename)

class StaffProfile(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    name_en = models.CharField(_('Name (English)'), max_length=100)
    name_es = models.CharField(_('Name (Spanish)'), max_length=100)
    title = models.CharField(_('Professional Title'), max_length=200)
    title_en = models.CharField(_('Title (English)'), max_length=200)
    title_es = models.CharField(_('Title (Spanish)'), max_length=200)
    bio = models.TextField(_('Biography'), blank=True)
    bio_en = models.TextField(_('Biography (English)'), blank=True)
    bio_es = models.TextField(_('Biography (Spanish)'), blank=True)

    # Contact Information
    phone = models.CharField(_('Phone'), max_length=20)
    email = models.EmailField(_('Email'))
    whatsapp = models.CharField(_('WhatsApp'), max_length=20, blank=True)

    # Social Media
    facebook = models.URLField(_('Facebook'), blank=True)
    twitter = models.URLField(_('Twitter'), blank=True)
    linkedin = models.URLField(_('LinkedIn'), blank=True)

    # Photo
    photo = models.ImageField(
        _('Profile Photo'),
        upload_to=staff_photo_path,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        null=True,
        blank=True,
        help_text=_('Recommended size: 300x300 pixels (square)')
    )

    # Display settings
    is_active = models.BooleanField(_('Active'), default=True)
    display_order = models.PositiveIntegerField(_('Display Order'), default=1)
    show_on_contact_page = models.BooleanField(_('Show on Contact Page'), default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Staff Profile')
        verbose_name_plural = _('Staff Profiles')
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name

    def get_photo_url(self):
        """Get photo URL or default avatar"""
        if self.photo and hasattr(self.photo, 'url'):
            try:
                # In production, don't check file existence as files are served by web server
                if settings.DEBUG:
                    # Only check file existence in development
                    if os.path.exists(self.photo.path):
                        return self.photo.url
                else:
                    # In production, trust that the file exists and return URL
                    return self.photo.url
            except (ValueError, AttributeError):
                pass
        return None

    def get_whatsapp_link(self):
        """Generate WhatsApp link"""
        if self.whatsapp:
            # Remove any non-numeric characters except +
            clean_number = ''.join(c for c in self.whatsapp if c.isdigit() or c == '+')
            return f"https://wa.me/{clean_number.replace('+', '')}"
        return None

def blog_image_path(instance, filename):
    """Generate path for blog post images"""
    ext = filename.split('.')[-1].lower()
    filename = f"blog_{instance.slug}_{instance.id}.{ext}"
    return os.path.join('blog', filename)

class BlogCategory(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    name_en = models.CharField(_('Name (English)'), max_length=100)
    name_es = models.CharField(_('Name (Spanish)'), max_length=100)
    slug = models.SlugField(unique=True)
    color = models.CharField(_('Color'), max_length=7, default='#4A90E2', help_text=_('Hex color code'))
    icon = models.CharField(_('Icon'), max_length=50, blank=True, help_text=_('FontAwesome icon class'))

    class Meta:
        verbose_name = _('Blog Category')
        verbose_name_plural = _('Blog Categories')
        ordering = ['name']

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    POST_TYPES = [
        ('news', _('News')),
        ('story', _('Community Story')),
        ('guide', _('Guide')),
        ('update', _('Update')),
    ]

    title = models.CharField(_('Title'), max_length=200)
    title_en = models.CharField(_('Title (English)'), max_length=200)
    title_es = models.CharField(_('Title (Spanish)'), max_length=200)
    slug = models.SlugField(unique=True)

    summary = models.TextField(_('Summary'), max_length=300)
    summary_en = models.TextField(_('Summary (English)'), max_length=300)
    summary_es = models.TextField(_('Summary (Spanish)'), max_length=300)

    content = models.TextField(_('Content'))
    content_en = models.TextField(_('Content (English)'))
    content_es = models.TextField(_('Content (Spanish)'))

    post_type = models.CharField(_('Post Type'), max_length=20, choices=POST_TYPES, default='news')
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')

    featured_image = models.ImageField(
        _('Featured Image'),
        upload_to=blog_image_path,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
        null=True,
        blank=True,
        help_text=_('Recommended size: 800x400 pixels')
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    is_published = models.BooleanField(_('Published'), default=False)
    is_featured = models.BooleanField(_('Featured'), default=False)

    published_date = models.DateTimeField(_('Published Date'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # SEO fields
    meta_description = models.TextField(_('Meta Description'), max_length=160, blank=True)
    meta_keywords = models.CharField(_('Meta Keywords'), max_length=255, blank=True)

    # Reading time estimation
    reading_time = models.PositiveIntegerField(_('Reading Time (minutes)'), default=5)

    class Meta:
        verbose_name = _('Blog Post')
        verbose_name_plural = _('Blog Posts')
        ordering = ['-published_date', '-created_at']
        indexes = [
            models.Index(fields=['is_published', '-published_date']),
            models.Index(fields=['post_type']),
            models.Index(fields=['is_featured']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.is_published and not self.published_date:
            self.published_date = timezone.now()
        elif not self.is_published:
            self.published_date = None
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/blog/{self.slug}/"

    def get_image_url(self):
        if self.featured_image and hasattr(self.featured_image, 'url'):
            try:
                # In production, don't check file existence as files are served by web server
                if settings.DEBUG:
                    # Only check file existence in development
                    if os.path.exists(self.featured_image.path):
                        return self.featured_image.url
                else:
                    # In production, trust that the file exists and return URL
                    return self.featured_image.url
            except (ValueError, AttributeError):
                pass
        return settings.STATIC_URL + 'img/default-blog.jpg'

    def get_reading_time(self):
        """Calculate estimated reading time based on content length"""
        import re
        word_count = len(re.findall(r'\w+', self.content))
        return max(1, round(word_count / 200))  # Average 200 words per minute

class Testimonial(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    country_of_origin = models.CharField(_('Country of Origin'), max_length=100)

    content = models.TextField(_('Testimonial'))
    content_en = models.TextField(_('Testimonial (English)'))
    content_es = models.TextField(_('Testimonial (Spanish)'))

    photo = models.ImageField(
        _('Photo'),
        upload_to='testimonials/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        null=True,
        blank=True,
        help_text=_('Optional photo (300x300 pixels recommended)')
    )

    is_featured = models.BooleanField(_('Featured'), default=False)
    is_published = models.BooleanField(_('Published'), default=True)
    consent_given = models.BooleanField(_('Consent Given'), default=False, help_text=_('Consent to publish story'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Testimonial')
        verbose_name_plural = _('Testimonials')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.country_of_origin}"

    def get_photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            try:
                # In production, don't check file existence as files are served by web server
                if settings.DEBUG:
                    # Only check file existence in development
                    if os.path.exists(self.photo.path):
                        return self.photo.url
                else:
                    # In production, trust that the file exists and return URL
                    return self.photo.url
            except (ValueError, AttributeError):
                pass
        return None
