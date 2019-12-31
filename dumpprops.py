#from pprint import pprint
#pprint(q, indent=4, depth=1)
from pprint import pprint
from qwikidata.mediawiki_api import get_entities_from_mwapi
from qwikidata.linked_data_interface import get_entity_dict_from_api
from qwikidata.entity import WikidataItem, WikidataProperty
import collections

f=open(r'../idb/wikidataIDs')
lines=f.readlines()
f.close()

entities={}
props={}

for i in range(0,len(lines), 50):
  print(i)
  ids="|".join([j.split(",")[1].strip() for j in lines[i:i+50] if j.split(",")[1].strip()])
  entities.update(get_entities_from_mwapi(ids)['entities'])

ids="|".join([j.split(",")[1].strip() for j in lines[i:] if j.split(",")[1].strip()])
entities.update(get_entities_from_mwapi(ids)['entities'])

#for i in entities:
#  print(entities[i]['labels']['en']['value'], len(entities[i]['claims'].keys()))

def flatten(l):
    aaa=[]
    for i in l:
        aaa.extend(i)
    return aaa

allprops=set(flatten([entities[i]['claims'].keys() for i in entities]))
c=collections.Counter(flatten([entities[i]['claims'].keys() for i in entities]))

print("Number of unqiue props", len(c))

for i in range(0,len(c), 50):
  print(i)
  ids="|".join(list(c.keys())[i:i+50])
  props.update(get_entities_from_mwapi(ids)['entities'])

ids="|".join(list(c.keys())[i:len(c)])
props.update(get_entities_from_mwapi(ids)['entities'])

def printObj(e):
  tmp={}
  w=WikidataItem(e)
  tmp['label']=w.get_label()
  tmp['desc']=w.get_description()
  tmp['wikiurl']=w.get_enwiki_title()
  claims=w.get_claim_groups()
  for claim in claims:
    prop=WikidataProperty(props[claim])
    tmp[prop.get_label()]=[]
    #each claim/prop can point at someother entity eg: an Organization/Country etc
    for i in range(0, len(claims[claim])):
      dv=claims[claim][i].mainsnak.datavalue
      if isinstance(dv.value, dict) and 'id' in dv.value:  
        qid = dv.value["id"]
        entity = WikidataItem(get_entity_dict_from_api(qid))
        tmp[prop.get_label()].append(entity.get_label())
      else:
        tmp[prop.get_label()].append(dv.value) 
    if len(tmp[prop.get_label()]) == 1:
      tmp[prop.get_label()]=tmp[prop.get_label()][0]
  return tmp

db={}    
for e in entities:
  db[e]=printObj(entities(e))