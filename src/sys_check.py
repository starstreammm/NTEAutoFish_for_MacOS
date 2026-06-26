import mss
import json
from pathlib import Path

from src.model import screenInfo

AREA_JSON_PATH = Path(__file__).parent.parent / "area.json"


class SysCheck:
    @staticmethod
    def get_screen_info(step_index: str, en: bool = False) -> screenInfo:
        with mss.MSS() as sct:
            index = 1  # 默认使用第一个屏幕
            monitor: dict = sct.monitors

            if en:
                print(
                    f"[{step_index}] Screen selection: {"Only one screen detected, automatically selected.\n" if len(monitor) <= 2 else ""}"
                )
            else:
                print(
                    f"[{step_index}] 屏幕选择: {"仅检测到一个屏幕，已自动选择。\n" if len(monitor) <= 2 else ""}"
                )

            if len(monitor) > 2:
                for i, m in enumerate(sct.monitors):
                    if i == 0:
                        continue  # 跳过第一个元素，它是所有屏幕的总和
                    if en:
                        print("Screen", end="")
                    else:
                        print("屏幕", end="")
                    print(
                        f" {i}: {m['width']} by {m['height']} pixels, position ({m['left']}, {m['top']})."
                    )

                index = int(
                    input(
                        f"{'Please select screen number (default 1): ' if en else '请选择屏幕编号(默认 1): '}"
                    )
                    or 1
                )
                print("")

            return screenInfo(
                width=monitor[index]["width"],
                height=monitor[index]["height"],
                left=monitor[index]["left"],
                top=monitor[index]["top"],
            )

    @staticmethod
    def get_area(step_index: str, si: screenInfo, en: bool = False) -> dict:
        with open(AREA_JSON_PATH, "r") as f:
            area: dict = json.load(f)["resolutions"]

            if f"{si.width}_{si.height}" not in area.keys():
                if en:
                    print(
                        f"[{step_index}] Detect area configuration: preset not found, using 1512_982 preset to calculate.\n"
                    )
                else:
                    print(
                        f"[{step_index}] 检测到区域配置: 未找到预设，使用 1512_982 预设进行计算.\n"
                    )
                scale_area = area["1512_982"]
                for k, v in scale_area.items():
                    v["x1"] = v["x1"] * (si.width / 1512)
                    v["x2"] = v["x2"] * (si.width / 1512)
                    v["y1"] = v["y1"] * (si.height / 982)
                    v["y2"] = v["y2"] * (si.height / 982)
                return scale_area

            else:
                if en:
                    print(f"[{step_index}] Detect area configuration: preset found.\n")
                else:
                    print(f"[{step_index}] 检测到区域配置: 找到预设.\n")
                return area[f"{si.width}_{si.height}"]
