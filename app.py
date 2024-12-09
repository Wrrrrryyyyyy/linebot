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

    if user_message == "熱門音樂":
        reply_message = AudioSendMessage(
            original_content_url='https://raw.githubusercontent.com/Wrrrrryyyyyy/linebot/main/Persona%205%20-%20Life%20Will%20Change%20(%E4%B8%AD%E8%8B%B1%E6%AD%8C%E8%A9%9E).mp3
',  # 替換為熱門音樂的 URL
            duration=264,000  # 音樂長度（毫秒），例如 240000 表示 4 分鐘
        )
    elif user_message == "放鬆音樂":
        reply_message = AudioSendMessage(
            original_content_url='https://raw.githubusercontent.com/Wrrrrryyyyyy/linebot/main/%E3%80%90%E5%8D%83%E8%88%87%E5%8D%83%E5%B0%8B%E7%89%87%E5%B0%BE%E6%9B%B2%E3%80%91%E6%B0%B8%E9%81%A0%E5%90%8C%E5%9C%A8%20Always%20With%20Me%20%E4%B8%AD%E6%97%A5%E6%AD%8C%E8%A9%9E.mp3
',  # 替換為放鬆音樂的 URL
            duration=229,000  # 音樂長度（毫秒），例如 180000 表示 3 分鐘
        )
    else:
        reply_message = TextSendMessage(text="很抱歉，我目前無法理解這個內容。")
    
    line_bot_api.reply_message(event.reply_token, reply_message)

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)