from django.contrib import admin
from .models import GeneratedBlog, UserQuery

admin.site.site_header = "Valmiki"
admin.site.index_title = "Welcome to Valmiki"
admin.site.site_title = "Valmiki"

# Register your models here.
admin.site.register(GeneratedBlog)
admin.site.register(UserQuery)
