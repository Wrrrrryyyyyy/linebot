# -*- coding: utf-8 -*-

#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('jKrk+s4/UE56v4zhupFXUagvcGibXCQW84IW4Zy7cEuALZtcCsWnD6WxYGN6FtpKlzCUer0yQB4GCtfuhR0C4aN4XpewSc+9J808QPdEud/YjwfQzrOlWad+3oQM7SBdrluEJehPJEiZMBYO9uz2iwdB04t89/1O/w1cDnyilFU=')

# 必須放上自己的Channel Secret
handler = WebhookHandler('a1d4fd09fa0d9c5a9d6127d1ac740fff')

line_bot_api.push_message('U66b7a622411ff2975fb04a3d2fb0a8c1', TextSendMessage(text='您好,目前時間是 2024/10/10 14:00 ，請問需要什麼服務呢?'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    if user_message == "心情好":
        reply_message = StickerSendMessage(
            package_id='446',  # 請替換為您想使用的貼圖包 ID
            sticker_id='1992'  # 請替換為您想使用的貼圖 ID
        )
    elif user_message == "心情不好":
        reply_message = StickerSendMessage(
            package_id='789',  # 請替換為您想使用的貼圖包 ID
            sticker_id='10880'   # 請替換為您想使用的貼圖 ID
        )
    else:
        reply_message = TextSendMessage(text="很抱歉，我目前無法理解這個內容。")
    
    line_bot_api.reply_message(event.reply_token, reply_message)

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)