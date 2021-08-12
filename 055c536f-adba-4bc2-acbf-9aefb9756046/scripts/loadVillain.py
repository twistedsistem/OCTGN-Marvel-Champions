#------------------------------------------------------------
# 'Load Villain' event
#------------------------------------------------------------

def loadVillain(group, x = 0, y = 0):
    mute()
    villainName = ''
    nbEncounter = 1

    if not deckNotLoaded(group,0,0,shared.villain):
        confirm("Cannot generate a deck: You already have cards loaded.  Reset the game in order to generate a new deck.")
        return

    choice = askChoice("Which villain would you like to defeat?", ["Rhino", "Klaw", "Ultron", "Green Goblin: Mutagen Formula", "Green Goblin: Risky Business", "The Wrecking Crew", "Baron Zemo: Firestarter (By: FelixFactory)", "Crossbones", "Absorbing Man", "Taskmaster", "Zola", "Red Skull", "Kang", "Drang", "Collector 1", "Collector 2", "Nebula", "Ronan"])
    passSharedControl(me)
    update()
    if choice == 0: return

    if choice == 1:
        createCards(shared.villain,sorted(rhino.keys()),rhino)
        notify('{} loaded "Rhino", Good Luck!'.format(me))
        villainName = 'Rhino'

    if choice == 2:
        createCards(shared.villain,sorted(klaw.keys()),klaw)
        notify('{} loaded "Klaw", Good Luck!'.format(me))
        villainName = 'Klaw'

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
        createCards(shared.villain,sorted(legions_of_hydra.keys()),legions_of_hydra)
        createCards(shared.villain,sorted(bomb_scare.keys()),bomb_scare)
        notify('{} loaded "Baron Zemo: Firestarter (By: FelixFactory)", Good Luck!'.format(me))
        villainName = 'Baron Zemo: Firestarter'

    if choice == 8:
        createCards(shared.villain,sorted(crossbones.keys()),crossbones)
        createCards(shared.special,sorted(exper_weapon.keys()),exper_weapon)
        nbEncounter = 3
        notify('{} loaded "Crossbones", Good Luck!'.format(me))
        villainName = 'Crossbones'

    if choice == 9:
        createCards(shared.villain,sorted(absorbing_man.keys()),absorbing_man)
        notify('{} loaded "Absorbing Man", Good Luck!'.format(me))
        villainName = 'Absorbing Man'

    if choice == 10:
        createCards(shared.villain,sorted(taskmaster.keys()),taskmaster)
        createCards(shared.encounter,sorted(hydra_patrol.keys()),hydra_patrol)
        for c in filter(lambda card: card.Type == "ally", villainDeck()):
            c.moveTo(specialDeck())
        shared.Special.shuffle()
        notify('{} loaded "Taskmaster", Good Luck!'.format(me))
        villainName = 'Taskmaster'

    if choice == 11:
        createCards(shared.villain,sorted(zola.keys()),zola)
        notify('{} loaded "Zola", Good Luck!'.format(me))
        villainName = 'Zola'

    if choice == 12:
        createCards(shared.villain,sorted(red_skull.keys()),red_skull)
        for c in filter(lambda card: card.Type == "side_scheme", villainDeck()):
            c.moveTo(specialDeck())
        shared.Special.shuffle()
        for c in filter(lambda card: card.CardNumber == "04130", villainDeck()):
            c.moveTo(removedFromGameDeck())
        nbEncounter = 2
        notify('{} loaded "Red Skull", Good Luck!'.format(me))
        villainName = 'Red Skull'

    if choice == 13:
        createCards(shared.villain,sorted(the_once_and_future_kang.keys()),the_once_and_future_kang)
        for c in filter(lambda card: card.CardNumber == "11023", villainDeck()):
            c.moveTo(removedFromGameDeck())
        notify('{} loaded "Kang", Good Luck!'.format(me))
        villainName = 'Kang'

    if choice == 14:
        createCards(shared.villain,sorted(brotherhood_of_badoon.keys()),brotherhood_of_badoon)
        createCards(shared.encounter,sorted(ship_command.keys()),ship_command)
        for c in filter(lambda card: card.CardNumber == "16142", encounterDeck()):
            c.moveToTable(-100, 100)
        createCards(shared.campaign,sorted(gmw_campaign_market.keys()),gmw_campaign_market)
        createCards(shared.campaign,sorted(gmw_campaign_challenge.keys()),gmw_campaign_challenge)
        notify('{} loaded "Drang", Good Luck!'.format(me))
        villainName = 'Drang'

    if choice == 15:
        createCards(shared.villain,sorted(collector1.keys()),collector1)
        createCards(shared.encounter,sorted(galactic_artifacts.keys()),galactic_artifacts)
        createCards(shared.campaign,sorted(gmw_campaign_market.keys()),gmw_campaign_market)
        createCards(shared.campaign,sorted(gmw_campaign_challenge.keys()),gmw_campaign_challenge)
        notify('{} loaded "Collector 1", Good Luck!'.format(me))
        villainName = 'Collector 1'

    if choice == 16:
        createCards(shared.villain,sorted(collector2.keys()),collector2)
        createCards(shared.encounter,sorted(galactic_artifacts.keys()),galactic_artifacts)
        createCards(shared.removed,sorted(ship_command.keys()),ship_command)
        createCards(shared.campaign,sorted(gmw_campaign_market.keys()),gmw_campaign_market)
        createCards(shared.campaign,sorted(gmw_campaign_challenge.keys()),gmw_campaign_challenge)
        notify('{} loaded "Collector 2", Good Luck!'.format(me))
        villainName = 'Collector 2'

    if choice == 17:
        createCards(shared.villain,sorted(nebula.keys()),nebula)
        createCards(shared.encounter,sorted(power_stone.keys()),power_stone)
        for c in filter(lambda card: card.CardNumber == "16149", encounterDeck()):
            c.moveToTable(0, 0)
        createCards(shared.encounter,sorted(ship_command.keys()),ship_command)
        for c in filter(lambda card: card.CardNumber == "16142", encounterDeck()):
            c.moveToTable(-100, 100)
        createCards(shared.campaign,sorted(gmw_campaign_market.keys()),gmw_campaign_market)
        createCards(shared.campaign,sorted(gmw_campaign_challenge.keys()),gmw_campaign_challenge)
        notify('{} loaded "Nebula", Good Luck!'.format(me))
        villainName = 'Nebula'

    if choice == 18:
        createCards(shared.villain,sorted(ronan.keys()),ronan)
        createCards(shared.encounter,sorted(power_stone.keys()),power_stone)
        for c in filter(lambda card: card.CardNumber == "16149", encounterDeck()):
            c.moveToTable(0, 0)
        createCards(shared.encounter,sorted(ship_command.keys()),ship_command)
        for c in filter(lambda card: card.CardNumber == "16142", encounterDeck()):
            c.moveToTable(-100, 100)
        createCards(shared.campaign,sorted(gmw_campaign_market.keys()),gmw_campaign_market)
        createCards(shared.campaign,sorted(gmw_campaign_challenge.keys()),gmw_campaign_challenge)
        notify('{} loaded "Ronan", Good Luck!'.format(me))
        villainName = 'Ronan'

    setGlobalVariable("villainSetup",str(villainName))
    update()
    loadEncounter(group, nbChoice=nbEncounter)
    loadDifficulty()
    tableSetup(doPlayer=False,doEncounter=True)


def loadDifficulty():
    vName = getGlobalVariable("villainSetup")
    if vName != 'The Wrecking Crew':
        choice = askChoice("What difficulty would you like to play at?", ["Standard", "Expert"])

        if choice == 0: return
        if choice == 1:
            createCards(shared.encounter,sorted(standard.keys()),standard)
        if choice == 2:
            createCards(shared.encounter,sorted(standard.keys()),standard)
            createCards(shared.encounter,sorted(expert.keys()),expert)
            setGlobalVariable("difficulty", "1")

    if vName == 'The Wrecking Crew':
        choice = askChoice("What difficulty would you like to play at?", ["Standard", "Expert"])

        if choice == 0: return
        if choice == 1: return
        if choice == 2:
            setGlobalVariable("difficulty", "1")
            return


def villainSetup(group=table, x = 0, y = 0):
    # Global Variables
    gameDifficulty = getGlobalVariable("difficulty")
    vName = getGlobalVariable("villainSetup")

    # Move cards from Villain Deck to Encounter and Scheme Decks
    encounterDeckCards = filter(lambda card: card.Type != "villain" and card.Type != "main_scheme", villainDeck())
    mainSchemeCards = filter(lambda card: card.Type == "main_scheme", villainDeck())
    villainCards = filter(lambda card: card.Type == "villain", villainDeck())
    villainEnvCards = filter(lambda card: card.Type == "environment", villainDeck())

    for c in encounterDeckCards:
        c.moveTo(encounterDeck())
    for c in mainSchemeCards:
        c.moveTo(mainSchemeDeck())

    # If we loaded the encounter deck - add the first main scheme card to the table
    sorted(mainSchemeCards)[0].moveToTable(tableLocations['mainScheme'][0],tableLocations['mainScheme'][1])
    sorted(mainSchemeCards)[0].anchor = False
    sorted(mainSchemeCards).pop(0)


    # If we loaded the encounter deck - add the villain(s) card(s) to the table
    villainCards = sorted(villainCards)
    if vName != 'The Wrecking Crew' and vName != 'Kang':
        if gameDifficulty == "1":
            villainCards[0].delete()
            villainCards.pop(0)
        else:
            villainCards[len(villainCards) - 1].delete()
            villainCards.pop(len(villainCards) - 1)
        villainCards[0].moveToTable(villainX(1,0),tableLocations['villain'][1])
        villainCards[0].anchor = False
    elif vName == 'The Wrecking Crew':
        if gameDifficulty == "1":
            vCards = villainCards[1::2]
        else:
            vCards = villainCards[::2]
        for idx, c in enumerate(vCards):
            c.moveToTable(villainX(4,idx),tableLocations['villain'][1]-35)
            if idx == 0:
                c.highlight = ActiveColour
        ssCards = filter(lambda card: card.Type == "side_scheme", encounterDeck())
        for idx, c in enumerate(sorted(ssCards)):
            c.moveToTable(villainX(4,idx)-10,tableLocations['villain'][1]+70)
    elif vName == 'Kang':
        if gameDifficulty == "1":
            villainCards = villainCards[6:]
        else:
            villainCards = villainCards[0:6]
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

def SpecificVillainSetup(vName = ''):

    vCardOnTable = sorted(filter(lambda card: card.Type == "villain", table), reverse=True)
    msCardOnTable = sorted(filter(lambda card: card.Type == "main_scheme", table))
    villainEnvCards = sorted(filter(lambda card: card.Type == "environment", encounterDeck()))
    villainAttCards = sorted(filter(lambda card: card.Type == "attachment", encounterDeck()))
    vilX, vilY = vCardOnTable[0].position
    msX, msY = msCardOnTable[0].position
    ssX = vilX + 100
    ssY = vilY + 20

    if vName == 'Rhino':
        if vCardOnTable[0].CardNumber == "01095":
            ssCard = filter(lambda card: card.CardNumber == "01107", encounterDeck())
            if len(ssCard) == 0:
                ssCard = filter(lambda card: card.CardNumber == "01107", encounterDiscardDeck())
            ssCard[0].moveToTable(ssX, ssY)


    if vName == 'Klaw':
        ssCard1 = filter(lambda card: card.CardNumber == "01125", encounterDeck())
        ssCard2 = filter(lambda card: card.CardNumber == "01127", encounterDeck())

        if msCardOnTable[0].CardNumber == "01116a" and len(ssCard1) > 0:
            ssCard1[0].moveToTable(ssX, ssY)

        if vCardOnTable[0].CardNumber == "01114":
            ssCard1_OnTable = filter(lambda card: card.CardNumber == "01125", table)
            if len(ssCard2) == 0:
                ssCard2 = filter(lambda card: card.CardNumber == "01127", encounterDiscardDeck())
            if len(ssCard1_OnTable) == 0:
                ssCard2[0].moveToTable(ssX, ssY)
            if len(ssCard1_OnTable) > 0:
                ssCard2[0].moveToTable(ssCard1_OnTable[0].position[0], ssCard1_OnTable[0].position[1] + 70)


    if vName == 'Ultron':
        EnvCard = sorted(filter(lambda card: card.CardNumber == "01140", encounterDeck()))
        if msCardOnTable[0].CardNumber == "01137a" and len(EnvCard) > 0:
            EnvCard[0].moveToTable(tableLocations['environment'][0], tableLocations['environment'][1])

        if vCardOnTable[0].CardNumber == "01136":
            ssCard = filter(lambda card: card.CardNumber == "01150", encounterDeck())
            if len(ssCard) == 0:
                ssCard = filter(lambda card: card.CardNumber == "01150", encounterDiscardDeck())
            ssCard[0].moveToTable(ssX, ssY)


    if vName == 'Risky Business':
        EnvCard = sorted(filter(lambda card: card.CardNumber == "02006a", encounterDeck()))
        if msCardOnTable[0].CardNumber == "02004a" and len(EnvCard) > 0:
            EnvCard[0].moveToTable(tableLocations['environment'][0], tableLocations['environment'][1])


    if vName == 'Baron Zemo: Firestarter':
        EnvCard = sorted(filter(lambda card: card.CardNumber == "91006", encounterDeck()))
        if msCardOnTable[0].CardNumber == "91004a" and len(EnvCard) > 0:
            EnvCard[0].moveToTable(tableLocations['environment'][0], tableLocations['environment'][1])
            ssCard = filter(lambda card: card.CardNumber == "01109", encounterDeck())
            ssCard[0].moveToTable(ssX, ssY)
            minionCard = filter(lambda card: card.CardNumber == "01182", encounterDeck())
            minionCard[0].moveToTable(tableLocations['environment'][0] - 90, tableLocations['environment'][1])


    if vName == 'Crossbones':
        if vCardOnTable[0].CardNumber == "04059":
            AttachmentCard = filter(lambda card: card.CardNumber == "04064", encounterDeck())
            if len(AttachmentCard) == 0:
                AttachmentCard = filter(lambda card: card.CardNumber == "01107", encounterDiscardDeck())
            AttachmentCard[0].moveToTable(vilX-25, vilY+5)
            AttachmentCard[0].sendToBack()


    if vName == 'Taskmaster':
        if msCardOnTable[0].CardNumber == "04096a":
            ssCard = filter(lambda card: card.CardNumber == "04154", encounterDeck())
            if len(ssCard) == 0:
                ssCard = filter(lambda card: card.CardNumber == "04154", encounterDiscardDeck())
            ssCard[0].moveToTable(ssX, ssY)


    if vName == 'Zola':
        ssCard1 = filter(lambda card: card.CardNumber == "04122", encounterDeck())
        ssCard2 = filter(lambda card: card.CardNumber == "04123", encounterDiscardDeck())
        minionCard = filter(lambda card: card.CardNumber == "04114", encounterDeck()) 

        if msCardOnTable[0].CardNumber == "04112a" and len(ssCard1) > 0:
            ssCard1[0].moveToTable(ssX, ssY)
            minionCard[0].moveToTable(tableLocations['environment'][0], tableLocations['environment'][1])

        if vCardOnTable[0].CardNumber == "04110":
            ssCard1_OnTable = filter(lambda card: card.CardNumber == "04122", table)
            if len(ssCard2) == 0:
                ssCard2 = filter(lambda card: card.CardNumber == "04123", encounterDeck())
            if len(ssCard1_OnTable) == 0:
                ssCard2[0].moveToTable(ssX, ssY)
            if len(ssCard1_OnTable) > 0:
                ssCard2[0].moveToTable(ssCard1_OnTable[0].position[0], ssCard1_OnTable[0].position[1] + 70)


    if vName == 'Red Skull':
        ssCard = filter(lambda card: card.CardNumber == "04139", specialDeck())

        if msCardOnTable[0].CardNumber == "04128a" and len(ssCard) > 0:
            ssCard[0].moveToTable(ssX, ssY)


    if vName == 'Drang':
        EnvCard = sorted(filter(lambda card: card.CardNumber == "16063", encounterDeck()))
        if msCardOnTable[0].CardNumber == "16061a" and len(EnvCard) > 0:
            EnvCard[0].moveToTable(tableLocations['environment'][0], tableLocations['environment'][1])


    if vName == 'Collector 2':
        EnvCard = sorted(filter(lambda card: card.CardNumber == "16085a", encounterDeck()))
        if msCardOnTable[0].CardNumber == "16082a" and len(EnvCard) > 0:
            EnvCard[0].moveToTable(tableLocations['environment'][0], tableLocations['environment'][1])


    if vName == 'Nebula':
        EnvCard = sorted(filter(lambda card: card.CardNumber == "16093", encounterDeck()))
        if msCardOnTable[0].CardNumber == "16091a" and len(EnvCard) > 0:
            EnvCard[0].moveToTable(tableLocations['environment'][0], tableLocations['environment'][1])


    if vName == 'Ronan':
        ssCard1 = filter(lambda card: card.CardNumber == "16111", encounterDiscardDeck())
        ssCard2 = filter(lambda card: card.CardNumber == "16113", encounterDiscardDeck())
		
        EnvCard = sorted(filter(lambda card: card.CardNumber == "16108", encounterDeck()))
        if msCardOnTable[0].CardNumber == "16106a" and len(EnvCard) > 0:
            EnvCard[0].moveToTable(tableLocations['environment'][0] - 20, tableLocations['environment'][1])
            AttachmentCard = filter(lambda card: card.CardNumber == "16109", encounterDeck())
            AttachmentCard[0].moveToTable(vilX-25, vilY+5)
            AttachmentCard[0].sendToBack()

        if vCardOnTable[0].CardNumber == "16104":
            ssCard1_OnTable = filter(lambda card: card.CardNumber == "16111", table)
            if len(ssCard1_OnTable) == 0:
                if len(ssCard1) == 0:
                    ssCard1 = filter(lambda card: card.CardNumber == "16111", encounterDeck())
                    ssCard1[0].moveToTable(ssX, ssY)

        if vCardOnTable[0].CardNumber == "16105":
            ssCard2_OnTable = filter(lambda card: card.CardNumber == "16113", table)
            if len(ssCard2_OnTable) == 0:
                if len(ssCard2) == 0:
                    ssCard2 = filter(lambda card: card.CardNumber == "16113", encounterDeck())
                    if len(ssCard1_OnTable) == 0:
                        ssCard2[0].moveToTable(ssX, ssY)
                    if len(ssCard1_OnTable) > 0:
                        ssCard2[0].moveToTable(ssCard1_OnTable[0].position[0], ssCard1_OnTable[0].position[1] + 70)