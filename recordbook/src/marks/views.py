# -*- coding: UTF-8 -*-
from datetime import date
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from src.userextended.models import Pupil, Teacher, Subject, Grade
from django.forms.models import modelformset_factory
from src.marks.models import Lesson, Mark
from src.marks.forms import LessonForm, MarkForm

def render_options(request):
    options = render_objects = options['render_objects'] = {}
    if request.user.username[0] == 't':
        user = Teacher.objects.get(id = request.user.id)
        subjects = []
        for subject in user.subjects.all():
            subjects.append({'id': subject.id, 'name': subject.name})
        if subjects.__len__() and not user.current_subject>0:
            user.current_subject = Subject.objects.get(id = subjects[0]['id'])
            user.save()
        render_objects['user'] = user
        render_objects['subjects'] = subjects
        render_objects['next'] = request.path
        options['render_objects'] = render_objects
        options['usertype'] = 'teacher'
        options['current_subject'] = user.current_subject
    else:
        user = Pupil.objects.get(id = request.user.id)
        options['usertype'] = 'pupil'
    return options

@login_required
def index(request):
    render = render_options(request)
    if render['usertype'] == 'pupil':
        marks = Mark.objects.filter(pupil = Pupil.objects.get(id = request.user.id)).order_by('lesson__date')
#        marks_list = {}
#        for mark in marks:
#            if not mark.lesson.date.strftime('%d.%m.%Y') in marks_list:
#                marks_list[mark.lesson.date.strftime('%d.%m.%Y')] = []
#            marks_list[mark.lesson.date.strftime('%d.%m.%Y')].append({'absent': mark.absent, 'mark': mark.mark})
#        render['render_objects']['marks'] = marks_list
        render['render_objects']['marks'] = marks
    return render_to_response('marks/%s/index.html' % render['usertype'], render['render_objects'])

def set_current_subject(request, subject_id):
    teacher = Teacher.objects.get(id = request.user.id)
    teacher.current_subject = Subject.objects.get(id = subject_id)
    teacher.save()
    return HttpResponseRedirect(request.GET['next'])

def lessonsList(request):
    render = render_options(request)
    teacher = Teacher.objects.get(id = request.user.id)
    try:
        render['render_objects']['lessons'] = Lesson.objects.filter(teacher = teacher,
                                                                    subject = teacher.current_subject)
    except ObjectDoesNotExist:
        render['render_objects']['lessons'] = {}
    return render_to_response('marks/teacher/lessons.html', render['render_objects']) 

#Помни, нужно фильтровать список класса
def lessonEdit(request, mode, id = 0):
    render = render_options(request)
    if request.method == 'GET':
        if mode == 'edit':
            render['render_objects']['form'] = LessonForm(instance = get_object_or_404(Lesson, id = id))
            render['render_objects']['lesson_id'] = id
            return render_to_response('marks/teacher/lesson.html', render['render_objects'])
        elif mode == 'delete': 
             lesson = get_object_or_404(Lesson, id = id)
             lesson.delete()
             return HttpResponseRedirect('/marks/lessons/')
        else:
            render['render_objects']['form'] = LessonForm()
            return render_to_response('marks/teacher/lesson.html', render['render_objects'])
    else:
        if mode == 'edit':
            form = LessonForm(request.POST)
            if form.is_valid():
                form = LessonForm(request.POST, instance = get_object_or_404(Lesson, id = id))
                form.save()
                return HttpResponseRedirect('/marks/lessons/')
            else:
                render['render_objects']['form'] = form
                return render_to_response('marks/teacher/lesson.html', render['render_objects'])
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
                return HttpResponseRedirect('/marks/lessons/')
            else:
                render['render_objects']['form'] = form
                return render_to_response('marks/teacher/lesson.html', render['render_objects'])

def gradesList(request):
    render = render_options(request)
    teacher = Teacher.objects.get(id = request.user.id)
    render['render_objects']['grades'] = teacher.grades.all()
    return render_to_response('marks/teacher/gradesList.html', render['render_objects'])

def gradeLessonsList(request, grade_id):
    render = render_options(request)
    teacher = Teacher.objects.get(id = request.user.id)
    render['render_objects']['grade_id'] = grade_id
    render['render_objects']['lessons'] = Lesson.objects.filter(grade = Grade.objects.get(id = grade_id),
                                                                teacher = teacher,
                                                                subject = teacher.current_subject)
    return render_to_response('marks/teacher/gradeLessonsList.html', render['render_objects'])

def marksList(request, grade_id, lesson_id):
    render = render_options(request)
    pupils = Pupil.objects.filter(grade = Grade.objects.get(id = grade_id))
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
    render['render_objects']['pupils'] = pupils_list
    return render_to_response('marks/teacher/marksList.html', render['render_objects'])

def giveMark(request, grade_id, lesson_id):
    #Очень сомнительное место, наверное самое сомнительное в коде
    #Каждая строчка полна отборного бреда
    #При выводе убрать списки! Это же полный ахтунг выводить всех учеников
#    render = render_options(request)
#    grade_id = int(grade_id)
    #Если мы ещё не отправляли форму
#    if not request.POST.get('max_num'):
#        max_num = 0
#        pupils = Pupil.objects.filter(grade = grade_id)
#        marks = []
#        for pupil in pupils:
#            if request.POST.get('pupil-%d' % pupil.id):
#                max_num += 1
#                #Полный ахтунг
#                mark = Mark.objects.get_or_create(pupil = pupil, lesson = Lesson.objects.get(id = request.POST.get('lesson')), mark = 0, absent = False)
#                marks.append(int(mark[0].id))
#        request.session['marks'] = marks
#    else:
#        max_num = int(request.POST.get('max_num'))
#    MarksFormSet = modelformset_factory(Mark, fields = ('mark', 'absent', 'comment', 'pupil'), max_num = max_num)
#    if not request.POST.get('send'):
#        render['render_objects']['marks'] = MarksFormSet(queryset = Mark.objects.filter(id__in = request.session['marks']))
#        render['render_objects']['max_num'] = max_num
#        return render_to_response('marks/teacher/giveMark.html', render['render_objects'])
#    else:
#        marks = MarksFormSet(request.POST, queryset = Mark.objects.filter(id__in = request.session['marks']))
#        if marks.is_valid():
#            marks.save()
#            return HttpResponseRedirect('/marks/grades/%d/' % grade_id)
#        else:
#            render['render_objects']['marks'] = marks
#            return render_to_response('marks/teacher/giveMark.html', render['render_objects'])
    
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
        render['render_objects']['marks'] = marks
        return render_to_response('marks/teacher/giveMark.html', render['render_objects'])
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
            return HttpResponseRedirect('/marks/grades/%d/' % grade_id)
        else: 
            marks = []
            for pupil in Pupil.objects.filter(grade = Grade.objects.get(id = grade_id)):
                if request.POST.get('%d-mark' % pupil.id) or request.POST.get('%d-absent' % pupil.id) or request.POST.get('%d-comment' % pupil.id):
                    marks.append({'name': pupil.fi(), 'form': MarkForm(request.POST, prefix = pupil.id)})
            render['render_objects']['marks'] = marks
            return render_to_response('marks/teacher/giveMark.html', render['render_objects'])
        