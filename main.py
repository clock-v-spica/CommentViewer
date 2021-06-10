import pytchat
import time

# PytchatCoreオブジェクトの取得
# video_idはhttps://....watch?v=より後ろの
livechat = pytchat.create(video_id="g5ao7NJ2vfk")
reqList = []

while livechat.is_alive():
    # チャットデータの取得
    chatdata = livechat.get()
    for c in chatdata.items:
        tmpstr = str(c.message)
        isReq = tmpstr.startswith("【リクエスト】")
        if isReq:
            if tmpstr not in reqList:
                reqList.append(tmpstr)
                print(f"{c.datetime} {c.author.name} {c.message} {c.amountString}")
                '''
                JSON文字列で取得:
                print(c.json())
                '''
    time.sleep(5)
