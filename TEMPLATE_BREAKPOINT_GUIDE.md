# Template Breakpoint Methods for Django

## 🐛 Method 1: Template Debug Tags with Conditional Breakpoints

Create template tags that act as breakpoints:

```python
# movies/templatetags/debug_tags.py
@register.simple_tag(takes_context=True)
def breakpoint(context, condition=True, message="Template breakpoint"):
    """
    Template breakpoint that can be triggered conditionally.
    Usage: {% breakpoint %} or {% breakpoint condition message %}
    """
    if condition:
        # This will cause an exception that stops template rendering
        raise Exception(f"TEMPLATE BREAKPOINT: {message}")
    return ""

@register.simple_tag(takes_context=True)
def debug_breakpoint(context, var_name=None, condition=True):
    """
    Debug breakpoint that shows variable info before stopping.
    Usage: {% debug_breakpoint 'movies' %}
    """
    if condition:
        if var_name:
            # Get variable value
            value = None
            if hasattr(context, 'dicts'):
                for context_dict in context.dicts:
                    if hasattr(context_dict, 'get') and var_name in context_dict:
                        value = context_dict[var_name]
                        break
            
            raise Exception(f"TEMPLATE DEBUG BREAKPOINT: {var_name} = {value} (type: {type(value).__name__})")
        else:
            raise Exception("TEMPLATE DEBUG BREAKPOINT: No variable specified")
    return ""
```

## 🐛 Method 2: Template Exception Breakpoints

Use Django's template error handling to create breakpoints:

```python
# movies/templatetags/debug_tags.py
@register.simple_tag(takes_context=True)
def template_breakpoint(context, message="Breakpoint hit"):
    """
    Template breakpoint using exception.
    Usage: {% template_breakpoint "Custom message" %}
    """
    # This will stop template rendering and show the exception
    raise TemplateSyntaxError(f"BREAKPOINT: {message}")

@register.simple_tag(takes_context=True)
def conditional_breakpoint(context, condition, message="Conditional breakpoint"):
    """
    Conditional template breakpoint.
    Usage: {% conditional_breakpoint movies.count > 5 "Too many movies" %}
    """
    if condition:
        raise TemplateSyntaxError(f"CONDITIONAL BREAKPOINT: {message}")
    return ""
```

## 🐛 Method 3: VS Code Template Breakpoints

Configure VS Code to break on template rendering:

```json
// .vscode/launch.json
{
    "name": "Django: Template Debug",
    "type": "python",
    "request": "launch",
    "program": "${workspaceFolder}/manage.py",
    "args": ["runserver", "127.0.0.1:8000", "--noreload"],
    "django": true,
    "console": "integratedTerminal",
    "justMyCode": false,
    "env": {
        "DJANGO_SETTINGS_MODULE": "demo_tables.settings"
    },
    "cwd": "${workspaceFolder}",
    "stopOnEntry": false,
    "showReturnValue": true,
    "breakOnSystemExit": true
}
```

## 🐛 Method 4: Custom Template Node Breakpoints

Create custom template nodes that act as breakpoints:

```python
# movies/templatetags/debug_tags.py
from django.template import Node, TemplateSyntaxError

class BreakpointNode(Node):
    def __init__(self, condition, message):
        self.condition = condition
        self.message = message
    
    def render(self, context):
        # Evaluate condition
        if self.condition:
            # This will stop template rendering
            raise Exception(f"TEMPLATE BREAKPOINT: {self.message}")
        return ""

@register.tag
def breakpoint(parser, token):
    """
    Template breakpoint tag.
    Usage: {% breakpoint "message" %}
    """
    try:
        tag_name, message = token.split_contents()
    except ValueError:
        message = "Template breakpoint"
    
    return BreakpointNode(True, message)
```

## 🐛 Method 5: JavaScript Template Breakpoints

Use JavaScript breakpoints in templates:

```html
<!-- In your template -->
<script>
    // JavaScript breakpoint
    debugger; // This will break in browser dev tools
    
    // Conditional JavaScript breakpoint
    {% if movies.count > 10 %}
        console.log("Too many movies, breaking...");
        debugger;
    {% endif %}
    
    // Variable inspection
    console.log("Movies count:", {{ movies.count }});
    debugger; // Break here to inspect
</script>
```

## 🐛 Method 6: Django Debug Toolbar Integration

Use Django Debug Toolbar for template debugging:

```python
# settings.py
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    
    INTERNAL_IPS = ['127.0.0.1']
```

## 🐛 Method 7: Template Logging Breakpoints

Use logging to create breakpoints:

```python
# movies/templatetags/debug_tags.py
import logging

logger = logging.getLogger(__name__)

@register.simple_tag(takes_context=True)
def log_breakpoint(context, message="Template breakpoint"):
    """
    Logging breakpoint for template debugging.
    Usage: {% log_breakpoint "Custom message" %}
    """
    logger.error(f"TEMPLATE BREAKPOINT: {message}")
    # This will show in Django logs
    return f"<!-- BREAKPOINT: {message} -->"
```

## 🐛 Method 8: Template Variable Inspection

Create template tags for variable inspection:

```python
# movies/templatetags/debug_tags.py
@register.simple_tag(takes_context=True)
def inspect_var(context, var_name, stop=False):
    """
    Inspect template variable and optionally stop.
    Usage: {% inspect_var 'movies' %} or {% inspect_var 'movies' stop %}
    """
    # Get variable value
    value = None
    if hasattr(context, 'dicts'):
        for context_dict in context.dicts:
            if hasattr(context_dict, 'get') and var_name in context_dict:
                value = context_dict[var_name]
                break
    
    if stop:
        raise Exception(f"INSPECT BREAKPOINT: {var_name} = {value}")
    
    return f"<!-- INSPECT: {var_name} = {value} -->"
```

## 🚀 Usage Examples

### In Templates:
```html
<!-- Method 1: Simple breakpoint -->
{% breakpoint "Stopping here" %}

<!-- Method 2: Conditional breakpoint -->
{% if movies.count > 5 %}
    {% breakpoint "Too many movies" %}
{% endif %}

<!-- Method 3: Variable inspection breakpoint -->
{% debug_breakpoint 'movies' %}

<!-- Method 4: JavaScript breakpoint -->
<script>debugger;</script>

<!-- Method 5: Logging breakpoint -->
{% log_breakpoint "Template rendering stopped" %}
```

### In Views (for template breakpoints):
```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["movies"] = Movie.objects.all()
    
    # Set breakpoint before template rendering
    import pdb; pdb.set_trace()
    
    return context
```

## 🎯 Best Practices

1. **Use conditional breakpoints** to avoid stopping on every request
2. **Combine with VS Code debugger** for full debugging experience
3. **Use JavaScript breakpoints** for frontend debugging
4. **Log breakpoints** for production debugging
5. **Clean up breakpoints** before deploying to production

## 🔧 VS Code Configuration

Add to your VS Code settings:

```json
{
    "python.analysis.autoImportCompletions": true,
    "python.analysis.typeCheckingMode": "basic",
    "django.snippets": true,
    "django.templates": ["templates", "movies/templates"]
}
```
