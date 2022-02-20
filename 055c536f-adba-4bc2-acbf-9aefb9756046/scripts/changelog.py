changelog = {
    '0000104': ("0.0.1.4", "16 December 2019", [
        "Welcome to the Marvel Champions OCTGN Plugin!",
        "Added Changelog",
        "Updated obligation cards to properly get generated",
        "Fixed issue with being able to use Deck Editor",
        "Player setup is now triggered automatically after a hero deck is loaded",
        "Promp users to load a hero deck after the game initializes",
        "Default double click option for face down cards now flips them over.",
        "Default double click option for scheme cards now flips them to the other side",
        "New Add card option added in case a card is needed in the game and can't be found",
        "New option to add 3 markers to a card for quick marker additions",
        "Updated some grammar on prompts"
        ]),
    '0000105': ("0.0.1.5", "16 December 2019", [
        "Fixed a bug that would not load the full encounter deck when loading a villain after the hero deck has been loaded first"
        ]),
    '0000106': ("0.0.1.6", "2 January 2020", [
        "Everyone who already had the image pack installed needs to redownload and install the new one as there were fixes put in place for certain cards like Wakanda Forever!",
        "Added Captain America Hero Pack",
        "Added Ms. Marvel Hero Pack",
        "Added Green Goblin Scenario Pack",
        "Fixed function to reshuffle encounter cards into encounter deck to only pull discarded cards and not all encounter cards on the table",
        "Added ability to load non published decks from marvelcdb. User needs to edit marvelcdb to check the 'Share Your Decks' option in your profile preferences",
        "Added right click option to add acceleration marker"
        ]),
    '0000107': ("0.0.1.7", "2 January 2020", [
        "Fixed flipping over cards that have an alternate back",
        "Fixed Captain America and Ms. Marvel decks being fliped while loading"
        ]),
    '0000108': ("0.0.1.8", "31 January 2020", [
        "Reworked the gameflow mecahnics with the turns and phases making the entire game move foward with pressing 'f12' when finished with current turn or villain action. Active player is now going to be highlighted in green and players that have finished their turn are going to be highlighted in gray.  Active player is the only one that can advance the game with the next 'f12' press.",
        "Fixed Green Goblin villains that have alternate backs",
        "Fixed a bug where you could discard cards from the table that should never be discarded",
        "Fixed a bug where the next scheme was pulling out in wrong order and rotating the card sideways",
        "Fixed a bug where moving to the next villain stage was not maintaining the status/markers of the previous villain",
        "Added a new keyboard shortcut to add an all purpose marker to any card by pressing Right",
        "Added a new keyboard shortcut to remove an all purpose marker to any card by pressing Left",
        "Added aspect type to the owner property on the cards to allow for easier Deck Building",
        "Change the table background to be two images that overlay so zooming in on the board will keep the cards in the designated positions on the image",
        "Expansion pack images have been uploaded to the website"
        ]),
    '0000109': ("0.0.1.9", "8 February 2020", [
        "The Wrecking Crew Scenario Pack added",
        "Fixed bug where first player was being set twice on setup",
        "Fixed bug where card control was not being passed on turn pass",
        "Fixed Green Goblin Environment cards not working as double sided",
        "Reworked the game setup to dynamically place the villain since wrecking crew has 4",
        "Removed the set table positions",
        "Added default double click action to the villains to draw the next encounter card",
        "Active villain is highlighted in green for The Wrecking Crew and a right click menu has been added to the cards to set a villain as active",
        "The Wrecking Crew Scenario Pack images have been uploaded to the website"
        ]),
    '0000110': ("0.0.1.10", "18 March 2020", [
        "Thor Hero Pack added",
        "Thor Hero Pack images have been uploaded to the website"
        ]),
    '0000111': ("0.0.1.11", "11 April 2020", [
        "Fixed Thor nemesis cards having the wrong backing",
        "Added option to move a card to the bottom of the hero deck",
        "Added option to move a card to the bottom of the encounter deck",
        "Changed the marker right click options to be shown on all cards to allow for adding damage tokens on cards that usually wouldn't take damage"
        ]),
    '0000112': ("0.0.1.12", "17 June 2020", [
        "Black Widow Hero Pack added",
        "Black Widow Hero Pack images have been uploaded to the website",
        "Changed game URL to point to new website",
        "Updated the rules PDF - thank you ZATGamer from github",
        "Updated some keyboard shortcuts to align better with the Arkham Horror OCTGN module - thank you pilunte23 from github",
        "Fixed player group definition in the definition.xml per OCTGN update",
        "Moved Marker definition to be in the definition.xml per OCTGN update"
        ]),
    '0000113': ("0.0.1.13", "18 June 2020", [
        "Fixed Black Widow Nemesis Deck"
        ]),
    '0000114': ("0.0.1.14", "9 July 2020", [
        "Doctor Strange Hero Pack added",
        "Doctor Strange Hero Pack images have been uploaded to the website",
        "Fixed reported bug when advancing the game with f12 and all players cards would not ready and would not automatically draw new hand - thank you bugu57 from github"
        ]),
    '0000115': ("0.0.1.15", "13 July 2020", [
        "Fixed Doctor Strange to allow for the Invocation Deck"
        ]),
    '0000116': ("0.0.1.16", "20 August 2020", [
        "Hulk Hero Pack added",
        "Hulk Hero Pack images have been uploaded to the website",
        "FFG Print and Play module Ronan added",
        "Ronan module images have been uploaded to the website",
        "Community Content Baron Zemo: Firestarter villain added - thank you FelixFactory from discord",
        "Baron Zemo: Firestarter images have been uploaded to the website - thank you FelixFactory from discord"
        ]),
    '0000117': ("0.0.1.17", "12 November 2020", [
        "The Rise of Red Skull added",
        "The Rise of Red Skull images have been uploaded to the website"
        ]),
    '0000118': ("0.0.1.18", "14 November 2020", [
        "Fixed issue where Standard and Expert encounter cards were not being created for the Red Skull villains.",
        "Set visibility for all global decks to ALL by default."
        ]),
    '0000119': ("0.0.1.19", "3 December 2020", [
        "Ant-Man Hero Pack added",
        "Ant-Man Hero Pack images have been uploaded to the website."
        ]),
    '0000120': ("0.0.1.20", "22 February 2021", [
        "Updated Ant-Man image pack to have Swarm Tactics. You will need to redownload and install the image pack",
        "Wasp Hero Pack added",
        "Wasp Hero Pack images have been uploaded to the website.",
        "Quicksilver Hero Pack added",
        "Quicksilver Hero Pack images have been uploaded to the website."
        ]),
    '0000200': ("0.0.2.00", "30 July 2021", [
        "Scheme size fixed",
        "Draw unrevealed action on player deck added",
        "Flip top card action on player/special/encounter deck added",
        "Kang Villain Pack added",
        "Galaxy's Most Wanted Extension added",
        "Scarlet Witch Hero Pack added",
        "Groot Hero Pack added",
        "Rocket Racoon Hero Pack added",
        "Star-Lord Hero Pack added",
        "Gamora Hero Pack added",
        "Drax Hero Pack added",
        "Venom Hero Pack added"
        ]),
    '0000201': ("0.0.2.01", "7 August 2021", [
        "Background changed",
        "Markers changed",
        "Fixed loading .o8d in actions.py per OCTGN update"
        ]),
    '0000202': ("0.0.2.02", "9 August 2021", [
        "Load encounter with default modular or custom setup",
        "Shared campaign deck added"
        ]),
    '0000203': ("0.0.2.03", "19 August 2021", [
        "Updated last published hero image packs to fix alter-ego/hero card coming the wrong side. You will need to redownload and install the image pack",
        "Updated image pack released at https://twistedsistem.wixsite.com/octgnmarvelchampions",
        "Turn counter fixed",
        "Notification added when encounter deck is empty",
        "Shuffle into deck fixed when used on Dr Strange special deck",
        "Shortcuts for status card changed : use \"alt\" instead of \"ctrl\" and \"ctrl+alt\" instead of \"ctrl+shift\"",
        "NEW! Save and load table option added - thanks to authors of the Arkham Horror OCTGN module that make most of it",
        "NEW! Highlight option added using numpad as shortcuts",
        "NEW! Take global control added using F8 as shortcuts to take control on all shared cards and piles"
        ]),
    '0000204': ("0.0.2.04", "20 August 2021", [
        "Fixed Pull Boost/encounter card when using right-click on table",
        "Fixed loading Kang not working"
        ]),
    '0000205': ("0.0.2.05", "27 September 2021", [
        "The Mad Titan's Shadow added",
        "Nebula Hero pack added",
        "Image packs released at https://twistedsistem.wixsite.com/octgnmarvelchampions",
        "Full custom setup for modulars encounters added",
        "Reworked the game setup for Kang to randomly place Kang II villain(s) when using \"Defeat Villain\" (\"Next Scheme\" is disabled for Kang)",
        "Random Loki generated while setting up and using \Defeat Villain\"",
        "Right-click on Special shared pile to load any modular encounter set after initial setup",
        "Double-click on Infinity Gauntlet encounter card on table to draw a card from the Special Deck"
        ]),
    '0000206': ("0.0.2.06", "3 October 2021", [
        "Fixed issue with Hela setup"
        ]),
    '0000207': ("0.0.2.07", "3 October 2021", [
        "Fixed issue where some Ebony Maw cards were discarded in player discard pile"
        ]),
    '0000208': ("0.0.2.08", "6 October 2021", [
        "Campaign cards size from MTS fixed (Cosmo, Black Swan and Jormungand)",
        "Fixed issues with pass shared control in multiplayer",
        "Spectrum permanent upgrade cards are now created in special Deck"
        ]),
    '0000209': ("0.0.2.09", "1 November 2021", [
        "Fixed issue where Nebula encounter cards are discarded in the player pile",
        "Victory display pile added"
        ]),
    '0000210': ("0.0.2.10", "11 November 2021", [
        "Fixed some minor issues"
        ]),
    '0000211': ("0.0.2.11", "04 December 2021", [
        "War Machine Hero pack added",
        "War Machine ENG image pack released at https://twistedsistem.wixsite.com/octgnmarvelchampions",
        "War Machine FR image pack released at https://twistedsistem.wixsite.com/octgnmarvelchampions",
        "The Hood scenario pack added",
        "The Hood ENG image pack (Low Quality) released at https://twistedsistem.wixsite.com/octgnmarvelchampions",
        "The Hood FR image pack released at https://twistedsistem.wixsite.com/octgnmarvelchampions",
        "Valkyrie Hero pack added",
        "Valkyrie ENG image pack (Low Quality) released at https://twistedsistem.wixsite.com/octgnmarvelchampions",
        "Valkyrie FR image pack released at https://twistedsistem.wixsite.com/octgnmarvelchampions"
        ]),
    '0000212': ("0.0.2.12", "07 December 2021", [
        "Improved quality for Valkyrie Hero ENG image pack",
        "Updated image pack released at https://twistedsistem.wixsite.com/octgnmarvelchampions",
        "NEW!! Option added when right-clicking on shared Special Deck to choose 1 set or at random in this deck and shuffle it in encounter deck"
        ]),
    '0000213': ("0.0.2.13", "21 January 2022", [
        "Vision Hero pack added",
        "Vision ENG image pack not released (no good image scan available)",
        "Vision FR image pack released at https://twistedsistem.wixsite.com/octgnmarvelchampions"
        ]),
    '0000214': ("0.0.2.14", "31 January 2022", [
        "The Hood ENG image pack (better quality) released at https://twistedsistem.wixsite.com/octgnmarvelchampions",
        "Vision ENG image pack released at https://twistedsistem.wixsite.com/octgnmarvelchampions",
        "Fixed issue where \"Draw Unrevealed\" displays card name in chat box",
        "Fixed issue where cards from Badoon Headhunter modular behaved as player cards",
        "Badoon Headhunter modular can be picked during the main villain setup" 
        ]),
    '0000215': ("0.0.2.15", "20 February 2022", [
        "Fixed issue where \"Viper's Ambition\" from Spider-Women Nemesis set were not displayed correctly",
        "Fixed default modular encounter setup for Crossbones"
        ])
}