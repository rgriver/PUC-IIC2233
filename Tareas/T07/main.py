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

app = flask.Flask(__name__)
bot_controller = BotController()

"""
bot_token = '415058552:AAH_h5aHopemW9hqMhEZpq1Ajg5LLRunhAM'
base_url = 'https://api.telegram.org/bot' + bot_token + '/setWebhook'
webhook_data = {'url': 'https://rgriverapp.herokuapp.com/telegram'}
# webhook_data = {'url': 'http://0.0.0.0:8080/telegram'}
requests.post(base_url, data=webhook_data)
"""


@app.route('/')
def index():
    return 'Damn son'


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
    return action


@app.route('/telegram', methods=['POST'])
def handle_telegram_event():
    data = json.loads(flask.request.data)
    chat_id = data['chat']['id']
    text = data['message']['text']
    bot_controller.send_message(chat_id, 'Damn son')
    return 'telegram section'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
