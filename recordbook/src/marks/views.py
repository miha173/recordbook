# -*- coding: UTF-8 -*-
from datetime import date

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from src.views import render_options
from src.userextended.models import Pupil, Teacher, Subject, Grade
from src.curatorship.models import Connection
from models import Lesson, Mark
from forms import LessonForm, MarkForm

@login_required
def index(request):
    render = render_options(request)
    if render['user_type'] == 'pupil':
        marks = Mark.objects.filter(pupil = Pupil.objects.get(id = request.user.id)).order_by('lesson__date')
#        marks_list = {}
#        for mark in marks:
#            if not mark.lesson.date.strftime('%d.%m.%Y') in marks_list:
#                marks_list[mark.lesson.date.strftime('%d.%m.%Y')] = []
#            marks_list[mark.lesson.date.strftime('%d.%m.%Y')].append({'absent': mark.absent, 'mark': mark.mark})
#        render['marks'] = marks_list
        render['marks'] = marks
    return render_to_response('marks/%s/index.html' % render['user_type'], render)

def set_current_subject(request, subject_id):
    teacher = Teacher.objects.get(id = request.user.id)
    teacher.current_subject = Subject.objects.get(id = subject_id)
    teacher.save()
    return HttpResponseRedirect(request.GET['next'])

def lessonList(request):
    render = render_options(request)
    teacher = Teacher.objects.get(id = request.user.id)
    try:
        render['lessons'] = Lesson.objects.filter(teacher = teacher,
                                                                    subject = teacher.current_subject)
    except ObjectDoesNotExist:
        render['lessons'] = {}
    return render_to_response('marks/teacher/lessonList.html', render) 

#Нужно проверять возможность учителя добавления записи к данному классу
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
        if mode == 'edit':
            form = LessonForm(request.POST)
            if form.is_valid():
                form = LessonForm(request.POST, instance = get_object_or_404(Lesson, id = id))
                form.save()
                return HttpResponseRedirect('/marks/lesson/')
            else:
                render['form'] = form
                return render_to_response('marks/teacher/lesson.html', render)
        else:
            form = LessonForm(request.POST)
            if form.is_valid():
                lesson = Lesson.objects.create(teacher = Teacher.objects.get(id = request.user.id),
                                               date = form.cleaned_data['date'],
                                               topic = form.cleaned_data['topic'],
                                               task = form.cleaned_data['task'],
                                               subject = Subject.objects.get(id = request.POST['current_subject']),
                                               grade = form.cleaned_data['grade']
                                               )
                lesson.save()
                return HttpResponseRedirect('/marks/lesson/')
            else:
                render['form'] = form
                return render_to_response('marks/teacher/lesson.html', render)

def gradeList(request):
    render = render_options(request)
    teacher = Teacher.objects.get(id = request.user.id)
    render['grades'] = teacher.grades.all()
    return render_to_response('marks/teacher/gradeList.html', render)

def gradeLessonList(request, grade_id):
    render = render_options(request)
    teacher = Teacher.objects.get(id = request.user.id)
    render['grade_id'] = grade_id
    render['lessons'] = Lesson.objects.filter(grade = Grade.objects.get(id = grade_id),
                                                                teacher = teacher,
                                                                subject = teacher.current_subject)
    return render_to_response('marks/teacher/gradeLessonList.html', render)

def markList(request, grade_id, lesson_id):
    render = render_options(request)
    pupils = Pupil.objects.filter(grade = Grade.objects.get(id = grade_id))
    connection = Connection.objects.get(grade = Grade.objects.get(id = grade_id), teacher = request.user)
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
