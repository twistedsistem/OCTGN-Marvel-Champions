import clr
import re
clr.AddReference('System.Web.Extensions')
from System.Web.Script.Serialization import JavaScriptSerializer

showDebug = False #Can be changed to turn on debug - we don't care about the value on game reconnect so it is safe to use a python global

def debug(str):
    if showDebug:
        whisper(str)

def toggleDebug(group, x=0, y=0):
    global showDebug
    showDebug = not showDebug
    if showDebug:
        notify("{} turns on debug".format(me))
    else:
        notify("{} turns off debug".format(me))

#Return the default x coordinate of the players hero
def playerX(player):
    pLeft = ((BoardWidth * -1) / 2) + ((BoardWidth/len(getPlayers())) * player)
    pRight = ((BoardWidth * -1) / 2) + ((BoardWidth/len(getPlayers())) * (player + 1))
    pWidth = pLeft - pRight
    pCenter = pLeft - (pWidth / 2)
    return (pCenter - 35)

#Return the default x coordinate of the villain
def villainX(villainCount, villain):
    pLeft = ((BoardWidth * -1) / 2) + ((BoardWidth/villainCount) * villain)
    pRight = ((BoardWidth * -1) / 2) + ((BoardWidth/villainCount) * (villain + 1))
    pWidth = pLeft - pRight
    pCenter = pLeft - (pWidth / 2)
    return (pCenter - 35)


#------------------------------------------------------------
# Card Type Checks
#------------------------------------------------------------

def isScheme(cards, x = 0, y = 0):
    for c in cards:
        if c.Type != 'main_scheme' and c.Type != 'side_scheme':
            return False
    return True

def isHero(cards, x = 0, y = 0):
    for c in cards:
        if c.Type != 'hero' and c.Type != 'alter_ego':
            return False
    return True

def isPlayerCard(card):
    return card.owner in getPlayers()

def isVillain(cards, x = 0, y = 0):
    for c in cards:
        if c.Type != 'villain':
            return False
    return True

def isAttackable(cards, x = 0, y = 0):
    for c in cards:
        if c.Type != 'villain' and c.Type != 'hero' and c.Type != 'minion' and c.Type != 'ally' and c.Type != 'alter_ego':
            return False
    return True

def exhaustable(cards, x = 0, y = 0):
    for c in cards:
        if c.Type != "hero" and c.Type != "alter_ego" and c.Type != "ally"  and c.Type != "upgrade" and c.Type != "support":
            return False
    return True

def isEncounter(cards, x = 0, y = 0):
    for c in cards:
        if c.Type != "minion" and c.Type != "attachment" and c.Type != "treachery" and c.Type != "environment" and c.Type != "side_scheme" and c.Type != "obligation":
            return False
    return True

def isPermanent(card):
    return re.search('.*Permanent.*', card.properties["Text"], re.IGNORECASE)

def hasVictory(card):
    return re.search('.*Victory \d+.*', card.properties["Text"], re.IGNORECASE)


#------------------------------------------------------------
# Shared Piles
#------------------------------------------------------------

def mainSchemeDeck():
    return shared.piles['Scheme']

def villainDeck():
    return shared.piles['Villain']

def encounterDeck():
    return shared.piles['Encounter']

def encounterDiscardDeck():
    return shared.piles['Encounter Discard']

def encounterAndDiscardDeck():
    deck = list(shared.piles['Encounter'])
    deck.extend(shared.piles['Encounter Discard'])
    return deck

def specialDeck():
    return shared.piles['Special']

def specialDeckDiscard():
    return shared.piles['Special Discard']

def removedFromGameDeck():
    return shared.piles['Removed']

def campaignDeck():
    return shared.piles['Campaign']

def victoryDisplay():
    return shared.piles['Victory']

def setupPile():
    return shared.piles["Setup"]

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

#Store this player's starting position (players ID for this game)
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
    debug("Player {} sits in position {} for game {}".format(me, id, game))
    return id

def playerID(p):
    return num(p.getGlobalVariable("playerID"))

#Returns player object based on the customer playerIDs givine from the myID() function default returns player 0
def getPlayerByID(id):
    for p in players:
        if num(p.getGlobalVariable("playerID")) == num(id):
            return p
        elif num(id) >= len(getPlayers()) and num(p.getGlobalVariable("playerID")) == 0:
            return p

def deckLocked():
    return me.getGlobalVariable("deckLocked") == "1"

def lockDeck():
    me.setGlobalVariable("deckLocked", "1")

def unlockDeck():
    me.setGlobalVariable("deckLocked", "0")

def deckNotLoaded(group, x = 0, y = 0, checkGroup = me.Deck):
    if len(checkGroup) > 0:
        return False
    return True

def setFirstPlayer(group = table, x = 0, y = 0):
    mute()
    currentFirstPlayer = num(getGlobalVariable("firstPlayer"))
    firstPlayerToken = [card for card in table if card.Type == 'first_player']
    if (currentFirstPlayer + 1) >= len(getPlayers()):
        newFirstPlayer = 0
    else:
        newFirstPlayer = currentFirstPlayer + 1
    setGlobalVariable("firstPlayer",str(newFirstPlayer))
    update()
    firstPlayerToken[0].controller = me
    firstPlayerToken[0].moveToTable(playerX(newFirstPlayer),firstPlayerToken[0].position[1])
    firstPlayerToken[0].sendToBack()

def setActiveVillain(card, x = 0, y = 0):
    if isVillain([card]):
        vCards = filter(lambda card: card.Type == "villain", table)
        for c in vCards:
            c.highlight = None
        card.highlight = ActiveColour

def getActiveVillain(group = table, x = 0, y = 0):
    vCards = filter(lambda card: card.Type == "villain", table)
    for c in vCards:
        if str(c.highlight).upper() == ActiveColour:
            return c


#------------------------------------------------------------
# Functions triggered by Events
#------------------------------------------------------------

#Triggered event OnTableLoad
# args: no args are passed with this event call
def initializeGame():
    mute()
    changeLog()
    pList = eval(getGlobalVariable("playerList"))
    pList.append(me._id)
    setGlobalVariable("playerList",str(pList))
    update()

#Triggered event OnLoadDeck
# args: player, groups
def deckLoaded(args):
    mute()
    if args.player != me:
        return

    isShared = False
    isPlayer = False
    for g in args.groups:
        if (g.name == 'Hand') or (g.name in me.piles):
            isPlayer = True

    update()
    tableSetup(table, 0, 0, isPlayer, isShared)

#Triggered event OnPlayerGlobalVariableChanged
#We use this to manage turn and phase management by tracking changes to the player "done" variable
def globalChanged(args):
    debug("globalChanged(Variable {}, from {}, to {})".format(args.name, args.oldValue, args.value))
    if args.name == "firstPlayer":
        notify("First player : {}".format(args.value))

def markersUpdate(args):
    mute()
    # if args.marker == "Damage" and args.card.Type == "villain":
        # shared.counters["HP"].value = shared.counters["HP"].value - (args.card.markers[DamageMarker] - args.value)
    # elif args.marker == "Damage" and (args.card.Type == "hero" or args.card.Type == "alter_ego"):
        # args.card.owner.counters["HP"].value = args.card.owner.counters["HP"].value - (args.card.markers[DamageMarker] - args.value)

#Triggered even OnCardDoubleClicked
def defaultCardAction(args):
    mute()
    if getActivePlayer() == None:
        whisper("No active player. Default double-click card action is disabled")
        return
    if args.card.group == table:
        if not args.card.isFaceUp or isScheme([args.card]):
             remoteCall(getActivePlayer(), "revealHide", args.card)
        else:
            if args.card.Type == "villain":
                villainBoost(args.card)
            elif args.card.Owner == "infinity_gauntlet":
                infinityGauntletBoost(args.card)
            elif exhaustable([args.card]):
                readyExhaust(args.card)

#Triggered event OnOverRideTurnPassed
def overrideTurnPass(args):
    whisper("Plugin has built a custom turn and phase mechanic so the default turn process has been disabled")
    return

#Triggered event OnPhasePassed
def phasePassed(args):
    debug("phasePassed triggered")
    mute()
    thisPhase = currentPhase()
    newPhase = thisPhase[1]

    if newPhase == 1:
        setGlobalVariable("phase", "Hero Phase")
    elif newPhase == 2:
        setGlobalVariable("phase", "Villain Phase")

#Triggered event OnTurnPassed
def turnPassed(args):
    debug("turnPassed triggered")
    setPhase(1)

#Triggered event OnScriptedCardsMoved and OnCardsMoved
def moveCards(args):
    mute()
    autoCharges(args)

#------------------------------------------------------------
# Game Flow functions
#------------------------------------------------------------

def changeLog():
    mute()
    #### LOAD CHANGELOG
    v1, v2, v3, v4 = gameVersion.split('.')  ## split apart the game's version number
    v1 = int(v1) * 1000000
    v2 = int(v2) * 10000
    v3 = int(v3) * 100
    v4 = int(v4)
    currentVersion = v1 + v2 + v3 + v4  ## An integer interpretation of the version number, for comparisons later
    lastVersion = getSetting("lastVersion", convertToString(currentVersion - 1))  ## -1 is for players experiencing the system for the first time
    lastVersion = int(lastVersion)
    for log in sorted(changelog):  ## Sort the dictionary numerically
        if lastVersion < int(log):  ## Trigger a changelog for each update they haven't seen yet.
            stringVersion, date, text = changelog[log]
            updates = '\n-'.join(text)
            confirm("What's new in {} ({}):\n-{}".format(stringVersion, date, updates))
    setSetting("lastVersion", convertToString(currentVersion))  ## Store's the current version to a setting

def tableSetup(group=table, x=0, y=0, doPlayer=True, doEncounter=False):
    mute()

    if not getLock():
        whisper("Others players are setting up, please try manual setup again (Ctrl+Shift+S)")
        return

    unlockDeck()

    if doPlayer:
        heroSetup()

    if doEncounter:
        villainSetup()

    if not clearLock():
        notify("Players performed setup at the same time causing problems, please reset and try again")

    update()

    g = getGlobalVariable("playersSetup")
    v = getGlobalVariable("villainSetup")
    if num(g) == len(getPlayers()) and len(v) > 0:
        table.create("65377f60-0de4-4196-a49e-96a550b4df81",playerX(0),tableLocations['hero'][1]+40,1,True)
        firstPlayerToken = filter(lambda card: card.Type == 'first_player', table)
        firstPlayerToken[0].sendToBack()
        for p in players:
            remoteCall(p,"addObligationsToEncounter",[table, x, y, p])
        update()
        players[0].setActive()
        setGlobalVariable("firstPlayer",str(0))
        debug("{} is active".format(str(players[0].name)))

        update()

def addObligationsToEncounter(group = table, x = 0, y = 0, p=me):
    vName = getGlobalVariable("villainSetup")
    update()
    if vName == 'The Wrecking Crew' or vName == 'Kang': return
    playerOblCard = filter(lambda card: card.Type == 'obligation', me.piles["Nemesis"])
    for c in playerOblCard:
        c.moveTo(encounterDeck())
    shuffle(encounterDeck())

def advanceGame(group = None, x = 0, y = 0):
    # Check if we should pass the turn or just change the phase
    debug("advanceGame triggered")
    if currentPhase()[1] == 1:
        doEndHeroPhase()
        remoteCall(getActivePlayer(), "setPhase", [2]) #Must be triggered by active player

    elif currentPhase()[1] == 2:
        setFirstPlayer()
        setGlobalVariable("phase", "Hero Phase")
        remoteCall(getActivePlayer(), "nextTurn", [Player(num(getGlobalVariable("firstPlayer"))+1), True]) #Must be triggered by active player to add +1 to turn counter
        update()
        shared.counters['Round'].value += 1
        saveTable(getGlobalVariable("phase"))

    update()

def doEndHeroPhase():
    mute()
    debug("doEndHeroPhase()")

    for p in players:
        remoteCall(p,"clearTargets",[])
        remoteCall(p,"readyAll",[])
        remoteCall(p,"drawMany",[p.piles['Deck'],p.MaxHandSize - len(p.piles['Hand'])])

        # Check for hand size!
        if len(p.piles['Hand']) > num(p.counters["MaxHandSize"].value):
            discardCount = len(p.piles['Hand']) - num(p.counters["MaxHandSize"].value)
            dlg = cardDlg(p.piles['Hand'])
            dlg.title = "You have more than the allowed cards in hand."
            dlg.text = "Select " + str(discardCount) + " Card(s) to discard :"
            dlg.min = 0
            dlg.max = discardCount
            cardsSelected = dlg.show()
            if cardsSelected is not None:
                for card in cardsSelected:
                    remoteCall(p,"discard",[card])

def passSharedControl(group, x=0, y=0):
    notify(me.name + " takes control of shared cards")
    mute()
    #Take control of each not player card on table
    for card in table:
        if not isPlayerCard(card):
            card.controller = me
    #Take control of each shared pile
    for p in shared.piles:
            if shared.piles[p].controller != me:
                shared.piles[p].controller = me

def readyAll(group = table, x = 0, y = 0):
    mute()
    for c in table:
        if c.controller == me and c.orientation != Rot0 and isEncounter([c]) != True and c.Type != "encounter" and c.Type != "villain" and c.Type != "main_scheme":
            c.orientation = Rot0
    notify("{} readies all their cards.".format(me))

def getPosition(card,x=0,y=0):
    t = getPlayers()
    notify("This cards position is {}".format(card.position))

def createCards(group,list,dict):
    for i in list:
        group.create(card_mapping[i],dict[i])

def deleteCards(group):
    mute()
    for card in group:
        card.delete()

def changeForm(card, x = 0, y = 0):
    mute()
    if card.Owner == 'ant' or card.Owner == 'wsp':
        choice = askChoice("Which form would you like to change into: ", ["Tiny", "Giant", "Alter-Ego"])
        if choice == 0: return
        if choice == 1:
            card.alternate = ""
            notify("{} changes form to {}.".format(me, card))
        if choice == 2:
            card.alternate = "c"
            notify("{} changes form to {}.".format(me, card))
        if choice == 3:
            card.alternate = "b"
            notify("{} changes form to {}.".format(me, card))
    elif "b" in card.alternates:
        if card.alternate == "":
            card.alternate = "b"
            notify("{} changes form to {}.".format(me, card))
        else:
            card.alternate = ""
            notify("{} changes form to {}.".format(me, card))
    me.counters["MaxHandSize"].value = num(card.HandSize)

def specific_hero_flip(card, x = 0, y = 0):
    mute()
    if card.Owner == 'warm':
        if card.Type == "hero":
            card.markers[AllPurposeMarker] = 5
            notify("{} adds 5 Marker on {}.".format(me, card))
        if card.Type == "alter_ego":
            card.markers[AllPurposeMarker] = 0
            notify("{} removes all Marker from {}.".format(me, card))

def villainBoost(card, x=0, y=0, who=me):
    mute()

    vName = getGlobalVariable("villainSetup")
    if card == table and vName != 'The Wrecking Crew':
        vCard = filter(lambda card: card.Type == "villain", table)
        card = vCard[0]
    elif card == table:
        vCard = filter(lambda card: getActiveVillain(), table)
        card = vCard[0]
    cardX = card.position[0] + 20
    cardY = card.position[1] + 20

    if card.controller != me:
        remoteCall(card.controller, "villainBoost", [card, x, y, me])
        return

    if vName != 'The Wrecking Crew':
        boostList = encounterDeck().top()
        boostList.moveToTable(cardX,cardY,True)
        boostList.controller = who
        if len(encounterDeck()) == 0:
            notifyBar("#FF0000", "Encounter pile is empty.")
            shuffleDiscardIntoDeck(encounterDiscardDeck())
    else:
        setActiveVillain(card, x, y)
        encCards = filter(lambda card: card.Owner == getActiveVillain().Owner, encounterDeck())
        boostList = encCards[0]
        boostList.moveToTable(cardX,cardY,True)
        boostList.controller = who
        newEncCards = filter(lambda card: card.Owner == getActiveVillain().Owner, encounterDeck())
        disEncCards = filter(lambda card: card.Owner == getActiveVillain().Owner, encounterDiscardDeck())
        if len(newEncCards) == 0:
            notifyBar("#FF0000", "{} encounter pile is empty.".format(getActiveVillain()))
            for c in disEncCards:
                c.moveTo(encounterDeck())
            encounterDeck().shuffle()

def infinityGauntletBoost(card, x=0, y=0, who=me):
    mute()

    cardX = card.position[0] + 20
    cardY = card.position[1] + 20

    if card.controller != me:
        remoteCall(card.controller, "infinityGauntletBoost", [card, x, y, me])
        return

    boostList = specialDeck().top()
    boostList.moveToTable(cardX,cardY,True)
    boostList.controller = who
    boostList.isFaceUp = True
    if len(specialDeck()) == 0:
        notifyBar("#FF0000", "Special pile is empty.")
        shuffleDiscardIntoDeck(specialDeck())

def addDamage(card, x = 0, y = 0):
    mute()
    card.markers[DamageMarker] += 1
    notify("{} adds 1 Damage on {}.".format(me, card))

def addMarker(card, x = 0, y = 0, qty = 1):
    mute()
    card.controller = me
    if isScheme([card]):
        card.markers[ThreatMarker] += qty
        notify("{} adds {} Threat on {}.".format(me, qty, card))
    elif card.Type in ["hero", "alter_ego", "villain"]:
        card.markers[HealthMarker] += qty
        notify("{} adds {} Hit Point on {}.".format(me, qty, card))
    elif isAttackable([card]):
        card.markers[DamageMarker] += qty
        notify("{} adds {} Damage on {}.".format(me, qty, card))
    else:
        card.markers[AllPurposeMarker] += qty
        notify("{} adds {} Marker on {}.".format(me, qty, card))

def removeMarker(card, x = 0, y = 0, qty = 1):
    mute()
    card.controller = me
    if isScheme([card]):
        card.markers[ThreatMarker] -= qty
        notify("{} removes {} Threat on {}.".format(me, qty, card))
    elif card.Type in ["hero", "alter_ego", "villain"]:
        card.markers[HealthMarker] -= qty
        notify("{} removes {} Hit Point on {}.".format(me, qty, card))
    elif isAttackable([card]):
        card.markers[DamageMarker] -= qty
        notify("{} removes {} Damage on {}.".format(me, qty, card))
    else:
        card.markers[AllPurposeMarker] -= qty
        notify("{} removes {} Marker on {}.".format(me, qty, card))

def clearMarker(card, x = 0, y = 0):
    mute()
    card.controller = me
    if isScheme([card]):
        card.markers[ThreatMarker] = 0
        notify("{} removes all Threat on {}.".format(me, card))
    elif card.Type in ["hero", "alter_ego", "villain"]:
        card.markers[HealthMarker] = 0
        notify("{} removes all Hit Point on {}.".format(me, card))
    elif isAttackable([card]):
        card.markers[DamageMarker] = 0
        notify("{} removes all Damage on {}.".format(me, card))
    else:
        card.markers[AllPurposeMarker] = 0
        notify("{} removes all Markers on {}.".format(me, card))

def add3Marker(card, x = 0, y = 0, qty = 3):
    mute()
    if isScheme([card]):
        card.markers[ThreatMarker] += qty
        notify("{} adds 3 Threats on {}.".format(me, card))
    elif card.Type in ["hero", "alter_ego", "villain"]:
        card.markers[HealthMarker] += qty
        notify("{} adds 3 Hit Points on {}.".format(me, card))
    elif isAttackable([card]):
        card.markers[DamageMarker] += qty
        notify("{} adds 3 Damages on {}.".format(me, card))
    else:
        card.markers[AllPurposeMarker] += qty
        notify("{} adds 3 Markers on {}.".format(me, card))

def removeDamage(card, x = 0, y = 0):
    mute()
    card.markers[DamageMarker] -= 1
    notify("{} removes 1 Damage from {}.".format(me, card))

def clearDamage(card, x = 0, y = 0):
    mute()
    card.markers[DamageMarker] = 0
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

def addAcceleration(card, x = 0, y = 0):
    mute()
    card.markers[AccelerationMarker] += 1
    notify("{} adds 1 Acceleration on {}.".format(me, card))

def removeAcceleration(card, x = 0, y = 0):
    mute()
    card.markers[AccelerationMarker] -= 1
    notify("{} removes 1 Acceleration from {}.".format(me, card))

def clearAcceleration(card, x = 0, y = 0):
    mute()
    card.markers[AccelerationMarker] = 0
    notify("{} removes all Acceleration from {}.".format(me, card))

def addAPCounter(card, x=0, y=0, qty=1):
    mute()
    card.controller = me
    card.markers[AllPurposeMarker] += qty
    notify("{} adds {} Marker(s) on {}.".format(me, qty, card))

def removeAPCounter(card, x = 0, y = 0):
    mute()
    card.controller = me
    card.markers[AllPurposeMarker] -= 1
    notify("{} removes 1 Marker from {}.".format(me, card))

def clearAPCounter(card, x = 0, y = 0):
    mute()
    card.controller = me
    card.markers[AllPurposeMarker] = 0
    notify("{} removes all Marker from {}.".format(me, card))

def stun(card, x = 0, y = 0):
    mute()
    if card.markers[StunnedMarker] == 2:
        notify("{} is already stunned.".format(card))
    else:
        card.markers[StunnedMarker] += 1
        notify("{} is stunned.".format(card))

def confuse(card, x = 0, y = 0):
    mute()
    if card.markers[ConfusedMarker] == 2:
        notify("{} is already confused.".format(card))
    else:
        card.markers[ConfusedMarker] += 1
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

def flipCoin(group, x = 0, y = 0):
    mute()
    n = rnd(1, 2)
    if n == 1:
        notify("{} flips heads.".format(me))
    else:
        notify("{} flips tails.".format(me))

def randomNumber(group, x=0, y=0):
    mute()
    max = askInteger("Random number range (1 to ....)", 6)
    if max == None: return
    notify("{} randomly selects {} (1 to {})".format(me, rnd(1,max), max))

def randomPlayer(group, x=0, y=0):
    mute()
    players = getPlayers()
    if len(players) <= 1:
        notify("{} randomly selects {}".format(me, me))
    else:
        n = rnd(0, len(players)-1)
        notify("{} randomly selects {}".format(me, players[n]))

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
    if "b" in card.alternates:
        if card.Type == "hero" or card.Type == "alter_ego":
            changeForm(card)
            specific_hero_flip(card)
        else:
            if card.alternate == "":
                card.alternate = "b"
                if isScheme([card]):
                    placeThreatOnScheme(card)
            else:
                card.alternate = ""

            if card.Type == "villain":
                setHPOnCharacter(card)

            # Handle environments with counters (such as Criminal Enterprise, Avengers Tower, Bell Tower, ...)
            # Some of them enters play with X counters
            if card.Type == "environment":
                lookForCounters(card)

    else:
        if card.isFaceUp:
            card.isFaceUp = False
            clearMarker(card)
            notify("{} hides {}.".format(me, card))
        else:
            card.isFaceUp = True
            notify("{} reveals {}.".format(me, card))
            lookForToughness(card)
            lookForCounters(card)
            placeThreatOnScheme(card)
            setHPOnCharacter(card)  # Uncomment to try the HP automation for characters

def discard(card, x = 0, y = 0):
    mute()
    card.controller = me

    if isPermanent(card):
        notify("{} has 'Permanent' keyword and cannot be discarded!".format(card.name))
        return
    if card.Type == "hero" or card.Type == "alter_ego":
        return
    elif card.Type == "villain":
        nextVillainStage()
    elif card.Type == "main_scheme":
        nextSchemeStage()
    elif card.Owner == 'infinity_gauntlet':
        notify("{} discards {} from {}.".format(me, card, card.group.name))
        card.moveTo(specialDeckDiscard())
    elif isEncounter([card]):
        if isScheme([card]) and getGlobalVariable("villainSetup") == "Red Skull":
            notify("{} sent back to side schemes deck!".format(card))
            card.moveTo(specialDeckDiscard())
        elif hasVictory(card):
            notify("{} has 'Victory' keyword and is then sent to Victory Display!".format(card))
            card.moveTo(victoryDisplay())
        else:
            card.moveTo(encounterDiscardDeck())
    elif card.Owner == 'invocation':
        notify("{} discards {} from {}.".format(me, card, card.group.name))
        card.moveTo(me.piles["Special Deck Discard"])
    else:
        pile = card.owner.piles["Deck Discard"]
        who = pile.controller

        notify("{} discards {} from {}.".format(me, card, card.group.name))
        card.moveTo(me.piles["Deck Discard"])

        if who != me:
            card.setController(who)
            remoteCall(who, "doDiscard", [card, pile])
        else:
            doDiscard(card, pile)

    clearMarker(card)

def doDiscard(card, pile):
    card.moveTo(pile)

def draw(group, x = 0, y = 0):
    mute()
    drawCard(group)
    notify("{} draws a card.".format(me))

def drawMany(group, count = None):
    mute()
    if len(group) == 0: return
    if deckLocked():
        whisper("Your deck is locked, you cannot draw cards at this time")
        return
    if count is None:
        count = askInteger("Draw how many cards?", 6)
    if count is None or count < 0:
        whisper("drawMany: invalid card count")
        return
    for c in group.top(count):
        if group.name == 'Special Deck':
            c.moveToTable(0,0,False)
        else:
            c.moveTo(me.hand)

def drawUnrevealed(group=None, x=0, y=0):
    mute()
    if len(group) == 0:
        notify("{} is empty.".format(group.name))
        return
    if deckLocked():
        whisper("Your deck is locked, you cannot draw cards at this time")
        return

    card = group[0]
    card.moveToTable(0, 0, True)
    notify("{} draws an unrevealed card from the {}.".format(me, group.name))
    return card

def FlipDeckTopCard(group=None, x=0, y=0):
    mute()
    if len(group) == 0:
        notify("{} is empty.".format(group.name))
        return
    if deckLocked():
        whisper("Your deck is locked, you cannot draw cards at this time")
        return

    card = group[0]
    if card.isFaceUp:
        card.isFaceUp = False
        notify("{} hides {} from the {}.".format(me, card, group))
    else:
        card.isFaceUp = True
        notify("{} reveals {} from the {}.".format(me, card.name, group.name))
    return card

def bottomPlayerDeck(card, x = 0, y = 0):
    mute()
    card.moveToBottom(me.Deck)

def removeTopXCards(group):
    mute()
    nbCards = askInteger("How many cards to remove from the game ?", len(group))
    if nbCards == None: return
    while nbCards > 0:
        group[0].moveTo(me.piles['Removed'])
        nbCards -= 1
    notify("{} moves all cards from {} to the Removed pile".format(me, group.name))

def bottomEncounterDeck(card, x = 0, y = 0):
    mute()
    card.moveToBottom(encounterDeck())

def moveAllToEncounter(group):
    mute()
    if confirm("Shuffle all cards from {} to Encounter Deck?".format(group.name)):
        for c in group:
            c.moveTo(encounterDeck())
        notify("{} moves all cards from {} to the Encounter Deck".format(me, group.name))
        shuffle(encounterDeck())

def moveAllToEncounterTop(group):
    mute()
    if confirm("Move all cards from {} to the top of the Encounter Deck?".format(group.name)):
        for c in group:
            c.moveTo(encounterDeck())
            notify("{} moves all cards from {} to the top of the Encounter Deck".format(me, group.name))

def moveAllToEncounterBottom(group):
    mute()
    if confirm("Move all cards from {} to the bottom of the Encounter Deck?".format(group.name)):
        for c in group:
            c.moveToBottom(encounterDeck())
            notify("{} moves all cards from {} to the bottom of the Encounter Deck".format(me, group.name))

def drawCard(group):
    mute()
    if len(me.piles[group.name]) == 0:
        if group.name == "Special Deck":
            for c in me.piles["Special Deck Discard"]: c.moveTo(c.owner.piles["Special Deck"])
            me.piles["Special Deck"].shuffle()
            rnd(1,1)
        else:
            for c in me.piles["Deck Discard"]:
                c.moveTo(c.owner.Deck)
            me.Deck.shuffle()
            rnd(1,1)
    if group.name == 'Special Deck':
        card = me.piles["Special Deck"][0]
        card.moveToTable(0,0,False)
    else:
        card = me.deck[0]
        card.moveTo(card.owner.hand)

def mulligan(group, x = 0, y = 0):
    mute()
    dlg = cardDlg(me.hand)
    dlg.min = 0
    dlg.max = len(me.hand)
    dlg.text = "Select which cards you would like to mulligan"
    mulliganList = dlg.show()
    if not mulliganList:
        return
    if not confirm("Confirm Mulligan?"):
        return
    notify("{} mulligans.".format(me))
    for card in mulliganList:
        card.moveTo(card.owner.piles["Deck Discard"])
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
    card.moveTo(card.owner.piles["Deck Discard"])
    notify("{} randomly discards {} from {}.".format(me, card, group.name))

def shuffleDiscardIntoDeck(group, x = 0, y = 0):
    mute()
    if len(group) == 0: return
    if group == me.piles["Deck Discard"]:
        for card in group:
            card.moveTo(me.piles["Deck"])
        me.piles["Deck"].shuffle()
        notify("{} shuffles their discard pile into their Deck.".format(me))
    if group == me.piles["Special Deck Discard"]:
        for card in group:
            card.moveTo(me.piles["Special Deck"])
        me.piles["Special Deck"].shuffle()
        notify("{} shuffles the special discard pile into the special Deck.".format(me))
    if group == encounterDiscardDeck():
        for card in group:
            card.moveTo(shared.encounter)
        shared.encounter.shuffle()
        notify("{} shuffles the encounter discard pile into the encounter Deck.".format(me))
    if group == specialDeckDiscard():
        for card in group:
            card.moveTo(specialDeck())
        shared.encounter.shuffle()
        notify("{} shuffles the special discard pile into the special Deck.".format(me))

def shuffleSetIntoEncounter(group, x = 0, y = 0):
    mute()
    if len(group) == 0: return

    ownerList = []

    if group == specialDeck():
        for card in group:
            ownerExistsInList = ownerList.count(card.Owner)
            if ownerExistsInList == 0:
                ownerList.append(card.Owner)
        ownerChoice = askChoice("Which encounter set would you like to shuffle into deck?", ["Random"] + ownerList)
        if ownerChoice == 0: return
        if ownerChoice == 1:
            ownerRandom = rnd(0, len(ownerList)-1)
            for card in group:
                if card.Owner == ownerList[ownerRandom]:
                    card.moveTo(shared.encounter)
            notify("{} shuffles {} into the Encounter Deck.".format(me, ownerList[ownerRandom]))
        else:
            for card in group:
                if card.Owner == ownerList[ownerChoice-2]:
                    card.moveTo(shared.encounter)
            notify("{} shuffles {} into the Encounter Deck.".format(me, ownerList[ownerChoice-2]))
        shared.encounter.shuffle()

def viewGroup(group, x = 0, y = 0):
    group.lookAt(-1)

def pluralize(num):
   if num == 1:
       return ""
   else:
       return "s"


def drawOpeningHand():
    me.deck.shuffle()
    drawMany(me.deck, me.MaxHandSize)

def setHeroCounters(heroCard):
    me.counters['HP'].value = num(heroCard.HP)
    me.counters['MaxHandSize'].value = num(heroCard.HandSize)

def countHeros(p):
    heros = 0
    for card in table:
        if card.controller == p and (card.Type == "hero" or card.Type == "alter_ego"):
            heros += 1
    return heros

def createCard(group=None, x=0, y=0):
    cardID, quantity = askCard()
    cards = table.create(cardID, x, y, quantity, True)
    try:
        iterator = iter(cards)
    except TypeError:
        # not iterable
        notify("{} created {}.".format(me, cards))
    else:
        # iterable
        for card in cards:
            notify("{} created {}.".format(me, card))

def num(s):
   if not s: return 0
   try:
      return int(s)
   except ValueError:
      return 0

def moveToVictory(card, x=0, y=0):
    mute()
    card.moveTo(victoryDisplay())
    notify("{} adds '{}' to the Global Victory Display".format(me, card))

#------------------------------------------------------------
# Global variable manipulations function
#------------------------------------------------------------

def nextSchemeStage(group=None, x=0, y=0):
    mute()
    schemeCards = []

    # Global Variable
    vName = getGlobalVariable("villainSetup")

    # We need a new Scheme card
    if group is None or group == table:
        group = mainSchemeDeck()
    if len(group) == 0: return

    if group.controller != me:
        remoteCall(group.controller, "nextSchemeStage", [group, x, y])
        return

    if vName == 'Kang':
        whisper("You can't advance to next scheme using \"Next Scheme\" function for Kang. Use \"Next Villain\" instead")
    else:
        for c in table:
            if c.Type == 'main_scheme':
                x = c.position[0]
                y = c.position[1]
                currentScheme = num(c.CardNumber[:-1])
                c.moveToBottom(removedFromGameDeck())

        for card in mainSchemeDeck():
            if num(card.CardNumber[:-1]) == currentScheme + 1:
                card.moveToTable(x, y)
                card.anchor = False
                notify("{} advances scheme to '{}'".format(me, card))

def nextVillainStage(group=None, x=0, y=0):
    mute()

    # Global Variable
    vName = getGlobalVariable("villainSetup")

    # We need a new Villain card
    if group is None or group == table:
        group = villainDeck()
    if len(group) == 0: return

    if group.controller != me:
        remoteCall(group.controller, "nextVillainStage", [group, x, y])
        return

    if vName == 'The Wrecking Crew':
        vCards = filter(lambda card: card.Owner == getActiveVillain().Owner and (card.Type == 'villain' or card.Type == 'side_scheme'), table)
        for c in vCards:
            c.moveToBottom(removedFromGameDeck())

    elif vName == 'Kang':
        vCardsOnTable = sorted(filter(lambda card: card.Type == "villain", table), key=lambda c: c.CardNumber)
        vCards = sorted(filter(lambda card: card.Type == "villain", villainDeck()), key=lambda c: c.CardNumber)
        msCardsOnTable = sorted(filter(lambda card: card.Type == "main_scheme", table), key=lambda c: c.CardNumber)
        msCards = sorted(filter(lambda card: card.Type == "main_scheme", mainSchemeDeck()), key=lambda c: c.CardNumber)
        update()
        if vCardsOnTable[0].CardNumber == "11001" or vCardsOnTable[0].CardNumber == "11034":# Kang I (Standard or Expert)
            y = vCardsOnTable[0].position[1]
            vCardsOnTable[0].moveToBottom(removedFromGameDeck())
            if msCardsOnTable[0].CardNumber == "11007b": # Stage 1 main scheme
                msX, msY = msCardsOnTable[0].position
                if len(getPlayers()) == 1:
                    msCards[0].moveToTable(msX, msY)
                else:
                    msCards[0].moveToTable(tableLocations['mainSchemeCentered'][0],tableLocations['mainSchemeCentered'][1])
                msCardsOnTable[0].moveToBottom(removedFromGameDeck())
                loop = len(vCards) - 1
                while loop > 0:
                    vCards = sorted(filter(lambda card: card.Type == "villain", villainDeck()), key=lambda c: c.CardNumber)
                    ssCards = sorted(filter(lambda card: card.Type == "main_scheme", mainSchemeDeck()), key=lambda c: c.CardNumber)
                    randomKang = rnd(0, len(vCards)-2)
                    if loop > len(getPlayers()):
                        vCards[randomKang].moveToBottom(removedFromGameDeck())
                        ssCards[randomKang].moveToBottom(removedFromGameDeck())
                    else:
                        vCards[randomKang].moveToTable(villainX(len(getPlayers()), len(getPlayers()) - loop), y)
                        ssCards[randomKang].moveToTable(villainX(len(getPlayers()), len(getPlayers()) - loop)-10, y+100)
                    loop -= 1
        else:
            choice = askChoice("Are all players ready to advance to stage 4A ?", ["Yes", "No"])
            if choice == None or choice == 2: return
            for c in vCardsOnTable:
                c.moveToBottom(removedFromGameDeck())
            for c in msCardsOnTable:
                c.moveToBottom(removedFromGameDeck())
            vCards = sorted(filter(lambda card: card.Type == "villain", villainDeck()), key=lambda c: c.CardNumber)
            ssCards = sorted(filter(lambda card: card.Type == "main_scheme", mainSchemeDeck()), key=lambda c: c.CardNumber)
            lastIndex = len(vCards)-1
            vCards[lastIndex].moveToTable(villainX(1,0), tableLocations['villain'][1])
            ssCards[lastIndex].moveToTable(tableLocations['mainScheme'][0], tableLocations['mainScheme'][1])

    elif vName == 'Tower Defense':
        for c in table:
            if c.Type == 'villain':
                if c.Name == 'Proxima Midnight':
                    x1, y1 = c.position
                    if len(c.alternates) > 1:
                        currentVillain1 = num(c.CardNumber[:-1])
                    else:
                        currentVillain1 = num(c.CardNumber)
                    currentStun1 = c.markers[StunnedMarker]
                    currentTough1 = c.markers[ToughMarker]
                    currentConfused1 = c.markers[ConfusedMarker]
                    currentAcceleration1 = c.markers[AccelerationMarker]
                    currentAllPurpose1 = c.markers[AllPurposeMarker]
                    c.moveToBottom(removedFromGameDeck())
                if c.Name == 'Corvus Glaive':
                    x2, y2 = c.position
                    if len(c.alternates) > 1:
                        currentVillain2 = num(c.CardNumber[:-1])
                    else:
                        currentVillain2 = num(c.CardNumber)
                    currentStun2 = c.markers[StunnedMarker]
                    currentTough2 = c.markers[ToughMarker]
                    currentConfused2 = c.markers[ConfusedMarker]
                    currentAcceleration2 = c.markers[AccelerationMarker]
                    currentAllPurpose2 = c.markers[AllPurposeMarker]
                    c.moveToBottom(removedFromGameDeck())

        for card in villainDeck():
            if len(card.alternates) > 1:
                checkNumber = num(card.CardNumber[:-1])
            else:
                checkNumber = num(card.CardNumber)
                if checkNumber == currentVillain1 + 1:
                    card.moveToTable(x1, y1)
                    card.markers[StunnedMarker] = currentStun1
                    card.markers[ToughMarker] = currentTough1
                    card.markers[ConfusedMarker] = currentConfused1
                    card.markers[AccelerationMarker] = currentAcceleration1
                    card.markers[AllPurposeMarker] = currentAllPurpose1
                    card.anchor = False
                if checkNumber == currentVillain2 + 1:
                    card.moveToTable(x2, y2)
                    card.markers[StunnedMarker] = currentStun2
                    card.markers[ToughMarker] = currentTough2
                    card.markers[ConfusedMarker] = currentConfused2
                    card.markers[AccelerationMarker] = currentAcceleration2
                    card.markers[AllPurposeMarker] = currentAllPurpose2
                    card.anchor = False
                    SpecificVillainSetup(vName)
                    notify("{} advances Villain to the next stage".format(me))

    elif vName == 'Loki':
        vCards = sorted(filter(lambda card: card.Type == "villain", villainDeck()), key=lambda c: c.CardNumber)
        if len(vCards) > 0:
            randomLoki = rnd(0, len(vCards)-1) # Returns a random INTEGER value and use it to choose which Loki will be loaded
            
        for c in table:
            if c.Type == 'villain':
                x, y = c.position
                currentHealth = c.markers[HealthMarker]
                currentStun = c.markers[StunnedMarker]
                currentTough = c.markers[ToughMarker]
                currentConfused = c.markers[ConfusedMarker]
                currentAllPurpose = c.markers[AllPurposeMarker]
                choice = askChoice("What do you want to do ?", ["Put Loki in Victory Pile and bring another one", "Swap Loki with another Loki"])
                if choice == None: return
                if choice == 1:
                    c.moveTo(victoryDisplay())
                    vCards[randomLoki].moveToTable(x, y)
                    vCards[randomLoki].markers[ToughMarker] = currentTough
                    vCards[randomLoki].markers[StunnedMarker] = currentStun
                    vCards[randomLoki].markers[ConfusedMarker] = currentConfused
                    vCards[randomLoki].markers[AllPurposeMarker] = currentAllPurpose
                if choice == 2:
                    vCards[randomLoki].moveToTable(x, y)
                    vCards[randomLoki].markers[HealthMarker] = currentHealth
                    vCards[randomLoki].markers[ToughMarker] = currentTough
                    vCards[randomLoki].markers[StunnedMarker] = currentStun
                    vCards[randomLoki].markers[ConfusedMarker] = currentConfused
                    vCards[randomLoki].markers[AllPurposeMarker] = currentAllPurpose
                    c.moveTo(villainDeck())

    else:
        for c in table:
            if c.Type == 'villain':
                x, y = c.position
                if len(c.alternates) > 1:
                    currentVillain = num(c.CardNumber[:-1])
                else:
                    currentVillain = num(c.CardNumber)
                currentStun = c.markers[StunnedMarker]
                currentTough = c.markers[ToughMarker]
                currentConfused = c.markers[ConfusedMarker]
                currentAcceleration = c.markers[AccelerationMarker]
                currentAllPurpose = c.markers[AllPurposeMarker]
                c.moveToBottom(removedFromGameDeck())

        for card in villainDeck():
            if len(card.alternates) > 1:
                checkNumber = num(card.CardNumber[:-1])
            else:
                checkNumber = num(card.CardNumber)
            if checkNumber == currentVillain + 1:
                card.moveToTable(x, y)
                card.markers[StunnedMarker] = currentStun
                card.markers[ToughMarker] = currentTough
                card.markers[ConfusedMarker] = currentConfused
                card.markers[AccelerationMarker] = currentAcceleration
                card.markers[AllPurposeMarker] = currentAllPurpose
                card.anchor = False
                SpecificVillainSetup(vName)
                notify("{} advances Villain to the next stage".format(me))


def clearTargets(group=table, x=0, y=0):
    for c in group:
        if c.controller == me or (c.targetedBy is not None and c.targetedBy == me):
            c.target(False)


#------------------------------------------------------------
# Highlight
#------------------------------------------------------------

def blueHighlight(card, x=0 , y=0):
    card.highlight = BlueColour

def orangeHighlight(card, x=0 , y=0):
    card.highlight = OrangeColour

def greenHighlight(card, x=0 , y=0):
    card.highlight = GreenColour

def purpleHighlight(card, x=0 , y=0):
    card.highlight = PurpleColour

def redHighlight(card, x=0 , y=0):
    card.highlight = RedColour

def blackHighlight(card, x=0 , y=0):
    card.highlight = BlackColour

def whiteHighlight(card, x=0 , y=0):
    card.highlight = WhiteColour

def clearHighlight(card, x=0, y=0):
    card.highlight = None

#------------------------------------------------------------
# Automation
#------------------------------------------------------------
def autoCharges(args):
    mute()
    # Only for move card from Pile to Table
    if isinstance(args.fromGroups[0],Pile) and isinstance(args.toGroups[0],Table):
        if len(args.cards) == 1:
            card = args.cards[0]
            if card.controller == me and card.isFaceUp:
                lookForCounters(card)
                lookForToughness(card)
                placeThreatOnScheme(card)
                setHPOnCharacter(card)  # Uncomment to try the HP automation for characters

def lookForToughness(card):
    """
    Adds a Tough status card to a character if such ability is found in card's text
    """
    if card.Type in ["villain", "minion", "ally"]:
        description_search = re.search('.*Toughness.*', card.properties["Text"], re.IGNORECASE)
        if description_search:
            tough(card)

def lookForCounters(card):
    """
    Init the number of counters (all purpose) on a given card
    """
    #Capture text between "(. counters)"
    if card.markers[AllPurposeMarker] == 0:
        nb_players = len(getPlayers())

        # This should match all "Uses (x whatever counters)" cases. Warning: some of them are based on number of players (such as Crossbone's Machine Gun)
        description_search = re.search('.*\((\d+)(.?\[per_player\])?.*counters\)*.', card.properties["Text"], re.IGNORECASE)
        if description_search:
            nb_base_counters = int(description_search.group(1))
            # If more than one group found, then the number of counters changes with number of players
            is_per_player = description_search.group(2) is not None

            nb_counters = (nb_base_counters * nb_players) if is_per_player else nb_base_counters
            log_msg = "Initializing {} with {} counter(s)".format(card.name, nb_counters)

            # Some cards add additional counters based on number of players (such as Fanaticism)
            additional_search = re.search('.*(\d+).?\[per_player\] additional*.', card.properties["Text"], re.IGNORECASE)
            additional_counters = 0
            if additional_search:
                additional_counters = int(additional_search.group(1)) * nb_players
                log_msg += " + {} additional counter(s)".format(additional_counters)

            notify(log_msg)
            total_counters = nb_counters + additional_counters
            addAPCounter(card, x=0, y=0, qty=total_counters)

    
        description_search = re.search('.*enters play with (\d+).?(\[per_player\])?.*counters on.*', card.properties["Text"], re.IGNORECASE)
        if description_search:
            nb_base_counters = int(description_search.group(1))
            # If more than one group found, then the number of counters changes with number of players
            is_per_player = description_search.group(2) is not None

            nb_counters = (nb_base_counters * nb_players) if is_per_player else nb_base_counters
            addAPCounter(card, x=0, y=0, qty=nb_counters)

def placeThreatOnScheme(card):
    """
    Init the number of threats on main & side schemes
    """
    if isScheme([card]) and card.markers[ThreatMarker] == 0:
        if card.properties["BaseThreat"] is not None and card.properties["BaseThreat"] != '' and card.properties["BaseThreatFixed"] is not None:
            init_val = int(card.properties["BaseThreat"])
            is_base_fixed = card.properties["BaseThreatFixed"] == "True"
            nb_players = len(getPlayers())
            scheme_txt = card.properties["Text"]
            log_msg = "Initializing {} with ".format(card.name)
            
            # Initial value
            base_threats = init_val
            if not is_base_fixed:
                base_threats = init_val * nb_players
            log_msg += "{} base threats".format(base_threats)
            
            # Handle 'Hinder' (Hinder 3[per_player])
            add_hinder = 0
            description_search = re.search('.*Hinder (\d+).?\[per_player\].*', card.properties["Text"], re.IGNORECASE)
            if description_search:
                add_hinder = int(description_search.group(1)) * nb_players
                log_msg += " + {} threats from Hinder keyword".format(add_hinder)

            # Edge cases: add threats when revealed (but only if not already found Hinder text because the reminder contains the searched text)
            # This is mainly due to inconsistent wording between beginning of the game before Hinder keyword arrived
            add_others = 0
            description_search = re.search('.*Place an additional (\d+).?\[per_hero\] threat here.*', card.properties["Text"], re.IGNORECASE)
            if description_search and add_hinder == 0:
                add_others = int(description_search.group(1)) * nb_players
                log_msg += " + {} threats from card text".format(add_others)

            total_threats = base_threats + add_hinder + add_others
            notify(log_msg)
            addMarker(card, x=0, y=0, qty=int(total_threats))

def setHPOnCharacter(card):
    """
    Sets Damage markers on characters based on their defined HP value
    """
    # Handle edge case: exchange Loki with another one, all HP and status cards must be kept
    if card.Type == "villain" and getGlobalVariable("villainSetup") == "Loki":
        lokis_on_table = [c for c in table if c.Type == 'villain']
        if len(lokis_on_table) == 2: # There should be 2 Loki cards on table: the previous one and the new one
            # The 'previous' one is the one that has still some HP, the 'new' one enters play and then has not yet defined HP		
            previous_loki = [c for c in lokis_on_table if c.markers[HealthMarker] > 0]
            new_loki = [c for c in lokis_on_table if c.markers[HealthMarker] == 0]
            if len(previous_loki) == 1 and len(new_loki) == 1:
                notify("Copy all markers from actual Loki to new one!")
                new_loki[0].markers[HealthMarker] = previous_loki[0].markers[HealthMarker]
                new_loki[0].markers[ToughMarker] = previous_loki[0].markers[ToughMarker]
                new_loki[0].markers[StunnedMarker] = previous_loki[0].markers[StunnedMarker]
                new_loki[0].markers[ConfusedMarker] = previous_loki[0].markers[ConfusedMarker]
                new_loki[0].markers[AllPurposeMarker] = previous_loki[0].markers[AllPurposeMarker]

    if card.Type in ["hero", "alter_ego", "villain"] and card.markers[HealthMarker] == 0:
        nb_players = len(getPlayers())
        base_hp = int(card.properties["HP"])
        is_per_hero = card.properties["HP_Per_Hero"] == "True"
        total_hp = base_hp * nb_players if is_per_hero else base_hp
        addMarker(card, x=0, y=0, qty=int(total_hp))