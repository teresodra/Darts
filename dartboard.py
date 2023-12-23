# from kivy.app import App
# from kivy.uix.widget import Widget
# from kivy.graphics import Color, Ellipse, Line, Point
# from kivy.uix.popup import Popup
# from kivy.uix.label import Label
# from math import pi, sin, cos
# from kivy.uix.button import Button
# from kivy.uix.label import Label
# from kivy.uix.textinput import TextInput
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.floatlayout import FloatLayout  # Import the FloatLayout
# from constants import positions, radiuses
# from players import Player
# from strategies import GameStrategy


# class Dartboard(Widget):
#     def __init__(self,  **kwargs):
#         super(Dartboard, self).__init__(**kwargs)
#         self.last_point = None
        
#         # Define colors
#         black = (0, 0, 0)
#         white = (1, 1, 1)
#         green = (0, 0.5, 0)
#         red = (1, 0, 0)
        
#         # Define some parameters
#         center_x = self.center_x
#         center_y = self.center_y
#         self.my_mm = self.width * 0.5 / radiuses[5]
#         radii = [radius * self.my_mm for radius in radiuses[5::-1]]
        
#         with self.canvas:
#             # Draw the circles
#             for i, r in enumerate(radii):
#                 # Alternate between white and black for the main sections
#                 Color(*green if i % 2 == 0 else white)
#                 Ellipse(pos=(center_x - r, center_y - r), size=(r*2, r*2))
            
#             # Draw the colored sections (double and triple score areas)
#             for angle in range(0, 360, 18):  # 20 sections, 360/20 = 18 degrees per section
#                 start_angle = 18 * pi / 360 + 2* angle * pi / 360
#                 Color(*black)
#                 Line(points=[center_x  + radii[0] * cos(start_angle),
#                              center_y  + radii[0] * sin(start_angle),
#                              center_x + radii[4] * cos(start_angle),
#                              center_y + radii[4] * sin(start_angle)], width=1.5)
#                     # Line(points=[center_x, center_y, center_x + r * cos(stop_angle), center_y + r * sin(stop_angle)], width=1.5)
                    
#         # Add the numbers
#         for i, number in enumerate(positions):
#             angle = i * 36 * pi / 360  # center the number in the middle of the section
#             r = self.width * 0.55  # position outside the dartboard
#             label = Label(text=str(number), size_hint=(None, None), font_size=20)
#             label.pos = (center_x + r * cos(angle) - label.width * 0.5,
#                          center_y + r * sin(angle) - label.height * 0.5)
#             self.add_widget(label)

#     def on_touch_down(self, touch):
#         if self.collide_point(*touch.pos):
#             App.get_running_app().handle_click(touch.pos)
#             return True
#         return super(Dartboard, self).on_touch_down(touch)

#     def draw_point(self, position):
#         """Draws a point at the given position on the dartboard."""
        
#         # If a point was drawn before, remove it
#         if self.last_point:
#             self.canvas.remove(self.last_point)

#         with self.canvas:
#             Color(1, 0, 0)  # Red color, you can change as per your preference
#             self.last_point = Point(points=[position[0], position[1]], pointsize=5)




# class DartboardApp(App):

#     def build(self):
#         # Change this to FloatLayout
#         self.layout = FloatLayout(size=(600, 600))

#         # Labels to display turns, darts, and points left
#         self.turns_left_label = Label(size_hint=(0.3, 0.1), pos_hint={'left': 1, 'top': 0.9})
#         self.layout.add_widget(self.turns_left_label)

#         self.darts_left_label = Label(size_hint=(0.3, 0.1), pos_hint={'left': 1, 'top': 0.8})
#         self.layout.add_widget(self.darts_left_label)

#         self.points_left_label = Label(size_hint=(0.3, 0.1), pos_hint={'left': 1, 'top': 0.7})
#         self.layout.add_widget(self.points_left_label)

#         self.probability_label = Label(size_hint=(0.3, 0.1), pos_hint={'left': 1, 'top': 0.6})
#         self.layout.add_widget(self.probability_label)


#         # Modify the layout for input boxes and move them to top right
#         self.input_layout = BoxLayout(orientation="vertical", size_hint=(0.3, 0.3), pos_hint={'right': 1, 'top': 1})
#         self.layout.add_widget(self.input_layout)

#         # Add labels and TextInput widgets for the required initial values
#         self.starting_points_label, self.starting_points_input = self.add_label_and_input("Starting Points:")
#         self.n_turns_label, self.n_turns_input = self.add_label_and_input("No. of Turns:")
#         self.skill_label, self.skill_input = self.add_label_and_input("Skill Level:")

#         # Button to process the entered values and display dartboard
#         btn = Button(text="Submit", size_hint_y=None, height=44)
#         btn.bind(on_press=self.initialize_dartboard)
#         self.input_layout.add_widget(btn)

#         return self.layout

#     def add_label_and_input(self, text):
#         """Utility function to add a Label and TextInput widget."""
#         label = Label(text=text, size_hint_y=None, height=44)
#         self.input_layout.add_widget(label)
#         text_input = TextInput(multiline=False, size_hint_y=None, height=44)
#         self.input_layout.add_widget(text_input)
#         return label, text_input  # Return both label and text input.

#     def initialize_dartboard(self, instance):
#         try:
#             self.points_left = int(self.starting_points_input.text)
#             self.points_previous_turn = self.points_left
#             self.turns_left = int(self.n_turns_input.text)-1
#             self.darts_left = 3
#             self.points_scored = 0

#             self.skill = int(self.skill_input.text)
#             print('self.skill', self.skill, type(self.skill))
#             # Placeholder for Player and GameStrategy classes. 
#             # Uncomment and replace these lines with actual classes as per your setup.
#             self.player = Player(sigma=((self.skill^2, 0), (0, self.skill^2)))
#             self.strategy = GameStrategy(player=self.player, n_turns=self.turns_left, max_points=self.points_left).generating_strategy()
#             self.game()
#             self.update_stats()  # <-- Add this line here
#         except ValueError:
#             label = Label(text="Please enter valid values!")
#             self.layout.add_widget(label)

#     def display_dartboard_with_aiming_point(self):
#         print(self.coordinates)

#         # Remove existing dartboard and input layout if they exist
#         if hasattr(self, 'dartboard'):
#             self.layout.remove_widget(self.dartboard)

#         if hasattr(self, 'input_layout'):
#             self.layout.remove_widget(self.input_layout)

#         # Create or recreate the dartboard and add to layout
#         self.dartboard = Dartboard(size=(500, 500), pos=(50, 50))
#         self.layout.add_widget(self.dartboard)

#         # Add a center point to the Dartboard's canvas
#         with self.dartboard.canvas:
#             Color(1, 0, 0)
#             self.coordinates
#             self.dartboard
#             self.dartboard.my_mm
#             print(self.coordinates)
#             Point(points=[self.dartboard.center_x + (self.coordinates[0] * cos(self.coordinates[1]))*self.dartboard.my_mm,
#                           self.dartboard.center_y + (self.coordinates[0] * sin(self.coordinates[1]))*self.dartboard.my_mm],
#                   pointsize=5)

#         # Create a VBox layout for score input and button
#         self.input_layout = BoxLayout(orientation="vertical", size_hint=(0.3, 0.2), pos_hint={'right': 1, 'top': 1})
#         self.score_input = self.add_label_and_input("Enter points scored:")[1]
#         score_btn = Button(text="Submit Score")
#         score_btn.bind(on_press=self.update_game)
#         self.input_layout.add_widget(score_btn)
#         self.layout.add_widget(self.input_layout)
    

#     def game(self, what = ''):
#         # self.update_stats()
#         print('WHAT', what)
#         print('self.points_left', self.points_left)
#         if self.points_left != 0:
#             if self.darts_left == 0:
#                 if self.turns_left == 0:
#                     # Player lost
#                     self.layout.clear_widgets()
#                     over_label = Label(text="You lost!")
#                     self.layout.add_widget(over_label)
#                     print("PLAYER LOST")
#                     return  # End the game method here
#                 else:
#                     self.points_previous_turn = self.points_left
#                     self.turns_left -= 1
#                     self.darts_left = 3
#             print(list(self.strategy.keys()))

#             self.coordinates = self.strategy[(self.turns_left, self.darts_left)][self.points_left]['coordinates']
#             self.probability = self.strategy[(self.turns_left, self.darts_left)][self.points_left]['probability']
#             print(list(self.strategy.keys())[0])
#             print(list(self.strategy[list(self.strategy.keys())[0]].keys()))
#             print(self.strategy[(2,2)])
#             self.display_dartboard_with_aiming_point()

#         else:
#             # Player has won
#             self.layout.clear_widgets()
#             win_label = Label(text="Congratulations! You've won!")
#             self.layout.add_widget(win_label)

#     def update_game(self, instance):
#         try:
#             self.points_scored = int(self.score_input.text)
#         except ValueError:
#             error_label = Label(text="Please enter a valid score!")
#             self.layout.add_widget(error_label)
#             return

#         if self.points_left - self.points_scored == 0:
#             # Player has won
#             self.layout.clear_widgets()
#             win_label = Label(text="Congratulations! You've won!")
#             self.layout.add_widget(win_label)
#             return
#         else:
#             self.darts_left -= 1
#             print("self.points_left - self.points_scored", self.points_left, self.points_scored)
#             if self.points_left - self.points_scored <= 1:
#                 self.points_left = self.points_previous_turn
#                 self.darts_left = 0
#             else:
#                 self.points_left -= self.points_scored
#             self.game()  # Continue the game
#             self.update_stats()  # <-- Add this line here

#     def update_stats(self):
#         self.turns_left_label.text = f"Turns Left: {self.turns_left}"
#         self.darts_left_label.text = f"Darts Left: {self.darts_left}"
#         self.points_left_label.text = f"Points Left: {self.points_left}"
#         self.probability_label.text = f"You will finish with probability: {round(self.probability,2)}"



#     def handle_click(self, position):
#         """Handle the user click on the dartboard."""
#         self.clicked_position = position
#         print('position', self.clicked_position)

#         if hasattr(self, 'dartboard'):
#             self.dartboard.draw_point(self.clicked_position)

# if __name__ == '__main__':
#     DartboardApp().run()
