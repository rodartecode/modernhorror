import os
import xml.etree.ElementTree as et


class DataLoader:
    
    # Some witchcraft to hardcode in the xml file paths
    # This file is gonna be full of repeating code
    # So this should be refactored into a few methods
    # and loops to automatically load all the files

    # For now, its hardcoded ~jr

    _basePath = os.path.dirname(os.path.realpath(__file__))
    _basePath = _basePath[:-4]
    #print(_basePath)
    _botDialogPath = os.path.join(_basePath, "Data\\text_scene_0_bot.xml")
    _botDialogPath1 = os.path.join(_basePath, "Data\\text_scene_1_bot.xml")
    _playerDialogPath = os.path.join(_basePath, "Data\\text_scene_0_player.xml")
    _playerDialogPath1 = os.path.join(_basePath, "Data\\text_scene_1_player.xml")
    #print(_botDialogPath)
    #print(_playerDialogPath)



    def __init__(self):
        self.playerDialog = []
        self.botDialog = []

    # returns an array of strings that represent every line
    # in the player xml file
    def setupPlayer(self):
        
        # initialize an Element Tree
        playerTree = et.parse(DataLoader._playerDialogPath)
        # get the root of the Element Tree
        playerRoot = playerTree.getroot()

        # Load all the "option" objects from the xml file
        playerDialog = playerRoot.findall(f"./scene/line/option")
        # Array to hold the strings
        playerText = []

        # Get all the strings and add them to playerText
        for elem in playerDialog:
            playerText.append(elem.text)

        # This is just to test that we got some lines in the array
        for elem in playerText:
            pass
            print(elem)

        # Return the array
        return playerText
        

    def setupPlayer2(self):
        
        # initialize an Element Tree
        playerTree = et.parse(DataLoader._playerDialogPath1)
        # get the root of the Element Tree
        playerRoot = playerTree.getroot()

        # Load all the "option" objects from the xml file
        playerDialog = playerRoot.findall(f"./scene/line/option")
        # Array to hold the strings
        playerText = []

        # Get all the strings and add them to playerText
        for elem in playerDialog:
            playerText.append(elem.text)

        # This is just to test that we got some lines in the array
        for elem in playerText:
            pass
            print(elem)

        # Return the array
        return playerText

    # same as setupPlayer but it loads the bot file
    def setupBot(self):
        botTree = et.parse(DataLoader._botDialogPath)
        botRoot = botTree.getroot()

        botDialog = botRoot.findall(f"./scene/line/option")
        botText = []

        for elem in botDialog:
            botText.append(elem.text)

        for elem in botText:
            pass
            print(elem)

        return botText

    def setupBot2(self):
        botTree = et.parse(DataLoader._botDialogPath1)
        botRoot = botTree.getroot()

        botDialog = botRoot.findall(f"./scene/line/option")
        botText = []

        for elem in botDialog:
            botText.append(elem.text)

        for elem in botText:
            pass
            print(elem)

        return botText

        
        