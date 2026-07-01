import yaml

from datetime import datetime, timezone
from pathlib import Path

from src.model import screenConfig, sysConfig, areaInfo, sellInfo
from src.logger import Logger
from src.sys_check import SysCheck

CONFIG_PATH = Path(__file__).parent.parent / "config.yaml"


class Config:
    _start_time = datetime.now(timezone.utc)
    _i: screenConfig = screenConfig()
    _sys_config = sysConfig()

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

        cls._i.screen = SysCheck.get_screen_info("2/4", cls._sys_config.en)
        area = SysCheck.get_area("3/4", cls._i.screen)
        cls._i.fish = cls.area_tran(area["fish"])
        cls._i.pullup = cls.area_tran(area["pullup"])
        cls._i.exp = cls.area_tran(area["exp"])
        cls._i.sell = sellInfo.model_validate(area["sell"])

        if cls._sys_config.en:
            Logger.info(f"Screen Info: {cls._i.screen}")
            Logger.info(f"Area Fish: {cls._i.fish}")
            Logger.info(f"Area Pullup: {cls._i.pullup}")
            Logger.info(f"Area Exp: {cls._i.exp}")
            Logger.info(f"Sell Axis: {cls._i.sell}\n")
        else:
            Logger.info(f"屏幕信息: {cls._i.screen}")
            Logger.info(f"钓鱼区域: {cls._i.fish}")
            Logger.info(f"拉起区域: {cls._i.pullup}")
            Logger.info(f"经验区域: {cls._i.exp}")
            Logger.info(f"出售坐标: {cls._i.sell}\n")

    @classmethod
    def area_tran(cls, position: dict) -> areaInfo:
        return areaInfo(
            top=cls._i.screen.top + int(position["y1"]),
            left=cls._i.screen.left + int(position["x1"]),
            width=int(position["x2"]) - int(position["x1"]),
            height=int(position["y2"]) - int(position["y1"]),
        )
