class Config:

    ant_move_modifier = 1               # move faster, turn harder
    ant_TTL = 0                        # in seconds
    network_configuration = [5, 15, 1]
    num_of_ants = 200
    sim_speed_multiplier = 10           # maximum; in practice may be less
    variance_range = 0.005              # the amount an ant's children differ from it
    screen_size = (400, 400)
    should_render = True
