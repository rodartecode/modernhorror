import os
import xml.etree.ElementTree as et


class DataLoader:
    

    _basePath = os.path.dirname(os.path.realpath(__file__))
    _basePath = _basePath[:-4]
    print(_basePath)
    _botDialogPath = os.path.join(_basePath, "Data\\text_scene_0_bot.xml")
    _playerDialogPath = os.path.join(_basePath, "Data\\text_scene_0_player.xml")
    print(_botDialogPath)
    print(_playerDialogPath)



    def __init__(self):
        self.playerDialog = []
        self.botDialog = []

    def setupPlayer(self):
        playerTree = et.parse(DataLoader._playerDialogPath)
        playerRoot = playerTree.getroot()

        playerDialog = playerRoot.findall(f"./scene/line/option")
        playerText = []

        for elem in playerDialog:
            playerText.append(elem.text)

        for elem in playerText:
            print(elem)

        return playerText


    def setupBot(self):
        botTree = et.parse(DataLoader._botDialogPath)
        botRoot = botTree.getroot()

        botDialog = botRoot.findall(f"./scene/line/option")
        botText = []

        for elem in botDialog:
            botText.append(elem.text)

        for elem in botText:
            print(elem)

        return botText

Loader = DataLoader()
Loader.setupPlayer()
Loader.setupBot()

        