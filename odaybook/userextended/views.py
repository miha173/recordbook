# -*- coding: UTF-8 -*-

import demjson

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import get_model
from django.core.urlresolvers import resolve, reverse

from models import School, Clerk, Superviser, Teacher, Pupil, Parent, BaseUser, Superuser, Subject
from forms import ClerkForm, PupilConnectionForm, ClerkRegisterForm
import odaybook.userextended.forms
import odaybook.attendance.forms
import odaybook.curatorship.forms
import odaybook.marks.forms
from odaybook.utils import PlaningError

def index(request):
    return HttpResponseRedirect('/')
#    return render_to_response('page.html', context_instance = RequestContext(request))


@login_required
@user_passes_test(lambda u: u.type in ['Superuser', 'Teacher'])
def objectList(request, app, model, filter_id = None):
    render = {}
    ext = {}
    app_model = '%s.%s' % (app, model)
    
    if app_model == 'userextended.School':
        if request.user.type == 'Teacher':
            ext['id'] = request.user.school.id
    elif app_model == 'curatorship.Connection':
        if request.user.type == 'Teacher':
            ext['grade__school'] = request.user.school
        elif request.user.type == 'Superuser':
            ext['grade__school'] = get_object_or_404(School, id = filter_id)
    elif app_model == 'userextended.Clerk':
        pass
    else:
        if request.user.type == 'Teacher':
            ext['school'] = request.user.school
        elif request.user.type == 'Superuser':
            ext['school'] = get_object_or_404(School, id = filter_id)

    render.update(ext)

    allowed_apps = [
            'userextended.Grade', 'userextended.Subject', 'userextended.Pupil',
            'userextended.Teacher', 'userextended.Staff', 'userextended.School',
            'userextended.Option', 'userextended.Achievement', 'marks.ResultDate',
            'curatorship.Connection'
    ]
    if request.user.type == 'Superuser': allowed_apps += 'userextended.Clerk', 
    if app + '.' + model not in allowed_apps:
        raise Http404('Object %s not allowed for usertype %s' % (app + '.' + model, request.user.type))
    if model == 'Clerk': render['schools'] = School.objects.all()
    template = render['object_name'] = model.lower()
    Object = get_model(app, model)

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

    return render_to_response('~userextended/%sList.html' % template, render, context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: u.type in ['Superuser', 'Teacher'])
def objectEdit(request, app, model, mode, filter_id = None, id = 0):
    render = {}
    ext = {}
    app_model = '%s.%s' % (app, model)

    allowed_apps = [
            'userextended.Grade', 'userextended.Subject', 'userextended.Pupil',
            'userextended.Teacher', 'userextended.Staff', 'userextended.School',
            'userextended.Option', 'userextended.Achievement', 'marks.ResultDate',
            'curatorship.Connection',
    ]
    if app + '.' + model not in allowed_apps: raise Http404('Object not allowed')
    template = render['object_name'] = model.lower()
    Object = get_model(app, model)
    Form = getattr(getattr(__import__('odaybook'), app).forms, model + 'Form')

    if app_model == 'userextended.School':
        if request.user.type == 'Teacher':
           ext['id'] = request.user.school.id
    elif app_model == 'curatorship.Connection':
        if request.user.type == 'Teacher':
            ext['grade__school'] = request.user.school
        elif request.user.type == 'Superuser':
            ext['grade__school'] = get_object_or_404(School, id = filter_id)
    else:
        if request.user.type == 'Teacher':
            ext['school'] = request.user.school
        elif request.user.type == 'Superuser':
            ext['school'] = get_object_or_404(School, id = filter_id)

    url = '/administrator/uni/%s.%s/' % (app, model)
    if filter_id: url += str(filter_id) + '/'

    render.update(ext)

    if request.method == 'GET':
        if mode == 'edit':
            render['form'] = Form(instance = get_object_or_404(Object, id = id, **ext), **ext)
            if model == 'Pupil':
                pupil = get_object_or_404(Object, id = id, **ext)
                render['groups'] = [PupilConnectionForm(sbj, pupil, prefix = sbj.id) for sbj in pupil.grade.get_subjects() if sbj.groups]
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
            if model == 'Pupil':
                render['groups'] = [PupilConnectionForm(sbj, prefix = sbj.id) for sbj in Subject.objects.filter(school = ext['school']) if sbj.groups]
        return render_to_response('~userextended/%s.html' % template, render, context_instance = RequestContext(request))
    if request.method == 'POST':
        if mode == 'edit':
            form = Form(data = request.POST, files = request.FILES, instance = get_object_or_404(Object, id = id, **ext), **ext)
            form_factory_valid = True
            if model == 'Pupil':
                pupil = get_object_or_404(Object, id = id, **ext)
                render['groups'] = [PupilConnectionForm(sbj, pupil, data = request.POST, prefix = sbj.id) for sbj in pupil.grade.get_subjects() if sbj.groups]
                form_factory_valid = all([f.is_valid() for f in render['groups']])
            if form.is_valid() and form_factory_valid:
                form.save()
                for f in render['groups']: f.save()
                return HttpResponseRedirect(url)
            else:
                render['form'] = form
                return render_to_response('~userextended/%s.html' % template, render, context_instance = RequestContext(request))
        else:
            form_factory_valid = True
            if model == 'Pupil':
                render['groups'] = [PupilConnectionForm(sbj, data = request.POST, prefix = sbj.id) for sbj in Subject.objects.filter(school = ext['school']) if sbj.groups]
                form_factory_valid = all([f.is_valid() for f in render['groups']])
            form = Form(data = request.POST, **ext)
            if form.is_valid() and form_factory_valid:
                result = form.save()
                if model == 'Pupil':
                    for f in render['groups']: f.save(pupil = result)
                return HttpResponseRedirect(url)
            else:
                render['form'] = form
                return render_to_response('~userextended/%s.html' % template, render, context_instance = RequestContext(request))


@login_required
@user_passes_test(lambda u: u.type in ['Superuser'])
def baseUserObjectEdit(request, mode, filter_id = None, id = 0):
    render = {}

    url = '/accounts/baseuser/'

    if request.method == 'GET':
        if mode == 'set_right':
            # FIXME: url reverse
            # FIXME: DRY
            clerk = get_object_or_404(Clerk, id = id)
            right = request.GET.get('set_right', None)

            if right not in ['Superuser', 'Superviser', 'EduAdmin']: raise Http404

            if right in ['Superviser', 'Superuser']:
                if right in clerk.get_roles_list_simple():
                    # FIXME: сообщение
                    pass
                else:
                    if right == 'Superviser': clerk.create_role(Superviser)
                    if right == 'Superuser': clerk.create_role(Superuser)

            if right == 'EduAdmin':
                school = get_object_or_404(School, id = request.GET.get('school_id', 0))
                if clerk.has_role('EduAdmin', school):
                    # FIXME: сообщение
                    pass
                else:
                    if clerk.has_role('Teacher', school):
                        teacher = clerk.get_role_obj('Teacher', school)[0]
                    else:
                        teacher = clerk.create_role(Teacher)
                        teacher.school = school
                    teacher.edu_admin = True
                    teacher.save()

            return HttpResponseRedirect('/accounts/baseuser/')

        if mode == 'dismiss':
            # FIXME: url reverse
            # FIXME: DRY
            clerk = get_object_or_404(Clerk, id = id)
            right = request.GET.get('right', None)

            if right not in ['Superuser', 'Superviser', 'EduAdmin', 'Teacher']: raise Http404

            if right == 'Superuser':
                clerk.is_superuser = False
                clerk.save()

            if right == 'Superviser':
                if 'Superviser' in clerk.get_roles_list_simple():
                    superviser = clerk.get_role_obj('Superviser')[0]
                    baseuser = BaseUser.objects.get(id = superviser.id)
                    clerk.roles.remove(baseuser)
                    clerk.save()
                    superviser.delete()
                    baseuser.delete()
                else:
                    # FIXME: сообщение
                    pass

            if right == 'EduAdmin':
                role = get_object_or_404(Teacher, id = request.GET.get('role_id'), edu_admin = True, clerk = clerk)
                role.edu_admin = False
                role.save()

            if right == 'Teacher':
                role = get_object_or_404(Teacher, id = request.GET.get('role_id'), clerk = clerk)
                clerk.roles.remove(role)
                clerk.save()
                role.delete()

            return HttpResponseRedirect('/accounts/baseuser/')

        if mode == 'edit':
            render['form'] = ClerkForm(instance = get_object_or_404(Clerk, id = id))
        elif mode == 'delete':
            try:
                get_object_or_404(Clerk, id = id).delete()
                return HttpResponseRedirect(url)
            except PlaningError, (error, ):
                render['error'] = error
                from django.contrib import messages
                messages.error(request, u'Удаление невозможно: %s' % error)
                return HttpResponseRedirect(url)
        else:
            render['form'] = ClerkForm()
        return render_to_response('~userextended/clerk.html', render, context_instance = RequestContext(request))
    if request.method == 'POST':
        if mode == 'edit':
            form = ClerkForm(data = request.POST, files = request.FILES, instance = get_object_or_404(Clerk, id = id))
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(url)
            else:
                render['form'] = form
                return render_to_response('~/userextended/clerk.html', render, context_instance = RequestContext(request))
        else:
            form = ClerkForm(data = request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(url)
            else:
                render['form'] = form
                return render_to_response('~userextended/clerk.html', render, context_instance = RequestContext(request))

@login_required
def set_role(request, role_id):
    request.user.set_current_role(role_id, request.GET.get('type', ''))
    return HttpResponseRedirect('/')

@login_required
@user_passes_test(lambda u: reduce(lambda x, y: x or y, map(lambda a: a in ['Superuser', 'EduAdmin'], u.types)))
def clerkAppendRole(request):
    render = {}
    render['step'] = request.GET.get('step', '1')
    render['username'] = request.POST.get('username', '')
    render['school'] = request.GET.get('school', '1')

    if request.GET.get('step', '1') == '1':
        if request.method == 'POST':
            try:
                clerk = Clerk.objects.get(username = request.POST.get('username'))
            except Clerk.DoesNotExist:
                render['error'] = u'Пользователя с таким ID не существует.'
                return render_to_response('~userextended/clerkAppendRole.html', render, context_instance = RequestContext(request))
            if 'Pupil' in clerk.get_roles_list():
                render['error'] = u'Этот пользователь ученик.'
                return render_to_response('~userextended/clerkAppendRole.html', render, context_instance = RequestContext(request))
            school = get_object_or_404(School, id = request.GET.get('school', '0'))
            if clerk.has_role('Teacher', school):
                render['error'] = u'Этот пользователь уже приписан к данной школе.'
                return render_to_response('~userextended/clerkAppendRole.html', render, context_instance = RequestContext(request))

            render['clerk'] = clerk

    elif request.GET.get('step', '1') == '2':
        if request.method == 'POST':
            try:
                clerk = Clerk.objects.get(username = request.POST.get('username'))
            except Clerk.DoesNotExist:
                render['error'] = u'Пользователя с таким ID не существует.'
                return render_to_response('~userextended/clerkAppendRole.html', render, context_instance = RequestContext(request))
            if 'Pupil' in clerk.get_roles_list():
                render['error'] = u'Этот пользователь ученик.'
                return render_to_response('~userextended/clerkAppendRole.html', render, context_instance = RequestContext(request))
            school = get_object_or_404(School, id = request.GET.get('school', '0'))
            if clerk.has_role('Teacher', school):
                render['error'] = u'Этот пользователь уже приписан к данной школе.'
                return render_to_response('~userextended/clerkAppendRole.html', render, context_instance = RequestContext(request))

            teacher = clerk.create_role(Teacher)
            teacher.school = school
            teacher.save()

            return HttpResponseRedirect('/administrator/uni/userextended.Teacher/%d/edit/%d/' % (school.id, teacher.id))

    return render_to_response('~userextended/clerkAppendRole.html', render, context_instance = RequestContext(request))

def get_subject(request, id):
    subject = get_object_or_404(Subject, id = id)
    return HttpResponse(demjson.encode({'subject': subject.name, 'groups': subject.groups}))

def register_clerk(request):
    from django.contrib.auth import login, authenticate
    render = {}

    is_parent = auto_login = False
    
    if request.GET.get('auto_login', False):
        render['params'] = {'auto_login': '1'}
        auto_login = True
    if request.GET.get('is_parent', False):
        render['params']['is_parent'] = '1'
        is_parent = True

    if request.method == 'POST':
        render['form'] = form = ClerkRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if auto_login:
                if is_parent:
                    user.create_role(Parent)
                # FIXME: password
                user = authenticate(username = user.username, password = '123456789')
                login(request, user)
                return HttpResponseRedirect(reverse('odaybook.curatorship.views.send_parent_request'))
    else:
        render['form'] = ClerkRegisterForm()

    return render_to_response('~userextended/register_clerk.html', render, context_instance = RequestContext(request))