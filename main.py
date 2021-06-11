import pytchat
import time
import threading
import logging
import sys
import os

import tkinter as tk
from tkinter import ttk

from pytchat.core_multithread.livechat import LiveChat

logging.basicConfig(stream=sys.stderr)
LOGLEVEL = os.environ.get('LOGLEVEL', 'WARN').upper()
print("Setting LogLevel to {}".format(LOGLEVEL))
logging.getLogger("ReqView").setLevel(LOGLEVEL)
logging.basicConfig(level=LOGLEVEL)

livechat = None
root = None
listbox = None
url_entry = None


def is_livechat_alive():
    global livechat
    if livechat is None:
        return

    logger = logging.getLogger("ReqView")
    logger.info("infoinfo")
    logger.warn("warnwarn")

    if not livechat.is_alive():
        root.destroy()
        print("destroy")


def update_listbox(chatdata):
    global listbox
    logger = logging.getLogger("ReqView")
    logger.info("infoinfo")
    logger.warn("warnwarn")
    print("update listbox")
    for c in chatdata.items:
        listbox.insert(tk.END, str(c.message))
        print(f"{c.datetime} [{c.author.name}]- {c.message}")
        chatdata.tick()


def init_livechat():
    global livechat
    global url_entry
    livechat = LiveChat(video_id=str(url_entry.get()), callback=update_listbox)
    print("init livechat")


def main():
    global root
    global livechat
    global url_entry
    global listbox
    # rootメインウィンドウの設定
    root = tk.Tk()
    root.title("YouTubeRequestViewer")
    root.geometry("640x320")

    # メインフレームの作成と設置
    frame = tk.Frame(root)
    frame.pack(padx=20, pady=10)

    # 各種ウィジェットの作成
    url_entry = ttk.Entry(frame, text="URL")
    startbutton = ttk.Button(
        frame, text="Start", command=init_livechat)

    scrollbar_frame = tk.Frame(root)
    scrollbar_frame.pack()
    listbox = tk.Listbox(scrollbar_frame)
    listbox.pack(side='left')
    scroll_bar = tk.Scrollbar(scrollbar_frame, command=listbox.yview)
    scroll_bar.pack(side='right', fill=tk.Y)
    listbox.config(yscrollcommand=scroll_bar.set)

    # 各種ウィジェットの設置
    startbutton.pack(side='left')
    url_entry.pack(side='left')

    root.after(1, is_livechat_alive)
    root.mainloop()
    livechat.terminate()


main()
