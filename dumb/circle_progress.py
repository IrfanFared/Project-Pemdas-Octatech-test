from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty
from kivy.graphics import Color, Line


class CircleProgress(Widget):
    value = NumericProperty(0)
    max = NumericProperty(100)
    thickness = NumericProperty(12)
    color = ListProperty([0.56, 0.35, 0.86, 1])
    bg_color = ListProperty([0.9, 0.9, 0.9, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update_canvas, size=self.update_canvas, value=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.clear()

        if not self.width or not self.height:
            return

        radius = min(self.width, self.height) / 2 - self.thickness / 2

        angle = (self.value / self.max) * 360

        with self.canvas:
            # Background ring
            Color(*self.bg_color)
            Line(circle=(self.center_x, self.center_y, radius, 0, 360), width=self.thickness)

            # Foreground progress
            Color(*self.color)
            Line(circle=(self.center_x, self.center_y, radius, -90, -90 + angle),
                 width=self.thickness, cap='round')
