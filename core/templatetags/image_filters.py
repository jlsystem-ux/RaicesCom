from django import template

# Create a library instance
register = template.Library()

def has_valid_extension(value):
    """
    Custom template filter to check if a file has a valid image extension
    """
    if not value:
        return False
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    return any(str(value).lower().endswith(ext) for ext in valid_extensions)

# Register the filter
register.filter('has_valid_extension', has_valid_extension)
