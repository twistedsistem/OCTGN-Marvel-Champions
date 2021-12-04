#------------------------------------------------------------
# 'Load Encounter' event
#------------------------------------------------------------

def loadEncounter(group, x = 0, y = 0, nbEncounter = 1):
    mute()
    vName = getGlobalVariable("villainSetup")
    if nbEncounter > 0:
        setupChoice = askChoice("Would you like to take on recommended modular encounter set(s) ?", ["Yes", "Let me choose which one(s)", "Let me choose how many and which one(s)"]) 
        if setupChoice == 0: return
        if setupChoice == 1: recommendedEncounter(group, villainName=vName)
        if setupChoice == 2: specificEncounter(group, nbModular = nbEncounter)
        if setupChoice == 3:
            nbEncounter = askInteger("How many modular encounter set(s) would you like to take on ?", nbEncounter)
            if nbEncounter == None: return
            else: specificEncounter(group, nbModular = nbEncounter)

def listEncounter():
    return ["Bomb Scare", "Masters of Evil", "Under Attack", "Legions of Hydra", "The Doomsday Chair", "Goblin Gimmicks", "A Mess of Things", "Power Drain", "Running Interference", "Temporal", "Anachronauts", "Master Of Time", "Ronan", "Experimental Weapon", "Hydra Assault", "Weapon Master", "Hydra Patrol", "Band of Badoon", "Galactic Artifacts", "Kree Militant", "Menagerie Medley", "Space Pirates", "Ship Command", "Power Stone", "The Black Order", "Armies of Titan", "Children of Thanos", "Infinity Gauntlet", "Legions of Hel", "Frost Giants", "Enchantress", "Streets of Mayhem", "Brothers Grimm", "Ransacked Armory", "State of Emergency", "Beasty Boys", "Mister Hyde", "Sinister Syndicate", "Crossfire's Crew", "Wrecking Crew"]


def specificEncounter(group, x = 0, y = 0, nbModular = 1):
    mute()
    while nbModular > 0:
        choice = askChoice("Which encounter would you like to take on?", listEncounter())

        if choice == 0: return
        if choice == 1:
            createCards(group,sorted(bomb_scare.keys()),bomb_scare)
        if choice == 2:
            createCards(group,sorted(masters_of_evil.keys()),masters_of_evil)
        if choice == 3:
            createCards(group,sorted(under_attack.keys()),under_attack)
        if choice == 4:
            createCards(group,sorted(legions_of_hydra.keys()),legions_of_hydra)
        if choice == 5:
            createCards(group,sorted(the_doomsday_chair.keys()),the_doomsday_chair)
        if choice == 6:
            createCards(group,sorted(goblin_gimmicks.keys()),goblin_gimmicks)
        if choice == 7:
            createCards(group,sorted(mess_of_things.keys()),mess_of_things)
        if choice == 8:
            createCards(group,sorted(power_drain.keys()),power_drain)
        if choice == 9:
            createCards(group,sorted(running_interference.keys()),running_interference)
        if choice == 10:
            createCards(group,sorted(temporal.keys()),temporal)
        if choice == 11:
            createCards(group,sorted(anachronauts.keys()),anachronauts)
        if choice == 12:
            createCards(group,sorted(mot.keys()),mot)
        if choice == 13:
            createCards(group,sorted(ronan_pnp.keys()),ronan_pnp)
        if choice == 14:
            createCards(group,sorted(exper_weapon.keys()),exper_weapon)
        if choice == 15:
            createCards(group,sorted(hydra_assault.keys()),hydra_assault)
        if choice == 16:
            createCards(group,sorted(weap_master.keys()),weap_master)
        if choice == 17:
            createCards(group,sorted(hydra_patrol.keys()),hydra_patrol)
        if choice == 18:
            createCards(group,sorted(band_of_badoon.keys()),band_of_badoon)
        if choice == 19:
            createCards(group,sorted(galactic_artifacts.keys()),galactic_artifacts)
        if choice == 20:
            createCards(group,sorted(kree_militant.keys()),kree_militant)
        if choice == 21:
            createCards(group,sorted(menagerie_medley.keys()),menagerie_medley)
        if choice == 22:
            createCards(group,sorted(space_pirates.keys()),space_pirates)
        if choice == 23:
            createCards(group,sorted(ship_command.keys()),ship_command)
        if choice == 24:
            createCards(group,sorted(power_stone.keys()),power_stone)
        if choice == 25:
            createCards(group,sorted(black_order.keys()),black_order)
        if choice == 26:
            createCards(group,sorted(armies_of_titan.keys()),armies_of_titan)
        if choice == 27:
            createCards(group,sorted(children_of_thanos.keys()),children_of_thanos)
        if choice == 28:
            createCards(group,sorted(infinity_gauntlet.keys()),infinity_gauntlet)
        if choice == 29:
            createCards(group,sorted(legions_of_hel.keys()),legions_of_hel)
        if choice == 30:
            createCards(group,sorted(frost_giants.keys()),frost_giants)
        if choice == 31:
            createCards(group,sorted(enchantress.keys()),enchantress)
        if choice == 32:
            createCards(group,sorted(streets_of_mayhem.keys()),streets_of_mayhem)
        if choice == 33:
            createCards(group,sorted(brothers_grimm.keys()),brothers_grimm)
        if choice == 34:
            createCards(group,sorted(ransacked_armory.keys()),ransacked_armory)
        if choice == 35:
            createCards(group,sorted(state_of_emergency.keys()),state_of_emergency)
        if choice == 36:
            createCards(group,sorted(beasty_boys.keys()),beasty_boys)
        if choice == 37:
            createCards(group,sorted(mister_hyde.keys()),mister_hyde)
        if choice == 38:
            createCards(group,sorted(sinister_syndicate.keys()),sinister_syndicate)
        if choice == 39:
            createCards(group,sorted(crossfire_crew.keys()),crossfire_crew)
        if choice == 40:
            createCards(group,sorted(wrecking_crew.keys()),wrecking_crew)

        nbModular -= 1


def recommendedEncounter(group, x = 0, y = 0, villainName=''):
    if villainName == 'Rhino':
            createCards(group,sorted(bomb_scare.keys()),bomb_scare)
    if villainName == 'Klaw':
            createCards(group,sorted(masters_of_evil.keys()),masters_of_evil)
    if villainName == 'Ultron':
            createCards(group,sorted(under_attack.keys()),under_attack)
    if villainName == 'Green Goblin: Mutagen Formula':
            createCards(group,sorted(goblin_gimmicks.keys()),goblin_gimmicks)
    if villainName == 'Green Goblin: Risky Business':
            createCards(group,sorted(goblin_gimmicks.keys()),goblin_gimmicks)
    if villainName == 'Crossbones':
            createCards(group,sorted(hydra_patrol.keys()),hydra_patrol)
            createCards(group,sorted(weap_master.keys()),weap_master)
            createCards(group,sorted(legions_of_hydra.keys()),legions_of_hydra)
    if villainName == 'Absorbing Man':
            createCards(group,sorted(hydra_patrol.keys()),hydra_patrol)
    if villainName == 'Taskmaster':
            createCards(group,sorted(weap_master.keys()),weap_master)
    if villainName == 'Zola':
            createCards(group,sorted(under_attack.keys()),under_attack)
    if villainName == 'Red Skull':
            createCards(group,sorted(hydra_assault.keys()),hydra_assault)
            createCards(group,sorted(hydra_patrol.keys()),hydra_patrol)
    if villainName == 'Kang':
            createCards(group,sorted(temporal.keys()),temporal)
    if villainName == 'Drang':
            createCards(group,sorted(band_of_badoon.keys()),band_of_badoon)
    if villainName == 'Collector 1':
            createCards(group,sorted(menagerie_medley.keys()),menagerie_medley)
    if villainName == 'Collector 2':
            createCards(group,sorted(menagerie_medley.keys()),menagerie_medley)
    if villainName == 'Nebula':
            createCards(group,sorted(space_pirates.keys()),space_pirates)
    if villainName == 'Ronan':
            createCards(group,sorted(kree_militant.keys()),kree_militant)
    if villainName == 'Ebony Maw':
            createCards(group,sorted(armies_of_titan.keys()),armies_of_titan)
            createCards(group,sorted(black_order.keys()),black_order)
    if villainName == 'Tower Defense':
            createCards(group,sorted(armies_of_titan.keys()),armies_of_titan)
    if villainName == 'Thanos':
            createCards(group,sorted(black_order.keys()),black_order)
            createCards(group,sorted(children_of_thanos.keys()),children_of_thanos)
    if villainName == 'Hela':
            createCards(group,sorted(legions_of_hel.keys()),legions_of_hel)
            createCards(group,sorted(frost_giants.keys()),frost_giants)
    if villainName == 'Loki':
            createCards(group,sorted(enchantress.keys()),enchantress)
            createCards(group,sorted(frost_giants.keys()),frost_giants)
    if villainName == 'The Hood':
        setupChoice = askChoice("Each encounter sets from The Hood Scenario Pack has been ranked from least to most difficult.", ["Lower difficulty (modular encounter sets ranked 1 to 7)", "Moderate difficulty (modular encounter sets ranked 2 to 8)", "Higher difficulty (modular encounter sets ranked 3 to 9)"]) 
        if setupChoice == 0: return
        if setupChoice == 1:
            createCards(shared.piles['Special'],sorted(streets_of_mayhem.keys()),streets_of_mayhem)
            createCards(shared.piles['Special'],sorted(brothers_grimm.keys()),brothers_grimm)
            createCards(shared.piles['Special'],sorted(ransacked_armory.keys()),ransacked_armory)
            createCards(shared.piles['Special'],sorted(state_of_emergency.keys()),state_of_emergency)
            createCards(shared.piles['Special'],sorted(beasty_boys.keys()),beasty_boys)
            createCards(shared.piles['Special'],sorted(mister_hyde.keys()),mister_hyde)
            createCards(shared.piles['Special'],sorted(sinister_syndicate.keys()),sinister_syndicate)
        if setupChoice == 2:
            createCards(shared.piles['Special'],sorted(brothers_grimm.keys()),brothers_grimm)
            createCards(shared.piles['Special'],sorted(ransacked_armory.keys()),ransacked_armory)
            createCards(shared.piles['Special'],sorted(state_of_emergency.keys()),state_of_emergency)
            createCards(shared.piles['Special'],sorted(beasty_boys.keys()),beasty_boys)
            createCards(shared.piles['Special'],sorted(mister_hyde.keys()),mister_hyde)
            createCards(shared.piles['Special'],sorted(sinister_syndicate.keys()),sinister_syndicate)
            createCards(shared.piles['Special'],sorted(crossfire_crew.keys()),crossfire_crew)
        if setupChoice == 3:
            createCards(shared.piles['Special'],sorted(ransacked_armory.keys()),ransacked_armory)
            createCards(shared.piles['Special'],sorted(state_of_emergency.keys()),state_of_emergency)
            createCards(shared.piles['Special'],sorted(beasty_boys.keys()),beasty_boys)
            createCards(shared.piles['Special'],sorted(mister_hyde.keys()),mister_hyde)
            createCards(shared.piles['Special'],sorted(sinister_syndicate.keys()),sinister_syndicate)
            createCards(shared.piles['Special'],sorted(crossfire_crew.keys()),crossfire_crew)
            createCards(shared.piles['Special'],sorted(wrecking_crew.keys()),wrecking_crew)