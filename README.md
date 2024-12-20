# 概要

2024年開発本部忘年会の抽選プログラム
各部長賞への応募に基づいて抽選

## install

```bash
pip install pyinstaller pandas numpy
```

## build

```bash
pyinstaller --onefile --windowed --add-data "present_members.csv:." --add-data "gacha.gif:." --add-data "images:images" gacha.py
```
