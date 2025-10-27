# Django Template Debugging Guide

## 🐛 Template Debugging Methods

### 1. **Template Debugging in Views**
Add breakpoints in your views where templates are rendered:

```python
# movies/views.py
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["movies"] = Movie.objects.all().order_by("title")
    
    # 🐛 DEBUG: Inspect context before template rendering
    import pdb; pdb.set_trace()  # Breakpoint here
    
    return context
```

### 2. **Template Context Debugging**
Use Django's built-in template debugging:

```python
# In your views, add debug information
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["movies"] = Movie.objects.all().order_by("title")
    
    # Debug context variables
    context["debug_context"] = {
        "movies_count": context["movies"].count(),
        "user": self.request.user if hasattr(self.request, 'user') else None,
        "request_method": self.request.method,
    }
    
    return context
```

### 3. **Template Debug Tags**
Add debug information directly in templates:

```html
<!-- In your templates -->
{% load debug_tags %}

<!-- Debug all context variables -->
{% debug %}

<!-- Debug specific variables -->
{% debug movies %}
{% debug request.user %}
```

### 4. **Custom Template Debug Filter**
Create a custom template filter for debugging:

```python
# movies/templatetags/debug_tags.py
from django import template
import json
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def debug(var):
    """Debug template variable"""
    return mark_safe(f"<pre>{json.dumps(var, indent=2, default=str)}</pre>")

@register.filter
def debug_type(var):
    """Get the type of a variable"""
    return type(var).__name__

@register.filter
def debug_attrs(var):
    """Get attributes of an object"""
    if hasattr(var, '__dict__'):
        return var.__dict__
    return "No attributes"
```

### 5. **Template Error Debugging**
Enable detailed template error messages in settings:

```python
# demo_tables/settings.py
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",  # ← Important!
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "debug": DEBUG,  # ← Enable template debugging
        },
    },
]
```

### 6. **Browser Developer Tools**
Use browser dev tools to inspect rendered HTML:

- **F12** - Open Developer Tools
- **Elements tab** - Inspect HTML structure
- **Console tab** - Check for JavaScript errors
- **Network tab** - Monitor template loading

### 7. **Template Inheritance Debugging**
Debug template inheritance issues:

```html
<!-- In base template -->
{% block content %}
    <!-- Debug template name -->
    <div style="display: none;">
        Template: {{ template_name|default:"Unknown" }}
        Block: {% block.super %}
    </div>
{% endblock %}
```

### 8. **Static Files Debugging**
Debug static file loading:

```python
# settings.py
STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Debug static files
if DEBUG:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
```

## 🔧 VS Code Template Debugging Setup

### 1. **Install Django Extension**
- Install "Django" extension in VS Code
- Install "HTML CSS Support" extension

### 2. **Template Syntax Highlighting**
Add to VS Code settings:

```json
{
    "files.associations": {
        "*.html": "django-html"
    },
    "emmet.includeLanguages": {
        "django-html": "html"
    }
}
```

### 3. **Template Breakpoints**
Set breakpoints in views that render templates:

```python
# Set breakpoint here before template rendering
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    # 🐛 Breakpoint here
    context["movies"] = Movie.objects.all()
    return context
```

## 🚀 Quick Template Debugging Steps

1. **Start VS Code debugger** (F5)
2. **Set breakpoint** in view method
3. **Visit the page** in browser
4. **Inspect context variables** in debugger
5. **Step through** template rendering
6. **Check browser** for rendered output

## 📝 Common Template Debugging Scenarios

### Debug Template Variables
```html
<!-- Check if variable exists -->
{% if movies %}
    Movies found: {{ movies.count }}
{% else %}
    No movies in context
{% endif %}
```

### Debug Template Filters
```html
<!-- Test template filters -->
{{ movies|length }}
{{ movies|first }}
{{ movies|slice:":5" }}
```

### Debug Template Tags
```html
<!-- Test template tags -->
{% for movie in movies %}
    {{ forloop.counter }}: {{ movie.title }}
{% empty %}
    No movies to display
{% endfor %}
```

## 🎯 Pro Tips

1. **Use `{% debug %}` tag** for quick context inspection
2. **Enable template debugging** in settings
3. **Use browser dev tools** for CSS/JS debugging
4. **Set breakpoints in views** before template rendering
5. **Use `{% load debug_tags %}`** for custom debugging
6. **Check Django logs** for template errors
7. **Use `{% comment %}` tags** for temporary debugging code
