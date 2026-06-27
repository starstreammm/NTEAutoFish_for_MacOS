<div align="center">
  <h1>NTEAutoFish_for_MacOS</h1>
  <br />
  <img alt="Node Current" src="https://img.shields.io/node/v/%40rolldown%2Fplugin-babel">
  <img alt="Python Version" src="https://img.shields.io/badge/python-3.10%2B-blue">
  <img alt="GitHub License" src="https://img.shields.io/github/license/Xu-Xihe/svtav1UI">
  <img alt="GitHub Release" src="https://img.shields.io/github/v/release/Xu-Xihe/svtav1UI">
  <img alt="GitHub Actions Workflow Status" src="https://img.shields.io/github/actions/workflow/status/Xu-Xihe/svtav1UI/release.yml?label=Release">
	<img alt="GitHub Actions Workflow Status" src="https://img.shields.io/github/actions/workflow/status/Xu-Xihe/svtav1UI/docker.yml?label=Docker">
  <br />
  <img alt="GitHub forks" src="https://img.shields.io/github/forks/Xu-Xihe/svtav1UI">
	<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/Xu-Xihe/svtav1UI">
	<img alt="GitHub Issues or Pull Requests" src="https://img.shields.io/github/issues/Xu-Xihe/svtav1UI">
  <br />
  <br />
  <a href="./README.md">简体中文</a> | <a href="./README_en.md">English</a>
  <br />
 </div>


## 0 简介

上 ~~Gay Hub~~ Github 找了一圈, 并没有发现任何可以用于macOS的异环钓鱼脚本. 作为为数不多的能在macOS上玩的游戏, 其钓鱼小玩法打满需要24小时以上的纯游玩时间, 这很显然并不现实. 因此, 半手搓 ~~ai还是太超模了~~ 了这个program, 以此填补异环macOS没有自动钓鱼的问题.

> [!CAUTION]
>
> 本项目仅以macOS下异环自动钓鱼为目标, 理论上适配Windows平台(未使用平台专属api), 但其适配与测试不在本项目目标之内.

## 1 安装

1. 安装Python

请按照Python官方网站文档安装, 注意python版本要求为>= 3.10.

2. Clone项目

```bash
git clone https://github.com/Xu-Xihe/NTEAutoFish_for_MacOS.git
```

3. 安装pip依赖

```bash
pip install -r requirements.txt
```

4. 区域选择与机型适配

详见 [3 运行机制与机型匹配](#3-运行机制与机型匹配)

> [!IMPORTANT]
>
> 本项目内置对于MacBook Pro M-Silicon 14.2-inch Retina display 的支持.
>
> 关于其他尺寸屏幕, 欢迎提交pr, 别忘了附上INFO与DEBUG输出哦.

5. 运行主程序

```bash
python main.py
```

## 2 配置项

配置文件位于根目录 `config.yaml` 中.

| key                 | 描述                                            |
| ------------------- | ----------------------------------------------- |
| en                  | 英文                                            |
| stop_when_no_pullup | 当pullup检测超时, 即当鱼饵耗尽时, 是否停止钓鱼. |
| random              | 随机数scale, 如非必要无需更改                   |
| log_level           | 日志等级, INFO / DEBUG                          |

## 3 运行机制与机型匹配

### 事件循环

整个钓鱼过程被拆分为 $4$ 个部分, 分别为:

1. 等待钓鱼-按下f开始钓鱼 (not_fish)
2. 等待鱼上钩-拉起鱼等待遛鱼 (pullup)
3. 开始遛鱼-完成钓鱼 (fish)
4. 完成钓鱼-收获界面弹出-单击关闭返回等待钓鱼 (exp)

事件识别采用图像识别+颜色识别+超时机制. 2 和 4 采用屏幕固定区域与图例相似度比较, 3 采用颜色识别.

### 区域划分

全部区域划分储存在根目录下 `area.json` 文件中.

> [!CAUTION]
>
> 全部坐标为 mss 输出坐标, 即逻辑坐标, 非Retina输出实际坐标. 具体分辨率可在程序初始化阶段查看.

#### Pullup 区域

文件位于根目录下 `resource/pullup.png`, 图像大小为320 × 40.

![pullup](./resource/pullup.png)

#### Fish 区域

即事件3中顶部滑动条, 取内层深黑色衬底部分. 注意取值时尽可能在左右两侧留有空隙, 防止黄色滑动条滑动到极限位置无法被检测.

#### Exp 区域

文件位于根目录下 `resource/exp.png`, 图像大小为78 ×  60.

![exp](./resource/exp.png)

## 4 致谢

部分灵感来源于:【异环mac端2k分辨率下自动钓鱼脚本】 https://www.bilibili.com/video/BV1eQjh6dE9t/?share_source=copy_web&vd_source=90e59bd1168d818983dd51105bc5e78f
