from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile

from ads.models import Ad
from ads.humanize import naturalsize


class AdForm(forms.ModelForm):
    upload_limit = 2 << 10 << 10
    upload_limit_text = naturalsize(upload_limit)

    picture = forms.FileField(required=False,
            label=f"File to Upload <= {upload_limit_text}")
    upload_field_name = 'picture'

    class Meta:
        model = Ad
        fields = ['title', 'price', 'text', 'picture']  # picture is manual
    
    def clean(self):
        # Validate the size of picture
        cleaned_data = super().clean()
        picture = cleaned_data.get('picture')
        if picture is None:
            return
        if len(picture) > self.upload_limit:
            self.add_error('picture',
                    f"File must be < {self.upload_limit_text}")

    def save(self, commit=False):
        # Convert uploaded file to a picture
        instance = super().save(commit=False)
        
        f = instance.picture
        if isinstance(f, InMemoryUploadedFile):
            byte_array = f.read()
            instance.content_type = f.content_type
            instance.picture = byte_array

        if commit:
            instance.save()

        return instance

class CommentForm(forms.Form):
    comment = forms.CharField(required=True, max_length=500, min_length=3, strip=True)

