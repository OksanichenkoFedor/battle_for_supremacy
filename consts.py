BACKGROUND_COLOR = (20, 20, 20)
HEX_COLORS = [
    (255, 0, 0),       # Красный
    (173, 255, 47),    # Салатовый
    (138, 43, 226),    # Фиолетовый
    (30, 144, 255),    # Синий
    (255, 255, 0),     # Жёлтый
    (64, 224, 208),    # Бирюзовый
]
HEX_COLORS_NAMES = [
    "Красный",       # Красный
    "Салатовый",    # Салатовый
    "Фиолетовый",    # Фиолетовый
    "Синий",    # Синий
    "Жёлтый",     # Жёлтый
    "Бирюзовый",    # Бирюзовый
]

HEX_COLORS_DICT = {
    "Красный": 0,       # Красный
    "Салатовый": 1,    # Салатовый
    "Фиолетовый": 2,    # Фиолетовый
    "Синий": 3,    # Синий
    "Жёлтый": 4,     # Жёлтый
    "Бирюзовый": 5,    # Бирюзовый
}

ADMIN_ID = {
    "Федя": 710672679,
    #"Марч": 723607313,
    #"Саша": 1084106632
}

BASE_HEX_COLOR = (255, 255, 255)
BORDER_COLOR = (128, 128, 128)
BORDER_WIDTH = 4
HEX_SIZE = 40
TEXT_COLOR = (0, 0, 0)

WIDTH, HEIGHT = 1400, 1100

HEX_COUNT = 8

BUTTON_CHOOSEN_WIDTH = 6
BUTTON_UNCHOOSEN_WIDTH = 4
BUTTON_CHOOSEN_COLOR = (150, 150, 150)
BUTTON_UNCHOOSEN_COLOR = (70, 70, 70)
BUTTON_SIZE = 50


BUTTON_SPACING = 70
BUTTON_X = WIDTH - 2*BUTTON_SIZE
BUTTON_Y = HEIGHT//2 - (len(HEX_COLORS)//2)*BUTTON_SPACING - BUTTON_SIZE//2

LOAD_BUTTON_COLOR = (255, 255, 255)
LOAD_BUTTON_TEXT_COLOR = (0, 0, 0)

MIN_NUM_STAR_POINTS = 1
MAX_NUM_STAR_POINTS = 3

STAR_COLOR = (255, 215, 0)      # Золотой цвет звезды
SPARKLE_COLOR = (255, 255, 0) # Цвет блесток


BETA = 50000.0
NUM_STAR = 5
TEAM_BASE_COEFF =8.0

ANIMATION_SPEED = 0.3