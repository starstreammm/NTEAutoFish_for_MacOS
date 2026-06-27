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
## 0 Introduction

After searching around on ~~Gay Hub~~ GitHub, I couldn’t find any macOS-compatible auto-fishing script for *Intertwined Ring*. As one of the few games playable on macOS, its fishing mini-game requires over 24 hours of continuous gameplay to fully complete, which is clearly unrealistic. Therefore, I semi-handcrafted this program ~~AI really is overpowered~~ to fill the gap of not having an auto-fishing solution for *Intertwined Ring* on macOS.

> [!CAUTION]
>
> This project is only intended for auto-fishing in *Intertwined Ring* on macOS. It is theoretically compatible with Windows (no platform-specific APIs are used), but adaptation and testing on Windows are not part of the project’s goals.


## 1 Installation

1. Install Python

Please follow the official Python documentation to install Python. Ensure the version is **>= 3.10**.

2. Clone the project

```bash
git clone https://github.com/Xu-Xihe/NTEAutoFish_for_MacOS.git
```

3. Install dependencies via pip

```bash
pip install -r requirements.txt
```

3. Region selection and device compatibility

See 3 Runtime Mechanism and Device Compatibility.

> [!IMPORTANT]
>
> This project includes built-in support for MacBook Pro M-Silicon 14.2-inch Retina displays.
>
> For other screen sizes, feel free to submit a PR. Don’t forget to include INFO and DEBUG outputs.

3. Run the main program

```bash
python main.py
```

## 2 Configuration

The configuration file is located at `config.yaml` in the root directory.

| key                 | description                                                  |
| ------------------- | ------------------------------------------------------------ |
| en                  | English mode                                                 |
| stop_when_no_pullup | Whether to stop fishing when pullup detection times out (i.e., bait is exhausted) |
| random              | Random scale factor; do not modify unless necessary          |
| log_level           | Logging level: INFO / DEBUG                                  |

## 3 Runtime Mechanism and Device Matching

### Event Loop

The entire fishing process is divided into 4 stages:

1. Idle state – press F to start fishing (not_fish)
2. Waiting for fish bite – pull up fish and prepare for reeling (pullup)
3. Fishing phase – complete the reeling process (fish)
4. Completion – reward screen appears, click to close and return to idle state (exp)

Event detection uses image recognition + color recognition + timeout mechanisms. Steps 2 and 4 use fixed screen regions and template similarity matching, while step 3 uses color detection.

### Region Definition

All region definitions are stored in `area.json` in the root directory.

> [!CAUTION]
>
> All coordinates are in mss output coordinates (logical coordinates), not Retina physical pixel coordinates. The actual resolution can be checked during program initialization.

#### Pullup Region

File located at `resource/pullup.png`, image size is 320 × 40.

![pullup](./resource/pullup.png)

#### Fish Region

This refers to the top slider bar in stage 3. Use the inner dark-black background area. When selecting the region, leave enough margin on both sides to prevent the yellow slider from reaching the extreme edge where it may become undetectable.

#### Exp Region

File located at `resource/exp.png`, image size is 78 × 60.

![exp](./resource/exp.png)

## 4 Acknowledgements

Some inspiration comes from:
https://www.bilibili.com/video/BV1eQjh6dE9t/?share_source=copy_web&vd_source=90e59bd1168d818983dd51105bc5e78f