import flask
import requests
import json


class RepositoryController:
    def __init__(self):
        self.repo_name = 'T07-test'

    def create_comment(self, issue_num, message):
        url = 'https://api.github.com/repos/rgriver/{}/issues/{}/comments'.\
            format(self.repo_name, issue_num)
        data = {'body': message}
        requests.post(url, json.dumps(data))

    def assign_label(self):
        pass

    def close_issue(self):
        pass


class BotController:
    def __init__(self):
        self.token = '415058552:AAH_h5aHopemW9hqMhEZpq1Ajg5LLRunhAM'
        self.telegram_url = 'https://api.telegram.org/bot' + self.token + '/'
        self.chat_ids = []
        self.repo_controller = RepositoryController()

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        requests.post(self.telegram_url + method, params)

    def process_message(self, chat_id, message):
        if chat_id not in self.chat_ids:
            self.chat_ids.append(chat_id)
        command = '/post'
        if command == '/get':
            pass
        elif command == '/post':
            self.repo_controller.create_comment(4, 'My comment')
        elif command == '/label':
            pass
        elif command == '/close':
            pass
        else:
            self.send_message(375779180, str(self.chat_ids))

    def comment_on_issue(self, issue_num):
        pass

    def send_message_to_all_users(self, message):
        for chat_id in self.chat_ids:
            self.send_message(chat_id, message)

    def notify_of_issue_opening(self, issue):
        try:
            message = "[{}]\n".format(issue['user']['login'])  # author
            message += "[#{} - {}]\n".format(issue['number'], issue['title'])
            message += issue['body'] + '\n'
            message += "[Link: {}]".format(issue['html_url'])
            for chat_id in self.chat_ids:
                self.send_message(chat_id, message)
        except Exception as e:
            for chat_id in self.chat_ids:
                self.send_message(chat_id, 'INTERNAL SERVER ERROR: ' + str(e))
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
    try:
        data = json.loads(flask.request.data)
        action = data['action']
        if str(action) == 'opened':
            bot_controller.notify_of_issue_opening(data['issue'])
    except Exception as e:
        message = str(e)
        bot_controller.send_message_to_all_users(message)
    # data = {
    #     'event': 'issues',

    # }
    # data = json.loads(flask.request.data)
    # print('sd')
    #req = requests.post('https://api.github.com/repos/rgriver/T07/hooks',
    #                    data=data)
    return flask.Response(status=200)


@app.route('/telegram', methods=['POST'])
def handle_telegram_event():
    chat_id = 375779180
    try:
        data = json.loads(flask.request.data)
        text = data['message']['text']
        chat_id = data['message']['chat']['id']
        message = 'Chat id :' + str(chat_id)
    except Exception as e:
        message = 'INTERNAL SERVER ERROR: ' + str(e)
    # bot_controller.send_message(chat_id, message)
    bot_controller.process_message(chat_id, message)
    return flask.Response(status=200)


@app.route('/')
def index():
    return 'ok'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
