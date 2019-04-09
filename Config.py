class Config:

    sim_speed_multiplier = 10               # maximum; in practice may be less
    num_of_ants = 10

    screen_size = (800, 800)
    render_state = 2
    should_wipe_screen = True               # 'False' creates ant movement trails

    ant_move_modifier = 1                   # move faster, turn harder
    ant_TTL = 10                            # in seconds

    network_config = [5, 10, 10, 1]         # 5 ... 1 formula is required
                                            # higher makes no difference, lower breaks it
    variance_range = 0.025                  # the amount each ant's children differ from it

    inaccuracy_of_measure = .05
    position_sample_rate = ant_TTL / 20     # in seconds
