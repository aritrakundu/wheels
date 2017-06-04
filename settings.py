import os

# App Settings
APP_NAME = 'Wheels'
DISPLAY_WIDTH = 300
DISPLAY_HEIGHT = 400
GAME_FPS = 30

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DIR_IMAGES = os.path.join(BASE_DIR, 'img')

# Common Settings
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
RED = (204, 0, 0)
FONT = 'monospace'
PATH_WIDTH = DISPLAY_WIDTH / 3
SEPARATOR_WIDTH = min(10, 0.05 * PATH_WIDTH)

# Module level Settings
CAR_NAME_LENGTH = 5
USER_CAR_IMG = 'car.png'
USER_CAR_TYPE = 'user-car'
USER_CAR_CONSTANT_FACTOR = 0.75
BOT_CAR_IMG = 'bot_car.png'
BOT_CAR_TYPE = 'bot-car'
BOT_CAR_CONSTANT_FACTOR = 0.0
BOT_CAR_SPEED_PER_FRAME = DISPLAY_HEIGHT / GAME_FPS
SPAWN_TIME_MAX_INTERVAL = GAME_FPS  # Spawn at 1 second intervals.
SPAWN_TIME_MIN_INTERVAL = GAME_FPS * 0.5  # Spawn at half second intervals.
SPAWN_TIME_DECREMENT = 5
LEVEL_UP_INTERVAL = 300  # Frames
