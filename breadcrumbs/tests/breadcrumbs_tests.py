# # coding: utf-8
import os
from django.conf import settings
from django.test import TestCase
from django.utils.datastructures import SortedDict

from breadcrumbs.breadcrumbs import Breadcrumb, Breadcrumbs


class BreadcrumbsTest(TestCase):
    urls = 'breadcrumbs.tests.urls'

    def setUp(self):
        self.old_MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES
        breadcrumbs_middleware_class = 'breadcrumbs.middleware.BreadcrumbsMiddleware'
        if breadcrumbs_middleware_class not in settings.MIDDLEWARE_CLASSES:
            settings.MIDDLEWARE_CLASSES += (breadcrumbs_middleware_class,)

        self.old_TEMPLATE_CONTEXT_PROCESSORS = settings.TEMPLATE_CONTEXT_PROCESSORS
        request_processor = 'django.core.context_processors.request'
        if request_processor not in settings.TEMPLATE_CONTEXT_PROCESSORS:
            settings.TEMPLATE_CONTEXT_PROCESSORS += (request_processor,)

        self.old_TEMPLATE_DIRS = settings.TEMPLATE_DIRS
        settings.TEMPLATE_DIRS = (
            os.path.join(
                os.path.dirname(__file__),
                'templates'
            ),
        )

        # set some common ta to use
        SD = SortedDict
        self.data = [
            SD([('name', 'Page1'), ('url', '/page1/')]),
            SD([('name', 'Page2'), ('url', '/page2/')]),
            SD([('name', 'Page3'), ('url', '/page2/page3/')]),
            SD([('name', 'Page4'), ('url', '/page4/')]),
            SD([('name', 'Page5'), ('url', '/page5/')]),
        ]

    def tearDown(self):
        settings.MIDDLEWARE_CLASSES = self.old_MIDDLEWARE_CLASSES
        settings.TEMPLATE_DIRS = self.old_TEMPLATE_DIRS
        settings.TEMPLATE_CONTEXT_PROCESSORS = self.old_TEMPLATE_CONTEXT_PROCESSORS

        del self.data

    def test_breadcrumb_class(self):
        b = Breadcrumb(**self.data[0])
        self.assertEqual(b.name, self.data[0]['name'])
        self.assertEqual(b.url, self.data[0]['url'])

    def test_breadcrumbs_params_and_iteration(self):

        b = Breadcrumbs()

        b.add(self.data[0]['name'], self.data[0]['url'])
        b.add(*self.data[1].values())
        b.add(**self.data[2])
        b.add(self.data[3:5])
        for i, bd in enumerate(b):
            self.assertEqual(bd, Breadcrumb(**self.data[i]).__dict__)

    def test_request_breadcrumbs(self):
        response = self.client.get('/page1/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
            '<ul id="breadcrumbs"><li><a href="/page1/">Page 1</a></li></ul>')

    def test_crumbs_enabled_decorator(self):
        response = self.client.get('/page2/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
            '<ul id="breadcrumbs"><li><a href="/page2/">Page 2</a></li></ul>')

    def test_detail_crumbs_enabled_decorator(self):
        from .models import A
        pk = A.objects.create().pk
        url = '/%s/' % pk
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
            '<ul id="breadcrumbs"><li><a href="%s">%s</a></li></ul>' % (url, pk))

    #def test_repeated_crumbs_behaviour(self):
    #    response = self.client.get('/page1/')
    #    self.assertEqual(response.status_code, 200)
    #    self.assertContains(response,
    #        '<ul id="breadcrumbs"><li><a href="/page1/">Page 1</a></li></ul>')
    #
    #
    #    response = self.client.get('/page2/')
    #    self.assertEqual(response.status_code, 200)
    #    self.assertContains(response,
    #        '<ul id="breadcrumbs"><li><a href="/page1/">Page 1</a></li><li><a href="/page2/">Page 2</a></li></ul>')
    #
    #
    #    response = self.client.get('/page1/')
    #    self.assertEqual(response.status_code, 200)
    #    self.assertContains(response,
    #        '<ul id="breadcrumbs"><li><a href="/page1/">Page 1</a></li></ul>')
