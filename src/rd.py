import random
import time

from src.config import Config


def random_delay():
    scale = Config._sys_config.random
    time.sleep(random.uniform(1.1 / scale, 2.3 * scale))


def random_click():
    scale = Config._sys_config.random
    time.sleep(random.uniform(0.8 / scale, 1.3 * scale))


def random_wait():
    scale = Config._sys_config.random
    time.sleep(random.uniform(2.3 / scale, 3.8 * scale))


def random_move() -> float:
    scale = Config._sys_config.random
    return random.uniform(0.3 / scale, 0.8 * scale)
