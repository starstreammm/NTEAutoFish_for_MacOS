import time
import signal
import time
import sys

from datetime import datetime, timezone
from pynput.keyboard import Controller as KeyboardController, Key

from src.config import Config
from src.mouse import Mouse
from src.logger import Logger
from src.rd import random_delay, random_click, random_wait
from src.screen_check import ScreenCheck

MAX_WAIT_TIME = 13
MAX_EXP_TIME = 18  # Slightly bigger
VALUE_THRESHOLD = 8.8
ALPHA = 0.83  # EMA 平滑系数
DEAD_ZONE = 33

turn = 0  # 0 = not fishing, 1 = pulling up, 2 = fishing, 3 = exp
timer = 0.0
err_confim = 0
s_timer = datetime.now(timezone.utc)
t_timer = 0.0
t_fish = 0
v_fish = 0


# Signal handler for graceful exit
def handler(sig, frame):
    if Config._sys_config.en:
        print("--- Statistics ---")
        print(f"Total fish caught: {t_fish}")
        print(f"Total time spent: {datetime.now(timezone.utc) - s_timer}")
        print(
            f"Average time per fish: {((datetime.now(timezone.utc) - s_timer).total_seconds() / t_fish if t_fish > 0 else 1):.1f} seconds"
        )
    else:
        print("--- 统计信息 ---")
        print(f"总共钓到的鱼: {t_fish-v_fish:>3}:{v_fish:>2}:{t_fish:>3}")
        print(f"总共花费的时间: {datetime.now(timezone.utc) - s_timer}")
        print(
            f"平均每条鱼的时间: {((datetime.now(timezone.utc) - s_timer).total_seconds() / t_fish if t_fish > 0 else 1):.1f} 秒"
        )
    sys.exit(0)


signal.signal(signal.SIGINT, handler)

# Initialize configuration and logger
Config.init()

# Initialize keyboard listener
Mouse.mouse_listener()
ky = KeyboardController()

if Config._sys_config.en:
    print(f"[4/4] Start Keyboard Listener.\n")
    print(
        "System initialized. Please now switch to the game window and press the right mouse button to start or pause the bot, control + c to exit."
    )
else:
    print(f"[4/4] 键盘监听器启动完成.\n")
    print(
        "系统初始化完成，请切换到游戏窗口，按鼠标右键开始或暂停自动钓鱼, control + c 退出。"
    )
s_timer = datetime.now(timezone.utc)

# Start main loop
while True:
    if not Mouse._pause.is_set():
        turn = 0
        if Config._sys_config.en:
            Logger.info("Bot paused. Press the right mouse button to resume.")
        else:
            Logger.info("自动钓鱼已暂停, 请按鼠标右键继续.")
        Mouse._pause.wait()  # Wait for the pause event to be cleared (i.e., the bot is active)
        if Config._sys_config.en:
            Logger.info("Bot resumed. Press the right mouse button to pause.")
        else:
            Logger.info("自动钓鱼已继续, 请按鼠标右键暂停.")
        continue  # Skip the rest of the loop and check the pause state again

    if turn == 0:  # Not fishing
        # auto sell
        if Config._sys_config.auto_sell and t_fish > 0 and t_fish % 1 == 0:
            if Config._sys_config.en:
                Logger.info("Auto selling items.")
            else:
                Logger.info("自动出售已获得鱼货.")
            ky.press("q")
            random_delay()
            ky.release("q")
            random_wait()
            Mouse.mouse_click(Config._i.sell.cabin)
            random_wait()
            Mouse.mouse_click(Config._i.sell.sell)
            random_wait()
            Mouse.mouse_click(Config._i.sell.confirm)
            random_wait()
            Mouse.mouse_click()
            random_wait()
            ky.press(Key.esc)
            random_delay()
            ky.release(Key.esc)

        t_timer = timer = time.time()  # Reset the timer when start fishing
        ky.press("f")
        random_delay()
        ky.release("f")
        turn = 1
        Logger.debug("Turn 0: Start fishing.")
        time.sleep(1.3)

    elif turn == 1 and ScreenCheck.is_pullup():
        ky.press("f")
        random_delay()
        ky.release("f")
        Logger.debug("Turn 1: Wait for fish & pull up.")
        timer = time.time()  # Reset the timer when start fishing
        turn = 2
        continue  # Skip pause

    elif turn == 1 and (time.time() - timer > MAX_WAIT_TIME):
        if Config._sys_config.en:
            Logger.info("Timeout, no pull-up detected, waiting for pause confirmation.")
        else:
            Logger.info("超时未检测到上鱼, 等待暂停确认.")

        is_timeout = True
        for _ in range(8):
            time.sleep(3)
            if ScreenCheck.is_exp():
                is_timeout = False
                break

        if is_timeout:
            if err_confim < 3:
                err_confim += 1
                turn = 0
            else:
                if Config._sys_config.en:
                    Logger.info(
                        "Timeout: No pull-up detected, possibly due to insufficient bait. Pausing the bot as per the stop_when_no_pullup setting."
                    )
                else:
                    Logger.info(
                        "超时未检测到上鱼, 可能由于鱼饵不足, 按照设置项 stop_when_no_pullup 暂停自动钓鱼."
                    )
                if Config._sys_config.stop_when_no_pullup:
                    err_confim = 0
                    Mouse._pause.clear()  # Pause the bot
        else:
            turn = 3
            t_fish -= 1  # Decrement fish count since no fish was caught
            continue  # Skip pause

    elif turn == 2 and (ScreenCheck.is_fish() or (time.time() - timer > 3)):
        timer = time.time()  # Reset the timer when start fishing
        Logger.debug("Turn 2: Fishing, moving cursor.")

        last_press = None

        # EMA only on b
        b_ema = None

        def release_all():
            global last_press
            if last_press is not None:
                ky.release(last_press)
                last_press = None

        while True:
            b, c = ScreenCheck.fish_block()

            # -------- 丢失检测 --------
            if b is None or c is None:
                release_all()

                if not ScreenCheck.is_fish():
                    Logger.debug("Fish lost or pulled up, exit loop.")

                    if (time.time() - timer) > VALUE_THRESHOLD:
                        v_fish += 1
                    timer = time.time()

                    turn = 3
                    time.sleep(0.8)
                    break

                time.sleep(0.1)
                continue

            # -------- 仅对 b 做 EMA --------
            if b_ema is None:
                b_ema = b
            else:
                b_ema = ALPHA * b + (1 - ALPHA) * b_ema

            # c 不平滑
            offset = b_ema - c

            # -------- 控制量 --------
            if abs(offset) <= DEAD_ZONE:
                target = None
            elif offset < 0:
                target = "a"
            else:
                target = "d"

            # -------- 状态机 --------
            if target != last_press:
                if last_press is not None:
                    ky.release(last_press)

                if target is not None:
                    ky.press(target)

                last_press = target

            time.sleep(0.01)

    elif turn == 3 and (ScreenCheck.is_exp() or (time.time() - timer > MAX_EXP_TIME)):
        Logger.debug("Turn 3: Wait for EXP.")
        Mouse.mouse_click()
        turn = 0
        t_fish += 1
        total_time = time.time() - t_timer
        if Config._sys_config.en:
            Logger.info(
                f"Index: {t_fish:>3}, Time: {datetime.now(timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M:%S')}, Duration: {total_time:.1f} seconds, Total: {t_fish-v_fish:>3}:{v_fish:>2}:{t_fish:>3}."
            )
        else:
            Logger.info(
                f"序号: {t_fish:>3}, 时间: {datetime.now(timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M:%S')}, 本次用时: {total_time:.1f} s, 总计: {t_fish-v_fish:>3}:{v_fish:>2}:{t_fish:>3}."
            )
        random_click()

    time.sleep(0.8)  # Prevent CPU overuse
