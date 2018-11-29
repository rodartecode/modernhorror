class Dialog:
    partner = ""
    scene = 0
    line_id = 0
    
    def __init__(self, newPartner, newScene, newLineId):
        self.partner = newPartner
        self.scene = newScene
        self.line_id = newLineId

    