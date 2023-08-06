from django.db import models
from django.apps import apps
from django_eveonline_connector.models import EveAsset
from django_eveonline_doctrine_manager.utilities.abstractions import EveSkillList
from django_eveonline_doctrine_manager.models import EveFitting, EveSkillPlan, EveDoctrineSettings, EveDoctrine, EveCharacterDoctrineReport
from django_eveonline_connector.models import EveCharacter
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import permission_required, login_required
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django_eveonline_doctrine_manager.tasks import generate_character_report as generate_character_report_task
import json, logging 
logger = logging.getLogger(__name__)


@login_required
@permission_required("django_eveonline_doctrine_manager.create_evecharacterdoctrinereport")
@cache_page(60*5)
def generate_character_report(request):
    if 'external_id' not in request.GET:
        return HttpResponse(status=400)
    else:
        character_id = request.GET['external_id']

    generate_character_report_task(character_id)
    return HttpResponse(status=204)
    
    


@login_required
@permission_required('django_eveonline_doctrine_manager.view_evefitting', raise_exception=True)
@permission_required('django_eveonline_connector.view_eveasset', raise_exception=True)
@permission_required('django_eveonline_doctrine_manager.view_evedoctrine', raise_exception=True)
def get_character_report(request):
    if 'external_id' not in request.GET:
        return HttpResponse(status=400)
    
    character_report = EveCharacterDoctrineReport.objects.filter(character__external_id=request.GET['external_id']).first()
    if not character_report:
        return HttpResponse(status=404)

    return JsonResponse(character_report.get_report())

@login_required
def get_character_fittings(request):
    user = request.user 

    if 'external_id' not in request.GET:
        return HttpResponse(status=400)

    try:
        character = EveCharacter.objects.get(external_id=request.GET['external_id'])
        report = character.evecharacterdoctrinereport.get_report()['fittings']
    except Exception as e:
        logger.warning(e)
        return HttpResponse(status=404)

    if user.has_perm("django_eveonline_doctrine_manager.view_evecharacterdoctrinereport") or character.token.user == user:
        fittings = [] 
        for fitting_key in report:
            fitting_data = report[fitting_key]
            fitting_data['fitting_pk'] = fitting_key
            fittings.append(fitting_data)
        return JsonResponse({
            "fittings": fittings
        },safe=False)

    else:
        return HttpResponse(status=403)


@login_required
def get_character_doctrines(request):
    user = request.user

    if 'external_id' not in request.GET:
        return HttpResponse(status=400)

    try:
        character = EveCharacter.objects.get(
            external_id=request.GET['external_id'])
        report = character.evecharacterdoctrinereport.get_report()['doctrines']
    except Exception as e:
        logger.warning(e)
        return HttpResponse(status=404)

    if user.has_perm("django_eveonline_doctrine_manager.view_evecharacterdoctrinereport") or character.token.user == user:
        objects = []
        for pk in report:
            data = report[pk]
            doctrine = EveDoctrine.objects.get(pk=pk)
            objects.append({
                "doctrine_pk": doctrine.pk,
                "name": doctrine.name, 
                "has_skills": len(data['skill_ready_fittings']) > 0,
            })
        return JsonResponse({
            "doctrines": objects,
        }, safe=False)

    else:
        return HttpResponse(status=403)


@permission_required('django_eveonline_doctrine_manager.view_evefitting', raise_exception=True)
def skillcheck_utility(request):
    external_id = None 
    fitting = None 
    doctrine = None 
    skillplan = None 
    if 'external_id' not in request.GET:
        return HttpResponse(status=400)
    else:
        external_id = request.GET['external_id']
    if 'fitting_id' in request.GET:
        fitting = EveFitting.objects.get(pk=request.GET['fitting_id'])
    elif 'doctrine_id' in request.GET:
        doctrine = EveDoctrine.objects.get(pk=request.GET['doctrine_id'])
    elif 'skillplan_id' in request.GET:
        skillplan = EveSkillPlan.objects.get(pk=request.GET['skillplan_id'])
    else:
        return HttpResponse(status=400)

    character_report = EveCharacterDoctrineReport.objects.filter(
        character__external_id=request.GET['external_id']).first()
    
    if not character_report:
        logger.info(f"No character report found for {external_id}")
        return HttpResponse(status=400)
    else:
        character_report = character_report.get_report()

    if fitting:
        if str(fitting.pk) not in character_report['fittings']:
            logger.info(f"Fitting {fitting.pk} not found in character report for {external_id}")
            return HttpResponse(status=400)
        fitting_id = str(fitting.pk)
        fitting = character_report['fittings'][fitting_id]

        missing_skills = fitting['missing_skills']
        if missing_skills:
            return JsonResponse({
                'missing_skills': missing_skills
            }, status=200)
        else:
            return HttpResponse(status=204)

    elif skillplan:
        if skillplan.pk not in character_report['skillplans']:
            return HttpResponse(status=400)
        missing_skills = character_report['skillplans'][skillplan.pk].missing_skills
        if missing_skills:
            return JsonResponse({
                'missing_skills': missing_skills
            }, status=200)
        else:
            return HttpResponse(status=204)
    elif doctrine:
        if str(doctrine.pk) not in character_report['doctrines']:
            return HttpResponse(status=404)
        
        available_fittings = character_report['doctrines'][str(doctrine.pk)]['skill_ready_fittings']

        if available_fittings:
            return JsonResponse({
                'ships': available_fittings
            }, status=200)
        return HttpResponse(status=204)


@permission_required('django_eveonline_connector.view_eveasset', raise_exception=True)
def hangarcheck_utility(request):
    if 'external_id' not in request.GET:
        return HttpResponse(status=400)
    else:
        external_id = request.GET['external_id']
    if not EveDoctrineSettings.objects.all().count() > 0:
        return HttpResponse(status=400)
    if not EveDoctrineSettings.get_instance().staging_structure:
        return HttpResponse(status=400)
    else:
        location_id = EveDoctrineSettings.get_instance().staging_structure.structure_id

    character_report = EveCharacterDoctrineReport.objects.filter(
        character__external_id=request.GET['external_id']).first()
    if not character_report:
        logger.info(f"No character report for {external_id}")
        return HttpResponse(status=400)

    character_report = character_report.get_report()

    if 'fitting_id' in request.GET:
        fitting = EveFitting.objects.get(pk=request.GET['fitting_id'])
        fitting_id = str(fitting.pk)
        if fitting_id not in character_report['fittings']:
            return HttpResponse(status=400)
        
        fitting = character_report['fittings'][fitting_id]
        if fitting['in_hangar'] == True:
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=404)

    if 'doctrine_id' in request.GET:
        doctrine = request.GET['doctrine_id']
        if doctrine not in character_report['doctrines']:
            return HttpResponse(status=400)
        
        if character_report['doctrines'][doctrine]['hangar_ready_fittings']:
            return HttpResponse(status=204)
        else:
            return JsonResponse(character_report)


@permission_required('django_eveonline_doctrine_manager.view_evefitting', raise_exception=True)
def get_fitting(request):
    if 'fitting_id' not in request.GET:
        return HttpResponse(status=400)
    fitting = EveFitting.objects.get(pk=request.GET['fitting_id']).json
    return JsonResponse(fitting)
