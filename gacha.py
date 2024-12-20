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

def display_random_person(data, award_name):
    filtered_data = data[(data['配属区分'] == "主務") & (data['賞'] == award_name)]

    if not filtered_data.empty:
        person = filtered_data.sample().iloc[0]
        name_text = f"{person['名前']}（{person['名前（読み仮名）']}）"
        org_text = f"{person['組織フルパス']}"
        result_label.config(text=name_text)
        org_label.config(text=org_text)
        result_label.place(relx=0.5, rely=0.35, anchor='center')
        org_label.place(relx=0.5, rely=0.55, anchor='center')
    else:
        result_label.config(text="該当する人はいません")
        org_label.config(text="")
        result_label.place(relx=0.5, rely=0.5, anchor='center')
        org_label.place_forget()

gif_frame = 0  # ここでgif_frameを初期化

def play_gif():
    global gif_label, gif_frame, selected_award

    result_label.place_forget()
    org_label.place_forget()

    gif_frame += 1
    try:
        gif_label.config(image=gif_frames[gif_frame])
        window.after(180, play_gif)
    except IndexError:
        gif_frame = 0
        display_random_person(data, selected_award)  # 選択された賞に基づいて抽選

def show_award_image(award_name):
    global selected_award
    selected_award = award_name

    image_path = get_resource_path(f"images/{award_name}.png")
    award_image = Image.open(image_path)
    award_photo = ImageTk.PhotoImage(award_image)
    gif_label.config(image=award_photo)
    gif_label.image = award_photo

    for button in award_buttons:
        button.pack_forget()

    start_button.place(relx=0.5, rely=0.8, anchor='center')
    start_button.config(command=play_gif)

def show_main_menu():
    # メインメニューを表示
    gif_label.place_forget()
    start_button.place_forget()
    result_label.place_forget()
    org_label.place_forget()
    for button in award_buttons:
        button.pack()

csv_path = "present_members.csv"
gif_path = get_resource_path("gacha.gif")

data = load_data(csv_path)

# Tkinterウィンドウの初期化
window = tk.Tk()
window.title("2024年忘年会抽選ガチャ")

# フォントスタイルの設定
name_font = tkFont.Font(family="Lucida Grande", size=45)
org_font = tkFont.Font(family="Lucida Grande", size=18)

# 名前と読み仮名を表示するラベル
result_label = tk.Label(window, text="", font=name_font, bg="white")
# 組織名を表示するラベル
org_label = tk.Label(window, text="", font=org_font, bg="white")

# GIFの読み込みとフレームの準備
gif = Image.open(gif_path)
gif_frames = []
for i in range(gif.n_frames):
    gif.seek(i)
    frame = ImageTk.PhotoImage(image=gif.copy())
    gif_frames.append(frame)

gif_label = ttk.Label(window)
gif_label.pack()

start_button = ttk.Button(window, text="ガチャを回す")
start_button.pack()

# 賞のボタンを作成
award_names = [
    "FDG首藤さん賞", "GPF永井さん賞", "INF_INF-DO大久保(将)さん賞",
    "INF-DO万年さん賞", "IT鈴木さん賞", "SEC大本さん賞",
    "JG1_JG4合津さん賞", "JG1大久保（吉）さん賞", "JG4嶺岸さん賞",
    "DT森田さん賞", "INF舟橋さん賞"
]

award_buttons = []
for award in award_names:
    button = ttk.Button(window, text=award, command=lambda a=award: show_award_image(a))
    award_buttons.append(button)

show_main_menu()

window.mainloop()