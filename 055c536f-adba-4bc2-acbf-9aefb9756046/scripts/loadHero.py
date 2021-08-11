#------------------------------------------------------------
# 'Load Hero' event
#------------------------------------------------------------

def loadHero(group, x = 0, y = 0):
    mute()
    if not deckNotLoaded(group):
        confirm("Cannot generate a deck: You already have cards loaded.  Reset the game in order to generate a new deck.")
        return
    choice = askChoice("What type of deck do you want to load?", ["An out of the box deck", "A registered deck"])

    if choice == 0: return
    if choice == 1:
        choice2 = askChoice("Which hero would you like to be?", ["Spider-Man", "Captain Marvel", "Iron Man", "She Hulk", "Black Panther", "Captain America", "Ms. Marvel", "Thor", "Black Widow", "Doctor Strange", "Hulk", "Hawkeye", "Spider-Woman", "Ant-man", "Wasp", "Quicksilver", "Scarlet Witch", "Groot", "Rocket Racoon", "Star Lord", "Gamora", "Drax", "Venom"])
        if choice2 == 0: return
        if choice2 == 1: deckname = createCards(me.Deck,sorted(spider_man.keys()),spider_man)
        if choice2 == 2: deckname = createCards(me.Deck,sorted(captain_marvel.keys()),captain_marvel)
        if choice2 == 3: deckname = createCards(me.Deck,sorted(iron_man.keys()),iron_man)
        if choice2 == 4: deckname = createCards(me.Deck,sorted(she_hulk.keys()),she_hulk)
        if choice2 == 5: deckname = createCards(me.Deck,sorted(black_panther.keys()),black_panther)
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
        if choice2 == 20: deckname = createCards(me.Deck,sorted(stld.keys()),stld)
        if choice2 == 21: deckname = createCards(me.Deck,sorted(gam.keys()),gam)
        if choice2 == 22: deckname = createCards(me.Deck,sorted(drax.keys()),drax)
        if choice2 == 23: deckname = createCards(me.Deck,sorted(vnm.keys()),vnm)
            
    if choice == 2:
        url = askString("Please enter the URL of the deck you wish to load.", "")
        if url == None: return
        if not "view/" in url:
            whisper("Error: Invalid URL.")
            return
        deckname = createAPICards(url)

    tableSetup()


def heroSetup(group=table, x = 0, y = 0):

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
        heroCard.moveToTable(playerX(id),tableLocations['hero'][1])
        heroCard.alternate = 'b'
        setHeroCounters(heroCard)
        notify("{} places his Hero on the table".format(me))

    if newHero:
        me.deck.shuffle()
        if len(me.hand) == 0:
            drawOpeningHand()

        createCards(heroCard.owner.piles["Nemesis Deck"],nemesis[str(heroCard.properties["Owner"])].keys(),nemesis[str(heroCard.properties["Owner"])])		

        #------------------------------------------------------------
        # Specific Hero setup
        #------------------------------------------------------------

        # Doctor Strange
        if str(heroCard.properties["Owner"]) == 'doctor_strange':
            createCards(me.piles['Special Deck'],special_decks['doctor_strange'].keys(),special_decks['doctor_strange'])



#------------------------------------------------------------
# 'Load Hero' specific functions
#------------------------------------------------------------

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