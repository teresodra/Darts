# I don't know what should go here, this is just a suggestion by chatgpt


from flask import Flask, request, render_template
import numpy as np
from players import Player
from strategies import GameStrategy
from constants import positions

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def run_this_fast():
    if request.method == 'POST':
        starting_points = int(request.form.get("starting_points", 40))
        n_turns = int(request.form.get("n_turns", 3))
        skill = int(request.form.get("skill", 200))
        mode = request.form.get("mode", 'optimal')

        player = Player(create_distribution=True)
        game_strategy = GameStrategy(player, n_turns=n_turns, max_points=starting_points, mode=mode)
        best_strategy_stored = game_strategy.strategy

        return render_template('results.html', strategy=best_strategy_stored, points=starting_points, turns=n_turns)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
