from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Organization)
admin.site.register(Campaign)
admin.site.register(Transaction)
admin.site.register(UploadedImage)
