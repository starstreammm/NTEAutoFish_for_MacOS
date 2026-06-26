import random
import time

from src.config import Config


def random_delay():
    scale = Config._sys_config.random
    time.sleep(random.uniform(0.8 / scale, 2.3 * scale))
