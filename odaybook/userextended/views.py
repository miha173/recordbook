# -*- coding: UTF-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings

from models import School, Clerk, Superviser, Teacher, Pupil, Parent, BaseUser
from forms import ClerkForm
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
    if filter_id:
        ext['school'] = get_object_or_404(School , id = filter_id)
    if request.user.type == 'Teacher':
        if app_model == 'userextended.School':
            ext['id'] = request.user.c.school.id
        else:
            ext['school'] = request.user.c.school
    
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
    Object = getattr(getattr(__import__('odaybook'), app).models, model)

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

    if filter_id:
        ext['school'] = get_object_or_404(School , id = filter_id)

    allowed_apps = [
            'userextended.Grade', 'userextended.Subject', 'userextended.Pupil',
            'userextended.Teacher', 'userextended.Staff', 'userextended.School',
            'userextended.Option', 'userextended.Achievement', 'marks.ResultDate',
            'curatorship.Connection',
    ]
    if app + '.' + model not in allowed_apps: raise Http404('Object not allowed')
    template = render['object_name'] = model.lower()
    Object = getattr(getattr(__import__('odaybook'), app).models, model)
    Form = getattr(getattr(__import__('odaybook'), app).forms, model + 'Form')

    url = '/administrator/uni/%s.%s/' % (app, model)
    if filter_id: url += str(filter_id) + '/'

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
        return render_to_response('~userextended/%s.html' % template, render, context_instance = RequestContext(request))
    if request.method == 'POST':
        if mode == 'edit':
            form = Form(data = request.POST, files = request.FILES, instance = get_object_or_404(Object, id = id, **ext), **ext)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(url)
            else:
                render['form'] = form
                return render_to_response('~/userextended/%s.html' % template, render, context_instance = RequestContext(request))
        else:
            form = Form(data = request.POST, **ext)
            if form.is_valid():
                form.save()
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

            if right == 'Superuser':
                if clerk.is_superuser:
                    # FIXME: сообщение
                    pass
                else:
                    clerk.is_superuser = True
                    clerk.save()

            if right == 'Superviser':
                if 'Supervisor' in clerk.get_roles_list_simple():
                    # FIXME: сообщение
                    pass
                else:
                    superviser = Superviser()
                    superviser.save()
                    baseuser = BaseUser.objects.get(id = superviser.id)
                    clerk.roles.add(baseuser)
                    clerk.save()

            if right == 'EduAdmin':
                school = get_object_or_404(School, id = request.GET.get('school_id', 0))
                if clerk.has_role('EduAdmin', school):
                    # FIXME: сообщение
                    pass
                else:
                    teacher = Teacher(edu_admin = True, school = school)
                    teacher.save()
                    baseuser = BaseUser.objects.get(id = teacher.id)
                    clerk.roles.add(baseuser)
                    clerk.save()

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
                school = get_object_or_404(School, id = request.GET.get('school_id', 0))
                if clerk.has_role('EduAdmin', school):
                    teacher = clerk.get_role_obj('EduAdmin', school)[0]
                    teacher.edu_admin = False
                    teacher.save()
                else:
                    # FIXME: сообщение
                    pass

            if right == 'Teacher':
                school = get_object_or_404(School, id = request.GET.get('school_id', 0))
                if clerk.has_role('Teacher', school):
                    teacher = clerk.get_role_obj('Teacher', school)[0]
                    clerk.roles.remove(teacher)
                    clerk.save()
                    teacher.delete()
                else:
                    # FIXME: сообщение
                    pass

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

def set_role(request, role_id):
    request.user.set_current_role(role_id, request.GET.get('type', ''))
    return HttpResponseRedirect('/')