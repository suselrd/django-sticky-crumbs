# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import DetailView, TemplateView
from breadcrumbs.decorators import crumbs_enabled, detail_crumbs_enabled
from .models import A


def page1(request):
    request.breadcrumbs.add("Page 1", request.get_full_path())
    return render_to_response('tests/page1.html', {},
                              context_instance=RequestContext(request))


@crumbs_enabled("Page 2")
class MyView(TemplateView):
    template_name = 'tests/page1.html'


@detail_crumbs_enabled("%(pk)s")
class MyView2(DetailView):
    model = A
    template_name = 'tests/page1.html'