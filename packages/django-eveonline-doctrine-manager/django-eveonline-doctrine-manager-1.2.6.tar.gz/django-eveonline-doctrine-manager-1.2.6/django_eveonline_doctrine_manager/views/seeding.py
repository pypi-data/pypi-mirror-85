from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django_eveonline_doctrine_manager.models import EveFittingMarketRule
from django_eveonline_connector.tasks import update_character_contracts
from django.contrib import messages
from celery import group

class FittingMarketRuleListView(ListView):
    template_name = 'django_eveonline_doctrine_manager/adminlte/fittings/fitting_market_rules.html'
    model = EveFittingMarketRule

def update_stock(request):
    tokens = request.user.eve_tokens.all()
    characters = [token.evecharacter for token in tokens]
    job_group = group([update_character_contracts.s(character.external_id) for character in characters])
    dispatched_group = job_group.apply_async()
    messages.warning(request, "Contract update queued in the backend, refresh in a minute or so.")
    return redirect('django-eveonline-doctrine-manager-fittings-market')
