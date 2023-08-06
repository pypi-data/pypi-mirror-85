from django_eveonline_connector.utilities.static.universe import query_static_database
from django.db import connections
import json 

def pull_skills():
    query = """
    SELECT
        groupID,
        typeID,
        typeName
    FROM
        invTypes
    WHERE
        groupID IN (
            SELECT
                groupID
            FROM
                invGroups
            WHERE
                categoryID = 16
        )
    ORDER BY
        typeName DESC;
    """
    result = query_static_database(query, fetchall=True)
    return result

def run():
    skill_dump = {}
    skills = pull_skills()
    for skill in skills:
        skill_dump[skill[2]] = {
            "group_id": skill[0],
            "type_id": skill[1],
            "name": skill[2],
        }

    import django_eveonline_doctrine_manager
    import os
    pth = os.path.dirname(django_eveonline_doctrine_manager.__file__)
    with open(pth + '/export/skills.json', 'w') as fp:
        json.dump(skill_dump, fp, indent=4, sort_keys=True)
    

