import pygame
import time

from errorceptions import CarOutOfBoundsException

from models import Dom, Car

from settings import APP_NAME, GAME_FPS
from settings import DISPLAY_WIDTH, DISPLAY_HEIGHT
from settings import USER_CAR_TYPE, BOT_CAR_TYPE
from settings import SPAWN_TIME_MAX_INTERVAL, SPAWN_TIME_MIN_INTERVAL
from settings import SPAWN_TIME_DECREMENT, LEVEL_UP_INTERVAL


def main(display):
    '''Launch HotWheels.'''

    spawn_interval = SPAWN_TIME_MAX_INTERVAL

    dom = Dom(display)
    user_car = Car(USER_CAR_TYPE, dom)
    dom.add_car(user_car)

    frames_elapsed = 0
    total_frames = 0
    score = 0
    curr_level_score = 10

    restart = False
    crashed = False

    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return restart

            # Move left or right. The car should not go outside the boundaries.
            if event.type == pygame.KEYDOWN:
                if(event.key == pygame.K_LEFT and
                   user_car.is_car_on_right_lane()):
                    user_car.switch_lane_to_left()
                if(event.key == pygame.K_RIGHT and
                   user_car.is_car_on_left_lane()):
                    user_car.switch_lane_to_right()

        if not frames_elapsed:
            bot_car = Car(BOT_CAR_TYPE, dom)
            dom.add_car(bot_car)

        for car_name, car in dom.cars.items():
            if car.car_type == BOT_CAR_TYPE:
                try:
                    if not car.is_collision(user_car):
                        car.move()
                    else:
                        dom.render_crash_message(score)
                        pygame.display.update()
                        restart = crashed = True
                        time.sleep(2)
                        break
                except CarOutOfBoundsException:
                    score += curr_level_score
                    dom.remove_car(car)

        if crashed:
            return restart

        dom.render_dom()
        pygame.display.update()
        clock.tick(GAME_FPS)

        frames_elapsed += 1
        if frames_elapsed == spawn_interval:
            total_frames += frames_elapsed
            if total_frames >= LEVEL_UP_INTERVAL:
                curr_level_score *= 2
                spawn_interval = max(SPAWN_TIME_MIN_INTERVAL,
                                     spawn_interval - SPAWN_TIME_DECREMENT)
                total_frames = 0
            frames_elapsed = 0
    return restart


pygame.init()
pygame.font.init()
display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption(APP_NAME)
clock = pygame.time.Clock()

restart = True
while restart:
    restart = main(display)

pygame.quit()
quit()
