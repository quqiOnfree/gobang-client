class BaceGame:
    def __init__(self,*arc,**kwargs) -> None:
        self.has_exit = False

    def on_draw(self):
        pass

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        pass

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        pass

    def on_update(self, delta_time: float):
        pass

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        pass

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        pass