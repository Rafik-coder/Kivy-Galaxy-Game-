
from kivy.config import Config

Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')


from kivy import platform
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line, Quad, Triangle
from kivy.properties import Clock
from kivy.core.window import Window
import random
from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder

Builder.load_file("menu.kv")

class MainWidget(RelativeLayout):
    from transforms import transform_2D, transform_perspective, transfrom
    from user_actions import keyboard_closed, on_keyboard_down, on_keyboard_up, on_touch_down, on_touch_up
    perspective_point_x = NumericProperty(0)
    perspective_point_y= NumericProperty(0)
    menu_widget = ObjectProperty()
    game_state = StringProperty()
    action_button = StringProperty()
    score = StringProperty()
    
    v_num_lines = 15
    v_lines_spacing = .35
    v_lines = []

    h_num_lines = 15
    h_lines_spacing = .15
    h_lines = []

    SPEED = .7
    current_offset_y = 0
    current_y_loop = 0

    SPEED_X = 3.0
    current_offset_x = 0

    current_speed_x = 0

    tiles = []
    num_tiles = 8
    tiles_cordinates = []

    ship = None
    ship_width = .1
    ship_height = 0.06
    ship_base_y = 0.04
    ship_cords = [(0, 0), (0, 0), (0, 0), (0, 0)]

    # start_game = False

    state_game_over = False
    game_has_started = False


    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.initvertical_lines()
        self.horizontal_lines()
        self.init_tiles()
        self.init_ship()
        self.reset_game()
        self.game_state = "G   A   L   A   Z   Y"
        self.action_button = "START"

        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1/60)

    def is_desktop(self):
        if platform in ("linux", "win", "macosx"):
            return True

        else:
            return False

    def init_ship(self):
        with self.canvas:
            # Color(0, 0, 0)
            self.ship = Quad(source="./galary/car2.png")

    def update_ship(self):
        center_x = self.width / 2
        base_y = self.ship_base_y * self.height
        ship_half_width = self.ship_width * center_x
        ship_height = self.ship_height * self.height

        self.ship_cords[0] = (center_x - ship_half_width, base_y)
        self.ship_cords[1] = (center_x - ship_half_width, base_y + ship_height)
        self.ship_cords[2] = (center_x + ship_half_width, base_y + ship_height)
        self.ship_cords[3] = (center_x + ship_half_width, base_y)


        x1, y1 = self.transfrom(*self.ship_cords[0])
        x2, y2 = self.transfrom(*self.ship_cords[1])
        x3, y3 = self.transfrom(*self.ship_cords[2])
        x4, y4 = self.transfrom(*self.ship_cords[3])

        self.ship.points = [x1, y1, x2, y2, x3, y3, x4, y4]


    def check_ship_collision(self):
        for i in range(0, len(self.tiles_cordinates)):
            tile_x, tile_y = self.tiles_cordinates[i]

            if tile_y > self.current_y_loop + 1:
                return False

            if self.check_ship_collision_with_tiles(tile_x, tile_y):
                return True
        
        return False

    def check_ship_collision_with_tiles(self, tile_x, tile_y):
        xmin, ymin = self.get_tile_cordinates(tile_x, tile_y)
        xmax, ymax = self.get_tile_cordinates(tile_x + 1, tile_y + 1)

        for i in range(0, 3):
            px, py = self.ship_cords[i]

            if xmin <= px <= xmax and ymin <= py <= ymax:
                return True

        return False

    
    def init_tiles(self):
        with self.canvas:

            Color(1, 1, 1)
            for i in range(0, self.num_tiles):
                self.tiles.append(Quad(source="./galary/cop.jpeg"))

    def pre_fill_tiles_cords(self):
        f_tiles = 10

        for i in range(0, f_tiles):
            self.tiles_cordinates.append((0, i))

    def generate_tiles_cordinates(self):
        last_y = 0
        last_x = 0

        for i in range(len(self.tiles_cordinates) - 1, -1, -1):
            if self.tiles_cordinates[i][1] < self.current_y_loop:
                del self.tiles_cordinates[i]
        
        # print("hey 1")

        if len(self.tiles_cordinates) > 0:
            last_cords = self.tiles_cordinates[-1]
            last_x = last_cords[0]
            last_y = last_cords[1] + 1

        for i in range(len(self.tiles_cordinates), self.num_tiles):

            start_index = -int(self.v_num_lines / 2) + 1
            end_index = start_index + self.v_num_lines - 2

            r = random.randint(0, 2)

            if last_x <= start_index:
                r = 1

            if last_x >= end_index:
                r = 2
            
            self.tiles_cordinates.append((last_x, last_y))

            if (r == 1):
                last_x += 1
                self.tiles_cordinates.append((last_x, last_y))

                last_y += 1
                self.tiles_cordinates.append((last_x, last_y))

            if (r == 2):
                last_x -= 1
                self.tiles_cordinates.append((last_x, last_y))

                last_y += 1
                self.tiles_cordinates.append((last_x, last_y))


            last_y += 1

        # print("hey 2")

    def update_tiles(self):
        for i in range(0, self.num_tiles):
            tile = self.tiles[i]
            tile_cords = self.tiles_cordinates[i]
            xmin, ymin = self.get_tile_cordinates(tile_cords[0], tile_cords[1])
            xmax, ymax = self.get_tile_cordinates(tile_cords[0] + 1, tile_cords[1] + 1)
            
            x1, y1 = self.transfrom(xmin, ymin)
            x2, y2 = self.transfrom(xmin, ymax)
            x3, y3 = self.transfrom(xmax, ymax)
            x4, y4 = self.transfrom(xmax, ymin)

            tile.points = [x1, y1, x2, y2, x3, y3, x4, y4]


    def initvertical_lines(self):
        with self.canvas:

            Color(1, 1, 1, 0)
            for l in range(0, self.v_num_lines):
                self.v_lines.append(Line())

    def get_line_x_from_index(self, index):
        center_line_x = self.perspective_point_x
        spacing = self.v_lines_spacing * self.width
        offset = index - 0.5
        line_x = center_line_x + offset * spacing + self.current_offset_x

        return line_x

    def get_line_y_from_index(self, index):
        spacing_y = self.h_lines_spacing * self.height
        
        line_y = index * spacing_y - self.current_offset_y

        return line_y

    def get_tile_cordinates(self, tile_index_x, tile_index_y):
        tile_index_y = tile_index_y - self.current_y_loop
        x = self.get_line_x_from_index(tile_index_x)
        y = self.get_line_y_from_index(tile_index_y)

        return x, y
        

    def update_vertical_lines(self):
        start_index = -int(self.v_num_lines / 2) + 1
        for i in range(start_index, start_index + self.v_num_lines):
            line_x = self.get_line_x_from_index(i)

            x1, y1 = self.transfrom(line_x, 0)
            x2, y2 = self.transfrom(line_x, self.height)

            self.v_lines[i].points = [x1, y1, x2, y2]

    def horizontal_lines(self):
        with self.canvas:

            Color(1, 1, 1, 0)
            for l in range(0, self.h_num_lines):
                self.h_lines.append(Line())

    def update_horizontal_lines(self):
        # center_line_x = int(self.width / 2)
        # spacing = self.v_lines_spacing * self.width
        # offset = -int(self.v_num_lines / 2) + 0.5

        # xmin = center_line_x + offset * spacing + self.current_offset_x
        # xmax = center_line_x - offset * spacing + self.current_offset_x

        start_index = -int(self.v_num_lines / 2) + 1
        end_index = start_index + self.v_num_lines -1

        xmin = self.get_line_x_from_index(start_index)
        xmax = self.get_line_x_from_index(end_index)

        for i in range(0, self.h_num_lines):
            line_y = self.get_line_y_from_index(i)

            x1, y1 = self.transfrom(xmin, line_y)
            x2, y2 = self.transfrom(xmax, line_y)

            self.h_lines[i].points = [x1, y1, x2, y2]

    def reset_game(self):
        self.current_offset_y = 0
        self.current_offset_x = 0
        self.current_speed_x = 0
        self.current_y_loop = 0

        self.tiles_cordinates = []
        self.pre_fill_tiles_cords()
        self.generate_tiles_cordinates()

        self.score = "Score: " +  str(self.current_y_loop)

        self.state_game_over = False

    def start_game(self):
        print("started")
        self.reset_game()
        self.game_has_started = True
        self.menu_widget.opacity = 0

    def update(self, dt):
        # print("dt:" + str(dt))

        self.update_tiles()
        self.update_ship()
        self.update_vertical_lines()
        self.update_horizontal_lines()

        time_factor = dt * 60
        # print(time_factor)

        if not self.state_game_over and self.game_has_started:
            speed_y = self.SPEED * self.height / 100
            speed_x = self.current_speed_x * self.width / 100

            self.current_offset_y += speed_y * time_factor
            self.current_offset_x += time_factor * speed_x

            spacing_y = self.h_lines_spacing * self.height
            spacing_x = self.v_lines_spacing * self.width

            while self.current_offset_y >= spacing_y:
                self.current_offset_y -= spacing_y
                self.current_y_loop += 1
                self.generate_tiles_cordinates()
                self.score = "Score: " +  str(self.current_y_loop)
                self.SPEED += 0.003

        if not self.check_ship_collision() and not self.state_game_over:
            self.state_game_over = True
            self.game_state = "G  A  M  E    O  V  E  R"
            self.action_button = "TRY AGAIN"
            self.menu_widget.opacity = 1


        # if self.current_offset_x >= spacing_x:
        #     self.current_offset_x -= spacing_x


    # def on_size(self, *args):
    #     # self.update_vertical_lines()
    #     # self.update_horizontal_lines()
    #     pass
    
    # def on_parent(self, widget, parent):
    #     print("Parent:" + str(self.width) + "," + str(self.height))

    # def on_perspective_point_x(self, widget, value):
    #     # print("Pers_x:" + str(value))
    #     pass

    # def on_perspective_point_y(self, widget, value):
    #     # print("Pers_y:" + str(value))
    #     pass
        

class GalaxyApp(App):
    # def build(self):
    #     return super().build()
    pass


if __name__ == "__main__":
    app = GalaxyApp()
    app.run()
