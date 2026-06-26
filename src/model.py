from pydantic import BaseModel
from typing import Literal
import numpy as np

# Color thresholds
GREEN_LOWER = np.array([75, 100, 100])
GREEN_UPPER = np.array([95, 255, 255])
YELLOW_LOWER = np.array([15, 80, 80])
YELLOW_UPPER = np.array([45, 255, 255])


class screenInfo(BaseModel):
    left: int = 0
    top: int = 0
    width: int = 1512
    height: int = 982


class area(BaseModel):
    left: int = 812
    top: int = 91
    width: int = 949
    height: int = 19


class sysConfig(BaseModel):
    en: bool = False
    random: float = 1.0
    stop_when_no_pullup: bool = True
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
