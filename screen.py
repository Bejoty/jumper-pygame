''' A wrapper for constants related to the game screen '''

import constants as c


class Screen():
    def __init__(self):
        self.width = c.SCREEN_WIDTH
        self.height = c.SCREEN_HEIGHT
        self.dimensions = (self.width, self.height)

        self.caption = c.SCREEN_CAPTION
