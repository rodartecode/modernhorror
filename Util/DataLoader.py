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

        playerDialog = playerRoot.findall(f"./Scene[@id='0']/Line[@id='0']/line")



    def setupBot(self):
        pass



        