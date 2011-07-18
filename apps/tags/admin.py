from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Tag
admin.site.register(Tag, MPTTModelAdmin)
