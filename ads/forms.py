from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile

from .models import Ad
from .humanize import naturalsize


class CreateForm(forms.ModelForm):
    upload_limit = 2 << 10 << 10
    upload_limit_text = naturalsize(upload_limit)

    picture = forms.FileField(required=False,
            label=f"File to Upload <= {upload_limit_text}")

    class Meta:
        model = Ad
        fields = ['title', 'text', 'picture']  # picture is manual
    
    def clean(self):
        # Validate the size of picture
        cleaned_data = super().clean()
        picture = cleaned_data.get('picture')
        if picture is None:
            return
        if len(picture) > self.upload_limit:
            self.add_error('picture', f"File must be < {upload_limit_text}")

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

