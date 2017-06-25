import flask
import json
from bot_controller import BotController


class App(flask.Flask):
    def __init__(self, x):
        super(App, self).__init__(x)
        self.bot_controller = BotController()
        self.add_url_rule('/', view_func=self.index)
        self.add_url_rule('/github', view_func=self.handle_github_event,
                          methods=['POST'])
        self.add_url_rule('/telegram', view_func=self.handle_telegram_event,
                          methods=['POST'])

    def handle_github_event(self):
        try:
            data = json.loads(flask.request.data)
            action = data['action']
            if str(action) == 'opened':
                self.bot_controller.notify_of_issue_opening(data['issue'])
        except Exception as e:
            message = str(e)
            self.bot_controller.send_message_to_all_users(message)
        return flask.Response(status=200)

    def handle_telegram_event(self):
        chat_id = 375779180
        try:
            data = json.loads(flask.request.data)
            message = data['message']['text']
            chat_id = data['message']['chat']['id']
        except Exception as e:
            message = 'INTERNAL SERVER ERROR: ' + str(e)
        # bot_controller.send_message(chat_id, message)
        self.bot_controller.process_message(chat_id, message)
        return flask.Response(status=200)

    def index(self):
        text = "Registro de ID's de chats:\n"
        for chat_id in self.bot_controller.chat_ids:
            text += '    ' + str(chat_id) + '\n'
        return text

