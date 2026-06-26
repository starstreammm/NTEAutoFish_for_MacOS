import yaml

from datetime import datetime, timezone
from pathlib import Path

from src.model import screenInfo, area, sysConfig
from src.logger import Logger
from src.sys_check import SysCheck

CONFIG_PATH = Path(__file__).parent.parent / "config.yaml"


class Config:
    _start_time = datetime.now(timezone.utc)
    _screen_info = screenInfo()
    _sys_config = sysConfig()
    _areaFish = area()
    _areaPullup = area()
    _areaExp = area()

    @classmethod
    def init(cls):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config_data: dict = yaml.safe_load(f)
            cls._sys_config = sysConfig.model_validate(config_data)

        Logger._level = cls._sys_config.log_level
        Logger.init()

        if cls._sys_config.en:
            print("[1/4] Configuration loaded: ")
        else:
            print("[1/4] 配置文件加载完成: ")
        print(f"    en: {cls._sys_config.en}")
        print(f"    random: {cls._sys_config.random}")
        print(f"    stop_when_no_pullup: {cls._sys_config.stop_when_no_pullup}")
        print(f"    log_level: {cls._sys_config.log_level}\n")

        cls._screen_info = SysCheck.get_screen_info("2/4", cls._sys_config.en)
        area = SysCheck.get_area("3/4", cls._screen_info)
        cls._areaFish = cls.area_tran(area["fish"])
        cls._areaPullup = cls.area_tran(area["pullup"])
        cls._areaExp = cls.area_tran(area["exp"])

        if cls._sys_config.en:
            Logger.info(f"Screen Info: {cls._screen_info}")
            Logger.info(f"Area Fish: {cls._areaFish}")
            Logger.info(f"Area Pullup: {cls._areaPullup}")
            Logger.info(f"Area Exp: {cls._areaExp}\n")
        else:
            Logger.info(f"屏幕信息: {cls._screen_info}")
            Logger.info(f"钓鱼区域: {cls._areaFish}")
            Logger.info(f"拉起区域: {cls._areaPullup}")
            Logger.info(f"经验区域: {cls._areaExp}\n")

    @classmethod
    def area_tran(cls, position: dict) -> area:
        return area(
            top=cls._screen_info.top + int(position["y1"]),
            left=cls._screen_info.left + int(position["x1"]),
            width=int(position["x2"]) - int(position["x1"]),
            height=int(position["y2"]) - int(position["y1"]),
        )
