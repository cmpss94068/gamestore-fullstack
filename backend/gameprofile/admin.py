from django.contrib import admin
from  .models import profile, platform, category

# Register your models here.
admin.site.register(profile)
admin.site.register(platform)
admin.site.register(category)