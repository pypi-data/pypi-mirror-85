from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from taggit.managers import TaggableManager

from .managers import PostManager, CategoryManager


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(db_index=True)
    cover = models.ImageField(upload_to="category_cover/%Y/%m/%d/", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    objects = CategoryManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ('title',)

    def get_active_posts(self):
        return Post.objects.active().filter(category=self)


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE)
    intro = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(db_index=True)
    is_on_main_page = models.BooleanField(
        default=True, db_index=True)
    is_popular = models.BooleanField(default=False)
    image = models.ImageField(upload_to="post/%Y/%m/%d/", blank=True, null=True)
    content = RichTextUploadingField(default='', blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    tags = TaggableManager(blank=True)
    objects = PostManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ('title',)
