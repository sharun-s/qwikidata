import requests
from qwikidata import typedefs

#logger = logging.getLogger(__name__)
WIKIDATA_MEDIAWIKI_URL = "https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&languages=en&ids="
VALID_ENTITY_PREFIXES = ("Q", "P", "L")

class ResponseNotOk(Exception):
    pass

class InvalidEntityId(Exception):
    pass

def get_entities_from_mwapi(entity_ids, base_url: str = WIKIDATA_MEDIAWIKI_URL):
    """Get a dictionary representing a wikidata entity/entities from the mediawiki interface API.

    https://www.wikidata.org/w/api.php?action=wbgetentities&ids=x|y|z"

    Parameters
    ----------
    entity_ids
      The IDs of the entities to get the data from Separate values with |
    base_url
      The linked data interface URL to use

    Examples
    --------
    Get the entity dictionary for item Q42,

    ::

      >>> entity_dict = get_entities_from_mwapi('Q42|Q45')
      >>> pprint(entity_dict, indent=4, depth=1)
      {   'aliases': {...},
          'claims': {...},
          'descriptions': {...},
          'id': 'Q42',
          'labels': {...},
          'lastrevid': 716282445,
          'modified': '2018-07-27T08:03:25Z',
          'ns': 0,
          'pageid': 138,
          'sitelinks': {...},
          'title': 'Q42',
          'type': 'item'}}}

    """
    if not isinstance(entity_ids, str):
        raise InvalidEntityId(
            'entity_ids must be a string (e.g. "Q42|Q35") but got entity_ids={}.'.format(entity_ids)
        )
    if not entity_ids[0] in VALID_ENTITY_PREFIXES:
        raise InvalidEntityId(
            "entity_id must start with one of {} but got entity_ids={}.".format(
                VALID_ENTITY_PREFIXES, entity_ids
            )
        )

    response = requests.get(base_url+entity_ids)
    if response.ok:
        entities_dict = response.json()
    else:
        raise LdiResponseNotOk(
            "input entity id: {}, "
            "response.headers: {}, "
            "response.status_code: {}, "
            "response.text: {}".format(
                entity_ids, response.headers, response.status_code, response.text
            )
        )

    return entities_dict