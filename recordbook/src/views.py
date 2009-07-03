from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

from src.userextended.models import Pupil, Teacher, Subject
from src.curatorship.models import Connection

def render_options(request):
    options = render_objects = options['render_objects'] = {}
    pathes = request.path.split('/')
    render_objects['path'] = pathes[pathes.__len__()-2]
    if request.user.username[0] == 't':
        user = Teacher.objects.get(id = request.user.id)
        subjects = []
        last_subject = None
        for connection in Connection.objects.filter(teacher = user).order_by('subject'):
            if last_subject != connection.subject:
                last_subject = connection.subject
                subjects.append({'id': connection.subject.id, 'name': connection.subject.name})
        if not user.current_subject:
            if subjects.__len__() != 0:
                user.current_subject = Subject.objects.get(id = subjects[0]['id'])
                user.save()
        render_objects['user'] = user
        render_objects['subjects'] = subjects
        render_objects['grade'] = user.grade
        render_objects['administrator'] = user.administrator
        render_objects['next'] = request.path
        render_objects['user_type'] = 'teacher'
        options = render_objects
        options['current_subject'] = user.current_subject
    else:
        user = Pupil.objects.get(id = request.user.id)
        options['usertype'] = 'pupil'
    options['school'] = user.school
    return options

def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login')
    render = render_options(request)
    return render_to_response('root/index.html', render)