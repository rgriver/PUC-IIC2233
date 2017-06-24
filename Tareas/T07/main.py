import flask
import requests
import json


class BotController:
    def __init__(self):
        self.token = '415058552:AAH_h5aHopemW9hqMhEZpq1Ajg5LLRunhAM'
        self.telegram_url = 'https://api.telegram.org/bot' + self.token + '/'

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        requests.post(self.telegram_url + method, params)

    def process_message(self, command, *args):
        if command == '/get':
            pass
        elif command == '/post':
            pass
        elif command == '/label':
            pass
        elif command == '/close':
            pass

    def comment_on_issue(self, issue_num):
        pass

bot_controller = BotController()
app = flask.Flask(__name__)

"""
bot_token = '415058552:AAH_h5aHopemW9hqMhEZpq1Ajg5LLRunhAM'
base_url = 'https://api.telegram.org/bot' + bot_token + '/setWebhook'
webhook_data = {'url': 'https://rgriverapp.herokuapp.com/telegram'}
# webhook_data = {'url': 'http://0.0.0.0:8080/telegram'}
requests.post(base_url, data=webhook_data)
"""


@app.route('/github', methods=['POST'])
def handle_github_event():
    data = json.loads(flask.request.data)
    if not data:
        return 'S'
    action = data['action']
    # data = {
    #     'event': 'issues',

    # }
    # data = json.loads(flask.request.data)
    # print('sd')
    #req = requests.post('https://api.github.com/repos/rgriver/T07/hooks',
    #                    data=data)
    return 'ok'


@app.route('/telegram', methods=['POST'])
def handle_telegram_event():
    return flask.Response(status=200)
    # data = json.loads(flask.request.data)
    #chat_id = data['chat']['id']
    # text = data['message']['text']
    bot_controller.send_message(375779180, 'Damn son')
    return flask.Response(status=200)


@app.route('/')
def index():
    return 'ok'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
