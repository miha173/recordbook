# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns("src.tests.views",
                       (r'^$', 'index'),
                       
                       (r'^test/$', 'testList'),
                       (r'^test/add/$', 'testEdit', {'mode': 'add'}),
                       (r'^test/edit/(?P<id>\d+)/$', 'testEdit', {'mode': 'edit'}),
                       (r'^test/delete/(?P<id>\d+)/$', 'testEdit', {'mode': 'remove'}),
                       
                       (r'test/(?P<test_id>\d+)/$', 'questionList'),

                       (r'test/(?P<test_id>\d+)/a/question/add/$', 'questionEdit', {'mode': 'add', 'type': 'A'}),
                       (r'test/(?P<test_id>\d+)/a/question/edit/(?P<question_id>\d+)/$', 'questionEdit', {'mode': 'edit', 'type': 'A'}),
                       (r'test/(?P<test_id>\d+)/a/question/delete/(?P<question_id>\d+)/$', 'questionEdit', {'mode': 'delete', 'type': 'A'}),
                       
                       (r'test/(?P<test_id>\d+)/a/variant/add/(?P<question_id>\d+)/$', 'variantEdit', {'mode': 'add', 'type': 'A'}),
                       (r'test/(?P<test_id>\d+)/a/variant/edit/(?P<variant_id>\d+)/$', 'variantEdit', {'mode': 'edit', 'type': 'A'}),
                       (r'test/(?P<test_id>\d+)/a/variant/delete/(?P<variant_id>\d+)/$', 'variantEdit', {'mode': 'delete', 'type': 'A'}),
                       
                       )