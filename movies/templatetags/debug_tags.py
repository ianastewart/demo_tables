from django import template
import json
from django.utils.safestring import mark_safe
from django.template import Context, TemplateSyntaxError
import logging

logger = logging.getLogger(__name__)

register = template.Library()


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
    Usage: {% conditional_breakpoint True "message" %}
    Note: Use {% if %} tags for complex conditions
    """
    # Convert string "True"/"False" to boolean
    if isinstance(condition, str):
        condition = condition.lower() == 'true'
    
    if condition:
        raise TemplateSyntaxError(f"CONDITIONAL BREAKPOINT: {message}")
    return ""


@register.simple_tag(takes_context=True)
def log_breakpoint(context, message="Template breakpoint"):
    """
    Logging breakpoint for template debugging.
    Usage: {% log_breakpoint "Custom message" %}
    """
    logger.error(f"TEMPLATE BREAKPOINT: {message}")
    # This will show in Django logs
    return f"<!-- BREAKPOINT: {message} -->"


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


@register.simple_tag(takes_context=True)
def js_breakpoint(context, condition=True, message="JavaScript breakpoint"):
    """
    Generate JavaScript breakpoint code.
    Usage: {% js_breakpoint %} or {% js_breakpoint condition "message" %}
    """
    if condition:
        return mark_safe(f"""
        <script>
            console.log('TEMPLATE BREAKPOINT: {message}');
            debugger; // This will break in browser dev tools
        </script>
        """)
    return ""


@register.simple_tag(takes_context=True)
def inspect_context(context, stop=False):
    """
    Inspect entire template context.
    Usage: {% inspect_context %} or {% inspect_context stop %}
    """
    debug_info = {}
    
    try:
        if hasattr(context, 'dicts'):
            for context_dict in context.dicts:
                if hasattr(context_dict, 'items'):
                    for key, value in context_dict.items():
                        debug_info[key] = {
                            'type': type(value).__name__,
                            'value': str(value)[:100] + '...' if len(str(value)) > 100 else str(value)
                        }
    except Exception as e:
        debug_info['error'] = str(e)
    
    if stop:
        raise Exception(f"CONTEXT INSPECT BREAKPOINT: {json.dumps(debug_info, indent=2)}")
    
    return mark_safe(f"<!-- CONTEXT INSPECT: {json.dumps(debug_info, indent=2)} -->")


@register.simple_tag(takes_context=True)
def debug(context):
    """
    Debug all context variables in a template.
    Usage: {% load debug_tags %} {% debug %}
    """
    debug_info = {}
    
    # Get all context variables from RequestContext
    try:
        # RequestContext has a 'dicts' attribute that contains the context data
        if hasattr(context, 'dicts'):
            # Flatten all context dictionaries
            for context_dict in context.dicts:
                if hasattr(context_dict, 'items'):
                    for key, value in context_dict.items():
                        try:
                            # Try to serialize the value
                            if hasattr(value, '__dict__'):
                                debug_info[key] = {
                                    'type': type(value).__name__,
                                    'str': str(value),
                                    'attributes': list(value.__dict__.keys()) if hasattr(value, '__dict__') else []
                                }
                            else:
                                debug_info[key] = {
                                    'type': type(value).__name__,
                                    'value': str(value)
                                }
                        except Exception as e:
                            debug_info[key] = {
                                'type': type(value).__name__,
                                'error': str(e)
                            }
        else:
            # Fallback for regular dict-like context
            for key, value in context.items():
                try:
                    if hasattr(value, '__dict__'):
                        debug_info[key] = {
                            'type': type(value).__name__,
                            'str': str(value),
                            'attributes': list(value.__dict__.keys()) if hasattr(value, '__dict__') else []
                        }
                    else:
                        debug_info[key] = {
                            'type': type(value).__name__,
                            'value': str(value)
                        }
                except Exception as e:
                    debug_info[key] = {
                        'type': type(value).__name__,
                        'error': str(e)
                    }
    except Exception as e:
        debug_info['error'] = f"Failed to process context: {str(e)}"
    
    return mark_safe(f"<pre style='background: #f0f0f0; padding: 10px; border: 1px solid #ccc;'><strong>Template Context Debug:</strong>\n{json.dumps(debug_info, indent=2, default=str)}</pre>")


@register.simple_tag(takes_context=True)
def debug_var(context, var_name):
    """
    Debug a specific context variable.
    Usage: {% debug_var 'movies' %}
    """
    # Try to get the variable from RequestContext
    try:
        if hasattr(context, 'dicts'):
            # Search through all context dictionaries
            for context_dict in context.dicts:
                if hasattr(context_dict, 'get') and var_name in context_dict:
                    value = context_dict[var_name]
                    break
            else:
                return mark_safe(f"<div style='background: #ffe6e6; padding: 10px; border: 1px solid #ff0000;'>Variable '{var_name}' not found in context</div>")
        else:
            # Fallback for regular dict-like context
            if var_name in context:
                value = context[var_name]
            else:
                return mark_safe(f"<div style='background: #ffe6e6; padding: 10px; border: 1px solid #ff0000;'>Variable '{var_name}' not found in context</div>")
        
        debug_info = {
            'name': var_name,
            'type': type(value).__name__,
            'value': str(value),
            'length': len(value) if hasattr(value, '__len__') else 'N/A'
        }
        
        # Add more info for QuerySets
        if hasattr(value, 'count'):
            debug_info['count'] = value.count()
        if hasattr(value, 'model'):
            debug_info['model'] = value.model.__name__
            
        return mark_safe(f"<pre style='background: #e8f4fd; padding: 10px; border: 1px solid #007acc;'><strong>Variable '{var_name}' Debug:</strong>\n{json.dumps(debug_info, indent=2, default=str)}</pre>")
        
    except Exception as e:
        return mark_safe(f"<div style='background: #ffe6e6; padding: 10px; border: 1px solid #ff0000;'>Error accessing variable '{var_name}': {str(e)}</div>")


@register.filter
def debug_type(var):
    """Get the type of a variable."""
    return type(var).__name__


@register.filter
def debug_attrs(var):
    """Get attributes of an object."""
    if hasattr(var, '__dict__'):
        return list(var.__dict__.keys())
    return []


@register.filter
def debug_methods(var):
    """Get methods of an object."""
    if hasattr(var, '__class__'):
        methods = [method for method in dir(var) if not method.startswith('_')]
        return methods
    return []


@register.simple_tag(takes_context=True)
def debug_request(context):
    """
    Debug request object in template.
    Usage: {% debug_request %}
    """
    # Try to get request from RequestContext
    try:
        if hasattr(context, 'dicts'):
            # Search through all context dictionaries for request
            request = None
            for context_dict in context.dicts:
                if hasattr(context_dict, 'get') and 'request' in context_dict:
                    request = context_dict['request']
                    break
        else:
            # Fallback for regular dict-like context
            request = context.get('request')
            
        if request:
            debug_info = {
                'method': request.method,
                'path': request.path,
                'user': str(request.user) if hasattr(request, 'user') else 'Anonymous',
                'GET_params': dict(request.GET),
                'POST_params': dict(request.POST) if request.method == 'POST' else {},
                'headers': dict(request.META) if hasattr(request, 'META') else {},
            }
            
            return mark_safe(f"<pre style='background: #fff3cd; padding: 10px; border: 1px solid #ffc107;'><strong>Request Debug:</strong>\n{json.dumps(debug_info, indent=2, default=str)}</pre>")
        else:
            return mark_safe("<div style='background: #ffe6e6; padding: 10px; border: 1px solid #ff0000;'>No request object in context</div>")
            
    except Exception as e:
        return mark_safe(f"<div style='background: #ffe6e6; padding: 10px; border: 1px solid #ff0000;'>Error accessing request: {str(e)}</div>")


@register.simple_tag(takes_context=True)
def debug_template_info(context):
    """
    Debug template information.
    Usage: {% debug_template_info %}
    """
    # Try to get template info from RequestContext
    try:
        if hasattr(context, 'dicts'):
            # Search through all context dictionaries
            template_name = 'Unknown'
            view_name = 'Unknown'
            app_name = 'Unknown'
            
            for context_dict in context.dicts:
                if hasattr(context_dict, 'get'):
                    if 'template_name' in context_dict:
                        template_name = context_dict['template_name']
                    if 'view_name' in context_dict:
                        view_name = context_dict['view_name']
                    if 'app_name' in context_dict:
                        app_name = context_dict['app_name']
        else:
            # Fallback for regular dict-like context
            template_name = context.get('template_name', 'Unknown')
            view_name = context.get('view_name', 'Unknown')
            app_name = context.get('app_name', 'Unknown')
        
        template_info = {
            'template_name': template_name,
            'view_name': view_name,
            'app_name': app_name,
        }
        
        return mark_safe(f"<pre style='background: #d1ecf1; padding: 10px; border: 1px solid #17a2b8;'><strong>Template Info:</strong>\n{json.dumps(template_info, indent=2)}</pre>")
        
    except Exception as e:
        return mark_safe(f"<div style='background: #ffe6e6; padding: 10px; border: 1px solid #ff0000;'>Error accessing template info: {str(e)}</div>")


@register.simple_tag
def debug_queryset(qs):
    """
    Debug a QuerySet.
    Usage: {% debug_queryset movies %}
    """
    if hasattr(qs, 'model'):
        debug_info = {
            'model': qs.model.__name__,
            'count': qs.count(),
            'sql': str(qs.query),
            'first_item': str(qs.first()) if qs.exists() else None,
        }
        
        return mark_safe(f"<pre style='background: #d4edda; padding: 10px; border: 1px solid #28a745;'><strong>QuerySet Debug:</strong>\n{json.dumps(debug_info, indent=2, default=str)}</pre>")
    else:
        return mark_safe(f"<div style='background: #ffe6e6; padding: 10px; border: 1px solid #ff0000;'>Not a QuerySet: {type(qs).__name__}</div>")


@register.simple_tag
def debug_form(form):
    """
    Debug a Django form.
    Usage: {% debug_form form %}
    """
    if hasattr(form, 'fields'):
        debug_info = {
            'form_class': form.__class__.__name__,
            'fields': list(form.fields.keys()),
            'is_valid': form.is_valid() if hasattr(form, 'is_valid') else 'Unknown',
            'errors': form.errors if hasattr(form, 'errors') else {},
            'data': form.data if hasattr(form, 'data') else {},
        }
        
        return mark_safe(f"<pre style='background: #f8d7da; padding: 10px; border: 1px solid #dc3545;'><strong>Form Debug:</strong>\n{json.dumps(debug_info, indent=2, default=str)}</pre>")
    else:
        return mark_safe(f"<div style='background: #ffe6e6; padding: 10px; border: 1px solid #ff0000;'>Not a form: {type(form).__name__}</div>")


@register.simple_tag(takes_context=True)
def debug_all(context):
    """
    Comprehensive debug information.
    Usage: {% debug_all %}
    """
    debug_sections = []
    
    # Context variables
    debug_sections.append(debug(context))
    
    # Request info
    debug_sections.append(debug_request(context))
    
    # Template info
    debug_sections.append(debug_template_info(context))
    
    return mark_safe('\n'.join(debug_sections))
