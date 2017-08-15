"""
:created on: 2017-08-14

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

"""
These mappings are translating needed fields from resources to our database scheme.
Note:
    - fields that have the same name in database and in resource are omitted here!
Structure:
    {
        'resource_name': 'database_name'
    }
"""

COMPANY_MAPPING = {
    # theirs: ours
    'company': 'name'
}

PEOPLE_MAPPING = {
    # theirs: ours
    'name': 'username',
    'eyeColor': 'eye_color',
    'favouriteFood': 'food',
    'company_id': 'company'
}
