from django.views.generic.edit import FormView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django_eveonline_doctrine_manager.models import EveSkillPlan
from django_eveonline_doctrine_manager.forms import EveSkillPlanForm
from django.urls import reverse_lazy


class SkillPlanDetailView(DetailView):
    template_name = 'django_eveonline_doctrine_manager/adminlte/skillplans/skillplan_detail.html'
    pk_url_kwarg = "id"
    model = EveSkillPlan


class SkillPlanListView(ListView):
    template_name = 'django_eveonline_doctrine_manager/adminlte/skillplans/skillplan_list.html'
    model = EveSkillPlan


class SkillPlanCreateView(FormView):
    template_name = 'django_eveonline_doctrine_manager/adminlte/skillplans/skillplan_form.html'
    form_class = EveSkillPlanForm
    success_url = reverse_lazy(
        'django-eveonline-doctrine-manager-skillplans-list')

    def form_valid(self, form):
        skillplan = EveSkillPlan.objects.create(
            name=form.cleaned_data['name'],
            description=form.cleaned_data['description'],
        )

        skillplan.doctrines.set(form.cleaned_data['doctrines'])
        skillplan.tags.set(form.cleaned_data['tags'])
        skillplan.roles.set(form.cleaned_data['roles'])
        
        return super().form_valid(form)


class SkillPlanUpdateView(UpdateView):
    model = EveSkillPlan
    fields = ['name', 'description', 'skills', 'doctrines', 'tags', 'roles']
    template_name = 'django_eveonline_doctrine_manager/adminlte/skillplans/skillplan_form.html'
    pk_url_kwarg = "id"
    success_url = reverse_lazy(
        'django-eveonline-doctrine-manager-skillplans-list')


class SkillPlanDeleteView(DeleteView):
    model = EveSkillPlan
    pk_url_kwarg = "id"
    template_name = 'django_eveonline_doctrine_manager/adminlte/skillplans/skillplan_delete.html'
    success_url = reverse_lazy(
        'django-eveonline-doctrine-manager-skillplans-list')
