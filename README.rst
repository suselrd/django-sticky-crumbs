==========================
Django Sticky Crumbs
==========================

Sticky breadcrumbs for Django>=1.6.1

Based on the implementation of django-breadcrumbs (by Felipe 'chronos' Prenholato).

Changelog
=========

0.2.0
-----
New wizard_crumbs_enabled decorator, for WizardView

0.1.1
-----
Non-conflicting multi-site breadcrumbs.

0.1.0
-----

PENDING...

Notes
-----

PENDING...

Usage
-----

1. Run ``python setup.py install`` to install.

2. Modify your Django settings to use ``breadcrumbs``

3. Add 'breadcrumbs.middleware.BreadcrumbsMiddleware' to your settings.MIDDLEWARE_CLASSES

4. Make sure you've included 'django.contrib.sessions' to your settings.INSTALLED_APPS

5. Make sure you've included 'django.core.context_processors.request' to your settings.TEMPLATE_CONTEXT_PROCESSORS

6. Decorate the views you want to leave a crumb, specifying the desired display_name or display_template and template_args, as required