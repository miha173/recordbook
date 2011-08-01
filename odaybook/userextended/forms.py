# -*- coding: UTF-8 -*-
'''

'''
from django import forms
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm

from models import Subject, Teacher, Pupil, Grade, School, Staff, Option, Achievement, Clerk, PupilConnection

class SubjectForm(forms.ModelForm):
    u'''
        Форма для работы с дисциплинами определнной школы.
    '''
    def __init__(self, school = None, *args, **kwargs):
        self.school = school
        super(SubjectForm, self).__init__(*args, **kwargs)

    def save(self):
        result = super(SubjectForm, self).save(commit = False)
        result.school = self.school
        result.save()
        return result

    class Meta:
        model = Subject
        fields = ['name', 'groups']

class SchoolForm(forms.ModelForm):
    u'''
        Работа со школой.
    '''
    class Meta:
        model = School
        fields = ['name', 'saturday', 'url', 'address', 'phone',
                  'max_mark', 'gapps_use', 'gapps_login', 'gapps_password',
                  'gapps_domain', 'private_domain', 'private_salute'
        ]
    def __init__(self, school = None, *args, **kwargs):
        super(SchoolForm, self).__init__(*args, **kwargs)
        self.fields['gapps_password'].widget = forms.PasswordInput()
        self.fields['url'].initial = 'http://'

class OptionForm(forms.ModelForm):
    u'''
        Работа с различными настройками. 
    '''
    def __init__(self, school = None, *args, **kwargs):
        self.school = school
        super(OptionForm, self).__init__(*args, **kwargs)
    def save(self):
        result = super(OptionForm, self).save(commit = False)
        result.school = self.school
        result.save()
        return result
    class Meta:
        model = Option
        fields = ['value']

class GradeForm(forms.ModelForm):
    u'''
        Работа с учебными классами.
    '''
    def __init__(self, school = None, *args, **kwargs):
        self.school = school
        super(GradeForm, self).__init__(*args, **kwargs)

    def save(self):
        result = super(GradeForm, self).save(commit = False)
        result.school = self.school
        result.save()
        return result

    class Meta:
        model = Grade
        fields = ['number', 'long_name', 'small_name']

class ClerkForm(forms.ModelForm):
    u'''
        Форма для админа. Редактирование наиболее общих полей.
    '''
    class Meta:
        model = Clerk
        fields = [
            'last_name', 'first_name', 'middle_name', 'email', 'phone',
        ]

class PupilForm(forms.ModelForm):
    u'''
        Редактирование ученика *администратором школы или системы*.
    '''
    def __init__(self, school = None, *args, **kwargs):
        super(PupilForm, self).__init__(*args, **kwargs)
        self.school = school
        self.fields['grade'].queryset = Grade.objects.filter(school = school)
        
    class Meta:
        model = Pupil
        fields = [
                'last_name', 'first_name', 'middle_name', 'email', 'phone',
                'sex', 'grade', 'special', 'order', 'health_group', 'health_note',
                'parent_phone_1', 'parent_phone_2',
        ]
    def save(self, *args, **kwargs):
        if self.school:
            result = super(PupilForm, self).save(commit = False)
            result.school = self.school
            result.save()
            return result
        else:
            return super(PupilForm, self).save(*args, **kwargs)

class StaffForm(forms.ModelForm):
    u'''
        Форма редактирования персонала. На данный момент не используется
    '''
    def __init__(self, school = None, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        if not Option.objects.filter(school = school, key = 'TC_IP'):
            del self.fields['cart']
    class Meta:
        model = Staff
        fields = [
                'edu_admin', 'tech_admin',
        ]

class TeacherForm(forms.ModelForm):
    u'''
        Редактирование учителя.
    '''
    def __init__(self, school = None, *args, **kwargs):
        super(TeacherForm, self).__init__(*args, **kwargs)
        self.fields['grades'].queryset = Grade.objects.filter(school = school)
        self.fields['subjects'].queryset = Subject.objects.filter(school = school)
        self.fields['grade'].queryset = Grade.objects.filter(school = school)
        self.school = school
        self.fields['email'].required = True

    class Meta:
        model = Teacher
        fields = [
                'last_name', 'first_name', 'middle_name', 'edu_admin',
                'grade', 'grades', 'subjects', 'email',
        ]

    def save(self, *args, **kwargs):
        if self.school:
            result = super(TeacherForm, self).save(commit = False)
            result.school = self.school
            result.save()
            self.save_m2m()
            return result
        else:
            return super(TeacherForm, self).save(*args, **kwargs)
        
    grades = forms.ModelMultipleChoiceField(queryset = Grade.objects.all(),
                                            required = False,
                                            widget = forms.CheckboxSelectMultiple())
    subjects = forms.ModelMultipleChoiceField(queryset = Subject.objects.all(),
                                              required = False,
                                              widget = forms.CheckboxSelectMultiple())

class AchievementForm(forms.ModelForm):
    u'''
        Редактирование достижения. Вроде не используется.
    '''
    def __init__(self, pupil = None, *args, **kwargs):
        super(AchievementForm, self).__init__(*args, **kwargs)
        self.fields['date'].input_formats = ('%d.%m.%Y', )
        self.fields['date'].widget = forms.DateInput(format = '%d.%m.%Y')
        self.fields['date'].help_text = u'В формате ДД.ММ.ГГГГ'

    class Meta:
        model = Achievement
        fields = ['title', 'description', 'date']

class PupilConnectionForm(forms.ModelForm):
    u'''
        Форма для привзяки ученика к конкретной группе по конкретному предмету.
    '''
    def __init__(self, subject, pupil = None, *args, **kwargs):
        if PupilConnection.objects.filter(pupil = pupil, subject = subject):
            kwargs['instance'] = PupilConnection.objects.get(pupil = pupil, subject = subject)
        super(PupilConnectionForm, self).__init__(*args, **kwargs)
        self.pupil = pupil
        self.subject = subject
        choices = zip(*(range(1, int(subject.groups)+1), )*2)
        choices.insert(0, ('0', u'Вне групп'))
        self.fields['value'] = forms.ChoiceField(
                choices = choices,
                label = subject.name,
        )
        self.fields['value'].empty_label = '-'*25

    def save(self, *args, **kwargs):
        result = super(PupilConnectionForm, self).save(commit = False)
        if 'pupil' in kwargs:
            result.pupil = kwargs['pupil']
        else:
            result.pupil = self.pupil
        result.subject = self.subject
        result.save()

    class Meta:
        model = PupilConnection
        fields = ['value']

class ClerkRegisterForm(forms.ModelForm):
    u'''
        Создание пользователя.
    '''
    class Meta:
        model = Clerk
        fields = ['last_name', 'first_name', 'middle_name', 'email']

    def __init__(self, *args, **kwargs):
        super(ClerkRegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['last_name'].required = True
        self.fields['first_name'].required = True

    def clean_email(self):
        u'''
            Контрольна уникальной email.
        '''
        if Clerk.objects.filter(email = self.cleaned_data['email']):
            raise forms.ValidationError(u'Пользователь с таким email уже зарегистрирован.')
        return self.cleaned_data['email']

class PasswordChangeForm(DjangoPasswordChangeForm):
    u'''
        Увы, традиционная форма смены пароля не подходит из-за особенностей
        работы системы с пользователями.
    '''
    def save(self, commit=True):
        self.user.clerk.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.clerk.save()
        return self.user.clerk

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.clerk.check_password(old_password):
            raise forms.ValidationError(u'Ваш старый пароль введён некорректно. Попробуйте ещё раз.')
        return old_password

class ImportForm(forms.Form):
    u'''
        FilField для всяких импортов.
    '''
    file = forms.FileField()