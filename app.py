import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from machine import createMachine
from utils import send_text_message

load_dotenv()

machine = {}

app = Flask(__name__, static_url_path="")

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)
    print(111111111111111111111111111111111111111)
    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        print(event.message.text)
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue

        if event.source.user_id not in machine:
            machine[event.source.user_id] = createMachine()
        response = machine[event.source.user_id].advance(event)
        if response == False:
            send_text_message(event.reply_token, "Not Entering any State")

    return "OK"


a = TocMachine(
    states=["user", "state", "fsm", "multiple", "cancel"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state",
            "conditions": "is_going_to_state",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "fsm",
            "conditions": "is_going_to_fsm",
        },
        {
            "trigger": "advance",
            "source": "state",
            "dest": "multiple",
            "conditions": "is_going_to_multiple"
        },
        {
            "trigger": "advance",
            "source": "multiple",
            "dest": "state",
            "conditions": "is_going_to_state"
        },
        {
            "trigger": "advance",
            "source": "state",
            "dest": "cancel",
            "conditions": "is_going_to_cancel"
        },
        {
            "trigger": "advance",
            "source": "fsm",
            "dest": "cancel",
            "conditions": "is_going_to_cancel"
        },
        {"trigger": "go_back", "source": ["cancel"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    a.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
    show_fsm()
