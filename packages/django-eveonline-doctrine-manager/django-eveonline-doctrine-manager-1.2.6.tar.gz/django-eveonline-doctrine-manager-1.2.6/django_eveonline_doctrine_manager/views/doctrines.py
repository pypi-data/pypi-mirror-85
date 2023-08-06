from django.views.generic.edit import FormView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django_eveonline_doctrine_manager.models import EveDoctrine
from django_eveonline_doctrine_manager.forms import EveDoctrineForm
from django.urls import reverse_lazy
"""
Doctrine CRUD
"""

class DoctrineDetailView(DetailView):
    template_name = 'django_eveonline_doctrine_manager/adminlte/doctrines/doctrine_detail.html'
    pk_url_kwarg = "id"
    model = EveDoctrine


class DoctrineAuditView(DetailView):
    template_name = 'django_eveonline_doctrine_manager/adminlte/doctrines/doctrine_audit.html'
    pk_url_kwarg = "id"
    model = EveDoctrine

class DoctrineListView(ListView):
    template_name = 'django_eveonline_doctrine_manager/adminlte/doctrines/doctrine_list.html'
    model = EveDoctrine 


class DoctrineCreateView(FormView):
    template_name = 'django_eveonline_doctrine_manager/adminlte/doctrines/doctrine_form.html'
    form_class = EveDoctrineForm
    success_url = reverse_lazy(
        'django-eveonline-doctrine-manager-doctrines-list')

    def form_valid(self, form):
        doctrine = EveDoctrine.objects.create(
            name=form.cleaned_data['name'],
            description=form.cleaned_data['description'],
            category=form.cleaned_data['category']
        )
        doctrine.tags.set(form.cleaned_data['tags'])
        return super().form_valid(form)


class DoctrineUpdateView(UpdateView):
    model = EveDoctrine 
    fields = ['name', 'description', 'tags', 'category']
    pk_url_kwarg = "id"
    template_name = 'django_eveonline_doctrine_manager/adminlte/doctrines/doctrine_form.html'
    success_url = reverse_lazy(
        'django-eveonline-doctrine-manager-doctrines-list')

class DoctrineDeleteView(DeleteView):
    template_name = 'django_eveonline_doctrine_manager/adminlte/doctrines/doctrine_delete.html'
    model = EveDoctrine
    pk_url_kwarg = "id"
    success_url = reverse_lazy(
        'django-eveonline-doctrine-manager-doctrines-list')
