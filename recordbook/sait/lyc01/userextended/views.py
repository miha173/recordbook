# Create your views here.
# -*- coding: UTF-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.core.cache import cache
from django.http import HttpResponse


from models import Probe, Pupil, Subject

def main(request):
#    pupil = Pupil.objects.get(username='p.komkov.aleksandr')
#    subject = Subject.objects.get(name=u'Физика')
#    Probe.objects.all().delete()
#    for i in xrange(1000001, 2000000):
#        pr = Probe()
#        pr.stars = i
#        pr.pupil = pupil
#        pr.subject = subject
#        pr.save()
    output = ''
    pr = Probe.objects.all().filter(stars__in=xrange(0, 40))
    i = 0
    for p in pr:
        i = i + 1
        output = output + str(p.pupil.username) + '-' + unicode(p.subject.name) + '-' + str(p.stars) + '-' + u'<br />'
    return HttpResponse(output)