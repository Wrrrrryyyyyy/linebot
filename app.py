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
    if re.match('電影推薦', message):
        image_carousel_template_message = TemplateSendMessage(
            alt_text='電影推薦',
            template=ImageCarouselTemplate(
                columns=[
                    # 第一部電影
                    ImageCarouselColumn(
                        image_url='https://m.media-amazon.com/images/M/MV5BYTg2Yjc5MzItNzVmMi00MTllLWI2MDQtOTYyOWNjYWIxNzEzXkEyXkFqcGc@._V1_.jpg',  # 替換為電影1的封面圖片URL
                        action=PostbackAction(
                            label='Sonic',
                            display_text='電影1 詳情',
                            data='1/12'
                        )
                    ),
                    # 第二部電影
                    ImageCarouselColumn(
                        image_url='https://m.media-amazon.com/images/M/MV5BMDBiYzk0YTMtNWRiYi00YWY0LWE3NjgtYmJiYTAwZmYzOTM0XkEyXkFqcGc@._V1_.jpg',  # 替換為電影2的封面圖片URL
                        action=PostbackAction(
                            label='Sonic2',
                            display_text='電影2 詳情',
                            data='11/3'
                        )
                    ),
                    # 第三部電影
                    ImageCarouselColumn(
                        image_url='https://dx35vtwkllhj9.cloudfront.net/paramountpictures/sonic-the-hedgehog-3-coppa/images/regions/us/onesheet_synopsis.jpg',  # 替換為電影3的封面圖片URL
                        action=PostbackAction(
                            label='Sonic3',
                            display_text='電影3 詳情',
                            data='12/27'
                        )
                    ),
                    # 第四部電影
                    ImageCarouselColumn(
                        image_url='https://m.media-amazon.com/images/M/MV5BMzMwMTAwODczN15BMl5BanBnXkFtZTgwMDk2NDA4MTE@._V1_.jpg',  # 替換為電影4的封面圖片URL
                        action=PostbackAction(
                            label='訓龍高手2',
                            display_text='電影4 詳情',
                            data='movie=4'
                        )
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, image_carousel_template_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))

# 主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
