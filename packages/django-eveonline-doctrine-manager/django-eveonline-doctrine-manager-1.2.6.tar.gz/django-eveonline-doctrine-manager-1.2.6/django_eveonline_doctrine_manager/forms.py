from django import forms

from django_eveonline_doctrine_manager.models import (EveDoctrineManagerTag, 
    EveDoctrineCategory, 
    EveDoctrineRole,
    EveDoctrine,
    EveFitting,
    EveSkillPlan)

class EveDoctrineForm(forms.Form):
    name = forms.CharField(max_length=32, required=True)
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': "wysihtml5"}))
    tags = forms.ModelMultipleChoiceField(
        queryset=EveDoctrineManagerTag.objects.all(),
        required=False)
    category = forms.ModelChoiceField(
        queryset=EveDoctrineCategory.objects.all(),
        required=False)

class EveFittingForm(forms.Form):
    name = forms.CharField(max_length=32, required=True)
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': "wysihtml5"}), required=False)
    fitting = forms.CharField(widget=forms.Textarea, required=True)
    
    refit_of = forms.ModelChoiceField(
        queryset=EveFitting.objects.all(),
        required=False
    )
    doctrines = forms.ModelMultipleChoiceField(
        queryset=EveDoctrine.objects.all(),
        required=False
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=EveDoctrineManagerTag.objects.all(),
        required=False)
    roles = forms.ModelMultipleChoiceField(
        queryset=EveDoctrineRole.objects.all(),
        required=False)


class EveSkillPlanForm(forms.Form):
    name = forms.CharField(max_length=32, required=True)
    skills = forms.CharField(widget=forms.Textarea, required=True)
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': "wysihtml5"}), required=False)
    
    doctrines = forms.ModelMultipleChoiceField(
        queryset=EveDoctrine.objects.all(),
        required=False
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=EveDoctrineManagerTag.objects.all(),
        required=False)
    roles = forms.ModelMultipleChoiceField(
        queryset=EveDoctrineRole.objects.all(),
        required=False)

