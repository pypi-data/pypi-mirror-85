from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_filter = ['is_active', ]
    prepopulated_fields = {'slug': ('title',), }


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), }
    list_filter = [
        'is_active',
        'is_on_main_page',
        'category']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
