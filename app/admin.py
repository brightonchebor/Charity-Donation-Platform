from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'description')
    list_filter = ('owner',)
admin.site.register(Campaign)
admin.site.register(Transaction)

