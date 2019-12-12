import clr
import re
clr.AddReference('System.Web.Extensions')
from System.Web.Script.Serialization import JavaScriptSerializer

DamageMarker = ("Damage", "396f9a8e-542c-4992-a776-5abe03353979")
ThreatMarker = ("Threat", "8b974efd-733c-4111-8f96-d667fee4de5a")
AllPurposeMarker = ("All Purpose", "bceb440d-2696-484e-8d76-cef609227779")
StunnedMarker = ("Stunned", "8fa2056b-5786-429f-9d33-b96138e7aa98")
ConfusedMarker = ("Confused", "1c0a87cf-3f38-4e84-9744-d627b9c54c93")
ToughMarker = ("Tough", "edcebfd6-3f75-40cb-b442-a8fb1154f6e2")

DoneColour = "#D8D8D8" # Grey

def initializeGame():
    mute()
    pList = eval(getGlobalVariable("playerList"))
    for p in players:
        pList.append(p._id)
    setGlobalVariable("playerList",str(pList))
    unlockDeck()
    setActivePlayer(None)
    if me._id == 1:
        setGlobalVariable("playersSetup", "")
        setGlobalVariable("game", str(num(getGlobalVariable("game"))+1))
        notify("Starting Game {}".format(getGlobalVariable("game")))

    #---------------------------------------------------------------------------
    # NEW
    #---------------------------------------------------------------------------
    setGlobalVariable("currentPlayers",str([]))
    update()

def playerSetup(group=table, x=0, y=0, doPlayer=True, doEncounter=False):
    mute()

    if not getLock():
        whisper("Others players are setting up, please try manual setup again (Ctrl+Shift+S)")
        return

    unlockDeck()
    if doPlayer:
        id = myID() # This ensures we have a unique ID based on our position in the setup order
        heroCount = countHeros(me)

        # Find any Permanent cards
        #permanents = filter(lambda card: "Permanent" in card.Keywords or "Permanent." in card.Text, me.deck)

        # Move Hero to the table
        newHero = False
        hero = filter(lambda card: card.Type == "hero", me.Deck)
        if hero:
            heroCount += 1
            newHero = True
            heroCard = hero[0]
            heroCard.moveToTable(tableLocations['player' + str(id + 1)][0],tableLocations['player' + str(id + 1)][1])
            heroCard.alternate = 'b'
            setHeroCounters(heroCard)
            notify("{} places his Hero on the table".format(me))

        if newHero:
            if len(me.hand) == 0:
                drawOpeningHand()
            createCards(heroCard.owner.piles["Nemesis Deck"],nemesis[str(heroCard.properties["Owner"])].keys(),nemesis[str(heroCard.properties["Owner"])])
    # If we loaded the encounter deck - add the first main scheme card to the table
    # if doEncounter or encounterDeck().controller == me:
    #     count = agendaCount(table)
    #     if count == 0:
    #         nextAgendaStage()
    #         nextActStage()
    #         shuffle(encounterDeck())
    #         shuffle(specialDeck())

    if not clearLock():
        notify("Players performed setup at the same time causing problems, please reset and try again")

def loadVillain(group, x = 0, y = 0):
    if not deckNotLoaded(group,0,0,shared.villain):
        confirm("Cannot generate a deck: You already have cards loaded.  Reset the game in order to generate a new deck.")
        return
    choice = askChoice("Which villain would you like to defeat?", ["Klaw", "Rhino", "Ultron"])

    if choice == 0: return
    if choice == 1:
        createCards(shared.villain,sorted(klaw.keys()),klaw)
        notify('{} loaded "Klaw", Good Luck!'.format(me))
    if choice == 2:
        createCards(shared.villain,sorted(rhino.keys()),rhino)
        notify('{} loaded "Rhino", Good Luck!'.format(me))
    if choice == 3:
        createCards(shared.villain,sorted(ultron.keys()),ultron)
        notify('{} loaded "Ultron", Good Luck!'.format(me))
    loadEncounter(group)
    setupVillainTable()

def loadEncounter(group, x = 0, y = 0):
    if not deckNotLoaded(group,0,0,shared.encounter):
        confirm("Cannot generate an deck: You already have cards loaded.  Reset the game in order to generate a new deck.")
        return
    choice = askChoice("Which encounter would you like to take on?", ["Bomb Scare", "The Doomsday Chair", "Legions of Hydra", "Masters of Evil", "Under Attack"])

    if choice == 0: return
    elif choice == 1:
        createCards(shared.encounter,sorted(bomb_scare.keys()),bomb_scare)
        notify('{} loaded "Bomb Scare", Good Luck!'.format(me))
    if choice == 2:
        createCards(shared.encounter,sorted(the_doomsday_chair.keys()),the_doomsday_chair)
    if choice == 3:
        createCards(shared.encounter,sorted(legions_of_hydra.keys()),legions_of_hydra)
    if choice == 4:
        createCards(shared.encounter,sorted(masters_of_evil.keys()),masters_of_evil)
    if choice == 5:
        createCards(shared.encounter,sorted(under_attack.keys()),under_attack)

    choice = askChoice("What difficulty would you like to play at?", ["Standard", "Expert"])

    if choice == 0: return
    if choice == 1:
        createCards(shared.encounter,sorted(standard.keys()),standard)
    if choice == 2:
        createCards(shared.encounter,sorted(standard.keys()),standard)
        createCards(shared.encounter,sorted(expert.keys()),expert)
        setGlobalVariable("difficulty", "1")

def getPosition(card,x=0,y=0):
    t = getPlayers()
    notify("This cards position is {}".format(card.position))

def createCards(group,list,dict):
    for i in list:
        group.create(card_mapping[i],dict[i])

def deckNotLoaded(group, x = 0, y = 0, checkGroup = me.Deck):
    if len(checkGroup) > 0:
        return False
    return True

def loadDeck(group, x = 0, y = 0):
    mute()
    if not deckNotLoaded(group):
        confirm("Cannot generate a deck: You already have cards loaded.  Reset the game in order to generate a new deck.")
        return
    choice = askChoice("What type of deck do you want to load?", ["A out of the box deck", "A registered deck"])

    if choice == 0: return
    if choice == 1:
        choice2 = askChoice("Which hero would you like to be?", ["Black Panther", "Captain Marvel", "Iron Man", "She Hulk", "Spider-Man"])
        if choice2 == 0: return
        if choice2 == 1: deckname = createAPICards("https://marvelcdb.com/decklist/view/1/black-panther-protection-starter-deck-1.0")
        if choice2 == 2: deckname = createAPICards("https://marvelcdb.com/decklist/view/2/captain-marvel-leadership-starter-deck-1.0")
        if choice2 == 3: deckname = createAPICards("https://marvelcdb.com/decklist/view/4/iron-man-aggression-starter-deck-1.0")
        if choice2 == 4: deckname = createAPICards("https://marvelcdb.com/decklist/view/3/she-hulk-aggression-starter-deck-1.0")
        if choice2 == 5: deckname = createAPICards("https://marvelcdb.com/decklist/view/5/spider-man-justice-starter-deck-1.0")
    if choice == 2:
        url = askString("Please enter the URL of the deck you wish to load.", "")
        if url == None: return
        if not "view/" in url:
            whisper("Error: Invalid URL.")
            return
        deckname = createAPICards(url)
    pList = eval(getGlobalVariable('playerList'))

def createAPICards(url):
    deckid = url.split("view/")[1].split("/")[0]
    data, code = webRead("https://marvelcdb.com/api/public/decklist/{}".format(deckid))
    if code != 200:
        whisper("Error retrieving online deck data, please try again.")
        return
    deckname = JavaScriptSerializer().DeserializeObject(data)["name"]
    deck = JavaScriptSerializer().DeserializeObject(data)["slots"]
    hero = JavaScriptSerializer().DeserializeObject(data)["investigator_code"]
    chars_to_remove = ['[',']']
    rx = '[' + re.escape(''.join(chars_to_remove)) + ']'
    for id in deck:
        line = re.sub(rx,'',str(id))
        line = line.split(',')
        cardid = line[0]
        card = me.Deck.create(card_mapping[cardid], int(line[1].strip()))
        if card == None:
            whisper("Error loading deck: Unknown card found.  Please restart game and try a different deck.")
    me.Deck.create(card_mapping[hero])
    return deckname

def setupVillainTable():
    mainSchemeCards = []
    villainCards = []
    for card in shared.villain:
        if card.properties["type"] <> "villain" and card.properties["type"] <> "main_scheme":
            mute()
            card.moveTo(shared.encounter)
        if card.properties["type"] == "main_scheme":
            card.moveTo(shared.scheme)
            mainSchemeCards.append(card)
        if card.properties["type"] == "villain":
            villainCards.append(card)
    sorted(mainSchemeCards)[0].moveToTable(tableLocations['mainScheme'][0],tableLocations['mainScheme'][1])
    #sorted(mainSchemeCards)[0].orientation = Rot90
    #sorted(mainSchemeCards)[0].alternate = "b"
    sorted(mainSchemeCards)[0].anchor = True
    sorted(mainSchemeCards).pop(0)
    gameDifficulty = getGlobalVariable("difficulty")
    villainCards = sorted(villainCards)
    if gameDifficulty == "1":
        villainCards[0].delete()
        villainCards.pop(0)
    else:
        villainCards[len(villainCards) - 1].delete()
        villainCards.pop(len(villainCards) - 1)
    villainCards[0].moveToTable(tableLocations['villain'][0],tableLocations['villain'][1])
    villainCards[0].anchor = True
    shared.counters["HP"].value = int(villainCards[0].properties["HP"]) * len(players)
    shared.encounter.shuffle()
    ecard = table.create('18976bc4-cfd2-4bca-bb47-e30de5eb2d7d',tableLocations['encounterCard'][0],tableLocations['encounterCard'][1],1)
    ecard.orientation = Rot270
    ecard.anchor = True
    table.create("65377f60-0de4-4196-a49e-96a550b4df81",tableLocations['player1'][0],int(tableLocations['player1'][1]) - 60,1,True)

def changeForm(card, x = 0, y = 0):
    mute()
    if "b" in card.alternates:
        if card.alternate == "":
            card.alternate = "b"
            notify("{} changes form to {}.".format(me, card))
        else:
            card.alternate = ""
            notify("{} changes form to {}.".format(me, card))
    me.counters["MaxHandSize"].value = num(card.HandSize)

def villainBoost(card, x = 0, y = 0):
    if len(shared.encounter) == 0:
        for c in table:
            if isEncounter([c]) == True:
                c.moveTo(shared.encounter)
                shared.encounter.shuffle()
    boostList = shared.encounter.top()
    boostList.moveToTable(0,0,True)

def moveToEncounterDiscard(args):
    mute()
    index = 0
    for card in args.cards:
        oldCoords = (args.xs[index], args.ys[index])
        newCoords = (card.position[0], card.position[1])
        #group = args.toGroups[index]
        if newCoords[0] >= -76 and newCoords[0] <= 5 and newCoords[1] >= -402 and newCoords[1] <= -346 and isEncounter([card]) == True:
            card.orientation = Rot90
            card.moveToTable(-47.0,-384.0)
            card.anchor = True
    index += 1

def addDamage(card, x = 0, y = 0):
    mute()
    card.markers[DamageMarker] += 1
#    if card.Type == 'villain':
#        shared.counters["HP"].value -= 1
    notify("{} adds 1 Damage on {}.".format(me, card))

def addMarker(card, x = 0, y = 0):
    mute()
    if card.Type == "side_scheme" or card.Type == "main_scheme":
        card.markers[ThreatMarker] += 1
        notify("{} adds 1 Threat on {}.".format(me, card))
    elif card.Type == "hero" or card.Type == "alter-ego" or card.Type == "minion" or card.Type == "villain" or card.Type == "ally":
        card.markers[DamageMarker] += 1
        notify("{} adds 1 Damage on {}.".format(me, card))
    else:
        card.markers[AllPurposeMarker] += 1
        notify("{} adds 1 Marker on {}.".format(me, card))

def removeMarker(card, x = 0, y = 0):
    mute()
    if card.Type == "side_scheme" or card.Type == "main_scheme":
        card.markers[ThreatMarker] -= 1
        notify("{} removes 1 Threat on {}.".format(me, card))
    elif card.Type == "hero" or card.Type == "alter-ego" or card.Type == "minion" or card.Type == 'ally':
        card.markers[DamageMarker] -= 1
        notify("{} removes 1 Damage on {}.".format(me, card))
    else:
        card.markers[AllPurposeMarker] -= 1
        notify("{} removes 1 Marker on {}.".format(me, card))

def clearMarker(card, x = 0, y = 0):
    mute()
    if card.Type == "side_scheme" or card.Type == "main_scheme":
        card.markers[ThreatMarker] = 0
        notify("{} removes all Threat on {}.".format(me, card))
    elif card.Type == "hero" or card.Type == "alter-ego" or card.Type == "minion" or card.Type == 'ally':
        card.markers[DamageMarker] = 0
        notify("{} removes all Damage on {}.".format(me, card))
    else:
        card.markers[AllPurposeMarker] = 0
        notify("{} removes all Markers on {}.".format(me, card))

def removeDamage(card, x = 0, y = 0):
    mute()
    card.markers[DamageMarker] -= 1
#    if card.Type == 'villain':
#        shared.counters["HP"].value += 1
    notify("{} removes 1 Damage from {}.".format(me, card))

def clearDamage(card, x = 0, y = 0):
    mute()
    card.markers[DamageMarker] = 0
#    if card.Type == 'villain':
#        shared.counters["HP"].value = int(card.properties["HP"])
    notify("{} removes all Damage from {}.".format(me, card))

def addThreat(card, x = 0, y = 0):
    mute()
    card.markers[ThreatMarker] += 1
    notify("{} adds 1 Threat on {}.".format(me, card))

def removeThreat(card, x = 0, y = 0):
    mute()
    card.markers[ThreatMarker] -= 1
    notify("{} removes 1 Threat from {}.".format(me, card))

def clearThreat(card, x = 0, y = 0):
    mute()
    card.markers[ThreatMarker] = 0
    notify("{} removes all Threat from {}.".format(me, card))

def addAPCounter(card, x = 0, y = 0):
    mute()
    card.markers[AllPurposeMarker] += 1
    notify("{} adds 1 Marker on {}.".format(me, card))

def removeAPCounter(card, x = 0, y = 0):
    mute()
    card.markers[AllPurposeMarker] -= 1
    notify("{} removes 1 Marker from {}.".format(me, card))

def clearAPCounter(card, x = 0, y = 0):
    mute()
    card.markers[AllPurposeMarker] = 0
    notify("{} removes all Marker from {}.".format(me, card))

def stun(card, x = 0, y = 0):
    mute()
    if card.markers[StunnedMarker] == 1:
        notify("{} is already stunned.".format(card))
    else:
        card.markers[StunnedMarker] = 1
        notify("{} is stunned.".format(card))

def confuse(card, x = 0, y = 0):
    mute()
    if card.markers[ConfusedMarker] == 1:
        notify("{} is already confused.".format(card))
    else:
        card.markers[ConfusedMarker] = 1
        notify("{} is confused.".format(card))

def tough(card, x = 0, y = 0):
    mute()
    if card.markers[ToughMarker] == 1:
        notify("{} already has a tough marker.".format(card))
    else:
        card.markers[ToughMarker] = 1
        notify("{} gains a tough marker.".format(card))

def removeStun(card, x = 0, y = 0):
    mute()
    card.markers[StunnedMarker] = 0
    notify("{} is no longer stunned.".format(card))

def removeConfuse(card, x = 0, y = 0):
    mute()
    card.markers[ConfusedMarker] = 0
    notify("{} is no longer confused.".format(card))

def removeTough(card, x = 0, y = 0):
    mute()
    card.markers[ToughMarker] = 0
    notify("{} is no longer tough.".format(card))

def readyExhaust(card, x = 0, y = 0):
    mute()
    if card.orientation == Rot0:
        card.orientation = Rot90
        notify("{} exhausts {}.".format(me, card))
    else:
        card.orientation = Rot0
        notify("{} readies {}.".format(me, card))

def revealHide(card, x = 0, y = 0):
    mute()
    if card.Type == "main_scheme":
        if "b" in card.alternates:
            if card.alternate == "":
                card.alternate = "b"
            else:
                card.alternate = ""
    elif card.Type == "hero" or card.Type == "alter-ego":
        changeForm(card)
    else:
        if card.isFaceUp:
            card.isFaceUp = False
            notify("{} hides {}.".format(me, card))
        else:
            card.isFaceUp = True
            notify("{} reveals {}.".format(me, card))

def readyAll(group = table, x = 0, y = 0):
    mute()
    for c in table:
        if c.controller == me and c.orientation != Rot0 and isEncounter([c]) != True and c.Type != "encounter" and c.Type != "villain" and c.Type != "main_scheme":
            c.orientation = Rot0
    notify("{} readies all their cards.".format(me))

def discard(card, x = 0, y = 0):
    mute()
    if isEncounter([card]):
        card.orientation = Rot90
        card.moveToTable(-47.0,-384.0)
        card.anchor = True
    elif card.Type == "main_scheme":
        card.moveTo(shared.scheme)
    elif card.Type == "villain":
        card.moveTo(shared.villain)
    else:
        notify("{} discards {} from {}.".format(me, card, card.group.name))
        card.moveTo(card.owner.piles["Discard Pile"])
    clearMarker(card)
def draw(group, x = 0, y = 0):
    mute()
    drawCard()
    notify("{} draws a card.".format(me))

def drawMany(group, count = None):
    mute()
    if len(group) == 0: return
    if deckLocked():
        whisper("Your deck is locked, you cannot draw cards at this time")
        return
    if count is None:
        count = askInteger("Draw how many cards?", 6)
    if count is None or count <= 0:
        whisper("drawMany: invalid card count")
        return
    for c in group.top(count):
        c.moveTo(me.hand)

def drawCard():
    mute()
    if len(me.Deck) == 0:
        for c in me.piles["Discard Pile"]:
            c.moveTo(c.owner.Deck)
        me.Deck.shuffle()
        rnd(1,1)
    if len(me.deck) == 0: return
    card = me.deck[0]
    card.moveTo(card.owner.hand)

def mulligan(group, x = 0, y = 0):
    mute()
    dlg = cardDlg(me.hand)
    dlg.min = 0
    dlg.max = len(me.hand)
    mulliganList = dlg.show()
    if len(mulliganList) <= 0:
        return
    if not confirm("Confirm Mulligan?"):
        return
    notify("{} mulligans.".format(me))
    for card in mulliganList:
        card.moveTo(card.owner.piles["Discard Pile"])
    for card in me.Deck.top(len(mulliganList)):
        card.moveTo(card.owner.hand)

def shuffle(group, x = 0, y = 0, silence = False):
    mute()
    for card in group:
        if card.isFaceUp:
            card.isFaceUp = False
    group.shuffle()
    if silence == False:
        notify("{} shuffled their {}".format(me, group.name))

def randomDiscard(group, x = 0, y = 0):
    mute()
    card = group.random()
    if card == None:
        return
    card.moveTo(card.owner.piles["Discard Pile"])
    notify("{} randomly discards {} from {}.".format(me, card, group.name))

def shuffleDiscardIntoDeck(group, x = 0, y = 0):
    mute()
    if len(group) == 0: return
    if group == me.piles["Discard Pile"]:
        for card in group:
            card.moveTo(card.owner.Deck)
        card.owner.Deck.shuffle()
        notify("{} shuffles their discard pile into their Deck.".format(me))
    if group == shared.piles["Encounter Discard"]:
        for card in group:
            card.moveTo(shared.encounter)
        shared.encounter.shuffle()
        notify("{} shuffles the encounter discard pile into the encounter Deck.".format(me))

def viewGroup(group, x = 0, y = 0):
    group.lookAt(-1)

def pluralize(num):
   if num == 1:
       return ""
   else:
       return "s"

def markersUpdate(args):
    if args.marker == "Damage" and args.card.Type == "villain":
        shared.counters["HP"].value = shared.counters["HP"].value - (args.card.markers[DamageMarker] - args.value)
    elif args.marker == "Damage" and (args.card.Type == "hero" or args.card.Type == "alter-ego"):
        args.card.owner.counters["HP"].value = args.card.owner.counters["HP"].value - (args.card.markers[DamageMarker] - args.value)

def defaultCardAction(args):
    if len(args.keysDown) > 0:
        for i in args.keysDown:
            if i == "D":
                if isAttackable([args.card]):
                    addDamage(args.card)
    else:
        if args.card.Type =="encounter":
            villainBoost(args.card)
        elif exhaustable([args.card]):
            readyExhaust(args.card)

def drawOpeningHand():
    me.deck.shuffle()
    drawMany(me.deck, me.MaxHandSize)

def setHeroCounters(heroCard):
    me.counters['HP'].value = num(heroCard.HP)
    me.counters['MaxHandSize'].value = num(heroCard.HandSize)

def deckLocked():
    return me.getGlobalVariable("deckLocked") == "1"

def lockDeck():
    me.setGlobalVariable("deckLocked", "1")

def unlockDeck():
    me.setGlobalVariable("deckLocked", "0")

def countHeros(p):
    heros = 0
    for card in table:
        if card.controller == p and (card.Type == "hero" or card.Type == "alter-ego"):
            heros += 1
    return heros

def mainSchemeDeck():
    return shared.piles['scheme']

def villainDeck():
    return shared.piles['villain']

#Store this player's starting position (his ID for this game)
#The first player is 0, the second 1 ....
#These routines set global variables so should be called within getLock() and clearLock()
#After a reset, the game count will be updated by the first player to setup again which invalidates all current IDs
def myID():
    if me.getGlobalVariable("game") == getGlobalVariable("game") and len(me.getGlobalVariable("playerID")) > 0:
        return playerID(me) # We already have a valid ID for this game

    g = getGlobalVariable("playersSetup")
    if len(g) == 0:
        id = 0
    else:
        id = num(g)
    me.setGlobalVariable("playerID", str(id))
    game = getGlobalVariable("game")
    me.setGlobalVariable("game", game)
    setGlobalVariable("playersSetup", str(id+1))
    update()
    #debug("Player {} sits in position {} for game {}".format(me, id, game))
    return id

#In phase management this represents the player highlighted in green
def setActivePlayer(p):
   if p is None:
       setGlobalVariable("activePlayer", "-1")
   else:
       setGlobalVariable("activePlayer", str(playerID(p)))
   update()

def setPlayerDone():
    done = getGlobalVariable("done")
    if done:
        playersDone = eval(done)
    else:
        playersDone = set()
    playersDone.add(me._id)
    setGlobalVariable("done", str(playersDone))
    update()

def playerID(p):
    return num(p.getGlobalVariable("playerID"))

def num(s):
   if not s: return 0
   try:
      return int(s)
   except ValueError:
      return 0

#------------------------------------------------------------
# Global variable manipulations function
#------------------------------------------------------------

def getLock():
    lock = getGlobalVariable("lock")
    if lock == str(me._id):
        return True

    if len(lock) > 0: #Someone else has the lock
        return False

    setGlobalVariable("lock", str(me._id))
    if len(getPlayers()) > 1:
        update()
    return getGlobalVariable("lock") == str(me._id)

def clearLock():
    lock = getGlobalVariable("lock")
    if lock == str(me._id):
        setGlobalVariable("lock", "")
        update()
        return True
    debug("{} id {} failed to clear lock id {}".format(me, me._id, lock))
    return False

#Called when the "done" global variable is changed by one of the players
#We use this check to see if all players are ready to advance to the next phase
#Note - all players get called whenever any player changes state. To ensure we don't all do the same thing multiple times
#       only the Encounter player is allowed to change the phase or step and only the player triggering the event is allowed to change the highlights
def checkPlayersDone():
    mute()
    if not turnManagement():
        return

    #notify("done updated: {} {}".format(numDone(), len(getPlayers())))
    if numDone() == len(getPlayers()):
        doEndHeroPhase()
        # doVillainPhase()
        setGlobalVariable("allowVillainPhase", "True")
        setGlobalVariable("phase", "villain")
        setGlobalVariable("done", str(set()))

#In phase management this represents the player highlighted in green
def setActivePlayer(p):
   if p is None:
       setGlobalVariable("activePlayer", "-1")
   else:
       setGlobalVariable("activePlayer", str(playerID(p)))
   update()

def nextSchemeStage(group=None, x=0, y=0):
    mute()

    #We need a new Scheme card
    if group is None or group == table:
        group = mainSchemeDeck()
    if len(group) == 0: return

    if group.controller != me:
        remoteCall(group.controller, "nextSchemeStage", [group, x, y])
        return

    for c in table:
        if c.Type == 'main_scheme':
            c.moveToBottom(group)
        x = tableLocations['mainScheme'][0]
        y = tableLocations['mainScheme'][1]

    card = group.top()
    card.moveToTable(x, y)
    card.orientation = Rot90
    card.anchor = True

    #agendaSetup(card)
    notify("{} advances scheme to '{}'".format(me, card))

def nextVillainStage(group=None, x=0, y=0):
    mute()

    #We need a new Villain card
    if group is None or group == table:
        group = villainDeck()
    if len(group) == 0: return

    if group.controller != me:
        remoteCall(group.controller, "nextVillainStage", [group, x, y])
        return

    for c in table:
        if c.Type == 'villain':
            c.moveToBottom(group)
        x = tableLocations['villain'][0]
        y = tableLocations['villain'][1]

    card = group.top()
    card.moveToTable(x, y)
    card.anchor = True

    #agendaSetup(card)
    notify("{} advances scheme to '{}'".format(me, card))

def readyForNextRound(group=table, x=0, y=0):
    mute()
    if turnManagement():
        highlightPlayer(me, DoneColour)
        setPlayerDone()

def turnManagementOn(group, x=0, y=0):
    mute()
    setGlobalVariable("Automation", "Turn")
    clearHighlights(group)

def automationOff(group, x = 0, y = 0):
    mute()
    setGlobalVariable("Automation", "Off")
    clearHighlights(group)
    notify("{} disables all turn management".format(me))

def turnManagement():
    mute()
    auto = getGlobalVariable("Automation")
    return auto == "Turn" or len(auto) == 0

def phasePassed(args):
    mute()
    thisPhase = currentPhase()
    newPhase = thisPhase[1]
    if newPhase == 1:
        # Hero Phase
        mute()
    elif newPhase == 2:
        if getGlobalVariable("allowVillainPhase") == "True":
            # doVillainPhase(False)
            setGlobalVariable("allowVillainPhase", "False")


def turnPassed(args):
    cards = filter(lambda card: isEncounter([card]) or card.type == 'main_scheme' or card.type == 'villain', table)
    for c in cards:
        c.controller = getActivePlayer()

def advancePhase(group = None, x = 0, y = 0):
    if turnNumber() == 0:
        me.setActive()
    else:
        thisPhase = currentPhase()
        nextPhase = thisPhase[1] + 1
        if nextPhase == 2:
            if str(getGlobalVariable("allowVillainPhase")) != "True":
                return
            else:
                setPhase(nextPhase)
        elif nextPhase > 2:
            me.setActive()
            setPhase(1)
        else:
            setPhase(nextPhase)

def doEndHeroPhase():
    mute()

    # if activePlayers() == 0:
    #     whisper("All players have been eliminated: You have lost the game")
    #     return
    # if eliminated(me):
    #     whisper("You have been eliminated from the game")
    #     return

    for p in players:
        clearTargets()
        readyAll()
        drawMany(me.deck, me.MaxHandSize - len(me.hand))

        # Check for hand size!
        if len(me.hand) > num(me.counters["MaxHandSize"].value):
            discardCount = len(me.hand) - num(me.counters["MaxHandSize"].value)
            dlg = cardDlg(me.hand)
            dlg.title = "You have more than the allowed cards in hand."
            dlg.text = "Select " + str(discardCount) + " Card(s):"
            dlg.min = 0
            dlg.max = discardCount
            cardsSelected = dlg.show()
            if cardsSelected is not None:
                for card in cardsSelected:
                    discard(card)
        clearHighlights()
    advancePhase()

def highlightPlayer(p, state):
    if len(getPlayers()) <= 1:
        return
    #debug("highlightPlayer {} = {}".format(p, state))
    for card in table:
        if card.Type == "hero" or card.Type == "alter-ego" and card.controller == p:
            card.highlight = state

# calculate the number of plays that are Done
def numDone():
    done = getGlobalVariable("done")
    if done:
        return len(eval(done))
    else:
        return 0

def clearTargets(group=table, x=0, y=0):
    for c in group:
        if c.controller == me or (c.targetedBy is not None and c.targetedBy == me):
            c.target(False)

def clearHighlights(group=table, x=0, y=0):
    for c in group: # Safe to do on all cards, not just ones we control
        c.highlight = None

# #Triggered event OnPlayerGlobalVariableChanged
# #We use this to manage turn and phase management by tracking changes to the player "done" variable
def globalChanged(args):
    #debug("globalChanged(Variable {}, from {}, to {})".format(args.name, args.oldValue, args.value))
    if args.name == "done":
        checkPlayersDone()
    # elif args.name == "phase":
    #     notify("Phase: {}".format(args.value))

#------------------
# Card Type Checks
#------------------

def isScheme(cards, x = 0, y = 0):
    for c in cards:
        if c.Type != 'main_scheme' and c.Type != 'side_scheme':
            return False
    return True

def isHero(cards, x = 0, y = 0):
    for c in cards:
        if c.Type != 'hero' and c.Type != 'alter-ego':
            return False
    return True

def isAttackable(cards, x = 0, y = 0):
    for c in cards:
        if c.Type != 'villain' and c.Type != 'hero' and c.Type != 'minion' and c.Type != 'ally' and c.Type != 'alter-ego':
            return False
    return True

def exhaustable(cards, x = 0, y = 0):
    for c in cards:
        if c.Type != "hero" and c.Type != "alter-ego" and c.Type != "ally"  and c.Type != "upgrade" and c.Type != "support":
            return False
    return True

def isEncounter(cards, x = 0, y = 0):
    for c in cards:
        if c.Type != "minion" and c.Type != "attachment" and c.Type != "treachery" and c.Type != "environment" and c.Type != "side_scheme" and c.Type != "obligation":
            return False
    return True
