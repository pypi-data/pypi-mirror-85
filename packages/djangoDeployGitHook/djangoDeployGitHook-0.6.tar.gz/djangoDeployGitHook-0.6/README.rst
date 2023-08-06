===================
DjangoDeployGitHook
===================

djangoDeployGitHook is a Django app to automatically update django instance from a git
hook signal.


Quick start
-----------

1. Add "djangoDeployGitHook" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'djangoDeployGitHook',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('deploy/', include('djangoDeployGitHook.urls')),

3. Visit http://127.0.0.1:8000/deploy/test_update too see 'Hello, From DjangoDeployGitHook!'.