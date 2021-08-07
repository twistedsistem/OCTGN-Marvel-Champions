#------------------------------------------------------------
# 'Load Encounter' event
#------------------------------------------------------------

def loadEncounter(group, x = 0, y = 0, nbChoice = 0):
    vName = getGlobalVariable("villainSetup")
    if vName != 'The Wrecking Crew' and vName != "Baron Zemo: Firestarter":
        setupChoice = askChoice("Would you like to take on recommended modular encounter set ?", ["Yes", "No"]) 
        if setupChoice == 0: return
        if setupChoice == 1: recommendedEncounter(group, villainName=vName)
        if setupChoice == 2: 

            while nbChoice > 0:
                choice = askChoice("Which encounter would you like to take on?", ["Bomb Scare", "Masters of Evil", "Under Attack", "Legions of Hydra", "The Doomsday Chair", "Goblin Gimmicks", "A Mess of Things", "Power Drain", "Running Interference", "Temporal", "Anachronauts", "Master Of Time", "Ronan", "Experimental Weapon", "Hydra Assault", "Weapon Master", "Hydra Patrol", "Band of Badoon", "Galactic Artifacts", "Kree Militant", "Menagerie Medley", "Space Pirates", "Ship Command", "Power Stone"])

                if choice == 0: return
                if choice == 1:
                    createCards(shared.encounter,sorted(bomb_scare.keys()),bomb_scare)
                if choice == 2:
                    createCards(shared.encounter,sorted(masters_of_evil.keys()),masters_of_evil)
                if choice == 3:
                    createCards(shared.encounter,sorted(under_attack.keys()),under_attack)
                if choice == 4:
                    createCards(shared.encounter,sorted(legions_of_hydra.keys()),legions_of_hydra)
                if choice == 5:
                    createCards(shared.encounter,sorted(the_doomsday_chair.keys()),the_doomsday_chair)
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
                    createCards(shared.encounter,sorted(ronan_pnp.keys()),ronan_pnp)
                if choice == 14:
                    createCards(shared.encounter,sorted(exper_weapon.keys()),exper_weapon)
                if choice == 15:
                    createCards(shared.encounter,sorted(hydra_assault.keys()),hydra_assault)
                if choice == 16:
                    createCards(shared.encounter,sorted(weap_master.keys()),weap_master)
                if choice == 17:
                    createCards(shared.encounter,sorted(hydra_patrol.keys()),hydra_patrol)
                if choice == 18:
                    createCards(shared.encounter,sorted(band_of_badoon.keys()),band_of_badoon)
                if choice == 19:
                    createCards(shared.encounter,sorted(galactic_artifacts.keys()),galactic_artifacts)
                if choice == 20:
                    createCards(shared.encounter,sorted(kree_militant.keys()),kree_militant)
                if choice == 21:
                    createCards(shared.encounter,sorted(menagerie_medley.keys()),menagerie_medley)
                if choice == 22:
                    createCards(shared.encounter,sorted(space_pirates.keys()),space_pirates)
                if choice == 23:
                    createCards(shared.encounter,sorted(ship_command.keys()),ship_command)
                if choice == 24:
                    createCards(shared.encounter,sorted(power_stone.keys()),power_stone)

                nbChoice -= 1

    elif vName == "Baron Zemo: Firestarter":
        createCards(shared.encounter,sorted(baron_zemo_firestarter_modules.keys()),baron_zemo_firestarter_modules)


def recommendedEncounter(group, x = 0, y = 0, villainName=''):
    if villainName == 'Rhino':
            createCards(shared.encounter,sorted(bomb_scare.keys()),bomb_scare)
    if villainName == 'Klaw':
            createCards(shared.encounter,sorted(masters_of_evil.keys()),masters_of_evil)
    if villainName == 'Ultron':
            createCards(shared.encounter,sorted(under_attack.keys()),under_attack)
    if villainName == 'Green Goblin: Mutagen Formula':
            createCards(shared.encounter,sorted(goblin_gimmicks.keys()),goblin_gimmicks)
    if villainName == 'Green Goblin: Risky Business':
            createCards(shared.encounter,sorted(goblin_gimmicks.keys()),goblin_gimmicks)
    if villainName == 'Crossbones':
            createCards(shared.encounter,sorted(hydra_patrol.keys()),hydra_patrol)
            createCards(shared.encounter,sorted(weap_master.keys()),weap_master)
            createCards(shared.encounter,sorted(legions_of_hydra.keys()),legions_of_hydra)
    if villainName == 'Absorbing Man':
            createCards(shared.encounter,sorted(hydra_patrol.keys()),hydra_patrol)
    if villainName == 'Taskmaster':
            createCards(shared.encounter,sorted(weap_master.keys()),weap_master)
    if villainName == 'Zola':
            createCards(shared.encounter,sorted(under_attack.keys()),under_attack)
    if villainName == 'Red Skull':
            createCards(shared.encounter,sorted(hydra_assault.keys()),hydra_assault)
            createCards(shared.encounter,sorted(hydra_patrol.keys()),hydra_patrol)
    if villainName == 'Kang':
            createCards(shared.encounter,sorted(temporal.keys()),temporal)
    if villainName == 'Drang':
            createCards(shared.encounter,sorted(band_of_badoon.keys()),band_of_badoon)
    if villainName == 'Collector 1':
            createCards(shared.encounter,sorted(menagerie_medley.keys()),menagerie_medley)
    if villainName == 'Collector 2':
            createCards(shared.encounter,sorted(menagerie_medley.keys()),menagerie_medley)
    if villainName == 'Nebula':
            createCards(shared.encounter,sorted(space_pirates.keys()),space_pirates)
    if villainName == 'Ronan':
            createCards(shared.encounter,sorted(kree_militant.keys()),kree_militant)