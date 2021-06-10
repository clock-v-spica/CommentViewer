import tkinter
import pytchat
import time

import tkinter as tk
from tkinter import ttk


def checkComment(url):
    # PytchatCoreオブジェクトの取得
    # video_idはhttps://....watch?v=より後ろの
    livechat = pytchat.create(video_id=str(url))
    reqList = []
    reqBool = {}

    rowList = 1

    while livechat.is_alive():
        # チャットデータの取得
        chatdata = livechat.get()
        for c in chatdata.items:
            tmpstr = str(c.message)
            isReq = tmpstr.startswith("")
            if isReq:
                if tmpstr not in reqList:
                    reqList.append(tmpstr)
                    reqBool[rowList-1] = tkinter.BooleanVar()
                    chk = tkinter.Checkbutton(
                        root, variable=reqBool[rowList-1], text=reqList[rowList-1])
                    chk.place(x=0, y=0 + (rowList * 24))
                    rowList += 1
                    print(
                        f"{c.datetime} {c.author.name} {c.message} {c.amountString}")
                    '''
                    JSON文字列で取得:
                    print(c.json())
                    '''
        time.sleep(5)


# rootメインウィンドウの設定
root = tk.Tk()
root.title("application")
root.geometry("640x320")

# メインフレームの作成と設置
frame = tk.Frame(root)
frame.pack(padx=20, pady=10)

# 各種ウィジェットの作成
entry_ttk = ttk.Entry(frame, text="URL")
button_ttk = ttk.Button(frame, text="Start",
                        command=lambda: checkComment(str(entry_ttk.get())))
# 各種ウィジェットの設置
button_ttk.grid(row=0, column=0)
entry_ttk.grid(row=0, column=1)
root.mainloop()
