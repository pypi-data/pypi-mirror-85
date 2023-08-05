from django.urls import path
from .views import *

urlpatterns = [
    path('c/<category_slug>', category_page, name="blog_category"),
    path('p/<post_slug>', post_page, name="blog_post"),
    path('', blog_main, name="blog_page"),

]
