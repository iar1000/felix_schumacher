class Camera():
    """keeps track of the global offset of the map"""
    def __init__(self):
        self.x = 5000
        self.y = 5000

    def update_pos(self, pos):
        self.x, self.y = pos