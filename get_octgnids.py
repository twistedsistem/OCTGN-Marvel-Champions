import json

cards = ""

with open('../marvelsdb-json-data/pack/qsv.json') as pack_json_file:
    packData = json.load(pack_json_file)
    for i in packData:
      cards = cards + ("'" + i['code'] + "':'" + i['octgn_id'] + "',\n")

with open('../marvelsdb-json-data/pack/qsv_encounter.json') as pack_json_file:
    packData = json.load(pack_json_file)
    for i in packData:
      cards = cards + ("'" + i['code'] + "':'" + i['octgn_id'] + "',\n")

print(cards)