"""Font for numbers"""
from gfxlcd_fonts.numbers import Numbers as Base


class Numbers(Base):
    """Digital font class"""
    def __init__(self):
        self.resource = self.get_resource("numbers_12x25.png")
        self.offsets = {
            0: 0,
            1: 14,
            2: 28,
            3: 42,
            4: 56,
            5: 70,
            6: 84,
            7: 98,
            8: 112,
            9: 126
        }
        self.loaded_resources = {}
        self.size = {'width': 13, 'height': 26}
        self.transparency = ((1, 1, 1), (0, 0, 0))
