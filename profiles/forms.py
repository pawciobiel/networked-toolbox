import logging
from django import forms
from django.forms import fields
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat

from django_countries.fields import LazyTypedChoiceField
from django_countries import countries

from bleach import clean

from .models import PROFILE_BIO_MAX_LEN


log = logging.getLogger(__name__)


class ProfileForm(forms.Form):
    MAX_PHOTO_SIZE = 2 * 1024 * 1024
    PHOTO_MAX_WIDTH = 1024
    PHOTO_MAX_HEIGH = 1024
    first_name = fields.CharField(max_length=30, required=False)
    last_name = fields.CharField(max_length=30, required=False)
    photo = forms.ImageField(required=False,
                             label='Profile image (recommended size: 160x160)',
                             widget=forms.FileInput)
    bio = fields.CharField(widget=forms.Textarea,
                           max_length=PROFILE_BIO_MAX_LEN,
                           required=False,
                           label='Bio (a short description of yourself)',
                           help_text='{} characters max.'.format(PROFILE_BIO_MAX_LEN))
    country = LazyTypedChoiceField(choices=[('', ''), ] + list(countries),
                                   required=False,
                                   label='Where do you live?')

    def clean_photo(self):
        photo = self.cleaned_data.get('photo', False)
        if photo and photo.image and photo.file:
            if photo.image.size[0] > self.PHOTO_MAX_WIDTH:
                raise ValidationError("Image width too large ( max %s px )" %
                                      self.PHOTO_MAX_WIDTH)
            if photo.image.size[1] > self.PHOTO_MAX_HEIGH:
                raise ValidationError("Image height too large ( max %s px )" %
                                      self.PHOTO_MAX_HEIGH)
            file_size = len(photo)
            if file_size > self.MAX_PHOTO_SIZE:
                raise ValidationError("Image size is too large ( max %s  )" %
                                      filesizeformat(self.PHOTO_MAX_HEIGH))
            if file_size < 1:
                raise ValidationError("Image is empty" %
                                      filesizeformat(self.PHOTO_MAX_HEIGH))
            return photo

    def clean_bio(self):
        import html.parser
        html_parser = html.parser.HTMLParser()

        bio = self.cleaned_data.get('bio', '')
        bio = clean(bio, tags=[], strip=True, strip_comments=True)
        return html_parser.unescape(bio)

class NetboxSignupForm(forms.Form):

    first_name = fields.CharField(max_length=30, required=True)
    last_name = fields.CharField(max_length=30, required=True)

    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(NetboxSignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].help_text = 'We recommend you use your work e-mail'

    def signup(self, request, user):
        """
        Invoked at signup time to complete the signup of the user.
        """
        pass
