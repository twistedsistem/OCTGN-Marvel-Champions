#------------------------------------------------------------
# 'Load Villain' event
#------------------------------------------------------------

def loadVillain(group, x = 0, y = 0):
    mute()
    villainName = ''
    nbModular = 1

    if not deckNotLoaded(group,0,0,shared.villain):
        confirm("Cannot generate a deck: You already have cards loaded. Reset the game in order to generate a new deck.")
        return

    for i in sorted(villain_setup.keys()):
        setupPile().create(i, 1)
    dlg = cardDlg(setupPile())
    dlg.title = "Which villain would you like to defeat ?"
    dlg.text = "Select your Opponent :"
    cardsSelected = dlg.show()
    if cardsSelected is None:
        deleteCards(setupPile())
        return
    else:
        for card in cardsSelected:
            createCards(shared.villain,sorted(eval(card.Owner).keys()), eval(card.Owner))
            deleteCards(setupPile())

            passSharedControl(group)
            update()
            if card.Owner == "the_wrecking_crew":
                nbModular = 0

            if card.Owner == "baron_zemo_firestarter":
                createCards(shared.villain,sorted(baron_zemo_firestarter_modules.keys()),baron_zemo_firestarter_modules)
                createCards(shared.villain,sorted(legions_of_hydra.keys()),legions_of_hydra)
                createCards(shared.villain,sorted(bomb_scare.keys()),bomb_scare)

            if card.Owner == "crossbones":
                createCards(shared.special,sorted(exper_weapon.keys()),exper_weapon)
                specialDeck().collapsed = False
                specialDeck().shuffle()
                createCards(shared.campaign,sorted(trors_campaign.keys()),trors_campaign)
                nbModular = 3

            if card.Owner == "absorbing_man":
                createCards(shared.campaign,sorted(trors_campaign.keys()),trors_campaign)

            if card.Owner == "taskmaster":
                createCards(shared.villain,sorted(hydra_patrol.keys()),hydra_patrol)
                createCards(shared.campaign,sorted(trors_campaign.keys()),trors_campaign)
                for c in filter(lambda card: card.Type == "ally", villainDeck()):
                    c.moveTo(specialDeck())
                specialDeck().shuffle()
                specialDeck().collapsed = False

            if card.Owner == "zola":
                createCards(shared.campaign,sorted(trors_campaign.keys()),trors_campaign)

            if card.Owner == "red_skull":
                createCards(shared.campaign,sorted(trors_campaign.keys()),trors_campaign)
                for c in filter(lambda card: card.Type == "side_scheme", villainDeck()):
                    c.moveTo(specialDeck())
                specialDeck().collapsed = False
                specialDeckDiscard().collapsed = False
                for c in filter(lambda card: card.CardNumber == "04130", villainDeck()):
                    c.moveTo(removedFromGameDeck())
                removedFromGameDeck().collapsed = False
                nbModular = 2

            if card.Owner == "the_once_and_future_kang":
                for c in filter(lambda card: card.CardNumber == "11023", villainDeck()):
                    c.moveTo(removedFromGameDeck())
                removedFromGameDeck().collapsed = False

            if card.Owner == "brotherhood_of_badoon":
                createCards(shared.villain,sorted(ship_command.keys()),ship_command)
                createCards(shared.campaign,sorted(gmw_campaign_market.keys()),gmw_campaign_market)
                createCards(shared.campaign,sorted(gmw_campaign_challenge.keys()),gmw_campaign_challenge)
                createCards(shared.campaign,sorted(badoon_headhunter.keys()),badoon_headhunter)

            if card.Owner == "collector1":
                createCards(shared.villain,sorted(galactic_artifacts.keys()),galactic_artifacts)
                createCards(shared.campaign,sorted(gmw_campaign_market.keys()),gmw_campaign_market)
                createCards(shared.campaign,sorted(gmw_campaign_challenge.keys()),gmw_campaign_challenge)
                createCards(shared.campaign,sorted(badoon_headhunter.keys()),badoon_headhunter)

            if card.Owner == "collector2":
                createCards(shared.villain,sorted(galactic_artifacts.keys()),galactic_artifacts)
                createCards(shared.special,sorted(ship_command.keys()),ship_command)
                specialDeck().collapsed = False
                createCards(shared.campaign,sorted(gmw_campaign_market.keys()),gmw_campaign_market)
                createCards(shared.campaign,sorted(gmw_campaign_challenge.keys()),gmw_campaign_challenge)
                createCards(shared.campaign,sorted(badoon_headhunter.keys()),badoon_headhunter)

            if card.Owner == "nebula":
                createCards(shared.villain,sorted(power_stone.keys()),power_stone)
                createCards(shared.villain,sorted(ship_command.keys()),ship_command)
                createCards(shared.campaign,sorted(gmw_campaign_market.keys()),gmw_campaign_market)
                createCards(shared.campaign,sorted(gmw_campaign_challenge.keys()),gmw_campaign_challenge)
                createCards(shared.campaign,sorted(badoon_headhunter.keys()),badoon_headhunter)

            if card.Owner == "ronan":
                createCards(shared.villain,sorted(power_stone.keys()),power_stone)
                createCards(shared.villain,sorted(ship_command.keys()),ship_command)
                createCards(shared.campaign,sorted(gmw_campaign_market.keys()),gmw_campaign_market)
                createCards(shared.campaign,sorted(gmw_campaign_challenge.keys()),gmw_campaign_challenge)
                createCards(shared.campaign,sorted(badoon_headhunter.keys()),badoon_headhunter)

            if card.Owner == "ebony_maw":
                createCards(shared.campaign,sorted(mts_campaign.keys()),mts_campaign)
                nbModular = 2

            if card.Owner == "tower_defense":
                createCards(shared.campaign,sorted(mts_campaign.keys()),mts_campaign)

            if card.Owner == "thanos":
                createCards(specialDeck(), sorted(infinity_gauntlet.keys()),infinity_gauntlet)
                specialDeck().shuffle()
                specialDeck().collapsed = False
                specialDeckDiscard().collapsed = False
                createCards(shared.campaign,sorted(mts_campaign.keys()),mts_campaign)
                nbModular = 2

            if card.Owner == "hela":
                createCards(removedFromGameDeck(), sorted(hela_setup.keys()), hela_setup)
                createCards(shared.campaign,sorted(mts_campaign.keys()),mts_campaign)
                nbModular = 2

            if card.Owner == "loki":
                villainDeck().collapsed = False
                createCards(specialDeck(), sorted(infinity_gauntlet.keys()),infinity_gauntlet)
                specialDeck().shuffle()
                specialDeck().collapsed = False
                specialDeckDiscard().collapsed = False
                createCards(shared.campaign,sorted(mts_campaign.keys()),mts_campaign)
                nbModular = 2

            if card.Owner == "hood":
                specialDeck().collapsed = False
                nbModular = 7

            if card.Owner == "sandman":
                createCards(shared.villain,sorted(city_in_chaos.keys()),city_in_chaos)
                createCards(shared.campaign,sorted(sm_campaign.keys()),sm_campaign)
                createCards(shared.campaign,sorted(osborn_tech.keys()),osborn_tech)
                nbModular = 1

            if card.Owner == "venom":
                createCards(shared.villain,sorted(symbiotic_strength.keys()),symbiotic_strength)
                createCards(shared.campaign,sorted(sm_campaign.keys()),sm_campaign)
                createCards(shared.campaign,sorted(osborn_tech.keys()),osborn_tech)
                nbModular = 1

            if card.Owner == "mysterio":
                createCards(shared.villain,sorted(personal_nightmare.keys()),personal_nightmare)
                createCards(shared.campaign,sorted(sm_campaign.keys()),sm_campaign)
                createCards(shared.campaign,sorted(osborn_tech.keys()),osborn_tech)
                nbModular = 1

            if card.Owner == "sinister_six":
                createCards(shared.villain,sorted(guerrilla_tactics.keys()),guerrilla_tactics)
                createCards(shared.campaign,sorted(sm_campaign.keys()),sm_campaign)
                createCards(shared.campaign,sorted(osborn_tech.keys()),osborn_tech)
                nbModular = 1

            if card.Owner == "venom_goblin":
                createCards(shared.villain,sorted(symbiotic_strength.keys()),symbiotic_strength)
                createCards(shared.campaign,sorted(sm_campaign.keys()),sm_campaign)
                createCards(shared.campaign,sorted(osborn_tech.keys()),osborn_tech)
                nbModular = 1

            villainName = card.Name
            setGlobalVariable("villainSetup",str(villainName))

    update()
    loadDifficulty()
    loadEncounter(shared.encounter, nbEncounter = nbModular)
    notify('{} loaded {}, Good Luck!'.format(me, villainName))
    tableSetup(doPlayer=False,doEncounter=True)


def loadDifficulty():
    vName = getGlobalVariable("villainSetup")
    choice = askChoice("What difficulty would you like to play at?", ["Standard", "Expert", "Standard II", "Expert II"])

    if vName == 'The Wrecking Crew':
        if choice == 0: return
        if choice == 1: return
        if choice == 2:
            setGlobalVariable("difficulty", "1")
            return
        if choice == 3: return
        if choice == 4:
            setGlobalVariable("difficulty", "1")
            return

    else:
        if choice == 0: return
        if choice == 1:
            createCards(shared.encounter,sorted(standard.keys()),standard)
        if choice == 2:
            createCards(shared.encounter,sorted(standard.keys()),standard)
            createCards(shared.encounter,sorted(expert.keys()),expert)
            setGlobalVariable("difficulty", "1")
        if choice == 3:
            createCards(shared.encounter,sorted(standard_ii.keys()),standard_ii)
            EnvCard = sorted(filter(lambda card: card.CardNumber == "24049a", shared.encounter)) # Formidable Foe environment
            EnvCard[0].moveToTable(tableLocations['environment'][0] - 90, tableLocations['environment'][1]) # Do not override other environment cards from scenario (if any)
        if choice == 4:
            createCards(shared.encounter,sorted(standard_ii.keys()),standard_ii)
            EnvCard = sorted(filter(lambda card: card.CardNumber == "24049a", shared.encounter)) # Formidable Foe environment
            EnvCard[0].moveToTable(tableLocations['environment'][0] - 90, tableLocations['environment'][1])
            EnvCardOnTable = sorted(filter(lambda card: card.CardNumber == "24049a", table)) # Formidable Foe environment
            EnvCardOnTable[0].alternate = 'b'
            createCards(shared.encounter,sorted(expert_ii.keys()),expert_ii)
            setGlobalVariable("difficulty", "1")


def villainSetup(group=table, x = 0, y = 0):
    # Global Variables
    gameDifficulty = getGlobalVariable("difficulty")
    vName = getGlobalVariable("villainSetup")

    # Move cards from Villain Deck to Encounter and Scheme Decks
    encounterDeckCards = filter(lambda card: card.Type != "villain" and card.Type != "main_scheme", villainDeck())
    mainSchemeCards = filter(lambda card: card.Type == "main_scheme", villainDeck())
    villainCards = filter(lambda card: card.Type == "villain", villainDeck())

    for c in encounterDeckCards:
        c.moveTo(encounterDeck())
    for c in mainSchemeCards:
        c.moveTo(mainSchemeDeck())

    villainCards = sorted(villainCards)
    villainEnvCards = sorted(filter(lambda card: card.Type == "environment", encounterDeck()))
    villainAttCards = sorted(filter(lambda card: card.Type == "attachment", encounterDeck()))

    if vName == 'The Wrecking Crew':
        # If we loaded the encounter deck - add the first main scheme card to the table
        sorted(mainSchemeCards)[0].moveToTable(tableLocations['mainSchemeCentered'][0],tableLocations['mainSchemeCentered'][1])
        sorted(mainSchemeCards)[0].anchor = False
        sorted(mainSchemeCards).pop(0)
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
            c.moveToTable(villainX(4,idx)-10,tableLocations['villain'][1]+100)

    elif vName == 'Kang':
        sorted(mainSchemeCards)[0].moveToTable(tableLocations['mainScheme'][0],tableLocations['mainScheme'][1])
        sorted(mainSchemeCards)[0].anchor = False
        sorted(mainSchemeCards).pop(0)
        loop = 6
        if gameDifficulty == "1":
            while loop > 0:
                villainCards[0].delete()
                villainCards.pop(0)
                loop -= 1
        else:
            while loop > 0:
                villainCards[6].delete()
                villainCards.pop(6)
                loop -= 1
        villainCards = villainCards[0:6]
        villainCards[0].moveToTable(villainX(1,0),tableLocations['villain'][1])
        villainCards[0].anchor = False

    elif vName == 'Tower Defense':
        if gameDifficulty == "1":
            villainCards[3].delete()
            villainCards.pop(3)
            villainCards[0].delete()
            villainCards.pop(0)
        else:
            villainCards[5].delete()
            villainCards.pop(5)
            villainCards[2].delete()
            villainCards.pop(2)
        vCardsProxima = villainCards[0:2]
        vCardsCorvus = villainCards[2:]
        vCardsProxima[0].moveToTable(villainX(2,0),tableLocations['villain'][1])
        vCardsCorvus[0].moveToTable(villainX(2,1),tableLocations['villain'][1])
        villainEnvCards[0].moveToTable(villainX(1,0),tableLocations['villain'][1])
        villainAttCards[0].moveToTable(villainX(2,1)-90,tableLocations['villain'][1]+75)

        for idx, c in enumerate(sorted(mainSchemeCards)):
            c.moveToTable(villainX(2,idx)-10,tableLocations['villain'][1]+100)

    elif vName == 'Loki':
        # If we loaded the encounter deck - add the first main scheme card to the table
        sorted(mainSchemeCards)[0].moveToTable(tableLocations['mainScheme'][0],tableLocations['mainScheme'][1])
        sorted(mainSchemeCards)[0].anchor = False
        sorted(mainSchemeCards).pop(0)
        randomLoki = rnd(0, 4) # Returns a random INTEGER value and use it to choose which Loki will be loaded
        villainCards[randomLoki].moveToTable(villainX(1,0),tableLocations['villain'][1])
        villainCards[randomLoki].anchor = False

    elif vName == 'Sinister Six':
        for idx, c in enumerate(villainCards):
            c.moveToTable(villainX(6,idx),tableLocations['villain'][1])
        loop = 6 - (1 + len(players))
        while loop > 0:
            vCardsOnTable = filter(lambda card: card.Type == "villain" and card.alternate == "", table)
            randomVillain = rnd(0, len(vCardsOnTable) - 1)
            vCardsOnTable[randomVillain].alternate = "b"
            clearMarker(vCardsOnTable[randomVillain], x = 0, y = 0)
            loop -= 1
        

        # If we loaded the encounter deck - add the first main scheme card to the table
        sorted(mainSchemeCards)[0].moveToTable(tableLocations['mainSchemeCentered'][0]-100,tableLocations['villain'][1]+100)
        sorted(mainSchemeCards)[0].anchor = False
        sorted(mainSchemeCards).pop(0)

    else:
        # If we loaded the encounter deck - add the first main scheme card to the table
        sorted(mainSchemeCards)[0].moveToTable(tableLocations['mainScheme'][0],tableLocations['mainScheme'][1])
        sorted(mainSchemeCards)[0].anchor = False
        sorted(mainSchemeCards).pop(0)
        # If we loaded the encounter deck - add the villain(s) card(s) to the table
        if gameDifficulty == "1":
            villainCards[0].delete()
            villainCards.pop(0)
        else:
            villainCards[len(villainCards) - 1].delete()
            villainCards.pop(len(villainCards) - 1)
        villainCards[0].moveToTable(villainX(1,0),tableLocations['villain'][1])
        villainCards[0].anchor = False


    shared.counters["HP"].value = int(villainCards[0].properties["HP"]) * len(players)
    shared.encounter.shuffle()

    SpecificVillainSetup(vName)



#------------------------------------------------------------
# 'Load Villain' specific functions
#------------------------------------------------------------
#------------------------------------------------------------
# Specific Villain setup
#------------------------------------------------------------
def revealCardOnSetup(ssName, ssCardNumber, posX, posY, isAttachment=False):
    card = filter(lambda c: c.CardNumber == ssCardNumber, encounterAndDiscardDeck())
    if len(card) > 0:
        card[0].moveToTable(posX, posY)
        if isAttachment:
            card[0].sendToBack()
        return card[0]
    else:
        notify("{} card not found in encounter deck nor encounter discard!".format(ssName))

def SpecificVillainSetup(vName = ''):

    vCardOnTable = sorted(filter(lambda card: card.Type == "villain", table), reverse=True)
    msCardOnTable = sorted(filter(lambda card: card.Type == "main_scheme", table))
    villainEnvCards = sorted(filter(lambda card: card.Type == "environment", encounterDeck()))
    villainAttCards = sorted(filter(lambda card: card.Type == "attachment", encounterDeck()))
    vilX, vilY = vCardOnTable[0].position
    msX, msY = msCardOnTable[0].position
    ssX = msX + 100
    ssY = msY

    if vName == 'Rhino':
        if vCardOnTable[0].CardNumber == "01095": # Rhino II
            revealCardOnSetup("Breakin' & Takin'", "01107", ssX, ssY)


    if vName == 'Klaw':
        if msCardOnTable[0].CardNumber == "01116a": # Stage 1 main scheme
            revealCardOnSetup("Defense Network", "01125", ssX, ssY)

        if vCardOnTable[0].CardNumber == "01114": # Klaw II
            ssCard1_OnTable = filter(lambda card: card.CardNumber == "01125", table)
            # Check if Defense Network already on table to adapt card's position for 2nd side scheme
            if len(ssCard1_OnTable) > 0:
                ssX = ssCard1_OnTable[0].position[0] + 100
                ssY = ssCard1_OnTable[0].position[1]
            revealCardOnSetup("'Immortal' Klaw", "01127", ssX, ssY)


    if vName == 'Ultron':
        if msCardOnTable[0].CardNumber == "01137a": # Stage 1 main scheme
            revealCardOnSetup("Ultron Drones", "01140", tableLocations['environment'][0], tableLocations['environment'][1])
        if vCardOnTable[0].CardNumber == "01136": # Ultron III
            revealCardOnSetup("Ultron's Imperative'", "01150", ssX, ssY)


    if vName == 'Green Goblin: Risky Business':
        if msCardOnTable[0].CardNumber == "02004a": # Stage 1 main scheme
            revealCardOnSetup("Criminal Enterprise", "02006", tableLocations['environment'][0], tableLocations['environment'][1])

			
    if vName == 'Green Goblin: Mutagen Formula':
        if msCardOnTable[0].CardNumber == "02017a": # Stage 1 main scheme
            minionCard = filter(lambda card: card.CardNumber == "02024", encounterDeck()) # Goblin Thrall minion
            for i in range(0, len(getPlayers())):
                minionCard[i].moveToTable(playerX(i), 0)

				
    if vName == 'Baron Zemo: Firestarter':
        EnvCard = sorted(filter(lambda card: card.CardNumber == "91006", encounterDeck())) # environment card
        if msCardOnTable[0].CardNumber == "91004a" and len(EnvCard) > 0: # Stage 1 main scheme
            EnvCard[0].moveToTable(tableLocations['environment'][0], tableLocations['environment'][1])
            ssCard = filter(lambda card: card.CardNumber == "01109", encounterDeck()) # Bomb Scare side scheme
            ssCard[0].moveToTable(ssX, ssY)
            minionCard = filter(lambda card: card.CardNumber == "01182", encounterDeck()) # Hydra Soldier minion
            minionCard[0].moveToTable(tableLocations['environment'][0] - 90, tableLocations['environment'][1])


    if vName == 'Absorbing Man':
        if vCardOnTable[0].CardNumber == "04077": # Absorbing Man II
            revealCardOnSetup("Super Absorbing Power", "04092", ssX, ssY)


    if vName == 'Crossbones':
        if vCardOnTable[0].CardNumber == "04059": # Crossbones II
            revealCardOnSetup("Crossbones' Machine Gun", "04064", vilX-35, vilY+5, isAttachment=True)

			
    if vName == 'Taskmaster':
        if msCardOnTable[0].CardNumber == "04096a": # Stage 1 main scheme
            revealCardOnSetup("Hydra Patrol", "04154", ssX, ssY)

			
    if vName == 'Zola':
        if msCardOnTable[0].CardNumber == "04112a": # Stage 1 main scheme
            revealCardOnSetup("Hydra Prison", "04122", ssX, ssY)

            # Ultimate Bio-Servant minion engaged with each player
            minionCard = filter(lambda card: card.CardNumber == "04114", encounterDeck())
            for i in range(0, len(getPlayers())):
                minionCard[i].moveToTable(playerX(i), 0)

        if vCardOnTable[0].CardNumber == "04110": # Zola II
            ssCard1_OnTable = filter(lambda card: card.CardNumber == "04122", table)
            # Check if Hydra Prison already on table to adapt card's position for 2nd side scheme
            if len(ssCard1_OnTable) > 0:
                ssX = ssCard1_OnTable[0].position[0] + 100
                ssY = ssCard1_OnTable[0].position[1]
            revealCardOnSetup("Test Subjects", "04123", ssX, ssY)

			
    if vName == 'Red Skull':
        ssCard = filter(lambda card: card.CardNumber == "04139", specialDeck()) # The Red House side scheme
        if msCardOnTable[0].CardNumber == "04128a" and len(ssCard) > 0: # Stage 1 main scheme
            ssCard[0].moveToTable(ssX, ssY)
        # Put all side schemes into Special deck
        for c in filter(lambda card: card.Type == "side_scheme", encounterDeck()):
            c.moveTo(specialDeck())
        specialDeck().shuffle()


    if vName == 'Drang':
        if msCardOnTable[0].CardNumber == "16061a": # Stage 1 main scheme
            revealCardOnSetup("Badoon Ship", "16063", tableLocations['environment'][0], tableLocations['environment'][1])
            revealCardOnSetup("Milano", "16142", playerX(0), 0) # Give Milano to 1st player

        if vCardOnTable[0].CardNumber == "16059": # Drang II
            revealCardOnSetup("Drang's Spear", "16064", vilX-20, vilY+5, isAttachment=True)


    if vName == 'Collector 2':
        if msCardOnTable[0].CardNumber == "16082a": # Stage 1 main scheme
            revealCardOnSetup("Library Labyrinth", "16085a", tableLocations['environment'][0], tableLocations['environment'][1])


    if vName == 'Nebula':
        if msCardOnTable[0].CardNumber == "16091a": # Stage 1 main scheme
            revealCardOnSetup("Nebula's Ship", "16093", tableLocations['environment'][0], tableLocations['environment'][1])
            revealCardOnSetup("Milano", "16142", playerX(0), 0) # Give Milano to 1st player
            revealCardOnSetup("Power Stone", "16149", vilX-20, vilY+10, isAttachment=True)


    if vName == 'Ronan':
        if msCardOnTable[0].CardNumber == "16106a": # Stage 1 main scheme
            revealCardOnSetup("Kree Command Ship", "16108", tableLocations['environment'][0] - 20, tableLocations['environment'][1])
            revealCardOnSetup("Milano", "16142", playerX(0), 0) # Give Milano to 1st player
            revealCardOnSetup("Universal Weapon", "16109", vilX-25, vilY+5, isAttachment=True)
            revealCardOnSetup("Power Stone", "16149", playerX(0) - 20, tableLocations['hero'][1]+5, isAttachment=True) # Attach Power Stone to 1st player

        if vCardOnTable[0].CardNumber == "16104": # Ronan II
            revealCardOnSetup("Cut the Power", "16111", ssX, ssY)

        if vCardOnTable[0].CardNumber == "16105": # Ronan III
            ssCard1_OnTable = filter(lambda card: card.CardNumber == "16111", table)
            # Check if 'Cut the Power' already on table to adapt card's position for 2nd side scheme
            if len(ssCard1_OnTable) > 0:
                ssX = ssCard1_OnTable[0].position[0] + 100
                ssY = ssCard1_OnTable[0].position[1]
            revealCardOnSetup("Superior Tactics", "16113", ssX, ssY)


    if vName == 'Tower Defense':
        if msCardOnTable[0].CardNumber == "21098a" or msCardOnTable[1].CardNumber == "21099a": # Stage 1 main scheme
            minionCard = filter(lambda card: card.CardNumber == "21102", encounterDeck()) # Black Order Besieger
            for i in range(0, len(getPlayers())):
                minionCard[i].moveToTable(playerX(i), 0)


    if vName == 'Thanos':
        if msCardOnTable[0].CardNumber == "21114a": # Stage 1 main scheme
            infinityCard = sorted(filter(lambda card: card.CardNumber == "21129", specialDeck())) # Infinity Gauntlet attachment
            infinityCard[0].moveToTable(tableLocations['environment'][0]-20, tableLocations['environment'][1])
            revealCardOnSetup("Sanctuary", "21116", ssX, ssY)

        if vCardOnTable[0].CardNumber == "21112": # Thanos II
            revealCardOnSetup("Thanos's Helmet", "21118", vilX-15, vilY+5, isAttachment=True)

        if vCardOnTable[0].CardNumber == "21113": # Thanos III
            revealCardOnSetup("Thanos's Armor", "21117", vilX-30, vilY+10, isAttachment=True)


    if vName == 'Hela':
        if msCardOnTable[0].CardNumber == "21138a": # Stage 1 main scheme
            odinCard = filter(lambda card: card.CardNumber == "21139a", removedFromGameDeck()) # Odin ally captive side
            odinCard[0].moveToTable(msX - 15, msY - 15)
            odinCard[0].sendToBack()
            ssCard = filter(lambda card: card.CardNumber == "21140", removedFromGameDeck()) # Gnipahellir side scheme
            ssCard[0].moveToTable(ssX, ssY)
            garmCard = filter(lambda card: card.CardNumber == "21143", removedFromGameDeck()) # Garm (minion)
            garmCard[0].moveToTable(playerX(0), 0) # Engage with 1st player


    if vName == 'Loki':
        if msCardOnTable[0].CardNumber == "21165a": # Stage 1 main scheme
            infinityCard = sorted(filter(lambda card: card.CardNumber == "21129", specialDeck())) # Infinity Gauntlet attachment
            infinityCard[0].moveToTable(tableLocations['environment'][0]-20, tableLocations['environment'][1])
            revealCardOnSetup("War in Asgard", "21167", ssX, ssY)


    if vName == 'Sandman':
        if msCardOnTable[0].CardNumber == "27064a": # Stage 1 main scheme
            c = revealCardOnSetup("City Streets", "27065", tableLocations['environment'][0], tableLocations['environment'][1])
            addMarker(c, 0, 0, 4)


    if vName == 'Venom':
        if msCardOnTable[0].CardNumber == "27076a": # Stage 1 main scheme
            revealCardOnSetup("Bell Tower", "27077a", tableLocations['environment'][0], tableLocations['environment'][1])

        if vCardOnTable[0].CardNumber == "27074": # Venom II
            revealCardOnSetup("Tooth and Nail", "27081", ssX, ssY)


    if vName == 'Mysterio':
        if msCardOnTable[0].CardNumber == "27087a": # Stage 1 main scheme
            minionCard = filter(lambda card: card.CardNumber == "27091", encounterDeck()) # Shifting Apparition minion
            for i in range(0, len(getPlayers())):
                minionCard[i].moveToTable(playerX(i), 0)


    if vName == 'Sinister Six':
        if msCardOnTable[0].CardNumber == "27100a": # Stage 1 main scheme
            revealCardOnSetup("Light at the End", "27102", tableLocations['mainSchemeCentered'][0]+100, tableLocations['villain'][1]+100)


    if vName == 'Venom Goblin':
        if msCardOnTable[0].CardNumber == "27116a": # Stage 1 main scheme
            msCards = filter(lambda card: card.Type == "main_scheme", mainSchemeDeck())
            for idx, c in enumerate(msCards):
                c.moveToTable(villainX(3, idx), tableLocations['villain'][1]+100)
