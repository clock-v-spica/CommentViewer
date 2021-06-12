import pytchat
import time

import logging
import sys
import os

import tkinter as tk
from tkinter import ttk

from pytchat.core_multithread.livechat import LiveChat

# logging.basicConfig(stream=sys.stderr)
# LOGLEVEL = os.environ.get('LOGLEVEL', 'WARN').upper()
# print("Setting LogLevel to {}".format(LOGLEVEL))
# logging.getLogger("ReqView").setLevel(LOGLEVEL)
# logging.basicConfig(level=LOGLEVEL)

# logger = logging.getLogger("ReqView")
# logger.info("infoinfo")
# logger.warn("warnwarn")

livechat = None
root = None
listbox = None
listbox2 = None
url_entry = None
ReqList = []


def is_livechat_alive():
    global livechat
    if livechat is None:
        return

    if not livechat.is_alive():
        root.destroy()
        print("destroy")


def update_listbox(chatdata):
    global listbox
    global ReqList
    prefix = ""
    print("update listbox")
    for c in chatdata.items:
        comment = str(c.message)
        if comment.startswith(prefix):
            if comment not in ReqList:
                listbox.insert(tk.END, comment.replace(prefix, ''))
                print(f"{c.datetime} [{c.author.name}]- {c.message}")
        chatdata.tick()


def init_livechat():
    global livechat
    global url_entry
    livechat = LiveChat(video_id=str(url_entry.get()).replace(
        'https://www.youtube.com/watch?v=', ''), callback=update_listbox)
    print("init livechat")


def listbox_dbclick(event):
    global listbox
    global listbox2
    target_index = listbox.curselection()
    listbox2.insert(tk.END, str(listbox.get(target_index)))
    selected_index = tk.ACTIVE
    listbox.delete(selected_index)


def listbox_rclick(event):
    global listbox
    selected_index = tk.ACTIVE
    listbox.delete(selected_index)


def listbox2_dbclick(event):
    global listbox2
    listbox2.delete(0, tk.END)


def main():
    global root
    global livechat
    global url_entry
    global listbox
    global listbox2
    # rootメインウィンドウの設定
    root = tk.Tk()
    root.title("YouTubeRequestViewer")
    root.geometry("640x320")

    # メインフレームの作成と設置
    frame1 = ttk.Frame(root)
    frame1.pack(padx=20, pady=10)
    frame2 = ttk.Frame(root)
    frame2.pack(padx=20, pady=10)

    # 各種ウィジェットの作成・設置
    url_entry = ttk.Entry(frame1, text="URL")
    startbutton = ttk.Button(
        frame1, text="Start", command=init_livechat)
    startbutton.pack(side='left')
    url_entry.pack(side='left')

    scrollbar_frame = ttk.Frame(frame2)
    scrollbar_frame.grid(row=1, column=0, columnspan=2)
    listbox = tk.Listbox(scrollbar_frame, width=30, height=15)
    listbox.pack(side='left', fill=tk.BOTH)
    scroll_bar = tk.Scrollbar(scrollbar_frame, command=listbox.yview)
    scroll_bar.pack(side='right', fill=tk.Y)
    listbox.config(yscrollcommand=scroll_bar.set)

    scrollbar_frame2 = ttk.Frame(frame2)
    scrollbar_frame2.grid(row=1, column=2, columnspan=2)
    listbox2 = tk.Listbox(scrollbar_frame2, width=30, height=15)
    listbox2.pack(side='left')
    scroll_bar2 = tk.Scrollbar(scrollbar_frame2, command=listbox2.yview)
    scroll_bar2.pack(side='right', fill=tk.Y)
    listbox2.config(yscrollcommand=scroll_bar2.set)

    listbox.bind("<Double-Button-1>", listbox_dbclick)
    listbox.bind("<Button-3>", listbox_rclick)
    listbox2.bind("<Double-Button-1>", listbox2_dbclick)

    root.after(1, is_livechat_alive)
    root.mainloop()
    livechat.terminate()


if __name__ == '__main__':
    main()
