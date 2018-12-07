import os


class DataLoader:
    

    basePath = os.path.dirname(os.path.realpath(__file__))
    basePath = basePath[:-4]
    print(basePath)
    botDialogPath = os.path.join(basePath, "Data\\text_scene_0_bot.xml")
    playerDialogPath = os.path.join(basePath, "Data\\text_scene_0_player.xml")
    print(botDialogPath)
    print(playerDialogPath)



    def __init__(self):
        self.dialog = ""

        