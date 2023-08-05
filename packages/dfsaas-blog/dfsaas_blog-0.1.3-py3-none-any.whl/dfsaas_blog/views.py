from django.shortcuts import render
from .models import Post, Category


# Create your views here.


def blog_main(request, *args, **kwargs):
    context = {
        "main_page_posts": Post.objects.main_page().order_by('-created')
    }
    return render(request, "dfsaas_blog/index.html", context=context)


def category_page(request, category_slug, *args, **kwargs):
    category = Category.objects.active().get(slug=category_slug)
    posts = Post.objects.active().filter(category=category).order_by('-created')
    context = {
        "object": category,
        "posts": posts,
        "categories": Category.objects.active(),
        "popular_posts": Post.objects.popular(),
    }
    return render(request, "dfsaas_blog/category.html", context=context)


def post_page(request, post_slug, *args, **kwargs):
    context = {
        "object": Post.objects.active().get(slug=post_slug),
        "categories": Category.objects.active(),
        "popular_posts": Post.objects.popular(),
    }
    return render(request, "dfsaas_blog/post.html", context=context)


def about_page(request, *args, **kwargs):
    return render(request, "dfsaas_blog/about.html")
