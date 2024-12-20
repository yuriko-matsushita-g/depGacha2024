import os
import sys
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from PIL import Image, ImageTk
import pandas as pd
import random

def get_resource_path(relative_path):
    """リソースのファイルパスを取得する。"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def load_data(csv_filename):
    # CSVファイルの読み込み
    csv_path = get_resource_path(csv_filename)
    return pd.read_csv(csv_path)

def display_random_person(data):
    # 「配属区分」が"主務"である行だけをフィルタリング
    filtered_data = data[data['配属区分'] == "主務"]

    # フィルタリングされたデータからランダムに選択
    if not filtered_data.empty:
        person = filtered_data.sample().iloc[0]
        name_text = f"{person['名前']}（{person['名前（読み仮名）']}）"
        org_text = f"{person['組織フルパス']}"
        result_label.config(text=name_text)
        org_label.config(text=org_text)
        # 配置を更新
        result_label.place(relx=0.5, rely=0.35, anchor='center')
        org_label.place(relx=0.5, rely=0.55, anchor='center')
    else:
        result_label.config(text="該当する人はいません")
        org_label.config(text="")
        # 配置を更新
        result_label.place(relx=0.5, rely=0.5, anchor='center')
        org_label.place_forget()

gif_frame = 0

def play_gif():
    # GIFアニメーションの再生
    global gif_label, gif_frame

    # GIF再生開始時にテキストを非表示にする
    result_label.place_forget()
    org_label.place_forget()

    gif_frame += 1
    try:
        gif_label.config(image=gif_frames[gif_frame])
        window.after(180, play_gif)  # 再生速度を調整
    except IndexError:
        gif_frame = 0
        display_random_person(data)  # GIF再生終了時にテキストを表示

csv_path = "members.csv"
gif_path = get_resource_path("gacha.gif")

data = load_data(csv_path)

# Tkinterウィンドウの初期化
window = tk.Tk()
window.title("ガチャガチャアプリケーション")

# GIFの読み込みとフレームの準備
gif = Image.open(gif_path)
gif_frames = []
for i in range(gif.n_frames):
    gif.seek(i)
    frame = ImageTk.PhotoImage(image=gif.copy())
    gif_frames.append(frame)

gif_label = ttk.Label(window, image=gif_frames[0])
gif_label.pack()

start_button = ttk.Button(window, text="ガチャを回す", command=play_gif)
start_button.pack()

# フォントスタイルの設定
name_font = tkFont.Font(family="Lucida Grande", size=45)
org_font = tkFont.Font(family="Lucida Grande", size=18)

# 名前と読み仮名を表示するラベル
result_label = tk.Label(window, text="", font=name_font, bg="white")
# 組織名を表示するラベル
org_label = tk.Label(window, text="", font=org_font, bg="white")

# ラベルを最初は表示しない
result_label.place_forget()
org_label.place_forget()

window.mainloop()