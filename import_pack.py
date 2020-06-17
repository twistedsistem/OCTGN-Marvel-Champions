from lxml import etree as ET
import json
import urllib.request


def getPack(set_code):
  with open('../marvelsdb-json-data/packs.json') as pack_json_file:
    packData = json.load(pack_json_file)
    for i in packData:
      if i['code'] == set_code:
        return i


def findAlt(data, findValue):
  for i in data:
    if i['code'] == findValue:
      return i


def buildXmlProps(propDict, xmlElement):
  cardNumber = ET.SubElement(xmlElement, 'property')
  cardNumber.set('name', 'CardNumber')
  cardNumber.set('value', propDict['code'])

  if 'type_code' in propDict.keys():
    cardType = ET.SubElement(xmlElement, 'property')
    cardType.set('name', 'Type')
    cardType.set('value', propDict['type_code'])

  if 'set_code' in propDict.keys():
    cardOwner = ET.SubElement(xmlElement, 'property')
    cardOwner.set('name', 'Owner')
    cardOwner.set('value', propDict['set_code'])

  if 'hand_size' in propDict.keys():
    cardHandSize = ET.SubElement(xmlElement, 'property')
    cardHandSize.set('name', 'HandSize')
    cardHandSize.set('value', str(propDict['hand_size']))

  if 'thwart' in propDict.keys():
    cardThwart = ET.SubElement(xmlElement, 'property')
    cardThwart.set('name', 'Thwart')
    cardThwart.set('value', str(propDict['thwart']))

  if 'thwart_cost' in propDict.keys():
    cardThwartCost = ET.SubElement(xmlElement, 'property')
    cardThwartCost.set('name', 'ThwartCost')
    cardThwartCost.set('value', str(propDict['thwart_cost']))

  if 'attack' in propDict.keys():
    cardAttack = ET.SubElement(xmlElement, 'property')
    cardAttack.set('name', 'Attack')
    cardAttack.set('value', str(propDict['attack']))

  if 'attack_cost' in propDict.keys():
    cardAttackCost = ET.SubElement(xmlElement, 'property')
    cardAttackCost.set('name', 'AttackCost')
    cardAttackCost.set('value', str(propDict['attack_cost']))

  if 'defense' in propDict.keys():
    cardDefense = ET.SubElement(xmlElement, 'property')
    cardDefense.set('name', 'Defense')
    cardDefense.set('value', str(propDict['defense']))

  if 'defense_cost' in propDict.keys():
    cardDefenseCost = ET.SubElement(xmlElement, 'property')
    cardDefenseCost.set('name', 'DefenseCost')
    cardDefenseCost.set('value', str(propDict['defense_cost']))

  if 'recover' in propDict.keys():
    cardRecovery = ET.SubElement(xmlElement, 'property')
    cardRecovery.set('name', 'Recovery')
    cardRecovery.set('value', str(propDict['recover']))

  if 'scheme' in propDict.keys():
    cardScheme = ET.SubElement(xmlElement, 'property')
    cardScheme.set('name', 'Scheme')
    cardScheme.set('value', str(propDict['scheme']))

  if 'boost' in propDict.keys():
    cardBoost = ET.SubElement(xmlElement, 'property')
    cardBoost.set('name', 'Boost')
    cardBoost.set('value', str(propDict['boost']))

  if 'cost' in propDict.keys():
    cardCost = ET.SubElement(xmlElement, 'property')
    cardCost.set('name', 'Cost')
    cardCost.set('value', str(propDict['cost']))

  if 'resource_mental' in propDict.keys():
    cardResourceMental = ET.SubElement(xmlElement, 'property')
    cardResourceMental.set('name', 'Resource_Mental')
    cardResourceMental.set('value', str(propDict['resource_mental']))

  if 'resource_physical' in propDict.keys():
    cardResourcePhysical = ET.SubElement(xmlElement, 'property')
    cardResourcePhysical.set('name', 'Resource_Physical')
    cardResourcePhysical.set('value', str(propDict['resource_physical']))

  if 'resource_energy' in propDict.keys():
    cardResourceEnergy = ET.SubElement(xmlElement, 'property')
    cardResourceEnergy.set('name', 'Resource_Energy')
    cardResourceEnergy.set('value', str(propDict['resource_energy']))

  if 'resource_wild' in propDict.keys():
    cardResourceWild = ET.SubElement(xmlElement, 'property')
    cardResourceWild.set('name', 'Resource_Wild')
    cardResourceWild.set('value', str(propDict['resource_wild']))

  if 'health' in propDict.keys():
    cardHP = ET.SubElement(xmlElement, 'property')
    cardHP.set('name', 'HP')
    cardHP.set('value', str(propDict['health']))

  if 'base_threat' in propDict.keys():
    cardBaseThreat = ET.SubElement(xmlElement, 'property')
    cardBaseThreat.set('name', 'BaseThreat')
    cardBaseThreat.set('value', str(propDict['base_threat']))

  if 'base_threat_fixed' in propDict.keys():
    cardBaseThreatFixed = ET.SubElement(xmlElement, 'property')
    cardBaseThreatFixed.set('name', 'BaseThreatFixed')
    cardBaseThreatFixed.set('value', str(propDict['base_threat_fixed']))

  if 'threat' in propDict.keys():
    cardThreat = ET.SubElement(xmlElement, 'property')
    cardThreat.set('name', 'Threat')
    cardThreat.set('value', str(propDict['threat']))

  if 'escalation_threat' in propDict.keys():
    cardEscalationThreat = ET.SubElement(xmlElement, 'property')
    cardEscalationThreat.set('name', 'EscalationThreat')
    cardEscalationThreat.set('value', str(propDict['escalation_threat']))

  if 'escalation_threat_fixed' in propDict.keys():
    cardEscalationThreatFixed = ET.SubElement(xmlElement, 'property')
    cardEscalationThreatFixed.set('name', 'EscalationThreatFixed')
    cardEscalationThreatFixed.set(
        'value', str(propDict['escalation_threat_fixed']))

  if 'scheme_acceleration' in propDict.keys():
    cardSchemeAcceleration = ET.SubElement(xmlElement, 'property')
    cardSchemeAcceleration.set('name', 'Scheme_Acceleration')
    cardSchemeAcceleration.set('value', str(propDict['scheme_acceleration']))

  if 'scheme_crisis' in propDict.keys():
    cardSchemeCrisis = ET.SubElement(xmlElement, 'property')
    cardSchemeCrisis.set('name', 'Scheme_Crisis')
    cardSchemeCrisis.set('value', str(propDict['scheme_crisis']))

  if 'scheme_hazard' in propDict.keys():
    cardSchemeHazard = ET.SubElement(xmlElement, 'property')
    cardSchemeHazard.set('name', 'Scheme_Hazard')
    cardSchemeHazard.set('value', str(propDict['scheme_hazard']))

  if 'traits' in propDict.keys():
    cardAttribute = ET.SubElement(xmlElement, 'property')
    cardAttribute.set('name', 'Attribute')
    cardAttribute.set('value', str(propDict['traits']))

  if 'text' in propDict.keys():
    cardText = ET.SubElement(xmlElement, 'property')
    cardText.set('name', 'Text')
    cardText.text = propDict['text']

  if 'flavor' in propDict.keys():
    cardQuote = ET.SubElement(xmlElement, 'property')
    cardQuote.set('name', 'Quote')
    cardQuote.text = propDict['flavor']

  if 'is_unique' in propDict.keys():
    cardUnique = ET.SubElement(xmlElement, 'property')
    cardUnique.set('name', 'Unique')
    cardUnique.set('value', str(propDict['is_unique']))

# response = urllib.request.urlopen('https://raw.githubusercontent.com/zzorba/marvelsdb-json-data/master/packs.json')
# packs = json.load(response)
# for x in packs:
#   print(x)

# parser = ET.XMLParser()
# tree = ET.parse('set.xml', parser)
# # print(tree.findall(".//card"))
# for x in tree.iter(tag='cards'):
#   print(ET.tostring(x))

with open('../marvelsdb-json-data/pack/bkw_encounter.json') as json_file:
  data = json.load(json_file)
  packInfo = getPack(data[1]['pack_code'])
  top = ET.Element('set')
  top.set('name', packInfo['name'])
  top.set('id', packInfo['octgn_id'])
  top.set('gameId', '055c536f-adba-4bc2-acbf-9aefb9756046')
  top.set('gameVersion', '0.0.0.0')
  top.set('version', '1.0.0.0')
  cards = ET.SubElement(top, 'cards')
  for i in data:
    card = ET.SubElement(cards, 'card')
    card.set('name', i['name'])
    card.set('id', i['octgn_id'])
    buildXmlProps(i, card)
    if 'back_link' in i.keys():
      alternateCard = findAlt(data, i['back_link'])
      cardAlternate = ET.SubElement(card, 'alternate')
      cardAlternate.set('name', alternateCard['name'])
      cardAlternate.set('type', alternateCard['code'][-1])
      buildXmlProps(alternateCard, cardAlternate)

# with open('../marvelsdb-json-data/pack/msm_encounter.json') as json_encounter_file:
#     encounter_data = json.load(json_encounter_file)
#     for i in encounter_data:
#       card = ET.SubElement(cards, 'card')
#       card.set('name', i['name'])
#       card.set('id', i['octgn_id'])
#       buildXmlProps(i, card)
#       if 'back_link' in i.keys():
#         alternateCard = findAlt(encounter_data, i['back_link'])
#         cardAlternate = ET.SubElement(card, 'alternate')
#         cardAlternate.set('name', alternateCard['name'])
#         cardAlternate.set('type', alternateCard['code'][-1])
#         buildXmlProps(alternateCard, cardAlternate)


# create a new XML file with the results
mydata = ET.tostring(top, pretty_print=True, encoding='utf-8',
                     xml_declaration=True, standalone="yes")
myfile = open("set.xml", "wb")
myfile.write(mydata)
