from django.forms import ModelForm

from autos.models import Auto


class AutoForm(ModelForm):
    class Meta:
        model = Auto
        fields = '__all__'
