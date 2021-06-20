import clr
import re
clr.AddReference('System.Web.Extensions')
from System.Web.Script.Serialization import JavaScriptSerializer

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

#Returns player object based on the customer playerIDs givine from the myID() function default returns player 0
def getPlayerByID(id):
    for p in players:
        if num(p.getGlobalVariable("playerID")) == num(id):
            return p
        elif num(id) >= len(getPlayers()) and num(p.getGlobalVariable("playerID")) == 0:
            return p

#------------------------------------------------------------
# Functions triggered by Events
#------------------------------------------------------------

#Triggered event OnTableLoad
# args: no args are passed with this event call
def initializeGame():
    mute()
    changeLog()
    setPlayerList()
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
    #     elif g.name in shared.piles:
    #         isShared = True

    # #If we are loading into the shared piles we need to become the controller of all the shared piles
    # if isShared:
    #     notify("{} Takes control of the encounter deck".format(me))
    #     for p in shared.piles:
    #         if shared.piles[p].controller != me:
    #             shared.piles[p].controller = me
    #     update()

    # #Cards for the encounter deck and player deck are loaded into the discard pile because this has visibility="all"
    # #Check for cards with a Setup effects and move other cards back into the correct pile
    # for pile in args.groups:
    #     for card in pile:
    #         if card.Setup == 't' and card.Type not in [ 'Agenda' , 'Act', 'Scenario' ]:
    #             addToTable(card)
    #         elif card.Setup == 's' and card.Type not in [ 'Agenda' , 'Act', 'Scenario' ]:
    #             addToStagingArea(card)
    #         elif pile == shared.piles['Encounter Discard Pile']:
    #             card.moveTo(shared.piles['Encounter'])
    #         elif pile == me.piles['Discard Pile']:
    #             card.moveTo(me.deck)
    #     if pile.name == "Chaos Bag":
    #         createChaosBag(table)
    #     elif pile.name == "Encounter Discard Pile":
    #         createEncounterCardClicky(table)

    update()
    tableSetup(table, 0, 0, isPlayer, isShared)

#Triggered event OnPlayerGlobalVariableChanged
#We use this to manage turn and phase management by tracking changes to the player "done" variable
def globalChanged(args):
    #debug("globalChanged(Variable {}, from {}, to {})".format(args.name, args.oldValue, args.value))
    if args.name == "done":
        checkPlayersDone()
    # elif args.name == "phase":
    #     notify("Phase: {}".format(args.value))

#Triggered even OnCardDoubleClicked
def defaultCardAction(args):
    if not args.card.isFaceUp or isScheme([args.card]):
         revealHide(args.card)
    else:
        if args.card.Type == "villain":
            villainBoost(args.card)
        elif exhaustable([args.card]):
            readyExhaust(args.card)

#Triggered event OnOverRideTurnPassed
def overrideTurnPass(args):
    whisper("Plugin has built a custom turn and phase mechanic so the default turn process has been disabled")
    return

#------------------------------------------------------------
# Game Flow functions
#------------------------------------------------------------

def readyToStartGame():
    g = getGlobalVariable("playersSetup")
    v = getGlobalVariable("villainSetup")
    if num(g) == len(getPlayers()) and len(v) > 0:
        return True
    else:
        return False

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

def setPlayerList():
    pList = eval(getGlobalVariable("playerList"))
    for p in players:
        pList.append(p._id)
    setGlobalVariable("playerList",str(pList))

def tableSetup(group=table, x=0, y=0, doPlayer=True, doEncounter=False):
    mute()

    if not getLock():
        whisper("Others players are setting up, please try manual setup again (Ctrl+Shift+S)")
        return

    unlockDeck()

    if doPlayer:
        id = myID() # This ensures we have a unique ID based on our position in the setup order
        heroCount = countHeros(me)
        passSharedControl(me)

        # Find any Permanent cards
        #permanents = filter(lambda card: "Permanent" in card.Keywords or "Permanent." in card.Text, me.deck)

        # Move Hero to the table
        newHero = False
        hero = filter(lambda card: card.Type == "hero", me.Deck)
        if hero:
            heroCount += 1
            newHero = True
            heroCard = hero[0]
            heroCard.moveToTable(playerX(id),playerY)
            heroCard.alternate = 'b'
            setHeroCounters(heroCard)
            notify("{} places his Hero on the table".format(me))

        if newHero:
            me.deck.shuffle()
            if len(me.hand) == 0:
                drawOpeningHand()

            createCards(heroCard.owner.piles["Nemesis Deck"],nemesis[str(heroCard.properties["Owner"])].keys(),nemesis[str(heroCard.properties["Owner"])]) 
            if str(heroCard.properties["Owner"]) == 'doctor_strange':
                createCards(me.piles['Special Deck'],special_decks['doctor_strange'].keys(),special_decks['doctor_strange'])
                
    # If we loaded the encounter deck - add the first main scheme card to the table
    if doEncounter:
        mainSchemeCards = filter(lambda card: card.Type == "main_scheme", villainDeck())
        villainCards = filter(lambda card: card.Type == "villain", villainDeck())
        encounterDeckCards = filter(lambda card: card.Type != "villain" and card.Type != "main_scheme", villainDeck())
        for c in encounterDeckCards:
            c.moveTo(encounterDeck())
        for c in mainSchemeCards:
            c.moveTo(schemeDeck())

        sorted(mainSchemeCards)[0].moveToTable(tableLocations['mainScheme'][0],tableLocations['mainScheme'][1])
        #sorted(mainSchemeCards)[0].orientation = Rot90
        #sorted(mainSchemeCards)[0].alternate = "b"
        sorted(mainSchemeCards)[0].anchor = True
        sorted(mainSchemeCards).pop(0)
        gameDifficulty = getGlobalVariable("difficulty")
        vName = getGlobalVariable("villainSetup")
        villainCards = sorted(villainCards)
        if vName != 'The Wrecking Crew' and vName != 'Kang':
            if gameDifficulty == "1":
                villainCards[0].delete()
                villainCards.pop(0)
            else:
                villainCards[len(villainCards) - 1].delete()
                villainCards.pop(len(villainCards) - 1)
            villainCards[0].moveToTable(villainX(1,0),tableLocations['villain'][1])
            villainCards[0].anchor = True
        elif vName == 'The Wrecking Crew':
            if gameDifficulty == "1":
                vCards = villainCards[1::2]
            else:
                vCards = villainCards[::2]
            for idx, c in enumerate(vCards):
                c.moveToTable(villainX(4,idx),tableLocations['villain'][1])
                if idx == 0:
                    c.highlight = ActiveColour
            ssCards = filter(lambda card: card.Type == "side_scheme", encounterDeck())
            for idx, c in enumerate(sorted(ssCards)):
                c.moveToTable(villainX(4,idx),-300)
        elif vName == 'Kang':
            if gameDifficulty == "1":
                villainCards = villainCards[6:]
            else:
                villainCards = villainCards[0:6]
            villainCards[0].moveToTable(villainX(1,0),tableLocations['villain'][1])
            villainCards[0].anchor = True

        shared.counters["HP"].value = int(villainCards[0].properties["HP"]) * len(players)
        shared.encounter.shuffle()
        # ecard = table.create('18976bc4-cfd2-4bca-bb47-e30de5eb2d7d',tableLocations['encounterCard'][0],tableLocations['encounterCard'][1],1,True)
        # ecard.orientation = Rot270
        # ecard.anchor = True
        table.create("65377f60-0de4-4196-a49e-96a550b4df81",playerX(0),playerY - 70,1,True)
        # setGlobalVariable("villainSetup",str(villainCards[0].name))

    if not clearLock():
        notify("Players performed setup at the same time causing problems, please reset and try again")

    update()

    if readyToStartGame():
        setGlobalVariable("firstPlayer",str(0))
        update()
        setPhase(1)
        setVirtualActivePlayer(getPlayerByID(num(getGlobalVariable("firstPlayer"))))
        addObligationsToEncounter()
        update()

def loadVillain(group, x = 0, y = 0):
    villainName = ''
    if not deckNotLoaded(group,0,0,shared.villain):
        confirm("Cannot generate a deck: You already have cards loaded.  Reset the game in order to generate a new deck.")
        return
    choice = askChoice("Which villain would you like to defeat?", ["Klaw", "Rhino", "Ultron", "Green Goblin: Mutagen Formula", "Green Goblin: Risky Business", "The Wrecking Crew", "Baron Zemo: Firestarter (By: FelixFactory)", "Crossbones", "Absorbing Man", "Taskmaster", "Zola", "Red Skull", "Kang"])
    passSharedControl(me)
    if choice == 0: return
    if choice == 1:
        createCards(shared.villain,sorted(klaw.keys()),klaw)
        notify('{} loaded "Klaw", Good Luck!'.format(me))
        villainName = 'Klaw'
    if choice == 2:
        createCards(shared.villain,sorted(rhino.keys()),rhino)
        notify('{} loaded "Rhino", Good Luck!'.format(me))
        villainName = 'Rhino'
    if choice == 3:
        createCards(shared.villain,sorted(ultron.keys()),ultron)
        notify('{} loaded "Ultron", Good Luck!'.format(me))
        villainName = 'Ultron'
    if choice == 4:
        createCards(shared.villain,sorted(mutagen_formula.keys()),mutagen_formula)
        notify('{} loaded "Mutagen Formula", Good Luck!'.format(me))
        villainName = 'Mutagen Formula'
    if choice == 5:
        createCards(shared.villain,sorted(risky_business.keys()),risky_business)
        notify('{} loaded "Risky Business", Good Luck!'.format(me))
        villainName = 'Risky Business'
    if choice == 6:
        createCards(shared.villain,sorted(the_wrecking_crew.keys()),the_wrecking_crew)
        notify('{} loaded "The Wrecking Crew", Good Luck!'.format(me))
        villainName = 'The Wrecking Crew'
    if choice == 7:
        createCards(shared.villain,sorted(baron_zemo_firestarter.keys()),baron_zemo_firestarter)
        notify('{} loaded "Baron Zemo: Firestarter (By: FelixFactory)", Good Luck!'.format(me))
        villainName = 'Baron Zemo: Firestarter'
    if choice == 8:
        createCards(shared.villain,sorted(crossbones.keys()),crossbones)
        createCards(shared.encounter,sorted(exper_weapon.keys()),exper_weapon)
        createCards(shared.encounter,sorted(weap_master.keys()),weap_master)
        createCards(shared.encounter,sorted(hydra_assault.keys()),hydra_assault)
        createCards(shared.encounter,sorted(legions_of_hydra.keys()),legions_of_hydra)
        notify('{} loaded "Crossbones", Good Luck!'.format(me))
        villainName = 'Crossbones'
    if choice == 9:
        createCards(shared.villain,sorted(absorbing_man.keys()),absorbing_man)
        createCards(shared.encounter,sorted(hydra_patrol.keys()),hydra_patrol)
        notify('{} loaded "Absorbing Man", Good Luck!'.format(me))
        villainName = 'Absorbing Man'
    if choice == 10:
        createCards(shared.villain,sorted(taskmaster.keys()),taskmaster)
        createCards(shared.encounter,sorted(hydra_patrol.keys()),hydra_patrol)
        createCards(shared.encounter,sorted(weap_master.keys()),weap_master)
        notify('{} loaded "Taskmaster", Good Luck!'.format(me))
        villainName = 'Taskmaster'
    if choice == 11:
        createCards(shared.villain,sorted(zola.keys()),zola)
        createCards(shared.encounter,sorted(under_attack.keys()),under_attack)
        notify('{} loaded "Zola", Good Luck!'.format(me))
        villainName = 'Zola'
    if choice == 12:
        createCards(shared.villain,sorted(red_skull.keys()),red_skull)
        createCards(shared.encounter,sorted(hydra_assault.keys()),hydra_assault)
        createCards(shared.encounter,sorted(hydra_patrol.keys()),hydra_patrol)
        notify('{} loaded "Red Skull", Good Luck!'.format(me))
        villainName = 'Red Skull'
    if choice == 13:
        createCards(shared.villain,sorted(the_once_and_future_kang.keys()),the_once_and_future_kang)
        notify('{} loaded "Kang", Good Luck!'.format(me))
        villainName = 'Kang'
    setGlobalVariable("villainSetup",str(villainName))
    update()
    loadEncounter(group)
    tableSetup(doPlayer=False,doEncounter=True)

def loadEncounter(group, x = 0, y = 0):
    vName = getGlobalVariable("villainSetup")
    if vName != 'The Wrecking Crew' and vName != "Baron Zemo: Firestarter" and vName != 'Crossbones' and vName !='Absorbing Man' and vName != 'Taskmaster' and vName != 'Zola' and vName != 'Red Skull':
        choice = askChoice("Which encounter would you like to take on?", ["Bomb Scare", "The Doomsday Chair", "Legions of Hydra", "Masters of Evil", "Under Attack", "Goblin Gimmicks", "A Mess of Things", "Power Drain", "Running Interference", "Temporal", "Anachronauts", "Master Of Time", "Ronan"])

        if choice == 0: return
        elif choice == 1:
            createCards(shared.encounter,sorted(bomb_scare.keys()),bomb_scare)
        if choice == 2:
            createCards(shared.encounter,sorted(the_doomsday_chair.keys()),the_doomsday_chair)
        if choice == 3:
            if vName != 'Crossbones':
                createCards(shared.encounter,sorted(legions_of_hydra.keys()),legions_of_hydra)
        if choice == 4:
            createCards(shared.encounter,sorted(masters_of_evil.keys()),masters_of_evil)
        if choice == 5:
            createCards(shared.encounter,sorted(under_attack.keys()),under_attack)
        if choice == 6:
            createCards(shared.encounter,sorted(goblin_gimmicks.keys()),goblin_gimmicks)
        if choice == 7:
            createCards(shared.encounter,sorted(mess_of_things.keys()),mess_of_things)
        if choice == 8:
            createCards(shared.encounter,sorted(power_drain.keys()),power_drain)
        if choice == 9:
            createCards(shared.encounter,sorted(running_interference.keys()),running_interference)
        if choice == 10:
            createCards(shared.encounter,sorted(temporal.keys()),temporal)
        if choice == 11:
            createCards(shared.encounter,sorted(anachronauts.keys()),anachronauts)
        if choice == 12:
            createCards(shared.encounter,sorted(mot.keys()),mot)
        if choice == 13:
            createCards(shared.encounter,sorted(ronan.keys()),ronan)
    elif vName == "Baron Zemo: Firestarter":
        createCards(shared.encounter,sorted(baron_zemo_firestarter_modules.keys()),baron_zemo_firestarter_modules)

    elif vName == 'The Wrecking Crew':
        choice = askChoice("What difficulty would you like to play at?", ["Standard", "Expert"])

        if choice == 0: return
        if choice == 1: return
        if choice == 2:
            setGlobalVariable("difficulty", "1")
            return

    choice = askChoice("What difficulty would you like to play at?", ["Standard", "Expert"])

    if choice == 0: return
    if choice == 1:
        createCards(shared.encounter,sorted(standard.keys()),standard)
    if choice == 2:
        createCards(shared.encounter,sorted(standard.keys()),standard)
        createCards(shared.encounter,sorted(expert.keys()),expert)
        setGlobalVariable("difficulty", "1")

def deckNotLoaded(group, x = 0, y = 0, checkGroup = me.Deck):
    if len(checkGroup) > 0:
        return False
    return True

def loadDeck(group, x = 0, y = 0):
    mute()
    if not deckNotLoaded(group):
        confirm("Cannot generate a deck: You already have cards loaded.  Reset the game in order to generate a new deck.")
        return
    choice = askChoice("What type of deck do you want to load?", ["An out of the box deck", "A registered deck"])

    if choice == 0: return
    if choice == 1:
        choice2 = askChoice("Which hero would you like to be?", ["Black Panther", "Captain Marvel", "Iron Man", "She Hulk", "Spider-Man", "Captain America", "Ms. Marvel", "Thor", "Black Widow","Doctor Strange","Hulk","Hawkeye","Spider-Woman","Ant-man","Wasp","Quicksilver","Scarlet Witch", "Groot", "Rocket Raccoon"])
        if choice2 == 0: return
        if choice2 == 1: deckname = createCards(me.Deck,sorted(black_panther.keys()),black_panther)
        if choice2 == 2: deckname = createCards(me.Deck,sorted(captain_marvel.keys()),captain_marvel)
        if choice2 == 3: deckname = createCards(me.Deck,sorted(iron_man.keys()),iron_man)
        if choice2 == 4: deckname = createCards(me.Deck,sorted(she_hulk.keys()),she_hulk)
        if choice2 == 5: deckname = createCards(me.Deck,sorted(spider_man.keys()),spider_man)
        if choice2 == 6: deckname = createCards(me.Deck,sorted(captain_america.keys()),captain_america)
        if choice2 == 7: deckname = createCards(me.Deck,sorted(ms_marvel.keys()),ms_marvel)
        if choice2 == 8: deckname = createCards(me.Deck,sorted(thor.keys()),thor)
        if choice2 == 9: deckname = createCards(me.Deck,sorted(black_widow.keys()),black_widow)
        if choice2 == 10: deckname = createCards(me.Deck,sorted(doctor_strange.keys()),doctor_strange)
        if choice2 == 11: deckname = createCards(me.Deck,sorted(hulk.keys()),hulk)
        if choice2 == 12: deckname = createCards(me.Deck,sorted(hawkeye.keys()),hawkeye)
        if choice2 == 13: deckname = createCards(me.Deck,sorted(spider_woman.keys()),spider_woman)
        if choice2 == 14: deckname = createCards(me.Deck,sorted(ant_man.keys()),ant_man)
        if choice2 == 15: deckname = createCards(me.Deck,sorted(wsp.keys()),wsp)
        if choice2 == 16: deckname = createCards(me.Deck,sorted(qsv.keys()),qsv)
        if choice2 == 17: deckname = createCards(me.Deck,sorted(scw.keys()),scw)
        if choice2 == 18: deckname = createCards(me.Deck,sorted(groot.keys()),groot)
        if choice2 == 19: deckname = createCards(me.Deck,sorted(rocket_raccoon.keys()),rocket_raccoon)

    if choice == 2:
        url = askString("Please enter the URL of the deck you wish to load.", "")
        if url == None: return
        if not "view/" in url:
            whisper("Error: Invalid URL.")
            return
        deckname = createAPICards(url)
    tableSetup()

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
    firstPlayerToken[0].moveToTable(playerX(newFirstPlayer),playerY - 70)

def villainBoost(card, x = 0, y = 0):
    vName = getGlobalVariable("villainSetup")
    if str(playerID(me)) == getGlobalVariable("activePlayer"):
        if vName != 'The Wrecking Crew':
            if len(encounterDeck()) == 0:
                shuffleDiscardIntoDeck(encounterDiscardDeck())
            boostList = encounterDeck().top()
            boostList.moveToTable(0,0,True)
        else:
            encCards = filter(lambda card: card.Owner == getActiveVillain().Owner, encounterDeck())
            disEncCards = filter(lambda card: card.Owner == getActiveVillain().Owner, encounterDiscardDeck())
            if len(encCards) == 0:
                for c in disEncCards:
                    c.moveTo(encounterDeck())
                encounterDeck().shuffle()
                newEncCards = filter(lambda card: card.Owner == getActiveVillain().Owner, encounterDeck())
                boostList = newEncCards[0]
            else:
                boostList = encCards[0]
            boostList.moveToTable(0,0,True)


def readyAll(group = table, x = 0, y = 0):
    mute()
    for c in table:
        if c.controller == me and c.orientation != Rot0 and isEncounter([c]) != True and c.Type != "encounter" and c.Type != "villain" and c.Type != "main_scheme":
            c.orientation = Rot0
    notify("{} readies all their cards.".format(me))

def advanceGame(group = None, x = 0, y = 0):
    # Check if we should pass the turn or just change the phase
    if str(playerID(me)) == getGlobalVariable("activePlayer"):
        if currentPhase()[1] == 1:
            setPlayerDone()
            if not checkPlayersDone():
                passTurn()
            else:
                doEndHeroPhase()
                passSharedControl(getPlayerByID(num(getGlobalVariable("firstPlayer"))))
                setVirtualActivePlayer(getPlayerByID(num(getGlobalVariable("firstPlayer"))))
                setGlobalVariable("done", str(set()))
                setPhase(2)
        if currentPhase()[1] == 2:
            clearHighlights()
            setFirstPlayer()
            setVirtualActivePlayer(getPlayerByID(num(getGlobalVariable("firstPlayer"))))
            passSharedControl(getPlayerByID(num(getVirtualActivePlayer())))
            setPhase(1)
        if currentPhase()[1] == 0:
            setPhase(1)
    else:
        notify("Only the active player, highlighted in green, may advance the game.")
    update()

def passTurn():
    setVirtualActivePlayer(getPlayerByID(num(me.getGlobalVariable("playerID"))+1))
    passSharedControl(getPlayerByID(num(getVirtualActivePlayer())))

def setVirtualActivePlayer(p):
   if p is None:
       setGlobalVariable("activePlayer", "-1")
   else:
       setGlobalVariable("activePlayer", str(playerID(p)))
       highlightPlayer(p,ActiveColour)
   update()

def getVirtualActivePlayer():
    return getGlobalVariable("activePlayer")

def setActiveVillain(card, x = 0, y = 0):
    if str(playerID(me)) == getGlobalVariable("activePlayer"):
        if isVillain([card]):
            vCards = filter(lambda card: card.Type == "villain", table)
            for c in vCards:
                c.highlight = None
            card.highlight = ActiveColour

def setPlayerDone():
    done = getGlobalVariable("done")
    if done:
        playersDone = eval(done)
    else:
        playersDone = set()
    playersDone.add(me._id)
    setGlobalVariable("done", str(playersDone))
    highlightPlayer(me, DoneColour)
    update()

def doEndHeroPhase():
    mute()
    for p in players:
        remoteCall(p,"clearTargets",[])
        remoteCall(p,"readyAll",[])
        remoteCall(p,"drawMany",[p.piles['Deck'],p.MaxHandSize - len(p.piles['Hand'])])
        # clearTargets()
        # readyAll()
        # drawMany(me.deck, me.MaxHandSize - len(me.hand))

        # Check for hand size!
        if len(p.piles['Hand']) > num(p.counters["MaxHandSize"].value):
            discardCount = len(p.piles['Hand']) - num(p.counters["MaxHandSize"].value)
            dlg = cardDlg(p.piles['Hand'])
            dlg.title = "You have more than the allowed cards in hand."
            dlg.text = "Select " + str(discardCount) + " Card(s):"
            dlg.min = 0
            dlg.max = discardCount
            cardsSelected = dlg.show()
            if cardsSelected is not None:
                for card in cardsSelected:
                    remoteCall(p,"discard",[card])
                    #discard(card)
        remoteCall(p,"clearHighlights",[])
        #clearHighlights()

def passSharedControl(p):
    encounterDeck().controller = p
    schemeDeck().controller = p
    villainDeck().controller = p
    cards = filter(lambda card: isEncounter([card]) or card.type == 'main_scheme' or card.type == 'villain' or card.type == 'first_player', table)
    for c in cards:
        c.controller = p
    update()

def getActiveVillain(group = table, x = 0, y = 0):
    vCards = filter(lambda card: card.Type == "villain", table)
    for c in vCards:
        if str(c.highlight).upper() == ActiveColour:
            return c

def getPosition(card,x=0,y=0):
    t = getPlayers()
    notify("This cards position is {}".format(card.position))

def createCards(group,list,dict):
    for i in list:
        group.create(card_mapping[i],dict[i])

def createAPICards(url):
    if "decklist/" in str(url):
        deckid = url.split("view/")[1].split("/")[0]
        data, code = webRead("https://marvelcdb.com/api/public/decklist/{}".format(deckid))
    elif "deck/" in str(url):
        deckid = url.split("view/")[1].split("/")[0]
        data, code = webRead("https://marvelcdb.com/api/public/deck/{}".format(deckid))
    if code != 200:
        whisper("Error retrieving online deck data, please try again.")
        return
    try:
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
    except ValueError:
        whisper("Error retrieving online deck data, please try again. If you are trying to load a non published deck make sure you have edited your account to select 'Share Your Decks'")

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

def addDamage(card, x = 0, y = 0):
    mute()
    card.markers[DamageMarker] += 1
    notify("{} adds 1 Damage on {}.".format(me, card))

def addMarker(card, x = 0, y = 0, qty = 1):
    mute()
    if isScheme([card]):
        card.markers[ThreatMarker] += qty
        notify("{} adds 1 Threat on {}.".format(me, card))
    elif isAttackable([card]):
        card.markers[DamageMarker] += qty
        notify("{} adds 1 Damage on {}.".format(me, card))
    else:
        card.markers[AllPurposeMarker] += qty
        notify("{} adds 1 Marker on {}.".format(me, card))

def removeMarker(card, x = 0, y = 0, qty = 1):
    mute()
    if isScheme([card]):
        card.markers[ThreatMarker] -= qty
        notify("{} removes 1 Threat on {}.".format(me, card))
    elif isAttackable([card]):
        card.markers[DamageMarker] -= qty
        notify("{} removes 1 Damage on {}.".format(me, card))
    else:
        card.markers[AllPurposeMarker] -= qty
        notify("{} removes 1 Marker on {}.".format(me, card))

def clearMarker(card, x = 0, y = 0):
    mute()
    if isScheme([card]):
        card.markers[ThreatMarker] = 0
        notify("{} removes all Threat on {}.".format(me, card))
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
        notify("{} adds 1 Threat on {}.".format(me, card))
    elif isAttackable([card]):
        card.markers[DamageMarker] += qty
        notify("{} adds 1 Damage on {}.".format(me, card))
    else:
        card.markers[AllPurposeMarker] += qty
        notify("{} adds 1 Marker on {}.".format(me, card))

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
    if "b" in card.alternates:
        if card.Type == "hero" or card.Type == "alter_ego":
            changeForm(card)
        else:
            if card.alternate == "":
                card.alternate = "b"
            else:
                card.alternate = ""
    else:
        if card.isFaceUp:
            card.isFaceUp = False
            notify("{} hides {}.".format(me, card))
        else:
            card.isFaceUp = True
            notify("{} reveals {}.".format(me, card))

def discard(card, x = 0, y = 0):
    mute()
    if isEncounter([card]):
        card.moveTo(encounterDiscardDeck())
    elif card.Type == "hero" or card.Type == "alter_ego" or card.Type == "main_scheme" or card.Type == "villain":
        return
    elif card.Owner == 'invocation':
        notify("{} discards {} from {}.".format(me, card, card.group.name))
        card.moveTo(card.owner.piles["Special Deck Discard Pile"])
    else:
        notify("{} discards {} from {}.".format(me, card, card.group.name))
        card.moveTo(card.owner.piles["Discard Pile"])
    clearMarker(card)

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
    if count is None or count <= 0:
        whisper("drawMany: invalid card count")
        return
    for c in group.top(count):
        if group.name == 'Special Deck':
            c.moveToTable(0,0,False)
        else:
            c.moveTo(me.hand)   

def bottomPlayerDeck(card, x = 0, y = 0):
    mute()
    card.moveToBottom(me.Deck)

def bottomEncounterDeck(card, x = 0, y = 0):
    mute()
    card.moveToBottom(encounterDeck())

def drawCard(group):
    mute()
    if len(me.piles[group.name]) == 0:
        if group.name == "Special Deck":
            for c in me.piles["Special Deck Discard Pile"]: c.moveTo(c.owner.piles["Special Deck"])
            me.piles["Special Deck"].shuffle()
            rnd(1,1) 
        else:
            for c in me.piles["Discard Pile"]:
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

def addObligationsToEncounter(group = table, x = 0, y = 0):
    oblCards = []
    for p in players:
        playerOblCard = filter(lambda card: card.Type == 'obligation', p.piles["Nemesis Deck"])
        oblCards.extend(playerOblCard)
    for c in oblCards:
        c.controller = getPlayerByID(num(getGlobalVariable("activePlayer")))
        c.moveTo(encounterDeck())

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
    elif args.marker == "Damage" and (args.card.Type == "hero" or args.card.Type == "alter_ego"):
        args.card.owner.counters["HP"].value = args.card.owner.counters["HP"].value - (args.card.markers[DamageMarker] - args.value)

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
        if card.controller == p and (card.Type == "hero" or card.Type == "alter_ego"):
            heros += 1
    return heros

def mainSchemeDeck():
    return shared.piles['scheme']

def villainDeck():
    return shared.piles['villain']

def encounterDeck():
    return shared.piles['encounter']

def encounterDiscardDeck():
    return shared.piles['Encounter Discard']

def removedFromGameDeck():
    return shared.piles['removed']

def schemeDeck():
    return shared.piles['scheme']

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

#Store this player's starting position (players ID for this game)
#The first player is 0, the second 1 ....
#These routines set global variables so should be called within getLock() and clearLock()
#After a reset, the game count will be updated by the first player to setup again which invalidates all current IDs
def myID():
    if len(me.getGlobalVariable("playerID")) > 0:
        return playerID(me) # Player already have a valid ID for this game
    g = getGlobalVariable("playersSetup")
    if len(g) == 0:
        id = 0
    else:
        id = num(g)
    me.setGlobalVariable("playerID", str(id))
    setGlobalVariable("playersSetup", str(id+1))
    update()
    return id

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
    if numDone() == len(getPlayers()):
        return True
    else:
        return False

def nextSchemeStage(group=None, x=0, y=0):
    mute()
    schemeCards = []
    #We need a new Scheme card
    if group is None or group == table:
        group = mainSchemeDeck()
    if len(group) == 0: return

    if group.controller != me:
        remoteCall(group.controller, "nextSchemeStage", [group, x, y])
        return

    for c in table:
        if c.Type == 'main_scheme':
            currentScheme = num(c.CardNumber[:-1])
            c.moveToBottom(removedFromGameDeck())
        x = tableLocations['mainScheme'][0]
        y = tableLocations['mainScheme'][1]

    for card in mainSchemeDeck():
        if num(card.CardNumber[:-1]) == currentScheme + 1:
            card.moveToTable(x, y)
            card.anchor = True
            notify("{} advances scheme to '{}'".format(me, card))

def nextVillainStage(group=None, x=0, y=0):
    mute()

    #We need a new Villain card
    if group is None or group == table:
        group = villainDeck()
    if len(group) == 0: return

    if str(playerID(me)) == getGlobalVariable("activePlayer"):
        if group.controller != me:
            remoteCall(group.controller, "nextVillainStage", [group, x, y])
            return

        if getGlobalVariable("villainSetup") != 'The Wrecking Crew':
            for c in table:
                if c.Type == 'villain':
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
                x = villainX(1,0)
                y = tableLocations['villain'][1]

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
                    card.anchor = True
                    notify("{} advances Villain to the next stage".format(me))
        else:
            vCards = filter(lambda card: card.Owner == getActiveVillain().Owner and (card.Type == 'villain' or card.Type == 'side_scheme'), table)
            for c in vCards:
                c.moveToBottom(removedFromGameDeck())


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

def highlightPlayer(p, state):
    if len(getPlayers()) <= 1:
        return
    #debug("highlightPlayer {} = {}".format(p, state))
    notify("highlightPlayer {} = {}".format(p, state))
    for card in table:
        if (card.Type == "hero" and card.controller == p) or (card.Type == "alter_ego" and card.controller == p):
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
        if isHero([c]):
            c.highlight = None

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
        if c.Type != 'hero' and c.Type != 'alter_ego':
            return False
    return True

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
