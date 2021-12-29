from transitions.extensions import GraphMachine

from utils import send_text_message, send_image_url


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_state(self, event):
        text = event.message.text
        return text.lower() == "go to state"

    def is_going_to_fsm(self, event):
        text = event.message.text
        return text.lower() == "fsm"

    def on_enter_state(self, event):
        print("I'm entering state")

        reply_token = event.reply_token
        send_text_message(reply_token, "Enter state")

    def on_exit_state(self, event):
        print("Leaving state")

    def on_enter_fsm(self, event):
        print("I'm entering fsm")

        reply_token = event.reply_token
        send_image_url(reply_token, "https://github.com/JoeySmith1103/LineBot1/blob/master/fsm.png?raw=true")

    def is_going_to_multiple(self, event):
        text = event.message.text
        print(text)
        return text.lower() == "check multiple user"

    def on_enter_multiple(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "I'm in multiple")

    def is_going_to_cancel(self, event):
        text = event.message.text
        return text.lower() == "cancel"
    def on_enter_cancel(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "cancel, back to user")
        self.go_back()

    def on_exit_fsm(self, event):
        print("Leaving fsm")
