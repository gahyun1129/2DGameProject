from pico2d import load_image, load_font
import server
import object.base as base


class MiniMapUI:
    one_base_image = None
    two_base_image = None
    three_base_image = None
    home_image = None

    def __init__(self):
        if MiniMapUI.one_base_image is None:
            MiniMapUI.one_base_image = load_image('resource/image/minimap_tile.png')
            MiniMapUI.two_base_image = load_image('resource/image/minimap_tile.png')
            MiniMapUI.three_base_image = load_image('resource/image/minimap_tile.png')
            MiniMapUI.home_image = load_image('resource/image/minimap_tile.png')

    def update(self):
        pass

    def draw(self):
        self.one_base_image.clip_draw(base.number_to_bases[base.one_base].has_runner * 40, 0, 40, 40, 755, 475)
        self.two_base_image.clip_draw(base.number_to_bases[base.two_base].has_runner * 40, 0, 40, 40, 730, 500)
        self.three_base_image.clip_draw(base.number_to_bases[base.three_base].has_runner * 40, 0, 40, 40, 705, 475)
        self.home_image.clip_draw(0, 0, 40, 40, 730, 450)
