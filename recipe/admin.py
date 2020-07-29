from django.contrib import admin
from .models import Category,Recipe, Comment, userprofile
# Register your models here.
admin.site.register(Category)
admin.site.register(Recipe)
admin.site.register(Comment)
admin.site.register(userprofile)
# admin.site.register(Comment)