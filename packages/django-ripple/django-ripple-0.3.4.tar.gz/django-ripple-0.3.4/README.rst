=============
Ripple Django
=============

Ripple Django is a base app for a Django-React-Bootstrap Framework that can be run in Google Cloud


Quick start
-----------

1. Add "rippledjango" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'ripple',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('auth/', include('rippledjango.urls')),

3. Run `python manage.py migrate` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/.