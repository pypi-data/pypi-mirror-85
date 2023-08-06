from django_eveonline_connector.models import EveCharacter, EveSkill
class EveSkillList():
    def __init__(self):
        self.skill_list = []
        self.skill_key = set()

    @staticmethod
    def from_list(skill_list):

        ESL = EveSkillList()
        for skill in skill_list:
            ESL.add_skill({
                'name': " ".join(skill.split(" ")[:-1]),
                'level': "".join(skill.split(" ")[-1:]).rstrip("\n\r")
            })
        return ESL 

    @staticmethod
    def from_json(skill_json):
        ESL = EveSkillList()
        for key in skill_json:
            ESL.add_skill({
                'name': key, 
                'level': skill_json[key]
            })
        return ESL
        

    def add_skill(self, skill):
        for level in range(1, int(skill['level'])+1):
            skill_to_add = f"{skill['name']} {level}"
            if skill_to_add in self.skill_key:
                continue
            self.skill_list.append(skill_to_add)
            self.skill_key.add(skill_to_add)

    def to_json(self):
        json_response = {}
        for skill in self.skill_list:
            skill_name = " ".join(skill.split(
                " ")[:-1])
            skill_level = "".join(skill.split(" ")[-1:]).rstrip("\n\r")

            if skill_name in json_response:
                if skill_level > json_response[skill_name]:
                    json_response[skill_name] = skill_level
            else:
                json_response[skill_name] = skill_level
        return json_response

    def get_missing_skills(self, external_id):
        """
        Expects a skill json to check against a character's skills
        """
        skills_json = {} 
        for skill in self.skill_list:
            skill_name = " ".join(skill.split(
                " ")[:-1])
            skill_level = "".join(skill.split(" ")[-1:]).rstrip("\n\r")
            if skill_name in skills_json and skills_json[skill_name] < skill_level:
                skills_json[skill_name] = skill_level 
            elif skill_name not in skills_json:
                skills_json[skill_name] = skill_level 
                
        missing_skills = []
        for skill in skills_json.keys():
            if EveSkill.objects.filter(skill_name=skill, trained_skill_level__gte=skills_json[skill], entity__external_id=external_id).exists():
                pass
            else:
                missing_skills.append({
                    'name': skill, 
                    'level': skills_json[skill]
                })
        return missing_skills

    # TODO: refactor this crap lol
    @staticmethod
    def get_missing_skills_from_json(skills_json, external_id):
        """
        Expects a skill json to check against a character's skills
        """
        missing_skills = []
        for skill in skills_json.keys():
            if EveSkill.objects.filter(skill_name=skill, trained_skill_level__gte=skills_json[skill], entity__external_id=external_id).exists():
                pass
            else:
                missing_skills.append({
                    'name': skill,
                    'level': skills_json[skill]
                })
        return missing_skills

