import pytchat
import time
import random

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
pf_entry = None
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
    global pf_entry
    prefix = pf_entry.get()
    print("update listbox")
    for c in chatdata.items:
        comment = str(c.message)
        if comment.startswith(prefix):
            request = comment.replace(prefix, '')
            if request not in ReqList:
                ReqList.append(request)
                listbox.insert(tk.END, request)
                # print(f"{c.datetime} [{c.author.name}]- {c.message}")
        chatdata.tick()


def init_livechat():
    global livechat
    global url_entry
    global listbox
    global listbox2
    global ReqList
    listbox.delete(0, tk.END)
    listbox2.delete(0, tk.END)
    ReqList = []
    livechat = LiveChat(video_id=str(url_entry.get()).replace(
        'https://www.youtube.com/watch?v=', ''), callback=update_listbox)
    print("init livechat")


def pause_livechat():
    global livechat
    livechat.pause()
    print("stop callback")


def resume_livechat():
    global livechat
    livechat.resume()
    print("resume callback")


def random_select():
    global listbox
    target_index = random.randrange(listbox.size())
    listbox.select_clear(0, tk.END)
    listbox.selection_set(target_index)
    print(target_index)
    print("random picked")


def setlist_clear():
    global listbox2
    listbox2.delete(0, tk.END)


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
    target_index = listbox2.curselection()
    listbox2.delete(target_index)


def main():
    global root
    global livechat
    global url_entry
    global pf_entry
    global listbox
    global listbox2
    # rootメインウィンドウの設定
    root = tk.Tk()
    root.title("YouTubeRequestViewer")
    root.geometry("480x540")
    root.resizable(False, False)

    # メインフレームの作成と設置
    frame1 = ttk.Frame(root)
    frame1.pack(padx=20, pady=10)
    frame2 = ttk.Frame(root)
    frame2.pack(padx=20, pady=0)
    frame_main = ttk.Frame(root)
    frame_main.pack(padx=20, pady=10)

    # 各種ウィジェットの作成・設置
    url_entry = ttk.Entry(frame1, text="URL")
    url_entry.insert(0, "URL")
    pf_entry = ttk.Entry(frame1, text="Prefix")
    pf_entry.insert(0, "【リクエスト】")
    start_button = ttk.Button(frame1, text="Start", command=init_livechat)
    pause_button = ttk.Button(frame2, text="Pause", command=pause_livechat)
    resume_button = ttk.Button(frame2, text="Resume", command=resume_livechat)
    random_button = ttk.Button(frame2, text="Random", command=random_select)
    clear_button = ttk.Button(frame2, text="SetClear", command=setlist_clear)
    url_entry.pack(side='left')
    pf_entry.pack(side='left')
    start_button.pack(side='left')
    pause_button.pack(side='left')
    resume_button.pack(side='left')
    random_button.pack(side='left')
    clear_button.pack(side='left')

    scrollbar_frame = ttk.Frame(frame_main)
    scrollbar_frame.grid(row=1, column=0, columnspan=2)
    listbox = tk.Listbox(scrollbar_frame, width=18,
                         height=17, font=("Meiryo", 12))
    listbox.pack(side='left', fill=tk.BOTH)
    scroll_bar = tk.Scrollbar(scrollbar_frame, command=listbox.yview)
    scroll_bar.pack(side='right', fill=tk.Y)
    listbox.config(yscrollcommand=scroll_bar.set)

    scrollbar_frame2 = ttk.Frame(frame_main)
    scrollbar_frame2.grid(row=1, column=2, columnspan=2)
    listbox2 = tk.Listbox(scrollbar_frame2, width=18,
                          height=17, font=("Meiryo", 12))
    listbox2.pack(side='left', fill=tk.BOTH)
    scroll_bar2 = tk.Scrollbar(scrollbar_frame2, command=listbox2.yview)
    scroll_bar2.pack(side='right', fill=tk.Y)
    listbox2.config(yscrollcommand=scroll_bar2.set)

    listbox.bind("<Double-Button-1>", listbox_dbclick)
    listbox2.bind("<Double-Button-1>", listbox2_dbclick)

    root.after(1, is_livechat_alive)
    root.mainloop()
    livechat.terminate()


if __name__ == '__main__':
    main()
