class Config:

    ant_move_modifier = 1               # move faster, turn harder
    ant_TTL = 5                        # in seconds
    network_configuration = [5, 10, 10, 1]
    num_of_ants = 100
    sim_speed_multiplier = 10           # maximum; in practice may be less
    variance_range = 0.05              # the amount an ant's children differ from it
    screen_size = (600, 600)
    should_render = True
    should_wipe_screen = True
    dist_scoring_leniency = 100
