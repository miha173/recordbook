# -*- coding: UTF-8 -*-
from datetime import date

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.conf import settings

from src.userextended.models import Pupil, Teacher, Subject, Grade
from src.curatorship.models import Connection
from models import Lesson, Mark, ResultDate, Result
from forms import LessonForm, MarkForm, ResultForm

@login_required
def index(request):
    render = {}
    temp = request.user_type
    if request.user_type == 'pupil':
        results = Result.objects.filter(pupil = request.user).order_by('resultdate__enddate')
        render['results'] = results
    return render_to_response('marks/%s/index.html' % request.user_type, render, context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: u.prefix=='t')
def set_current_subject(request, subject_id):
    request.user.current_subject = Subject.objects.get(id = subject_id)
    request.user.save()
    next = request.GET.get('next', '').strip()
    if len(next) == 0:
        next = '/marks/'
    return HttpResponseRedirect(next)

@login_required
@user_passes_test(lambda u: u.prefix=='t')
def lessonList(request):
    render = {}
    if request.GET.get('search_str'): 
        objects = Lesson.objects.search(request.GET.get('search_str'))
        render['search_str'] = request.GET.get('search_str')
    else: objects = Lesson.objects
    paginator = Paginator(objects.filter(teacher = request.user, subject = request.user.current_subject), settings.PAGINATOR_OBJECTS)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        render['objects'] = paginator.page(page)
    except:
        render['objects'] = paginator.page(paginator.num_pages)
    render['paginator'] = paginator.num_pages - 1
    return render_to_response('marks/teacher/lessonList.html', render, context_instance = RequestContext(request)) 

#Нужно проверять возможность учителя добавления записи к данному классу
@login_required
@user_passes_test(lambda u: u.prefix=='t')
def lessonEdit(request, mode, id = 0):
    render = {}
    if request.method == 'GET':
        if mode == 'edit':
            lesson = get_object_or_404(Lesson, id = id, teacher = request.user)
            render['form'] = LessonForm(instance = lesson)
            grades_id = []
            for connection in Connection.objects.filter(teacher = request.user):
                grades_id.append(connection.grade.id)
            render['form'].fields['grade'].queryset = Grade.objects.filter(id__in = grades_id)
            render['lesson_id'] = id
            return render_to_response('marks/teacher/lesson.html', render, context_instance = RequestContext(request))
        elif mode == 'delete': 
             lesson = get_object_or_404(Lesson, id = id, teacher = request.user)
             lesson.delete()
             return HttpResponseRedirect('/marks/lesson/')
        else:
            render['form'] = LessonForm()
            grades_id = []
            for connection in Connection.objects.filter(teacher = request.user):
                grades_id.append(connection.grade.id)
            render['form'].fields['grade'].queryset = Grade.objects.filter(id__in = grades_id)
            return render_to_response('marks/teacher/lesson.html', render, context_instance = RequestContext(request))
    else:
        form = LessonForm(request.POST)
        grades_id = []
        for connection in Connection.objects.filter(teacher = request.user):
            grades_id.append(connection.grade.id)
        form.fields['grade'].queryset = Grade.objects.filter(id__in = grades_id)
        if mode == 'edit':
            if form.is_valid():
                lesson = get_object_or_404(Lesson, id = id, teacher = request.user)
                form = LessonForm(request.POST, instance = lesson)
                form.save()
                return HttpResponseRedirect('/marks/lesson/')
            else:
                render['form'] = form
                return render_to_response('marks/teacher/lesson.html', render, context_instance = RequestContext(request))
        else:
            if form.is_valid():
                lesson = form.save(commit = False)
                lesson.teacher = request.user
                lesson.subject = request.user.current_subject
                lesson.save()
                form.save_m2m()
                return HttpResponseRedirect('/marks/lesson/')
            else:
                render['form'] = form
                return render_to_response('marks/teacher/lesson.html', render, context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: u.prefix=='t')
def gradeList(request):
    render = {}
    connections = Connection.objects.filter(teacher = request.user, subject = request.user.current_subject)
    render['grades'] = []
    for connection in connections:
        render['grades'].append(connection.grade)
    return render_to_response('marks/teacher/gradeList.html', render, context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: u.prefix=='t')
def gradeLessonList(request, grade_id):
    render = {}
    render['grade_id'] = grade_id
    if Grade.objects.get(id = grade_id) in request.user.grades.all():
        render['lessons'] = Lesson.objects.filter(grade__id = grade_id, teacher = request.user, subject = request.user.current_subject)
        return render_to_response('marks/teacher/gradeLessonList.html', render, context_instance = RequestContext(request))
    else:
        return Http404

@login_required
@user_passes_test(lambda u: u.prefix=='t')
def markList(request, grade_id, lesson_id):
    render = {}
    grade = Grade.objects.get(id = grade_id)
    lesson = get_object_or_404(Lesson, id = lesson_id)
    if (grade in request.user.grades.all()) and (lesson.teacher == request.user):
        pupils = Pupil.objects.filter(grade = grade)
        connection = Connection.objects.get(grade = grade, teacher = request.user, subject = request.user.current_subject)
        if connection.connection == '1':
            pupils = pupils.filter(group = '1')
        if connection.connection == '2':
            pupils = pupils.filter(group = '2')
        if connection.connection == '3':
            pupils = pupils.filter(sex = '1')
        if connection.connection == '4':
            pupils = pupils.filter(sex = '2')
        if connection.connection == '5':
            pupils = pupils.filter(special = True)
        pupils_list = []
        for pupil in pupils:
            try:
                mark_ = Mark.objects.get(lesson = lesson, pupil = pupil)
                mark = mark_.mark
                absent = mark_.absent
            except ObjectDoesNotExist:
                mark = 0
                absent = False
            pupils_list.append({'id': pupil.id, 'name': pupil.fi(), 'mark': mark, 'absent': absent})
        render['pupils'] = pupils_list
        return render_to_response('marks/teacher/markList.html', render, context_instance = RequestContext(request))
    else:
        return Http404

@login_required
@user_passes_test(lambda u: u.prefix=='t')
def giveMark(request, grade_id, lesson_id):
    render = {}
    grade = get_object_or_404(Grade, id = grade_id)
    lesson = get_object_or_404(Lesson, id = lesson_id)
    if (grade in request.user.grades.all()) and (lesson.teacher == request.user):
        if not request.POST.get('send'):
            marks = []
            pupilsForMarks = []
            for pupil in Pupil.objects.filter(grade = grade):
                if request.POST.get('pupil-%d' % pupil.id):
                    try:
                        mark = Mark.objects.get(lesson = lesson, pupil = pupil)
                        markForm = MarkForm(prefix = pupil.id, instance = mark)
                    except ObjectDoesNotExist:
                        markForm = MarkForm(prefix = pupil.id)
                    marks.append({'name': pupil.fi(), 'form': markForm})
                    pupilsForMarks.append(pupil.id)
            render['marks'] = marks
            return render_to_response('marks/teacher/giveMark.html', render, context_instance = RequestContext(request))
        else:
            error = 0
            for pupil in Pupil.objects.filter(grade = grade):
                if request.POST.get('%d-mark' % pupil.id) or request.POST.get('%d-absent' % pupil.id):
                    form = MarkForm(request.POST, prefix = pupil.id)
                    if form.is_valid():
                        try:
                            mark = Mark.objects.get(pupil = Pupil.objects.get(id = pupil.id), 
                                                    lesson = lesson)
                        except ObjectDoesNotExist:
                            mark = Mark()
                        mark.pupil = Pupil.objects.get(id = pupil.id)
                        mark.lesson = lesson
                        mark.mark = form.cleaned_data['mark']
                        mark.absent = form.cleaned_data['absent']
                        mark.comment = form.cleaned_data['comment']
                        mark.save()
                    else:
                        error = 1
            if error == 0:
                return HttpResponseRedirect('/marks/grade/%d/' % grade.id)
            else: 
                marks = []
                for pupil in Pupil.objects.filter(grade = grade):
                    if request.POST.get('%d-mark' % pupil.id) or request.POST.get('%d-absent' % pupil.id):
                        marks.append({'name': pupil.fi(), 'form': MarkForm(request.POST, prefix = pupil.id)})
                render['marks'] = marks
                return render_to_response('marks/teacher/giveMark.html', render, context_instance = RequestContext(request))
    return Http404

@login_required
@user_passes_test(lambda u: u.prefix=='t')
def gradeResultList(request):
    render = {}
    connections = Connection.objects.filter(teacher = request.user, subject = request.user.current_subject)
    render['grades'] = []
    for connection in connections:
        render['grades'].append(connection.grade)
    render['resultdates'] = ResultDate.objects.filter(school = request.user.school)
    return render_to_response('marks/teacher/gradeResultList.html', render, context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: u.prefix=='t')
def gradeResult(request):
    render = {}
    grade = get_object_or_404(Grade, id = request.POST.get('grade'))
    resultdate = get_object_or_404(ResultDate, id = request.POST.get('resultdate'))
    render['grade'] = grade.id
    render['resultdate'] = resultdate.id
    if grade in request.user.grades.all():
        if not request.POST.get('send'):
            pupils = Pupil.objects.filter(grade = grade)
            results = []
            from math import pow
            for pupil in pupils:
                try:
                    result = Result.objects.get(resultdate = resultdate, pupil = pupil)
                    form = ResultForm(prefix = pupil.id, instance = result)
                except ObjectDoesNotExist:
                    form = ResultForm(prefix = pupil.id)
                sum = 0
                marks = Mark.objects.filter(lesson__date__range = (resultdate.startdate, resultdate.enddate), 
                                            pupil = pupil,
                                            lesson__subject = request.user.current_subject)
                for mark in marks:
                    if mark.mark:
                        sum += mark.mark
                if marks.__len__()<>0 and sum<>0:
                    sa = round(float(sum)/float(marks.__len__()), 3)
                else:
                    sa = 0
                results.append({'name': pupil.fi(), 'form': form, 'sa': sa})
            render['pupils'] = results
            return render_to_response('marks/teacher/gradeResult.html', render, context_instance = RequestContext(request))
        else:
            error = 0
            for pupil in Pupil.objects.filter(grade = grade):
                if request.POST.get('%d-mark' % pupil.id):
                    form = ResultForm(request.POST, prefix = pupil.id)
                    if form.is_valid():
                        try:
                            result = Result.objects.get(pupil = Pupil.objects.get(id = pupil.id),
                                                        resultdate = resultdate, subject = request.user.current_subject)
                        except ObjectDoesNotExist:
                            result = Result()
                        result.pupil = pupil
                        result.resultdate = resultdate
                        result.mark = form.cleaned_data['mark']
                        result.subject = request.user.current_subject
                        result.save()
                    else:
                        error = 1
            if error == 0:
                return HttpResponseRedirect('/marks/result/')
            else: 
                results = []
                pupils = Pupil.objects.filter(grade = grade)
                for pupil in pupils:
                    results.append({'name': pupil.fi(), 'form': ResultForm(request.POST, prefix = pupil.id)})
                render['pupils'] = results
                return render_to_response('marks/teacher/gradeResult.html', render, context_instance = RequestContext(request))
    else:
        return Http404

@login_required
def marksView(request, subject_id):
    render = {}
    paginator = Paginator(Mark.objects.filter(pupil = request.user, lesson__subject = get_object_or_404(Subject, id = subject_id)).order_by('-lesson__date'), settings.PAGINATOR_OBJECTS)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        render['objects'] = paginator.page(page)
    except:
        render['objects'] = paginator.page(paginator.num_pages)
    render['paginator'] = paginator.num_pages - 1
    request.user.current_subject = int(subject_id)
    return render_to_response('marks/pupil/marks.html', render, context_instance = RequestContext(request))