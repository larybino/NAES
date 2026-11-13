from urllib.parse import urlencode

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def query_params(context, **updates):
    """Build a query string while preserving the current filter parameters."""
    request = context['request']
    params = request.GET.copy()
    for key, value in updates.items():
        if value is None:
            params.pop(key, None)
        else:
            params[key] = value
    encoded = urlencode(params, doseq=True)
    return f'?{encoded}' if encoded else ''
