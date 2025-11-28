from django import template
from django.contrib.messages import constants as messages_constants

register = template.Library()

# Map Django message levels to CSS classes
ALERT_CLASSES = {
    messages_constants.DEBUG: "alert-debug",
    messages_constants.INFO: "alert-info",
    messages_constants.SUCCESS: "alert-success",
    messages_constants.WARNING: "alert-warning",
    messages_constants.ERROR: "alert-error",
}


@register.inclusion_tag("movies/messages.html", takes_context=True)
def render_messages(context):
    """
    Renders Django messages as dismissable alerts.
    """
    request = context.get("request")
    if not request:
        return {"messages": []}

    messages = getattr(request, "_messages", [])
    return {
        "messages": [
            {
                "message": msg.message,
                "level_class": ALERT_CLASSES.get(msg.level, "alert-info"),
            }
            for msg in messages
        ]
    }
