from celery import task, shared_task
from django_eveonline_doctrine_manager.models import EveDoctrine, EveDoctrineSettings, EveCharacterDoctrineReport, EveFitting
from django_eveonline_connector.models import EveSkill, EveCharacter, EveCorporation, EveAsset
from .utilities.fittings import get_required_skills, get_market_format
import logging, json
logger = logging.getLogger(__name__)

@shared_task
def update_character_reports():
    """
    Update characters that can use/have doctrine ships 
    """
    characters = EveCharacter.objects.filter(corporation__track_characters=True)
    for character in characters:
        generate_character_report.apply_async(args=[character.external_id])

@shared_task
def generate_character_report(character_id):
    character = EveCharacter.objects.get(external_id=character_id)
    character_report = EveCharacterDoctrineReport.objects.get_or_create(
        character=character)[0]
    character_report_json = character_report.reset().get_report()
    doctrines = EveDoctrine.objects.all() 
    if EveDoctrineSettings.get_instance().staging_structure:
        location_id = EveDoctrineSettings.get_instance().staging_structure.structure_id 
    else:
        location_id = None

    fittings = {}
    skill_plans = {}

    for doctrine in doctrines:

        skill_ready_fittings = []
        hangar_ready_fittings = []
        for fitting in doctrine.fittings:
            missing_skills = fitting.get_missing_skills(character_id)
            if location_id:
                logger.debug(f"Location ID set for doctrine settings, searching assets for {fitting.ship_id} at {location_id}")
                in_hangar = EveAsset.objects.filter(entity=character, 
                    type_id=fitting.ship_id, 
                    location_id=location_id).exists()
                logger.debug(f"Found ship in hangar: {in_hangar}")
            else:
                in_hangar = None 

            doctrine_fitting = {
                "name": fitting.name,
                "type_id": fitting.ship_id,
            }
            if not missing_skills:
                skill_ready_fittings.append(doctrine_fitting)

            if in_hangar:
                hangar_ready_fittings.append(doctrine_fitting)

            fittings[fitting.pk] = {
                "name": fitting.name,
                "type_id": fitting.ship_id,
                "missing_skills": missing_skills,
                "in_hangar": in_hangar,
            }

        for skillplan in doctrine.skill_plans:
            missing_skills = skillplan.get_required_skills().get_missing_skills(character_id)
            
            skill_plans[skillplan.pk] = {
                "name": skillplan.name,
                "missing_skills": missing_skills
            }

        character_report_json['doctrines'][doctrine.pk] = {
            "name": doctrine.name,
            "skill_ready_fittings": skill_ready_fittings,
            "hangar_ready_fittings": hangar_ready_fittings
        }

    character_report_json["fittings"] = fittings 
    character_report_json["skillplans"] = skill_plans

    character_report.save_report(character_report_json)

"""
Fitting Tasks
Backend tasks for fittings.
"""
@shared_task
def populate_fitting_fields(fitting_id):
    fitting = EveFitting.objects.get(pk=fitting_id)
    required_skills_raw = json.dumps(get_required_skills(fitting))
    market_format_raw = get_market_format(fitting)

    fitting.required_skills_raw = required_skills_raw
    fitting.market_format_raw = market_format_raw
    fitting.save(update_fields=['required_skills_raw', 'market_format_raw'])