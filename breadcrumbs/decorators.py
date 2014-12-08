# coding=utf-8
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def crumbs_enabled(display_name, clear_breadcrumbs=False):

    def decorator(cls):
        from django.views.generic import View
        if not issubclass(cls, View):
            raise ImproperlyConfigured("crumbs_enabled decorator is only suitable for View descendants.")

        normal_method = getattr(cls, 'dispatch')

        def dispatch(self, request, *args, **kwargs):
            try:
                if clear_breadcrumbs:
                    request.breadcrumbs.clear()
                request.breadcrumbs.add(display_name, request.get_full_path())
                request.session['breadcrumbs_%d' % settings.SITE_ID] = self.request.breadcrumbs.dict_repr()
            except:
                pass
            return normal_method(self, request, *args, **kwargs)

        setattr(cls, 'dispatch', dispatch)
        return cls

    return decorator


def detail_crumbs_enabled(display_template, template_args=None, clear_breadcrumbs=False):

    if not template_args:
        template_args = []
    if 'pk' not in template_args:
        template_args.append('pk')

    def decorator(cls):
        from django.views.generic import DetailView
        if not issubclass(cls, DetailView):
            raise ImproperlyConfigured("detail_crumbs_enabled decorator is only suitable for DetailView descendants.")

        normal_method = getattr(cls, 'get_object')

        def get_object(self, queryset=None):
            result = normal_method(self, queryset)
            try:
                args = dict([(arg, getattr(result, arg)) for arg in template_args])
                if clear_breadcrumbs:
                    self.request.breadcrumbs.clear()
                self.request.breadcrumbs.add(display_template % args, self.request.get_full_path())
                self.request.session['breadcrumbs_%d' % settings.SITE_ID] = self.request.breadcrumbs.dict_repr()
            except:
                pass
            return result


        setattr(cls, 'get_object', get_object)
        return cls

    return decorator


def wizard_crumbs_enabled(display_names, clear_breadcrumbs=False):

    def decorator(cls):
        from django.contrib.formtools.wizard.views import WizardView
        if not issubclass(cls, WizardView):
            raise ImproperlyConfigured("crumbs_enabled decorator is only suitable for WizardView descendants.")

        normal_method = getattr(cls, 'dispatch')

        def dispatch(self, request, *args, **kwargs):
            try:
                step_url = kwargs.get('step', None)
                if clear_breadcrumbs and not step_url:
                    request.breadcrumbs.clear()
                request.breadcrumbs.add(display_names[step_url], request.get_full_path())
                request.session['breadcrumbs_%d' % settings.SITE_ID] = self.request.breadcrumbs.dict_repr()
            except:
                pass
            return normal_method(self, request, *args, **kwargs)

        setattr(cls, 'dispatch', dispatch)
        return cls

    return decorator
