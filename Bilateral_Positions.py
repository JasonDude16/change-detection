# ------------------------------------------------------------------------
#  Module for Discrete Whole Report, Change Detection, etc.
#
#  Returns a list of coordinates for stimuli that are bilateral and
#  are a minimum distance away from each other and the fixation.
#
#  Rachel Klein, April 2016

import random, math

stim_size = 72  # Size in pixels of the sides of the squares.

min_distance = 2.5*stim_size  # Distance the center of each stimulus should be from others

def create_up_to_2_pos(stim_number, x_axis_limit, y_axis_limit):
    # Creating lists of possible placements that exclude being too close to fixation on x or y plane
    # Also adjusting for the radius of the fixation (6 pixels)
    possible_x = []
    possible_y = []
    fixation_buffer = int(1.5*stim_size + 6)  # Minimum distance each stimulus should be from the fixation

    left_x = range(int(-x_axis_limit), int(-fixation_buffer-1))
    for x in left_x:
        possible_x.append(x)
    right_x = range(int(fixation_buffer), int(x_axis_limit+1))
    for x in right_x:
        possible_x.append(x)
        
    top_y = range(int(fixation_buffer), int(y_axis_limit+1))
    for y in top_y:
        possible_y.append(y)
    bottom_y = range(int(-y_axis_limit), int(-fixation_buffer-1))
    for y in bottom_y:
        possible_y.append(y)

    pos_list = []
    
    if stim_number == 1 or stim_number == 2:
        pos = [random.choice(possible_x), random.choice(possible_y)]  # First position can be in any quadrant
        pos_list.append(pos)
        
    if stim_number == 2:
        # If previous position was left, choose one on the right
        # Top/bottom placement is chosen randomly for second stim, as in previous Matlab version
        if pos_list[0][0] < 0:
            pos = [random.choice(right_x), random.choice(possible_y)]
        else:  # If was right, choose left
            pos = [random.choice(left_x), random.choice(possible_y)]
        pos_list.append(pos)

    return pos_list

def create_up_to_6_pos(stim_number, x_axis_limit, y_axis_limit):
    # Creating lists of possible placements that exclude being too close to fixation on x or y plane
    # Also adjusting for the radius of the fixation (6 pixels)
    possible_x = []
    possible_y = []
    fixation_buffer = int(1.5*stim_size + 6)  # Minimum distance each stimulus should be from the fixation

    left_x = range(int(-x_axis_limit), int(-fixation_buffer-1))
    for x in left_x:
        possible_x.append(x)
    right_x = range(int(fixation_buffer), int(x_axis_limit+1))
    for x in right_x:
        possible_x.append(x)
        
    top_y = range(int(fixation_buffer), int(y_axis_limit+1))
    for y in top_y:
        possible_y.append(y)
    bottom_y = range(int(-y_axis_limit), int(-fixation_buffer-1))
    for y in bottom_y:
        possible_y.append(y)
    pos_list = []

    # First four stim get placed one in each quadrant of screen
    pos = [random.choice(left_x), random.choice(top_y)]  # Upper left
    pos_list.append(pos)

    pos = [random.choice(right_x), random.choice(top_y)]  # Upper right
    pos_list.append(pos)

    pos = [random.choice(left_x), random.choice(bottom_y)]  # Lower left
    pos_list.append(pos)

    pos = [random.choice(right_x), random.choice(bottom_y)]  # Lower right
    pos_list.append(pos)

    if stim_number == 5:
        # Quadrant chosen randomly for fifth stim
        random_positions = range(1, 5)  # Quadrants where stim 5 can go
        fifth_stim_quadrant = random.choice(random_positions)

        if fifth_stim_quadrant == 1:
            first_x = pos_list[0][0]
            first_y = pos_list[0][1]

            while True:
                pos = [random.choice(left_x), random.choice(top_y)]  # Upper left
                fifth_x = pos[0]
                fifth_y = pos[1]
                
                # Make sure it's not too close to first stim
                if math.sqrt(abs(first_x - fifth_x)**2 + abs(first_y - fifth_y)**2) > min_distance:
                    break
            pos_list.append(pos)

        elif fifth_stim_quadrant == 2:
            second_x = pos_list[1][0]
            second_y = pos_list[1][1]

            while True:
                pos = [random.choice(right_x), random.choice(top_y)]  # Upper right
                fifth_x = pos[0]
                fifth_y = pos[1]
                # Make sure it's not too close to second stim
                if math.sqrt(abs(second_x - fifth_x)**2 + abs(second_y - fifth_y)**2) > min_distance:
                    break
            pos_list.append(pos)

        elif fifth_stim_quadrant == 3:
            third_x = pos_list[2][0]
            third_y = pos_list[2][1]

            while True:
                pos = [random.choice(left_x), random.choice(bottom_y)]  # Lower left
                fifth_x = pos[0]
                fifth_y = pos[1]

                # Make sure it's not too close to third stim
                if math.sqrt(abs(third_x - fifth_x)**2 + abs(third_y - fifth_y)**2) > min_distance:
                    break
            pos_list.append(pos)
            
        elif fifth_stim_quadrant == 4:
            fourth_x = pos_list[3][0]
            fourth_y = pos_list[3][1]

            while True:
                pos = [random.choice(right_x), random.choice(bottom_y)]  # Lower right
                fifth_x = pos[0]
                fifth_y = pos[1]

                # Make sure it's not too close to fourth stim
                if math.sqrt(abs(fourth_x - fifth_x)**2 + abs(fourth_y - fifth_y)**2) > min_distance:
                    break
            pos_list.append(pos)
    
    elif stim_number == 6:
        
        possible_positions = range(1, 7)  # Choosing from 6 possible placements for 5 and 6

        position_choice = random.choice(possible_positions)

        # 1 = both top (one left, one right)
        if position_choice == 1:
            first_x = pos_list[0][0]
            first_y = pos_list[0][1]

            while True:
                pos = [random.choice(left_x), random.choice(top_y)]  # Upper left
                fifth_x = pos[0]
                fifth_y = pos[1]
                
                # Make sure it's not too close to first stim
                if math.sqrt(abs(first_x - fifth_x)**2 + abs(first_y - fifth_y)**2) > min_distance:
                    break
            pos_list.append(pos)
            
            second_x = pos_list[1][0]
            second_y = pos_list[1][1]

            while True:
                pos = [random.choice(right_x), random.choice(top_y)]  # Upper right
                sixth_x = pos[0]
                sixth_y = pos[1]
                # Make sure it's not too close to second stim
                if math.sqrt(abs(second_x - sixth_x)**2 + abs(second_y - sixth_y)**2) > min_distance:
                    break
            pos_list.append(pos)

        # 2 = both bottom (one left, one right)
        elif position_choice == 2:
            third_x = pos_list[2][0]
            third_y = pos_list[2][1]

            while True:
                pos = [random.choice(left_x), random.choice(bottom_y)]  # Lower left
                fifth_x = pos[0]
                fifth_y = pos[1]

                # Make sure it's not too close to third stim
                if math.sqrt(abs(third_x - fifth_x)**2 + abs(third_y - fifth_y)**2) > min_distance:
                    break
            pos_list.append(pos)

            fourth_x = pos_list[3][0]
            fourth_y = pos_list[3][1]

            while True:
                pos = [random.choice(right_x), random.choice(bottom_y)]  # Lower right
                sixth_x = pos[0]
                sixth_y = pos[1]

                # Make sure it's not too close to fourth stim
                if math.sqrt(abs(fourth_x - sixth_x)**2 + abs(fourth_y - sixth_y)**2) > min_distance:
                    break
            pos_list.append(pos)

        # 3 = both left (one top, one bottom)
        elif position_choice == 3:
            first_x = pos_list[0][0]
            first_y = pos_list[0][1]

            while True:
                pos = [random.choice(left_x), random.choice(top_y)]  # Upper left
                fifth_x = pos[0]
                fifth_y = pos[1]
                
                # Make sure it's not too close to first stim
                if math.sqrt(abs(first_x - fifth_x)**2 + abs(first_y - fifth_y)**2) > min_distance:
                    break
            pos_list.append(pos)

            third_x = pos_list[2][0]
            third_y = pos_list[2][1]

            while True:
                pos = [random.choice(left_x), random.choice(bottom_y)]  # Lower left
                sixth_x = pos[0]
                sixth_y = pos[1]

                # Make sure it's not too close to third stim
                if math.sqrt(abs(third_x - sixth_x)**2 + abs(third_y - sixth_y)**2) > min_distance:
                    break
            pos_list.append(pos)

        # 4 = both right (one top, one bottom)
        elif position_choice == 4:
            second_x = pos_list[1][0]
            second_y = pos_list[1][1]

            while True:
                pos = [random.choice(right_x), random.choice(top_y)]  # Upper right
                fifth_x = pos[0]
                fifth_y = pos[1]
                # Make sure it's not too close to second stim
                if math.sqrt(abs(second_x - fifth_x)**2 + abs(second_y - fifth_y)**2) > min_distance:
                    break
            pos_list.append(pos)

            fourth_x = pos_list[3][0]
            fourth_y = pos_list[3][1]

            while True:
                pos = [random.choice(right_x), random.choice(bottom_y)]  # Lower right
                sixth_x = pos[0]
                sixth_y = pos[1]

                # Make sure it's not too close to fourth stim
                if math.sqrt(abs(fourth_x - sixth_x)**2 + abs(fourth_y - sixth_y)**2) > min_distance:
                    break
            pos_list.append(pos)

        # 5 = one upper right, one lower left
        elif position_choice == 5:
            second_x = pos_list[1][0]
            second_y = pos_list[1][1]
            third_x = pos_list[2][0]
            third_y = pos_list[2][1]

            while True:
                pos = [random.choice(right_x), random.choice(top_y)]  # Upper right
                fifth_x = pos[0]
                fifth_y = pos[1]
                # Make sure it's not too close to second stim
                if math.sqrt(abs(second_x - fifth_x)**2 + abs(second_y - fifth_y)**2) > min_distance:
                    break
            pos_list.append(pos)

            while True:
                pos = [random.choice(left_x), random.choice(bottom_y)]  # Lower left
                sixth_x = pos[0]
                sixth_y = pos[1]

                # Make sure it's not too close to third stim
                if math.sqrt(abs(third_x - sixth_x)**2 + abs(third_y - sixth_y)**2) > min_distance:
                    break
            pos_list.append(pos)

        # 6 = one upper left, one lower right
        elif position_choice == 6:
            first_x = pos_list[0][0]
            first_y = pos_list[0][1]
            fourth_x = pos_list[3][0]
            fourth_y = pos_list[3][1]

            while True:
                pos = [random.choice(left_x), random.choice(top_y)]  # Upper left
                fifth_x = pos[0]
                fifth_y = pos[1]
                
                # Make sure it's not too close to first stim
                if math.sqrt(abs(first_x - fifth_x)**2 + abs(first_y - fifth_y)**2) > min_distance:
                    break
            pos_list.append(pos)

            while True:
                pos = [random.choice(right_x), random.choice(bottom_y)]  # Lower right
                sixth_x = pos[0]
                sixth_y = pos[1]

                # Make sure it's not too close to fourth stim
                if math.sqrt(abs(fourth_x - sixth_x)**2 + abs(fourth_y - sixth_y)**2) > min_distance:
                    break
            pos_list.append(pos)

    return pos_list