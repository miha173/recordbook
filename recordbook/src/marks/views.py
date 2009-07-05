# -*- coding: UTF-8 -*-
from datetime import date

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator

from src.views import render_options, is_teacher
from src.userextended.models import Pupil, Teacher, Subject, Grade
from src.curatorship.models import Connection
from models import Lesson, Mark, ResultDate, Result
from forms import LessonForm, MarkForm, ResultForm

@login_required
def index(request):
    render = render_options(request)
    if render['user_type'] == 'pupil':
        marks = Mark.objects.filter(pupil = render['user']).order_by('-lesson__date')
        render_objects['marks'] = marks
    return render_to_response('marks/%s/index.html' % render['user_type'], render)

@login_required
@user_passes_test(is_teacher)
def set_current_subject(request, subject_id):
    teacher = Teacher.objects.get(id = request.user.id)
    teacher.current_subject = Subject.objects.get(id = subject_id)
    teacher.save()
    return HttpResponseRedirect(request.GET['next'])

@login_required
@user_passes_test(is_teacher)
def lessonList(request):
    render = render_options(request)
    teacher = Teacher.objects.get(id = request.user.id)
    paginator = Paginator(Lesson.objects.filter(teacher = teacher, subject = teacher.current_subject), 40)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        render['objects'] = paginator.page(page)
    except:
        render['objects'] = paginator.page(paginator.num_pages)
    render['paginator'] = paginator.num_pages - 1

    return render_to_response('marks/teacher/lessonList.html', render) 

#Нужно проверять возможность учителя добавления записи к данному классу
@login_required
@user_passes_test(is_teacher)
def lessonEdit(request, mode, id = 0):
    render = render_options(request)
    if request.method == 'GET':
        if mode == 'edit':
            render['form'] = LessonForm(instance = get_object_or_404(Lesson, id = id))
            grades_id = []
            for connection in Connection.objects.filter(teacher = request.user):
                grades_id.append(connection.grade.id)
            render['form'].fields['grade'].queryset = Grade.objects.filter(id__in = grades_id)
            render['lesson_id'] = id
            return render_to_response('marks/teacher/lesson.html', render)
        elif mode == 'delete': 
             lesson = get_object_or_404(Lesson, id = id)
             lesson.delete()
             return HttpResponseRedirect('/marks/lesson/')
        else:
            render['form'] = LessonForm()
            grades_id = []
            for connection in Connection.objects.filter(teacher = request.user):
                grades_id.append(connection.grade.id)
            render['form'].fields['grade'].queryset = Grade.objects.filter(id__in = grades_id)
            return render_to_response('marks/teacher/lesson.html', render)
    else:
        form = LessonForm(request.POST)
        grades_id = []
        for connection in Connection.objects.filter(teacher = request.user):
            grades_id.append(connection.grade.id)
        form.fields['grade'].queryset = Grade.objects.filter(id__in = grades_id)
        if mode == 'edit':
            if form.is_valid():
                form = LessonForm(request.POST, instance = get_object_or_404(Lesson, id = id))
                form.save()
                return HttpResponseRedirect('/marks/lesson/')
            else:
                render['form'] = form
                return render_to_response('marks/teacher/lesson.html', render)
        else:
            if form.is_valid():
                lesson = form.save(commit = False)
                lesson.teacher = render['user']
                lesson.subject = render['current_subject']
                lesson.save()
                form.save_m2m()
                return HttpResponseRedirect('/marks/lesson/')
            else:
                render['form'] = form
                return render_to_response('marks/teacher/lesson.html', render)

@login_required
@user_passes_test(is_teacher)
def gradeList(request):
    render = render_options(request)
    connections = Connection.objects.filter(teacher = request.user, subject = render['current_subject'])
    render['grades'] = []
    for connection in connections:
        render['grades'].append(connection.grade)
    return render_to_response('marks/teacher/gradeList.html', render)

@login_required
@user_passes_test(is_teacher)
def gradeLessonList(request, grade_id):
    render = render_options(request)
    teacher = Teacher.objects.get(id = request.user.id)
    render['grade_id'] = grade_id
    render['lessons'] = Lesson.objects.filter(grade = Grade.objects.get(id = grade_id),
                                                                teacher = teacher,
                                                                subject = teacher.current_subject)
    return render_to_response('marks/teacher/gradeLessonList.html', render)

@login_required
@user_passes_test(is_teacher)
def markList(request, grade_id, lesson_id):
    render = render_options(request)
    pupils = Pupil.objects.filter(grade = Grade.objects.get(id = grade_id))
    connection = Connection.objects.get(grade = Grade.objects.get(id = grade_id), 
                                        teacher = request.user,
                                        subject = render['current_subject'])
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
            mark_ = Mark.objects.get(lesson = Lesson.objects.get(id = lesson_id),
                                    pupil = pupil)
            mark = mark_.mark
            absent = mark_.absent
        except ObjectDoesNotExist:
            mark = 0
            absent = False
        pupils_list.append({'id': pupil.id, 'name': pupil.fi(), 'mark': mark, 'absent': absent})
    render['pupils'] = pupils_list
    return render_to_response('marks/teacher/markList.html', render)

@login_required
@user_passes_test(is_teacher)
def giveMark(request, grade_id, lesson_id):
    #Здесь есть скользкий момент, заключающийся в способе определения кому нужно выставлять отметки
    render = render_options(request)
    grade_id = int(grade_id)
    lesson_id = int(lesson_id)
    if not request.POST.get('send'):
        marks = []
        pupilsForMarks = []
        for pupil in Pupil.objects.filter(grade = grade_id):
            if request.POST.get('pupil-%d' % pupil.id):
                try:
                    mark = Mark.objects.get(lesson = Lesson.objects.get(id = lesson_id),
                                            pupil = pupil)
                    markForm = MarkForm(prefix = pupil.id, instance = mark)
                except ObjectDoesNotExist:
                    markForm = MarkForm(prefix = pupil.id)
                marks.append({'name': pupil.fi(), 'form': markForm})
                pupilsForMarks.append(pupil.id)
        #request.session['pupilsForMarks'] = pupilsForMarks
        render['marks'] = marks
        return render_to_response('marks/teacher/giveMark.html', render)
    else:
        #session = request.session.get('pupilsForMarks')
        error = 0
        for pupil in Pupil.objects.filter(grade = Grade.objects.get(id = grade_id)):
            if request.POST.get('%d-mark' % pupil.id) or request.POST.get('%d-absent' % pupil.id) or request.POST.get('%d-comment' % pupil.id):
                form = MarkForm(request.POST, prefix = pupil.id)
                if form.is_valid():
                    try:
                        mark = Mark.objects.get(pupil = Pupil.objects.get(id = pupil.id), 
                                                lesson = Lesson.objects.get(id = lesson_id))
                    except ObjectDoesNotExist:
                        mark = Mark()
                    mark.pupil = Pupil.objects.get(id = pupil.id)
                    mark.lesson = Lesson.objects.get(id = lesson_id)
                    mark.mark = form.cleaned_data['mark']
                    mark.absent = form.cleaned_data['absent']
                    mark.comment = form.cleaned_data['comment']
                    mark.save()
                else:
                    error = 1
        if error == 0:
            #del request.session['marks']
            return HttpResponseRedirect('/marks/grade/%d/' % grade_id)
        else: 
            marks = []
            for pupil in Pupil.objects.filter(grade = Grade.objects.get(id = grade_id)):
                if request.POST.get('%d-mark' % pupil.id) or request.POST.get('%d-absent' % pupil.id) or request.POST.get('%d-comment' % pupil.id):
                    marks.append({'name': pupil.fi(), 'form': MarkForm(request.POST, prefix = pupil.id)})
            render['marks'] = marks
            return render_to_response('marks/teacher/giveMark.html', render)

@login_required
@user_passes_test(is_teacher)
def gradeResultList(request):
    render = render_options(request)
    connections = Connection.objects.filter(teacher = request.user, subject = render['current_subject'])
    render['grades'] = []
    for connection in connections:
        render['grades'].append(connection.grade)
    render['resultdates'] = ResultDate.objects.filter(school = render['school'])
    return render_to_response('marks/teacher/gradeResultList.html', render)

@login_required
@user_passes_test(is_teacher)
def resultList(request):
    render = render_options(request)
    #Проверка доступа!!!
    #Здесь, как и раньше, есть скользкий момент, заключающийся в способе определения кому нужно выставлять отметки
    if not request.POST.get('send'):
        pupils = Pupil.objects.filter(grade = get_object_or_404(Grade, id = request.POST.get('grade')))
        resultdate_id = request.POST.get('resultdate')
        resultdate = ResultDate.objects.get(id = resultdate_id)
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
                                        lesson__subject = render['current_subject'])
            for mark in marks:
                if mark.mark:
                    sum += mark.mark
            if marks.__len__()<>0 and sum<>0:
                sa = round(float(sum)/float(marks.__len__()), 3)
            else:
                sa = 0
            results.append({'name': pupil.fi(), 'form': form, 'sa': sa})
        render['pupils'] = results
        render['grade_id'] = request.POST.get('grade')
        render['resultdate_id'] = resultdate_id
        return render_to_response('marks/teacher/resultList.html', render)
    else:
        error = 0
        for pupil in Pupil.objects.filter(grade = Grade.objects.get(id = request.POST.get('grade_id'))):
            if request.POST.get('%d-mark' % pupil.id):
                form = ResultForm(request.POST, prefix = pupil.id)
                if form.is_valid():
                    try:
                        result = Result.objects.get(pupil = Pupil.objects.get(id = pupil.id),
                                                    resultdate = ResultDate.objects.get(id = request.POST.get('resultdate_id')))
                    except ObjectDoesNotExist:
                        result = Result()
                    result.pupil = Pupil.objects.get(id = pupil.id)
                    result.resultdate = ResultDate.objects.get(id = request.POST.get('resultdate_id'))
                    result.mark = form.cleaned_data['mark']
                    result.subject = render['current_subject']
                    result.save()
                else:
                    error = 1
        if error == 0:
            return HttpResponseRedirect('/marks/result/')
        else: 
            results = []
            pupils = Pupil.objects.filter(grade = get_object_or_404(Grade, id = request.POST.get('grade')))
            for pupil in pupils:
                results.append({'name': pupil.fi(), 'form': resultsForm(request.POST, prefix = pupil.id)})
            render['results'] = results
            return render_to_response('marks/teacher/resultList.html', render)

@login_required
def marksView(request, subject_id):
    render = render_options(request)
    paginator = Paginator(Mark.objects.filter(pupil = render['user'], lesson__subject = get_object_or_404(Subject, id = subject_id)).order_by('-lesson__date'), 40)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        render['objects'] = paginator.page(page)
    except:
        render['objects'] = paginator.page(paginator.num_pages)
    render['paginator'] = paginator.num_pages - 1
    render['current_subject'] = int(subject_id)
    return render_to_response('marks/pupil/marks.html', render)