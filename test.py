from next_move import next_move



win, points_left, last_turn_points, turn, darts_left, best_coordinates, best_probability = \
    next_move(player_name='mario',
              max_points=101,
              points_left=101,
              points_scored=3,
              last_turn_points=101,
              turn=3,
              darts_left=3,
              mode='given',
              hit_double=False)

assert(win==False)
assert(points_left==98)
assert(last_turn_points==101)
assert(darts_left==2)
assert(best_coordinates==(103.0, 3.7699))
assert(best_probability==0.013420966366774196)
