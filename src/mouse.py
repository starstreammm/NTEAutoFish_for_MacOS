import threading
import time

from pynput.mouse import (
    Button,
    Controller as MouseController,
    Listener as MouseListener,
)

from src.config import Config
from src.rd import random_click
from src.model import axisInfo


class Mouse:
    _lock = threading.Lock()

    _mouse = MouseController()

    _pause = threading.Event()  # 用于暂停和恢复的事件对象
    _pause.clear()

    @classmethod
    def mouse_click(
        cls,
        position: axisInfo = axisInfo(
            x=Config._i.screen.width // 2,
            y=Config._i.screen.height // 2,
        ),
    ):
        cls._mouse.position = (position.x, position.y)
        time.sleep(0.01)
        cls._mouse.press(Button.left)
        random_click()
        cls._mouse.release(Button.left)

    @classmethod
    def mouse_listener(cls):
        _last_click_time: float = 0
        _press: bool = False

        def on_click(x, y, button, pressed):
            nonlocal _last_click_time, _press

            if button == Button.right and pressed:
                now = time.time()
                if not _press and now - _last_click_time > 1:  # 1秒内只能点击一次
                    _press = True
                    cls._pause.clear() if cls._pause.is_set() else cls._pause.set()
                    _last_click_time = now
            else:
                _press = False

        def run():
            with MouseListener(on_click=on_click) as listener:
                listener.join()

        threading.Thread(target=run, daemon=True).start()
