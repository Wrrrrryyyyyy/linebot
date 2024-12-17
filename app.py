from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import re

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('jKrk+s4/UE56v4zhupFXUagvcGibXCQW84IW4Zy7cEuALZtcCsWnD6WxYGN6FtpKlzCUer0yQB4GCtfuhR0C4aN4XpewSc+9J808QPdEud/YjwfQzrOlWad+3oQM7SBdrluEJehPJEiZMBYO9uz2iwdB04t89/1O/w1cDnyilFU=')

# 必須放上自己的Channel Secret
handler = WebhookHandler('a1d4fd09fa0d9c5a9d6127d1ac740fff')

line_bot_api.push_message('U66b7a622411ff2975fb04a3d2fb0a8c1', TextSendMessage(text='您好,目前時間是 2024/10/10 14:00 ，請問需要什麼服務呢?'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 訊息處理區塊
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
   if re.match('我想吃飯', message):
        # 顯示 QuickReply 選單
        quick_reply_message = TextSendMessage(
            text='請選擇您想要的選項：',
            quick_reply=QuickReply(items=[
                QuickReplyButton(action=MessageAction(label="主菜", text="主菜")),
                QuickReplyButton(action=MessageAction(label="湯品", text="湯品")),
                QuickReplyButton(action=MessageAction(label="飲料", text="飲料"))
            ])
        )
         line_bot_api.reply_message(event.reply_token, quick_reply_message)
    elif re.match('主菜', message):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="您已成功將【主菜】加入購物車"))
    elif re.match('湯品', message):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="您已成功將【湯品】加入購物車"))
    elif re.match('飲料', message):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="您已成功將【飲料】加入購物車"))
        
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))

# 主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
