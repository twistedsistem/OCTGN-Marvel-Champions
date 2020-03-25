#
# Routines for writing out updated decks based on either the player piles or the shared piles
#
from datetime import datetime as dt
import collections
import clr
clr.AddReference('System.Web.Extensions')
from System.Web.Script.Serialization import JavaScriptSerializer as json #since .net 3.5?

PLAYER_DECK = ['Investigator', 'Special', 'Asset', 'Event', 'Skill', 'Weakness', 'Sideboard', 'Basic Weaknesses']

def saveTable(group, x=0, y=0):
  mute()

  if 1 != askChoice('You are about to SAVE the table states including the elements on the table, shared deck and each player\'s hand and piles.\nThis option should be execute on the a game host.'
    , ['I am the Host!', 'I am not...'], ['#dd3737', '#d0d0d0']):
    return

  if not getLock():
    whisper("Others players are saving, please try manual saving again")
    return

  try:
    tab = {"table":[], "shared": {}, 'counters': None, "players": None, "gameProperties": None}

    # loop and retrieve cards from the table
    for card in table:
      tab['table'].append(serializeCard(card))

    # loop and retrieve item from the shared decks
    for p in shared.piles :
      if p == 'Trash':
        continue
      for card in shared.piles[p]:
        if p not in tab['shared']:
          tab['shared'].update({p: []})
        tab['shared'][p].append(serializeCard(card))

    tab['counters'] = serializeCounters(shared.counters)

    # loop each player
    players = sorted(getPlayers(), key=lambda x: x._id, reverse=False)
    tab['players'] = [serializePlayer(pl) for pl in players]

    tab['gameProperties'] = [serializePlayerVariables(None)]
    dir = wd('marvel-champions-table-state-{}.json'.format('{:%Y%m%d%H%M%S}'.format(dt.now())))
    if 'GameDatabase' in dir:
      filename = dir.replace('GameDatabase','Decks').replace('055c536f-adba-4bc2-acbf-9aefb9756046\\','')
    else:
      filename = "Decks".join(dir.rsplit('OCTGN',1)).replace('055c536f-adba-4bc2-acbf-9aefb9756046\\','')

    filename = askString('Please input the path to save the game state', filename)

    if filename == None:
      return

    with open(filename, 'w+') as f:
      f.write(json().Serialize(tab))

    notify("Table state saves to {}".format(filename))
    savedGames = getSetting("SavedGames",'')
    if len(savedGames) != 0:
      savedGames = savedGames + '|' + str(filename).split("\\")[-1]
    else:
      savedGames = str(filename).split("\\")[-1]
    setSetting("SavedGames",str(savedGames))
  finally:
    clearLock()

def loadTable(group, x=0, y=0):
  mute()

  if 1 != askChoice('You are about to LOAD the table states including the elements on the table, shared deck and each player\'s hand and piles.\nThis option should be execute on the a game host.'
    , ['I am the Host!', 'I am not...'], ['#dd3737', '#d0d0d0']):
    return

  if not getLock():
    whisper("Others players are locking the table, please try again")
    return

  try:
    dir = wd('table-state.json')
    if 'GameDatabase' in dir:
      filename = dir.replace('GameDatabase','Decks').replace('055c536f-adba-4bc2-acbf-9aefb9756046\\','')
    else:
      filename = "Decks".join(dir.rsplit('OCTGN',1)).replace('055c536f-adba-4bc2-acbf-9aefb9756046\\','')

    filename = askString('Please provide the file path to load the table states', filename)

    if filename == None:
      return

    with open(filename, 'r') as f:
      tab = json().DeserializeObject(f.read())

    deserializeTable(tab['table'])

    if tab['counters'] is not None and len(tab['counters']) > 0:
      deserializeCounters(tab['counters'], shared)

    if tab['shared'] is not None and len(tab['shared']) > 0:
      for k in tab['shared'].Keys:
        if k not in shared.piles:
          continue
        deserializePile(tab['shared'][k], shared.piles[k])

    if tab['counters'] is not None and len(tab['counters']) > 0:
      deserializeCounters(tab['counters'], shared)

    if tab['players'] is not None and len(tab['players']) > 0:
      for player in tab['players']:
        deserializePlayer(player)

    notify("Successfully load table state from {}".format(filename))
  finally:
    clearLock()

def saveDeck(group, x=0, y=0):
  mute()

  if not getLock():
    whisper("Others players are saving, please try manual saving again")
    return

  try:
    suffix = '{:%Y%m%d%H%M%S}'.format(dt.now())
    suffix = askString('Please provide a filename suffix (e.g. current scenerio name)', suffix)
    if suffix == None:
      whisper("Failed to save deck, missing file suffix")
      return

    investigators = {}
    lookForInvestigator(table, investigators)

    for pl in getPlayers():
      lookForInvestigator(pl.hand, investigators)

    if len(investigators) == 0:
      whisper("No investigators you are controlling, save is cancelled")
      return

    for key in investigators:
      savePlayerDeck(me, investigators[key], suffix)
  finally:
    clearLock()

def lookForInvestigator(cardList, investigators):
  for card in cardList:
    if card.owner == me:
      if card.Type == 'Investigator':
        if card.name not in investigators:
          investigators.update({card.name:[]})
        investigators[card.name].append(card)
      if card.Type == 'Mini':
        if card.name not in investigators:
          investigators.update({card.name:[]})
        investigators[card.name].append(card)

#Save the player deck - it is named after the character
def savePlayerDeck(player, invCards, suffix): #me.hand or table
  sections = { p : {} for p in PLAYER_DECK}

  #Add in the character sheet card (from the table)
  investigator = None
  for card in invCards:
    investigator = card
    sections["Investigator"][(card.name, card.model)] = 1

  if investigator is None:
    whisper("Failed to find investigator to save")
    return

  piles = [ me.piles[p] for p in me.piles if p != 'Basic Weaknesses']
  piles.append(me.hand)
  filename = savePiles('{}-saved-{}.o8d'.format("".join(c for c in investigator.name if c not in ('!','.',':', '"', "'")), suffix), sections, piles, True, False)
  if filename is None:
    whisper("Failed to save deck")
  else:
    notify("{} saves deck to {}".format(me, filename))

# Generic deck saver
# Loops through the piles and count how many cards there are of each type in each section
# Calls the routine getSection (passed as a parameter) to determine which section a card should be stored in
def savePiles(name, sections, piles, skipInvestigator, isShared):
  for p in piles:
    if len(p) > 0:
      for card in p:
        s = getSection(sections, card)
        if s is None:
          continue
        if skipInvestigator and s == 'Investigator':
          continue
        if (card.name, card.model) in sections[s]:
          sections[s][(card.name, card.model)] += 1
        else:
          sections[s][(card.name, card.model)] = 1
  dir = wd(name)
  if 'GameDatabase' in dir:
    filename = dir.replace('GameDatabase','Decks').replace('a6d114c7-2e2a-4896-ad8c-0330605c90bf','Arkham Horror - The Card Game')
  else:
    filename = "Decks\Arkham Horror - The Card Game".join(dir.rsplit('OCTGN',1))
  with open(filename, 'w+') as f:
    f.write('<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n')
    f.write('<deck game="a6d114c7-2e2a-4896-ad8c-0330605c90bf">\n')
    for s in sections:
      if len(sections[s]) > 0:
        f.write(" <section name=\"{}\" shared=\"{}\">\n".format(s, isShared))
        count = 0
        for t in sorted(sections[s].keys()):
          #whisper("  <card qty=\"{}\" id=\"{}\">{}</card>\n".format(sections[s][t], t[1], t[0]))
          f.write("  <card qty=\"{}\" id=\"{}\">{}</card>\n".format(sections[s][t], t[1], t[0]))
          count += sections[s][t]
        f.write(" </section>\n")
        #whisper("{} - {}".format(s, count))
    f.write("</deck>\n")
    return filename
  return None

orientation = {
        0: Rot0,
        1: Rot90,
        2: Rot180,
    3: Rot270
    }

def deserializePlayer(plData):
  if plData is None or len(plData) == 0:
    return

  players = [x for x in getPlayers() if x._id == plData['_id'] ]
  if players == None or len(players) == 0:
    return

  player = players[0]

  if player is None:
    return

  deserializeCounters(plData['counters'], player)

  if plData['hand'] is not None and len(plData['hand']) > 0:
    if player != me:
      remoteCall(player, "deserializePile", [plData['hand'], player.hand])
    else:
      deserializePile(plData['hand'], player.hand)

  if plData['piles'] is not None and len(plData['piles']) > 0:
    for k in plData['piles'].Keys:
      if k not in player.piles:
        continue
      deserializePile(plData['piles'][k], player.piles[k], player)

def deserializePile(pileData, group, who = me):
  if pileData is None or len(pileData) == 0:
    return
  if group != shared and who != me and group.controller != me:
    remoteCall(who, "deserializePile", [pileData, group, who])
  else:
    for c in pileData:
      card = group.create(c['model'])

def deserializeCounters(counters, player):
  if counters is None or len(counters) == 0:
    return
  for k in counters.Keys:
    player.counters[k].value = counters[k]

def deserializeTable(tbl):
  if len(tbl) == 0:
    return
  for cardData in tbl:
    deserizlizeCard(cardData)

def deserizlizeCard(cardData):
  card = table.create(cardData['model'], cardData['position'][0], cardData['position'][1], 1, True)
  if 'markers' in cardData and cardData['markers'] is not None and len(cardData['markers']) > 0:
    for key, qty in {(i['name'], i['model']): i['qty'] for i in cardData['markers']}.items():
      card.markers[key] = qty
  if 'orientation' in cardData:
    card.orientation = orientation.get(cardData['orientation'], 0)
  if 'isFaceUp' in cardData and cardData['isFaceUp'] is not None:
    card.isFaceUp = cardData['isFaceUp']
  if 'alternate' in cardData:
    card.alternate = cardData['alternate']
  return card

def serializeCard(card):
  cardData = {'model':'', 'markers':{}, 'orientation':0, 'position':[], 'isFaceUp':False}
  cardData['model'] = card.model
  cardData['orientation'] = card.orientation
  cardData['markers'] = serializeCardMarkers(card)
  cardData['position'] = card.position
  cardData['isFaceUp'] = card.isFaceUp
  cardData['alternate'] = card.alternate
  #notify("cardData {}".format(str(cardData)))
  return cardData

def serializePlayer(player):
  plData = {'_id':None, 'name': None, 'counters':None, 'hand':[], 'piles': {}}
  plData['_id'] = player._id
  plData['name'] = player.name
  plData['counters'] = serializeCounters(player.counters)
  plData['globalVariables'] = serializePlayerVariables(player)

  # serialize player hand
  if len(player.hand) > 0:
    for card in player.hand:
      plData['hand'].append(serializeCard(card))

  # serialize player's piles
  for k,v in player.piles.items():
    if len(v) == 0:
      continue
    plData['piles'].update({k: [serializeCard(c) for c in v]})

  return plData

def serializeCounters(counters):
  if len(counters) == 0:
    return None
  return {k: counters[k].value for k in counters}

def serializePlayerVariables(player):
  playerVariable = {'done':'', 'playerID':'', 'firstPlayer':'', 'activePlayer':''}
  if player != None:
    playerVariable['done'] = player.getGlobalVariable("done")
    playerVariable['playerID'] = player.getGlobalVariable("playerID")
  else:
    playerVariable['firstPlayer'] = getGlobalVariable("firstPlayer")
    playerVariable['activePlayer'] = getGlobalVariable("activePlayer")
  return playerVariable

def serializeCardMarkers(card):
  if len(card.markers) == 0:
    return None
  markers = []
  for id in card.markers:
    markers.append({'name': id[0], 'model': id[1], 'qty': card.markers[id]})
  return markers

def getSection(sections, card):
  if card.Type is not None and card.Type in sections:
    return card.Type
  if card.Subtype is not None:
    if card.Subtype == 'Basic Weakness':
      return 'Weakness'
    if card.Subtype in sections:
      return card.Subtype
  return None

def getListValidSavedGames():
  checkList = getSetting("SavedGames",'')
  validList = []
  notify("{}".format(checkList))
  if len(checkList) != 0:
    for f in checkList.split('|'):
      try:
        with open(wd(f).replace('GameDatabase','Decks').replace('055c536f-adba-4bc2-acbf-9aefb9756046\\',''), 'r') as file:
          validList.append(f)
      except IOError:
        continue
  return validList
