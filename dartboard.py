from kivy.core.window import Window
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Point
from kivy.uix.label import Label
from math import pi, sin, cos
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView

from constants import positions, radiuses
from players import Player
from strategies import GameStrategy

# Open window maximized
Window.maximize()

font_size = 34


class Dartboard(Widget):
    def __init__(self, **kwargs):
        super(Dartboard, self).__init__(**kwargs)
        self.last_point = None

        # Define colors
        black = (0, 0, 0)
        white = (1, 1, 1)
        green = (0, 0.5, 0)

        # Use explicit center based on widget size/position
        center_x = self.x + self.width / 2
        center_y = self.y + self.height / 2

        self.my_mm = self.width * 0.5 / radiuses[5]
        radii = [radius * self.my_mm for radius in radiuses[5::-1]]

        with self.canvas:
            # Draw circles
            for i, r in enumerate(radii):
                Color(*(green if i % 2 == 0 else white))
                Ellipse(pos=(center_x - r, center_y - r), size=(r * 2, r * 2))

            # Draw radial section lines
            for angle in range(0, 360, 18):
                start_angle = 18 * pi / 360 + 2 * angle * pi / 360
                Color(*black)
                Line(
                    points=[
                        center_x + radii[0] * cos(start_angle),
                        center_y + radii[0] * sin(start_angle),
                        center_x + radii[4] * cos(start_angle),
                        center_y + radii[4] * sin(start_angle),
                    ],
                    width=1.5,
                )

        # Add numbers around the dartboard
        for i, number in enumerate(positions):
            angle = i * 36 * pi / 360
            r = self.width * 0.55

            label = Label(
                text=str(number),
                size_hint=(None, None),
                size=(50, 50),
                font_size=font_size * 1.2,
            )
            label.pos = (
                center_x + r * cos(angle) - label.width * 0.5,
                center_y + r * sin(angle) - label.height * 0.5,
            )
            self.add_widget(label)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            App.get_running_app().handle_click(touch.pos)
            return True
        return super(Dartboard, self).on_touch_down(touch)

    def draw_point(self, position):
        """Draws a point at the given position on the dartboard."""
        if self.last_point:
            self.canvas.remove(self.last_point)

        with self.canvas:
            Color(1, 0, 0)
            self.last_point = Point(points=[position[0], position[1]], pointsize=8)


class DartboardApp(App):
    def build(self):
        self.layout = FloatLayout()

        # Labels for stats
        self.turns_left_label = Label(
            size_hint=(0.3, 0.1),
            pos_hint={"right": 0.75, "top": 0.92},
            font_size=font_size,
        )
        self.layout.add_widget(self.turns_left_label)

        self.darts_left_label = Label(
            size_hint=(0.3, 0.1),
            pos_hint={"right": 0.75, "top": 0.84},
            font_size=font_size,
        )
        self.layout.add_widget(self.darts_left_label)

        self.points_left_label = Label(
            size_hint=(0.3, 0.1),
            pos_hint={"right": 0.75, "top": 0.76},
            font_size=font_size,
        )
        self.layout.add_widget(self.points_left_label)

        self.probability_label = Label(
            size_hint=(0.3, 0.1),
            pos_hint={"right": 0.75, "top": 0.68},
            font_size=font_size,
        )
        self.layout.add_widget(self.probability_label)

        # Scrollable input section
        self.scroll_view = ScrollView(
            size_hint=(0.3, 0.4),
            pos_hint={"right": 1, "top": 1},
        )

        self.input_layout = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=10,
            padding=10,
        )
        self.input_layout.bind(minimum_height=self.input_layout.setter("height"))
        self.scroll_view.add_widget(self.input_layout)

        self.starting_points_label, self.starting_points_input = self.add_label_and_input("Starting Points:")
        self.n_turns_label, self.n_turns_input = self.add_label_and_input("No. of Turns:")
        self.skill_label, self.skill_input = self.add_label_and_input("Skill Level:")

        btn = Button(
            text="Submit",
            size_hint_y=None,
            height=60,
            font_size=font_size,
        )
        btn.bind(on_press=self.initialize_dartboard)
        self.input_layout.add_widget(btn)

        self.layout.add_widget(self.scroll_view)
        return self.layout

    def add_label_and_input(self, text):
        """Utility function to add a Label and TextInput widget."""
        label = Label(
            text=text,
            size_hint_y=None,
            height=60,
            font_size=font_size,
        )
        self.input_layout.add_widget(label)

        text_input = TextInput(
            multiline=False,
            size_hint_y=None,
            height=60,
            font_size=font_size,
        )
        self.input_layout.add_widget(text_input)

        return label, text_input

    def initialize_dartboard(self, instance):
        try:
            self.points_left = int(self.starting_points_input.text)
            self.points_previous_turn = self.points_left
            self.turns_left = int(self.n_turns_input.text) - 1
            self.darts_left = 3
            self.points_scored = 0

            self.skill = float(self.skill_input.text)

            self.player = Player(skill=self.skill)
            self.strategy = GameStrategy(
                player=self.player,
                n_turns=self.turns_left,
                max_points=self.points_left,
            ).generating_strategy()

            self.game()
            self.update_stats()

        except ValueError:
            label = Label(
                text="Please enter valid values!",
                font_size=font_size,
                size_hint=(0.5, 0.1),
                pos_hint={"center_x": 0.5, "center_y": 0.5},
            )
            self.layout.add_widget(label)

    def display_dartboard_with_aiming_point(self):
        # Remove old dartboard
        if hasattr(self, "dartboard"):
            self.layout.remove_widget(self.dartboard)

        # Remove old input UI
        if hasattr(self, "scroll_view"):
            self.layout.remove_widget(self.scroll_view)

        if hasattr(self, "input_layout"):
            self.layout.remove_widget(self.input_layout)

        # Create dartboard
        self.dartboard = Dartboard(size=(1100, 1100), pos=(100, 100))
        self.layout.add_widget(self.dartboard)

        # Draw aiming point
        with self.dartboard.canvas:
            Color(1, 0, 0)
            self.coordinates
            Point(
                points=[
                    self.dartboard.center_x + self.coordinates[0] * self.dartboard.my_mm,
                    self.dartboard.center_y + self.coordinates[1] * self.dartboard.my_mm,
                ],
                pointsize=8,
            )

        # Score input on the right
        self.input_layout = BoxLayout(
            orientation="vertical",
            size_hint=(0.3, 0.25),
            pos_hint={"right": 1, "top": 1},
            spacing=10,
            padding=10,
        )

        self.score_input = self.add_label_and_input("Enter points scored:")[1]

        score_btn = Button(
            text="Submit Score",
            font_size=font_size,
            size_hint_y=None,
            height=60,
        )
        score_btn.bind(on_press=self.update_game)
        self.input_layout.add_widget(score_btn)

        self.layout.add_widget(self.input_layout)

    def game(self, what=""):
        if self.points_left != 0:
            if self.darts_left == 0:
                if self.turns_left == 0:
                    self.layout.clear_widgets()
                    over_label = Label(text="You lost!", font_size=font_size * 1.5)
                    self.layout.add_widget(over_label)
                    return
                else:
                    self.points_previous_turn = self.points_left
                    self.turns_left -= 1
                    self.darts_left = 3

            turn_key = (self.turns_left, self.darts_left)
            state_info = self.strategy.get(turn_key, {}).get(self.points_left)

            if state_info is None or state_info.get("coordinates") is None:
                Window.close()
                raise RuntimeError("Impossible to finish the game from this position.")

            self.coordinates = state_info["coordinates"]
            self.probability = state_info.get("probability", 0)

            self.display_dartboard_with_aiming_point()

        else:
            self.layout.clear_widgets()
            win_label = Label(text="Congratulations! You've won!", font_size=font_size * 1.5)
            self.layout.add_widget(win_label)

    def update_game(self, instance):
        try:
            self.points_scored = int(self.score_input.text)
        except ValueError:
            error_label = Label(
                text="Please enter a valid score!",
                font_size=font_size,
                size_hint=(0.5, 0.1),
                pos_hint={"center_x": 0.5, "center_y": 0.08},
            )
            self.layout.add_widget(error_label)
            return

        if self.points_left - self.points_scored == 0:
            self.layout.clear_widgets()
            win_label = Label(
                text="Congratulations! You've won!",
                font_size=font_size * 1.5,
            )
            self.layout.add_widget(win_label)
            return
        else:
            self.darts_left -= 1
            if self.points_left - self.points_scored <= 1:
                self.points_left = self.points_previous_turn
                self.darts_left = 0
            else:
                self.points_left -= self.points_scored

            self.game()
            self.update_stats()

    def update_stats(self):
        self.turns_left_label.text = f"Turns Left: {self.turns_left}"
        self.darts_left_label.text = f"Darts Left: {self.darts_left}"
        self.points_left_label.text = f"Points Left: {self.points_left}"
        self.probability_label.text = (
            f"You will finish with probability: {round(self.probability, 2)}"
        )

    def handle_click(self, position):
        """Handle the user click on the dartboard."""
        self.clicked_position = position

        if hasattr(self, "dartboard"):
            self.dartboard.draw_point(self.clicked_position)


if __name__ == "__main__":
    DartboardApp().run()