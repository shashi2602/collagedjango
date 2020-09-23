import django_filters
from django_filters import CharFilter
from django import forms
from .models import *

class Showassignmentsfilter(django_filters.FilterSet):
    Pin=CharFilter(field_name="submit_by__username",label="Pinnumber")
    dpt=django_filters.ChoiceFilter(choices=[ [o.shortname,o.name] for o in Dept.objects.all()],field_name="assignment__dept__shortname",label="departments")
    yr=django_filters.ChoiceFilter(choices=LIST_YEARS,field_name="assignment__year",label="year")
    sub=django_filters.ChoiceFilter(choices=[ [o.short_name,o.short_name] for o in Subjects.objects.all()],field_name="assignment__subject__short_name",label="subject")
    class Meta:
        model= SubmitAssignment
        fields=["Pin","dpt","yr","sub"]