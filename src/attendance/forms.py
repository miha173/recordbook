# -*- coding: UTF-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render_to_response
from django.forms.util import ErrorList

from src import settings

class TimetableForm(forms.Form):
    def get_fields(self):
        str = ''
        for day in settings.WORKDAYS:
            str += "<tr><td colspan='3'><h3>%s</h3></td></tr>" % day[1]
            for lesson in settings.LESSON_NUMBERS:
                str +='''
<tr>
    <td rowspan="2"><a href='#' onclick="$('#id_l_s_''' + day[0] + '''_''' + lesson[0] + '''_2').val($('#id_l_s_''' + day[0] + '''_''' + lesson[0] + '''_1').val()); $('#id_l_r_''' + day[0] + '''_''' + lesson[0] + '''_2').val($('#id_l_r_''' + day[0] + '''_''' + lesson[0] + '''_1').val()); return false;">''' + lesson[1] + '''</a></td>
    <td>''' + self['l_s_%s_%s_1' % (day[0], lesson[0])].__str__() + '''</td>
    <td>''' + self['l_r_%s_%s_1' % (day[0], lesson[0])].__str__() + '''</td>
</tr>
<tr>
    <td>''' + self['l_s_%s_%s_2' % (day[0], lesson[0])].__str__() + '''</td>
    <td>''' + self['l_r_%s_%s_2' % (day[0], lesson[0])].__str__() + '''</td>
</tr>
<tr><td colspan='3'>&nbsp;</td></tr>
        '''
        return str

class RingTimetableForm(forms.Form):
    def get_fields(self):
        str = ''
        for day in settings.WORKDAYS:
            str += "<tr><td colspan='3'><h3>%s</h3></td></tr>" % day[1]
            for lesson in settings.LESSON_NUMBERS:
                str +='''
<tr>
<td>''' + lesson[1]  + '''</td>
    <td>''' + self['l_s_%s_%s' % (day[0], lesson[0])].__str__() + '''</td>
    <td>''' + self['l_e_%s_%s' % (day[0], lesson[0])].__str__() + '''</td>
</tr>
        '''
        return str




    