#
# Routines for writing out updated decks based on either the player piles or the shared piles
#
from datetime import datetime as dt
import collections
import clr
clr.AddReference('System.Web.Extensions')
from System.Web.Script.Serialization import JavaScriptSerializer as json #since .net 3.5?


def saveManual(group, x=0, y=0):
    phase = ""
    if currentPhase()[1] == 1:
        saveTable(phase)
    if currentPhase()[1] != 1:
        notify("You can save only when current phase is \"Hero Phase\"")

def saveTable(phase):
    mute()
    if phase == "":
        if 1 != askChoice('You are about to SAVE the table states including the elements on the table, shared deck and each player\'s hand and piles.\nThis option should be execute on the a game host.'
            , ['I am the Host!', 'I am not...'], ['#dd3737', '#d0d0d0']):
            return
    
        if not getLock():
            whisper("Others players are saving, please try manual saving again")
            return
    
    try:
        tab = {"table":[], "shared": {}, 'counters': None, "players": None, "ActivePlayer": None, "phase": None, "globalVariable": {}}

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

        # Active Player
        tab['ActivePlayer'] = str(getActivePlayer()._id)

        # Phase
        tab['phase'] = getGlobalVariable("phase")

        # Global Variable
        tab['globalVariable'] = serializeGlobalVariable()

        if phase == "":
            filename = saveFileDlg('', '', 'Json Files|*.json')
        else: 
            with open("data.path", 'r') as f:
                dir = f.readline()
                filename = dir + "\\GameDatabase\\055c536f-adba-4bc2-acbf-9aefb9756046\\" + "AutoSave.json"
            
        if filename == None:
            return
        
        with open(filename, 'w+') as f:
            f.write(json().Serialize(tab))
        
        if phase == "":
            notify("Table state saves to {}".format(filename))

    finally:
        clearLock()

def loadManual(group, x=0, y=0):
    phase = ""
    loadTable(phase)

def restoreSave(group, x=0, y=0):
    phase = "restore"
    loadTable(phase)

def loadTable(phase):
    mute()
    
    if 1 != askChoice('You are about to LOAD the table states including the elements on the table, shared deck and each player\'s hand and piles.\nThis option should be execute on the a game host.'
        , ['I am the Host!', 'I am not...'], ['#dd3737', '#d0d0d0']):
        return
    
    if not getLock():
        whisper("Others players are locking the table, please try again")
        return
    
    try:
        if phase == "":
            filename = openFileDlg('', '', 'Json Files|*.json')
        else: 
            with open("data.path", 'r') as f:
                dir = f.readline()
                filename = dir + "\\GameDatabase\\055c536f-adba-4bc2-acbf-9aefb9756046\\" + "AutoSave.json"
                notify("Restore Table state saves to last phase")

        if not filename:
            return

        with open(filename, 'r') as f:
            tab = json().DeserializeObject(f.read())
        
        deserializeTable(tab['table'])
        
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

        if tab['ActivePlayer'] is not None and len(tab['ActivePlayer']) > 0:
            setActivePlayer(Player(num(tab['ActivePlayer'])))

        if tab['phase'] is not None and len(tab['phase']) > 0:
            activePlayerNum = num(tab['ActivePlayer']) - 1
            if tab['phase'] == "Hero Phase":
                players[activePlayerNum].setActive()
            if tab['phase'] == "Villain Phase":
                players[activePlayerNum].setActive()
                setPhase(2)

        if tab['globalVariable'] is not None and len(tab['globalVariable']) > 0:
            for k in tab['globalVariable'].Keys:
                deserializeGlobalVariable(k, tab['globalVariable'][k])
                
    finally:
        clearLock()
