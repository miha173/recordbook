# -*- coding: UTF-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings

from models import Teacher, Pupil, Grade, Subject, School, Staff, Cam, Option, Achievement
from forms import SubjectForm, GradeForm, PupilForm, TeacherForm, ResultDateForm, StaffForm, \
                  SchoolForm, CamForm, OptionForm, AchievementForm
from src.curatorship.models import Connection
from src.curatorship.forms import ConnectionGlobalForm
from src.marks.models import ResultDate
from src.utils import PlaningError

def index(request):
    return render_to_response('userextended/page.html', context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: u.prefix == 'a')
def objectList4Administrator(request, object, school_id = 0):
    ext = {}
    if object == 'achievement': 
        ext['pupil'] = get_object_or_404(Pupil, id = school_id)
    elif object == 'connection': 
        ext['grade__school'] = get_object_or_404(School, id = school_id)
    else:
        if school_id: ext['school'] = get_object_or_404(School, id = school_id)
    return objectList(request, object, ext)

@login_required
@user_passes_test(lambda u: u.prefix == 'a')
#@user_passes_test(lambda u: u.is_administrator())
def objectEdit4Administrator(request, object, mode, id = 0, school_id = 0):
    ext = {}
    if object == 'achievement': 
        ext['pupil'] = get_object_or_404(Pupil, id = school_id)
    elif object == 'connection': 
        ext['grade__school'] = get_object_or_404(School, id = school_id)
    else:
        if school_id: ext['school'] = get_object_or_404(School, id = school_id)
    return objectEdit(request, object, mode, id, ext)

def objectList(request, object, ext = {}):
    render = {}
    render.update(ext)
    templ = render['object_name'] = object
    if object == 'grade':
        Object = Grade
    if object == 'subject':
        Object = Subject
    if object == 'pupil':
        Object = Pupil
    if object == 'teacher':
        Object = Teacher
    if object == 'staff':
        Object = Staff
    if object == 'resultdate':
        Object = ResultDate
    if object == 'school':
        Object = School
    if object == 'cam':
        Object = Cam
    if object == 'option':
        Object = Option
    if object == 'achievement':
        Object = Achievement
    if object == 'connection':
        Object = Connection
    if request.GET.get('search_str'): 
        objects = Object.objects.search(request.GET.get('search_str'))
        render['search_str'] = request.GET.get('search_str')
    else:
        objects = Object.objects.all()
    objects = objects.filter(**ext)    
    paginator = Paginator(objects, settings.PAGINATOR_OBJECTS)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        render['objects'] = paginator.page(page)
    except:
        render['objects'] = paginator.page(paginator.num_pages)
    render['paginator'] = paginator.num_pages - 1
    return render_to_response('userextended/%sList.html' % templ, render, context_instance = RequestContext(request))

@login_required
def objectEdit(request, object, mode, id = 0, ext = {}):
    templ = object
    if object == 'grade':
        Object = Grade
        Form = GradeForm
    if object == 'subject':
        Object = Subject
        Form = SubjectForm
    if object == 'pupil':
        Object = Pupil
        Form = PupilForm
    if object == 'teacher':
        Object = Teacher
        Form = TeacherForm
    if object == 'staff':
        Object = Staff
        Form = StaffForm
    if object == 'resultdate':
        Object = ResultDate
        Form = ResultDateForm
    if object == 'school':
        Object = School
        Form = SchoolForm
    if object == 'cam':
        Object = Cam
        Form = CamForm
    if object == 'option':
        Object = Option
        Form = OptionForm
    if object == 'achievement':
        Object = Achievement
        Form = AchievementForm
    if object == 'connection':
        Object = Connection
        Form = ConnectionGlobalForm
    
    url = '/administrator/uni/%s/' % templ
    if 'school' in ext.keys(): url += str(ext['school'].id) + '/'
    if 'grade__school' in ext.keys(): url += str(ext['grade__school'].id) + '/'
    elif 'pupil' in ext.keys(): url += str(ext['pupil'].id) + '/'
    
    render = {}
    render.update(ext)
    if request.method == 'GET':
        if mode == 'edit':
            render['form'] = Form(instance = get_object_or_404(Object, id = id, **ext), **ext)
        elif mode == 'delete':
            try:
                get_object_or_404(Object, id = id, **ext).delete()
                return HttpResponseRedirect(url)
            except PlaningError, (error, ):
                render['error'] = error
                from django.contrib import messages
                messages.error(request, u'Удаление невозможно: %s' % error)
                return HttpResponseRedirect(url)
        else:
            render['form'] = Form(**ext)
        return render_to_response('userextended/%s.html' % templ, render, context_instance = RequestContext(request))
    if request.method == 'POST':
        if mode == 'edit':
            form = Form(data = request.POST, files = request.FILES, instance = get_object_or_404(Object, id = id, **ext), **ext)
            a = form.data
            temp = form.is_bound
            if form.is_valid():
                form.save()
                if object == 'pupil':
                    if 'photo' in request.FILES.keys():
                        folder = '/home/entropius/GTD/job/ika/special_recordbook/photos'
                        f = file('%s/%d.jpg' % (folder, int(id)), 'w')
                        f.write(request.FILES['photo'].read())
                        f.close()
                    
                return HttpResponseRedirect(url)
            else:
                render['form'] = form
                return render_to_response('userextended/%s.html' % templ, render, context_instance = RequestContext(request))
        else:
            form = Form(data = request.POST, **ext)
            if form.is_valid():
                obj = form.save(commit = False)
                if object == 'pupil':
                    if 'photo' in request.FILES.keys():
                        folder = '/home/entropius/GTD/job/ika/special_recordbook/photos'
                        f = file('%s/%d.jpg' % (folder, int(id)), 'w')
                        f.write(request.FILES['photo'].read())
                        f.close()
                if object != 'school': 
                    if 'school' in ext.keys():
                        obj.school = ext['school']
                    elif 'pupil' in ext.keys():
                        obj.pupil = ext['pupil']
                    elif 'grade__school':
                        pass
                    else:
                        obj.school = request.user.school
                obj.save()
                form.save_m2m()
                return HttpResponseRedirect(url)
            else:
                render['form'] = form
#                render['temp'] = dir(form)
                return render_to_response('userextended/%s.html' % templ, render, context_instance = RequestContext(request))
