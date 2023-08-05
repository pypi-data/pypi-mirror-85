Django For SaaS Blog
====================

Blog is a Django app to run blog.


Quick start
-----------

1. Add "dfsaas_blog" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'dfsaas_blog',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('blog/', include('dfsaas_blog.urls')),

3. Run ``python manage.py migrate`` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/blog/ to participate in the poll.