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

    while livechat.is_alive():
        # チャットデータの取得
        chatdata = livechat.get()
        for c in chatdata.items:
            tmpstr = str(c.message)
            isReq = tmpstr.startswith("")  # prefix指定
            if isReq:  # prefixを持つ？
                if tmpstr not in reqList:  # 重複していない？
                    reqList.append(tmpstr)
                    ckbox = tk.Checkbutton(root, text=tmpstr)
                    ckbox.pack()
                    print(
                        f"{c.datetime} {c.author.name} {c.message} {c.amountString}")
                    '''
                    JSON文字列で取得:
                    print(c.json())
                    '''
        time.sleep(5)


if __name__ == '__main__':
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
