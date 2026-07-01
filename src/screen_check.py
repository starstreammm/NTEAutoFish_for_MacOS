import cv2
import numpy as np
import mss

from typing import Tuple
from pathlib import Path
from skimage.metrics import structural_similarity as ssim

from src.model import (
    GREEN_LOWER,
    GREEN_UPPER,
    YELLOW_LOWER,
    YELLOW_UPPER,
    areaInfo,
)
from src.logger import Logger
from src.config import Config

SSIM_THRESHOLD = 0.3


class ScreenCheck:
    _pullup_img = cv2.imread(
        Path(__file__).parent.parent / "resource" / "pullup.png", cv2.IMREAD_GRAYSCALE
    )
    _exp_img = cv2.imread(
        Path(__file__).parent.parent / "resource" / "exp.png", cv2.IMREAD_GRAYSCALE
    )

    @staticmethod
    def get_largest_color_center_x(
        hsv_img, lower: np.ndarray, upper: np.ndarray
    ) -> int | None:
        mask = cv2.inRange(hsv_img, lower, upper)

        v = hsv_img[:, :, 2]
        mask = mask & (v > 203)  # 关键：过滤黑遮罩/暗黄

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            return None

        largest = max(contours, key=cv2.contourArea)

        x, y, w, h = cv2.boundingRect(largest)

        return x + w // 2

    @staticmethod
    def color_persantage(hsv_img, lower: np.ndarray, upper: np.ndarray) -> float:
        mask = cv2.inRange(hsv_img, lower, upper)
        return cv2.countNonZero(mask) * 100.0 / mask.size

    @classmethod
    def is_fish(cls) -> bool:
        hsv_img, _ = cls.get_screen_shot(Config._i.fish)
        green = cls.color_persantage(hsv_img, GREEN_LOWER, GREEN_UPPER)
        yellow = cls.color_persantage(hsv_img, YELLOW_LOWER, YELLOW_UPPER)
        Logger.debug(f"is_fish: green={green}, yellow={yellow}")
        return green > 3 and yellow > 0.3

    @classmethod
    def fish_block(cls) -> Tuple[int, int] | Tuple[None, None]:
        """
        Returns the center x-coordinates of the largest green and yellow contours in the given HSV image.
        """
        hsv_img, _ = cls.get_screen_shot(Config._i.fish)
        center_b = cls.get_largest_color_center_x(hsv_img, GREEN_LOWER, GREEN_UPPER)
        center_c = cls.get_largest_color_center_x(hsv_img, YELLOW_LOWER, YELLOW_UPPER)
        if center_b is None or center_c is None:
            return None, None
        Logger.debug(f"fish_block: block center={center_b}, cursor center={center_c}")
        return center_b, center_c

    @classmethod
    def is_pullup(cls) -> bool:
        _, grey_img = cls.get_screen_shot(Config._i.pullup)

        if cls._pullup_img is None or grey_img is None:
            raise ValueError("Picture reading failed")

        if cls._pullup_img.shape != grey_img.shape:
            cls._pullup_img = cv2.resize(
                cls._pullup_img, (grey_img.shape[1], grey_img.shape[0])
            )

        score = ssim(cls._pullup_img, grey_img, full=True)
        Logger.debug(f"is_pullup: SSIM score={float(score[0])}")
        return float(score[0]) > SSIM_THRESHOLD

    @classmethod
    def is_exp(cls) -> bool:
        _, grey_img = cls.get_screen_shot(Config._i.exp)

        if cls._exp_img is None or grey_img is None:
            raise ValueError("Picture reading failed")

        if cls._exp_img.shape != grey_img.shape:
            cls._exp_img = cv2.resize(
                cls._exp_img, (grey_img.shape[1], grey_img.shape[0])
            )

        score = ssim(cls._exp_img, grey_img, full=True)
        Logger.debug(f"is_exp: SSIM score={float(score[0])}")
        return float(score[0]) > SSIM_THRESHOLD

    @staticmethod
    def get_screen_shot(region: areaInfo) -> tuple[np.ndarray, np.ndarray]:
        """
        Captures a screenshot of the specified monitor and returns it as a NumPy array in BGR format.
        """
        with mss.MSS() as sct:
            img = np.array(sct.grab(region.model_dump()))
            bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
            grey = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        return hsv, grey
