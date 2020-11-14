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
        ])
}
