import os
import pygame

from errorceptions import CarOutOfBoundsException

from settings import BLACK, WHITE, GREEN, RED, FONT
from settings import DIR_IMAGES
from settings import DISPLAY_WIDTH, DISPLAY_HEIGHT
from settings import PATH_WIDTH, SEPARATOR_WIDTH
from settings import USER_CAR_TYPE, USER_CAR_CONSTANT_FACTOR, USER_CAR_IMG
from settings import BOT_CAR_TYPE, BOT_CAR_CONSTANT_FACTOR, BOT_CAR_IMG
from settings import CAR_NAME_LENGTH
from settings import BOT_CAR_SPEED_PER_FRAME

from utils import generate_random_car_name
from utils import generate_random_initial_position


class Dom(object):
    _CRASH_MESSAGE = 'YOU CRASHED'
    _SCORE_MESSAGE = 'Score : %s'

    def __init__(self, pygame_display):
        self.display = pygame_display
        self.PATH_WIDTH = PATH_WIDTH
        self.DISPLAY_WIDTH = DISPLAY_WIDTH
        self.DISPLAY_HEIGHT = DISPLAY_HEIGHT
        self.SEPARATOR_WIDTH = SEPARATOR_WIDTH

        self.left_strip_x = (self.DISPLAY_WIDTH - 2 * self.PATH_WIDTH) / 2
        self.right_strip_x = self.left_strip_x + self.PATH_WIDTH
        self.separator_x = self.right_strip_x - self.SEPARATOR_WIDTH / 2
        self.cars = {}

    def add_car(self, car):
        '''Add car to the list of active cars.'''

        self.cars[car.car_name] = car

    def remove_car(self, car):
        '''Remove car from the list of active cars.'''

        del self.cars[car.car_name]

    def render_dom(self):
        self.display.fill(GREEN)
        pygame.draw.rect(
            self.display, WHITE,
            (self.left_strip_x, 0, self.PATH_WIDTH, self.DISPLAY_HEIGHT))
        pygame.draw.rect(
            self.display, WHITE,
            (self.right_strip_x, 0, self.PATH_WIDTH, self.DISPLAY_HEIGHT))
        pygame.draw.rect(
            self.display, BLACK,
            (self.separator_x, 0, self.SEPARATOR_WIDTH, self.DISPLAY_HEIGHT))
        for car_name, car in self.cars.items():
            car.render_car()

    def render_crash_message(self, score):
        font = pygame.font.SysFont(FONT, 30, True)
        text_surface = font.render(Dom._CRASH_MESSAGE, True, RED)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.DISPLAY_WIDTH / 2, self.DISPLAY_HEIGHT / 4)
        self.display.blit(text_surface, text_rect)

        text_surface = font.render(Dom._SCORE_MESSAGE % (score), True, RED)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.DISPLAY_WIDTH / 2, self.DISPLAY_HEIGHT / 2)
        self.display.blit(text_surface, text_rect)


class Car(object):
    def __init__(self, car_type, dom):
        car_image = ''
        constant_factor = None
        if car_type == USER_CAR_TYPE:
            constant_factor = USER_CAR_CONSTANT_FACTOR
            car_image = USER_CAR_IMG
        elif car_type == BOT_CAR_TYPE:
            car_image = BOT_CAR_IMG
            constant_factor = BOT_CAR_CONSTANT_FACTOR

        assert car_image, constant_factor

        self.dom = dom
        self.car_type = car_type
        self.car_name = generate_random_car_name(CAR_NAME_LENGTH)

        car_image = os.path.join(DIR_IMAGES, car_image)
        self.car_image = pygame.image.load(car_image)
        self.car_width, self.car_height = self.car_image.get_rect().size
        self.x, self.y = generate_random_initial_position(
            dom.left_strip_x, dom.right_strip_x, dom.PATH_WIDTH,
            self.car_width, dom.DISPLAY_HEIGHT, constant_factor)

    def car_within_boundary(self):
        '''Check if the car is within boundary limits.'''

        left_strip_start = self.dom.left_strip_x
        right_strip_end = self.dom.right_strip_x + self.dom.PATH_WIDTH
        if left_strip_start <= self.x <= right_strip_end:
            return True
        return False

    def is_car_on_left_lane(self):
        '''Validate if the car is on the left strip.'''

        if self.car_within_boundary() and self.x < self.dom.right_strip_x:
            return True
        return False

    def is_car_on_right_lane(self):
        '''Validate if the car is on the right strip.'''

        if self.car_within_boundary() and self.x > self.dom.right_strip_x:
            return True
        return False

    def is_car_on_same_lane(self, car):
        '''Return True if both cars are on the same lane.'''

        if(self.is_car_on_left_lane() and car.is_car_on_left_lane() or
           self.is_car_on_right_lane() and car.is_car_on_right_lane()):
            return True
        return False

    def move(self):
        '''Move the car vertically.'''

        self.y += BOT_CAR_SPEED_PER_FRAME
        if self.y >= self.dom.DISPLAY_HEIGHT:
            raise CarOutOfBoundsException()

    def switch_lane_to_left(self):
        '''Switch the user's car to left lane.'''

        self.x += -self.dom.PATH_WIDTH

    def switch_lane_to_right(self):
        '''Switch the user's car to left lane.'''

        self.x += self.dom.PATH_WIDTH

    def is_collision(self, user_car):
        '''Check if there is a collision of bot car and user's car.'''

        if self.car_type == BOT_CAR_TYPE:
            bot_car_rect = self.car_image.get_rect().move(self.x, self.y)
            user_car_rect = user_car.car_image.get_rect().move(
                user_car.x, user_car.y)
            if(self.y > user_car.y and self.is_car_on_same_lane(user_car) or
               bot_car_rect.colliderect(user_car_rect)):
                return True
        return False

    def render_car(self):
        '''Instruct pygame to reender the car on screen.'''

        coordinates = (self.x, self.y)
        self.dom.display.blit(self.car_image, coordinates)
