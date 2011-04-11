# -*- coding: UTF-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings

from odaybook.views import render_options, is_teacher
from odaybook.userextended.models import Subject, Grade
from models import Test, Question, VariantA, VariantB
from forms import TestForm, VariantAForm, VariantBForm, QuestionForm

@login_required
@user_passes_test(is_teacher)
def index(request):
    return render_to_response('index.html', render_options(request))

def testList(request):
    render = render_options(request)
    paginator = Paginator(Test.objects.filter(teacher = request.user), settings.PAGINATOR_OBJECTS)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        render['objects'] = paginator.page(page)
    except:
        render['objects'] = paginator.page(paginator.num_pages)
    render['paginator'] = paginator.num_pages - 1
    return render_to_response('testList.html', render)

@login_required
@user_passes_test(is_teacher)
def testEdit(request, mode, id = 0):
    render = render_options(request)
    if request.method == 'GET':
        if mode == 'add':
            form = TestForm()
        elif mode == 'edit':
            form = TestForm(instance = get_object_or_404(Test, id = id))
        else:
            get_object_or_404(Test, id = id).delete()
            return HttpResponseRedirect('/tests/test/')
        form.fields['subject'].queryset = request.user.subjects
        form.fields['grades'].queryset = request.user.grades
        del form.fields['share']
        render['form'] = form
        return render_to_response('test.html', render)
    else:
        if mode == 'add':
            form = TestForm(request.POST)
            if form.is_valid():
                test = form.save(commit = False)
                test.teacher = request.user
                test.save()
                form.save_m2m()
                return HttpResponseRedirect('/tests/test/')
            else:
                form.fields['subject'].queryset = request.user.subjects
                form.fields['grades'].queryset = request.user.grades
                del form.fields['share']
                render['form'] = form
                return render_to_response('test.html', render)
        elif mode == 'edit':
            form = TestForm(request.POST, instance = get_object_or_404(Test, id = id))
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/tests/test/')
            else:
                form.fields['subject'].queryset = request.user.subjects
                form.fields['grades'].queryset = request.user.grades
                del form.fields['share']
                render['form'] = form
                return render_to_response('test.html', render)
        else:
            return HttpResponseRedirect('/tests/test/')

def questionList(request, test_id):
    render = render_options(request)
    variantsA = {}
    variantsB = {}
    questions = Question.objects.filter(test = get_object_or_404(Test, id = test_id))
    for question in questions:
        if question.type == 'A':
            variantsA[question.number] = VariantA.objects.filter(question = question)
        else:
            variantsB[question.number] = VariantB.objects.filter(question = question)
    render['variantsA'] = variantsA
    render['variantsB'] = variantsB
    render['test'] = test_id
    return render_to_response('variants.html', render)

def questionEdit(request, mode, type, test_id, question_id = 0):
    render = render_options(request)
    if request.method == 'GET':
        if mode == 'add':
            render['form'] = QuestionForm()
        elif mode == 'edit':
            render['form'] = QuestionForm(instance = get_object_or_404(Question, id = question_id))
        else:
            question = get_object_or_404(Question, id = question_id)
            question.delete()
            return HttpResponseRedirect('/tests/test/%s/' % test_id)
        return render_to_response('question.html', render)
    else:
        if mode == 'add':
            form = QuestionForm(request.POST)
            if form.is_valid():
                from django.db.models import Max
                question = form.save(commit = False)
                question.test = get_object_or_404(Test, id = test_id)
                question.type = type
                number = Question.objects.aggregate(Max('number'))['number__max']
                if number == None:
                    number = 0
                question.number = number + 1
                question.save()
                return HttpResponseRedirect('/tests/test/%s/#%s' % (test_id, question.id))
            else:
                return render_to_response('question.html', render)
        elif mode == 'edit':
            form = QuestionForm(request.POST, instance = get_object_or_404(Question, id = question_id))
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/tests/test/%s/#%s' % (test_id, question.id))
            else:
                return render_to_response('question.html', render)
        else:
            return HttpResponseRedirect('/tests/test/%s/' % test_id)
        
def variantEdit(request, mode, type, test_id, variant_id = 0, question_id = 0):
    render = render_options(request)
    if type == 'A':
        Form = VariantAForm
        Obj = VariantA
    if type == 'B':
        Form = VariantBForm
        Obj = VariantB
    if request.method == 'GET':
        if mode == 'add':
            render['form'] = Form()
        elif mode == 'edit':
            obj = get_object_or_404(Obj, id = variant_id)
            render['form'] = Form(instance = obj)
            render['answer'] = obj.answer
        else:
            obj = get_object_or_404(Obj, id = variant_id)
            obj.delete()
            return HttpResponseRedirect('/tests/test/%s/' % test_id)
        return render_to_response('variant%s.html' % type, render)
    else:
        if mode == 'add':
            form = Form(request.POST)
            if form.is_valid():
                obj = form.save(commit = False)
                obj.question = get_object_or_404(Question, id = question_id)
                obj.save()
                return HttpResponseRedirect('/tests/test/%s/#%s' % (test_id, obj.id))
            else:
                return render_to_response('variant%s.html' % type, render)
        elif mode == 'edit':
            obj = get_object_or_404(Obj, id = variant_id)
            form = Form(request.POST, instance = obj)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/tests/test/%s/#%s' % (test_id, obj.id))
            else:
                return render_to_response('variant%s.html' % type, render)
        else:
            return HttpResponseRedirect('/tests/test/%s/' % test_id)
        