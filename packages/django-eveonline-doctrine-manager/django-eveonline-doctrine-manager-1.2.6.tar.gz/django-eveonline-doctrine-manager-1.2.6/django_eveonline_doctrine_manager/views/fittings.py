from django.views.generic.edit import FormView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django_eveonline_doctrine_manager.models import EveFitting
from django_eveonline_doctrine_manager.forms import EveFittingForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
import logging 
logger = logging.getLogger(__name__)

class FittingDetailView(DetailView):
    template_name = 'django_eveonline_doctrine_manager/adminlte/fittings/fitting_detail.html'
    pk_url_kwarg = "id"
    model = EveFitting 

class FittingAuditView(DetailView):
    template_name = 'django_eveonline_doctrine_manager/adminlte/fittings/fitting_audit.html'
    pk_url_kwarg = "id"
    model = EveFitting
class FittingListView(ListView):
    template_name = 'django_eveonline_doctrine_manager/adminlte/fittings/fitting_list.html'
    model = EveFitting 

class FittingCreateView(FormView):
    template_name = 'django_eveonline_doctrine_manager/adminlte/fittings/fitting_form.html'
    form_class = EveFittingForm
    success_url = reverse_lazy(
        'django-eveonline-doctrine-manager-fittings-list')

    def form_valid(self, form):
        try:
            fitting = EveFitting.objects.create(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                fitting=form.cleaned_data['fitting'],
            )
        except Exception as e:
            messages.error(
                self.request, "Failed to create fitting. Try again (carefully) and contact your administrator.")
            logger.error(e)
            return redirect(self.success_url)

        fitting.doctrines.set(form.cleaned_data['doctrines'])
        fitting.tags.set(form.cleaned_data['tags'])
        fitting.roles.set(form.cleaned_data['roles'])

        if 'refit_of' in form.cleaned_data and form.cleaned_data['refit_of']:
            fitting.refit_of = form.cleaned_data['refit_of']
            fitting.save()
        
        return super().form_valid(form)

class FittingUpdateView(UpdateView):
    model = EveFitting
    fields = ['name', 'description', 'fitting', 'refit_of', 'doctrines', 'tags', 'roles']
    template_name = 'django_eveonline_doctrine_manager/adminlte/fittings/fitting_form.html'
    pk_url_kwarg = "id"
    success_url = reverse_lazy(
        'django-eveonline-doctrine-manager-fittings-list')

    def form_valid(self, form):
        try:
            super().form_valid(form)
        except Exception as e:
            messages.error(
                self.request, "Failed to update fitting. Try again (carefully) and contact your administrator.")
            logger.error(e)

        return redirect(self.success_url)

class FittingDeleteView(DeleteView):
    model = EveFitting
    pk_url_kwarg = "id"
    template_name = 'django_eveonline_doctrine_manager/adminlte/fittings/fitting_delete.html'
    success_url = reverse_lazy(
        'django-eveonline-doctrine-manager-fittings-list')
