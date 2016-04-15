
import bleach
from django import template
from ..utils import get_profile_photo_url

register = template.Library()


@register.filter
def bleach_striptags(strval):
    return bleach.clean(strval, tags=[], strip=True, strip_comments=True)


@register.inclusion_tag('profiles/_profile_photo.html')
def render_profile_photo(user):
    """
    {% render_profile_photo user %}
    """
    photo_url = get_profile_photo_url(user)
    return {'photo_url': photo_url, 'profile_user_id': user.id}
