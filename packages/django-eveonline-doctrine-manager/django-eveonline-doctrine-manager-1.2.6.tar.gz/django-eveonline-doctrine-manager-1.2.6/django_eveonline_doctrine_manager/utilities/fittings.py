from django_eveonline_connector.utilities.static.universe import resolve_type_name_to_type_id, get_type_id_prerq_skill_ids, get_prerequisite_skills, resolve_type_id_to_type_name, resolve_type_id_to_category_name
from django_eveonline_doctrine_manager.utilities.abstractions import EveSkillList
import json
import logging
import re
import roman

def parse_eft_format(fitting):
    fit = {
        'ship': None,
        'highslots': [],
        'midslots': [],
        'lowslots': [],
        'rigs': [],
        'drones': [],
        'implants': [],
        'cargo': [],
    }

    regex_pattern = "(?P<type_name>[[A-Za-z0-9\-_' ]*(?<![x0-9]))(?P<loaded>,.*)?(?P<quantity>x[0-9]*)?"

    fitting = fitting.fitting.splitlines()
    fitting.reverse()
    ship_info_line = fitting.pop()
    ship_info = {
        'name': ship_info_line[1:-1].split(',')[1].strip(),
        'type_name': ship_info_line[1:-1].split(',')[0].strip(),
         'type_id': resolve_type_name_to_type_id(ship_info_line[1:-1].split(',')[0].strip()),
        }

    fit['ship'] = ship_info
    case = -1
    cases = ['lowslots', 'midslots', 'highslots', 'rigs', 'cargo']
    while len(fitting) > 1:
        if (fitting[-1] == '' or fitting[-1].isspace()):
            line = fitting.pop()
            if case < 4:
                case += 1
            while(fitting[-1].isspace() or fitting[-1] == ""):
                excess = fitting.pop()
            continue
        else:
            line = fitting.pop()

        if 'Empty' in line or not line:
            continue

        results = re.search(regex_pattern, line)
        try:
            type_name = results.group('type_name').rstrip()
            quantity = results.group('quantity')
        except IndexError as e:
            pass  # just means no quantity
        type_id = resolve_type_name_to_type_id(type_name)
        category = resolve_type_id_to_category_name(type_id)
        if case == 4 and category == 'Drone':
            fit['drones'].append({
                "type_name": type_name,
                "type_id": type_id,
                "quantity": int(quantity[1:]) if quantity else None,
            })
        elif case == 4 and category == 'Implant':
            fit['drones'].append({
                "type_name": type_name,
                "type_id": type_id,
                "quantity": int(quantity[1:]) if quantity else None,
            })
        elif case == 4:
            fit['cargo'].append({
                "type_name": type_name,
                "type_id": type_id,
                "quantity":  int(quantity[1:]) if quantity else None,
            })
        else:
            fit[cases[case]].append({
                "type_name": type_name,
                "type_id": type_id,
                "quantity": quantity if quantity else None,
            })

    return fit

def get_required_skills(fitting):
    fitting = json.loads(fitting.parsed_format_raw)
    exclude_keys = ['ship']
    top_level_skills = []

    for key in fitting:

        if key in exclude_keys:
            continue

        module_list = fitting[str(key)]
        unique_modules = set()
        unique_modules.add(fitting['ship']['type_id'])
        for module in module_list:
            unique_modules.add(module['type_id'])

        for module in unique_modules:
            top_level_skills += get_type_id_prerq_skill_ids(module)

        skill_list = EveSkillList()
        for skill in top_level_skills:
            for prerq_skill in reversed(get_prerequisite_skills([skill])):
                skill_list.add_skill(prerq_skill)

    return skill_list.to_json()

def get_market_format(fitting):
    fitting_json = json.loads(fitting.parsed_format_raw)
    fitting_paste = []
    exclude_keys = ['ship']
    fitting_paste.append(fitting.ship_name)
    for key in fitting_json:
        if key in exclude_keys:
            continue
        for module in fitting_json[key]:
            name = module['type_name']
            quantity = module['quantity']
            if not quantity:
                quantity = 1
            fitting_paste.append(f"{name} x{quantity}")
    return "\n".join(fitting_paste)


def get_ship_name(fitting):
    fitting = fitting.fitting.splitlines()
    line = fitting[0]
    return line[1:-1].split(',')[0].strip()
