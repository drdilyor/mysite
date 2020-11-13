from django.contrib import admin

# Register your models here.
from polls.models import Choice, Question

admin.site.register(Choice)
admin.site.register(Question)