=====
Django Leafage
=====

Simple and Easiest paginator for Django.

Installation
-----------

    pip install django-leafage


Quick start
-----------

1. Add "leafage" to your INSTALLED_APPS in settings.py like this::

    INSTALLED_APPS = [
        ...
        'leafage',
        ...
    ]

2. Ensure "APP_DIRS" to "True" in settings.py like this::
    TEMPLATES = [
        {
            ...
            'DIRS': [],
            'APP_DIRS': True,
            ...
        },
    ]

3. In views ""import leafage" like this::

    import leafage

    def home(request):
    """
        Home page handler.
    """
    template = 'home.html'

    per_page_obj = 10 # default = 10(if not provided)

    queryset = Model.objects.all()
    queryset = leafage.pagination(request=request, obj_list=queryset, obj_count=per_page_obj)

    context = {
        'queryset': queryset
    }
    return render(request, template, context)

4. At beginning of template include following code and template look like this.

    {% load leafage %}

5. End of template add following code look like this.

    {% paginate request=request object_list=queryset %}


Licence
-----------
Copyright (c) 2020 Nilesh Kumar Dubey

This repository is licensed under the MIT license.
See LICENSE for details
