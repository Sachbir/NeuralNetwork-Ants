class Config:

    ant_move_modifier = 1  # move faster, turn harder
    ant_TTL = 3                         # in seconds
    network_configuration = [5, 15, 1]
    num_of_ants = 100
    sim_speed_multiplier = 10           # maximum; in practice may be less
    variance_range = 0.005              # the amount an ant's children differ from it
    screen_size = (900, 900)

    should_render = False
