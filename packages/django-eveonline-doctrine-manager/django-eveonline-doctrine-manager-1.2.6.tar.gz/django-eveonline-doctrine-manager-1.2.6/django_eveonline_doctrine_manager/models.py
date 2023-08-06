from django.db import models
from django.apps import apps
from django_eveonline_connector.models import EveStructure, EveEntity, EveCharacter, EveContract
from django_eveonline_connector.utilities.static.universe import resolve_type_name_to_type_id
from django_eveonline_doctrine_manager.utilities.abstractions import EveSkillList
from django.core.validators import MaxValueValidator, MinValueValidator
from django_singleton_admin.models import DjangoSingleton
from .utilities.fittings import parse_eft_format, get_required_skills, get_market_format, get_ship_name
import json, logging, re, roman

logger = logging.getLogger(__name__)

"""
Helper functions
"""

bootstrap_color_choices = (
    ('primary', 'Blue'),
    ('secondary', 'Gray'),
    ('success', 'Green'),
    ('danger', 'Red'),
    ('warning', 'Yellow'),
    ('info', 'Light Blue'),
    ('dark', 'Dark Gray'),
)


def get_skill_names_from_static_dump():
    import django_eveonline_doctrine_manager
    import os
    pth = os.path.dirname(django_eveonline_doctrine_manager.__file__)
    with open(pth + '/export/skills.json', 'r') as fp:
        skills = json.load(fp)

    return [ (skill, skill) for skill in skills.keys()]

class EveDoctrineSettings(DjangoSingleton):
    staging_structure = models.OneToOneField(EveStructure, on_delete=models.SET_NULL, null=True, blank=True)
    contract_entity = models.OneToOneField(EveEntity, on_delete=models.SET_NULL, null=True, blank=True)
    seeding_contract_prefix = models.CharField(max_length=12, blank=True, null=True, default=None)
    seeding_enabled = models.BooleanField(default=False)

    @staticmethod
    def get_instance():
        return EveDoctrineSettings.objects.all()[0]

    class Meta:
        verbose_name = "Doctrine Settings"
        verbose_name_plural = "Doctrine Settings"

"""
Core models
These are the main data models for the doctrine manager
"""
class EveDoctrine(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField("EveDoctrineManagerTag", blank=True)
    category = models.ForeignKey(
        "EveDoctrineCategory", on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def fittings(self):
        return EveFitting.objects.filter(doctrines__in=[self])
    
    @property
    def skill_plans(self):
        return EveSkillPlan.objects.filter(doctrines__in=[self])

    @property
    def character_list(self):
        return EveCharacter.objects.filter(corporation__track_characters=True)

    def __str__(self):
        return self.name
    
class EveFitting(models.Model):
    name = models.CharField(max_length=32)
    fitting = models.TextField()  # eft format
    description = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField("EveDoctrineManagerTag", blank=True)
    doctrines = models.ManyToManyField("EveDoctrine", blank=True)
    roles = models.ManyToManyField("EveDoctrineRole", blank=True)
    # eve static info
    ship_id = models.IntegerField(editable=False, blank=True, null=True)
    ship_name = models.CharField(max_length=128, default="Unknown Hull")
    # associations 
    refit_of = models.ForeignKey("EveFitting", blank=True, null=True, default=None, on_delete=models.CASCADE)
    # globs
    required_skills_raw = models.TextField()
    parsed_format_raw = models.TextField(null=True, blank=True)
    market_format_raw = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.ship_id = resolve_type_name_to_type_id(get_ship_name(self))
        self.ship_name = get_ship_name(self)
        self.parsed_format_raw = json.dumps(parse_eft_format(self))
        super(EveFitting, self).save(*args, **kwargs)

    @property
    def market_format(self):
        return self.market_format_raw

    @property
    def parsed_format(self):
        return dict(json.loads(self.parsed_format_raw))

    @property
    def required_skills(self):
        return dict(json.loads(self.required_skills_raw))

    @property
    def refits(self):
        return EveFitting.objects.filter(refit_of=self)
    
    @property
    def character_list(self):
        return EveCharacter.objects.filter(corporation__track_characters=True)

    def get_missing_skills(self, character_id):
        character = EveCharacter.objects.get(external_id=character_id)
        return EveSkillList.get_missing_skills_from_json(self.required_skills, character_id)

class EveSkillPlan(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(blank=True, null=True)
    skills = models.TextField()
    tags = models.ManyToManyField("EveDoctrineManagerTag", blank=True)
    doctrines = models.ManyToManyField("EveDoctrine", blank=True)
    roles = models.ManyToManyField("EveDoctrineRole", blank=True)

    def save(self, *args, **kwargs):
        super(EveSkillPlan, self).save(*args, **kwargs)

    def get_required_skills(self):
        cleaned_skill_list = []
        # clean skills from "SKILL V" format to "SKILL 1"
        skills = self.skills
        skills = skills.replace("<p>", "").replace("</p>", "")
        skills = skills.replace("<br>", "\n")
        for skill in filter(None, skills.split("\n")):
            skill_name = " ".join(skill.split(" ")[:-1])
            skill_level = roman.fromRoman("".join(skill.split(" ")[-1:]).rstrip("\n\r"))
            cleaned_skill_list.append(f"{skill_name} {skill_level}")
        return EveSkillList.from_list(cleaned_skill_list)

    def __str__(self):
        return self.name    

class EveFittingMarketRule(models.Model):
    fitting = models.OneToOneField(EveFitting, on_delete=models.CASCADE)
    requested_stock = models.IntegerField()
    structure = models.ForeignKey(EveStructure, on_delete=models.CASCADE)

    def __str__(self):
        return f"<{self.requested_stock} {self.fitting.name} @ {self.structure.name}>"

    @property 
    def required_name(self):
        prefix = EveDoctrineSettings.get_instance().seeding_contract_prefix
        if prefix:
            title = prefix + self.fitting.name
        else:
            title = self.fitting.name
        return title 

    @property
    def current_stock(self):
        title=self.required_name
        return EveContract.objects.filter(end_location_id=self.structure.structure_id, title=title, status="outstanding").count()

"""
Grouping models
Used to group fittings and doctrines for users and clarity.
"""
class EveRequiredSkill(models.Model):
    name = models.CharField(
        max_length=64, choices=get_skill_names_from_static_dump())
    level = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)])
    skill_for = models.ForeignKey("EveSkillPlan", on_delete=models.CASCADE)

class EveDoctrineRole(models.Model):
    name = models.CharField(max_length=128)
    icon = models.URLField()
    color = models.CharField(max_length=32, choices=bootstrap_color_choices)


    def __str__(self):
        return self.name

class EveDoctrineCategory(models.Model):
    name = models.CharField(max_length=128)
    icon = models.URLField()
    color = models.CharField(max_length=32, choices=bootstrap_color_choices)

    def __str__(self):
        return self.name

class EveDoctrineManagerTag(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


"""
Reports
"""
class EveCharacterDoctrineReport(models.Model):
    """
    JSON report in the following format:
        {
            doctrines: [ Object doctrine (see below)],
            fittings: [ Object fitting (see below)],
            skillplans: [ Object skillplan (see below)],
        }

    Object formats
        doctrine: {
            "name": string, 
            skill_ready_fittings: [],
            hangar_ready_fittings: [],
        }

        fitting: {
            name: string, 
            type_name: string
            type_id: int
            missing_skills: {},
            in_hangar: bool
        }

        skillplan: {
            name: string,
            missing_skills: {},
        }
    """
    character = models.OneToOneField(EveCharacter, on_delete=models.CASCADE)
    data = models.TextField()

    # def save(self, *args, **kwargs):
    #     self.data = json.dumps(self.data)
    #     super(EveCharacterDoctrineReport, self).save(*args, **kwargs)

    def reset(self):
        self.data = json.dumps({
            "doctrines": {},
            "fittings": {},
            "skillplans": {}
        })
        self.save()
        return self

    def save_report(self, report):
        self.data = json.dumps(report, sort_keys=True, indent=4)
        self.save()

    def get_report(self):
        return dict(json.loads(self.data))
