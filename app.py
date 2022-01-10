from flask import Flask, request, abort
import requests
from config import *
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    keyword = event.message.text
    res = requests.get('https://covid19.ddc.moph.go.th/api/Cases/today-cases-all')
    dict_covid = res.json()
    new_case = dict_covid[0]['new_case']
    total_case = dict_covid[0]['total_case']
    new_death = dict_covid[0]['new_death']
    total_death = dict_covid[0]['total_death']
    new_recovered = dict_covid[0]['new_recovered']
    total_recovered = dict_covid[0]['total_recovered']
    update_date = dict_covid[0]['update_date']
    # print(keyword)
    if keyword == 'ผู้ติดเชื้อวันนี้':
        reply_message = f'วันนี้มีผู้ติดเชื่อเพิ่ม {new_case} คน'
        
    elif keyword == 'ผู้ติดเชื้อสะสม':
        reply_message = f'ผู้ติดเชื้อสะสมจำนวน {total_case} คน'
        
    elif keyword == 'เสียชีวิติวันนี้':
        reply_message = f'ผู้เสียชีวิติวันนี้ จำนวน {new_death} คน'
    elif keyword == 'รักษาหายวันนี้':
        reply_message = f'ผู้รักษาหายวันนี้ จำนวน {new_recovered} คน'
    elif keyword == 'เสียชีวิตสะสม':
        reply_message = f'ผู้เสียชีวิตสะสม จำนวน {total_death} คน'
    elif keyword == 'ติดต่อผู้พัฒนา':
        reply_message = f'''====ช่องทางการติดต่อ====
        github : neon-lab
        facebook : NE OE
        line_id : ikwan
        '''
    else:
        reply_message = f'กรุณาเลือกเมนูอึกครั้ง'

    line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message))
