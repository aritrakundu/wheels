import random
import string


def generate_random_initial_position(left_strip_x, right_strip_x,
                                     path_width, car_width, display_height,
                                     constant_factor):
    '''Generate starting positions for the car.'''

    x_left = left_strip_x + path_width / 2 - car_width / 2
    x_right = right_strip_x + path_width / 2 - car_width / 2
    y = display_height * constant_factor

    choice_1 = (x_left, y)
    choice_2 = (x_right, y)
    choices = [choice_1, choice_2]
    return random.choice(choices)


def generate_random_car_name(length):
    '''Generate random string for the car.'''

    generation_set = (
        string.ascii_uppercase + string.ascii_lowercase + string.digits)
    random_string = ''.join(
        random.choice(generation_set) for _ in range(length))
    return random_string


def render_car(display, car_img, x, y):
    '''Render the car at (x, y) coordinates.'''

    coordinates = (x, y)
    display.blit(car_img, coordinates)
