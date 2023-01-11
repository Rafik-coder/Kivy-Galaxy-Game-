
from kivy.uix.relativelayout import RelativeLayout


def keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self.on_keyboard_down)
    self._keyboard.unbind(on_key_up=self.on_keyboard_up)
    self._keyboard = None

def on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] == "left" or keycode[1] == "a":
        # print("Left")
        self.current_speed_x += 2
    elif keycode[1] == "right" or keycode[1] == "d":
        # print("Right")
        self.current_speed_x -= 2

    return True

def on_keyboard_up(self, keyboard, keycode):
    self.current_speed_x = 0
    return True

def on_touch_down(self, touch):

    if not self.state_game_over and self.game_has_started:
        if touch.x < self.width / 2:
            self.current_speed_x += 2
        
        else:
            self.current_speed_x -= 2

    return super(RelativeLayout, self).on_touch_down(touch)

def on_touch_up(self, touch):
    self.current_speed_x = 0
    