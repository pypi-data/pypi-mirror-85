import numpy as np
from fury import actor, window, ui


def build_label(text):
    label = ui.TextBlock2D()
    label.message = text
    label.font_size = 18
    label.font_family = 'Arial'
    label.justification = 'left'
    label.bold = False
    label.italic = False
    label.shadow = False
    label.background = (0, 0, 0)
    label.color = (1, 1, 1)

    return label


class Viewer():
    def __init__(self, title='Pymaid Viewer'):
        self.scene = window.Scene()

        self.show_m = window.ShowManager(scene,
                                         title=title,
                                         size=(1200, 900))

        # Keep track of current size
        self._old_size = self.size

    def add(self, actor):
        self.scene.add(actor)

    def _make_panel(self):
        pass

    @property
    def size(self):
        return self.scene.GetSize()

    def win_callback(self, _event):
        if self._old_size != self.size:
            size_change = [self.size[0] - self._old_size[0],
                           self.size[1] - self._old_size[1]]
            self._old_size = self.size
            self.panel.re_align(size_change)


lines = [np.array([[0,0,0],
                   [1,1,1],
                   [1,1,2]])]

stream_actor = actor.line(lines)

scene.add(stream_actor)

panel = ui.Panel2D(size=(300, 200),
                   color=(1, 1, 1),
                   opacity=0.1,
                   align="right")
panel.center = (1030, 120)

cb = ui.Checkbox(['test1', 'test2'])

show_m.scene.add(panel)

global size
size = scene.GetSize()

show_m.add_window_callback(win_callback)

show_m.initialize()
