import flask
import requests
import json
import re


class RepositoryController:
    def __init__(self):
        self.owner = 'rgriver'
        self.repo_name = 'T07-test'
        self.credentials = ('T07bot',
                            '8b9c17535a9ba3f80c5f0da2306b3e2bf951c493')
        self.owner_credentials = ('rgriver',
                                  '3e99ab62d354ecc3e7ff05eb949524895fef15fe')

    def create_comment(self, issue_num, message):
        url = 'https://api.github.com/repos/{}/{}/issues/{}/comments'.\
            format(self.owner, self.repo_name, issue_num)
        data = {'body': message}
        r = requests.post(url, json.dumps(data), auth=self.credentials)
        if r.status_code == 201:
            message = 'New comment created!'
        else:
            message = "Sorry, I couldn't create your comment."
        return message

    def add_label(self, issue_num, label):
        url = 'https://api.github.com/repos/{}/{}/issues/{}/labels'. \
            format(self.owner, self.repo_name, issue_num)
        data = [label]
        r = requests.post(url, data=json.dumps(data), auth=self.credentials)
        if r.status_code == 200:
            message = "Label '{}' added to issue #{}.".format(label, issue_num)
        else:
            message = "Sorry, I couldn't add the label you provided."
        return message

    def close_issue(self, issue_num):
        url = 'https://api.github.com/repos/{}/{}/issues/{}'. \
            format(self.owner, self.repo_name, issue_num)
        r = requests.get(url)
        if r.status_code != 200:
            return "It seems that the provided issue doesn't exist."
        if r.json()['state'] == 'closed':
            return 'This issue is already closed.'
        url = 'https://api.github.com/repos/{}/{}/issues/{}'\
            .format(self.owner, self.repo_name, issue_num)
        data = {'state': 'closed'}
        r = requests.patch(url, data=json.dumps(data), auth=self.credentials)
        if r.status_code == 200:
            return 'Issue #{} closed!'.format(issue_num)
        else:
            return "Sorry, I couldn't close the specified issue."

    def get_issue(self, issue_num):
        url = 'https://api.github.com/repos/{}/{}/issues/{}'.\
            format(self.owner, self.repo_name, issue_num)
        r = requests.get(url)
        if r.status_code == 200:
            issue = r.json()
            message = "[{}]\n".format(issue['user']['login'])
            message += "[#{} - {}]\n".format(issue['number'], issue['title'])
            message += issue['body'] + '\n'
            message += "[Link: {}]".format(issue['html_url'])
        else:
            message = \
                "Sorry, I couldn't get the issue you requested (Error {}).".\
                format(r.status_code)
        return message


class CommandInterpreter:
    def __init__(self):
        self.get_pattern = re.compile(r'^(/get)\s+([0-9]+)$')
        self.post_pattern = re.compile(r'^(/post)\s+([0-9]+)\s+[*](.+)$')
        self.label_pattern = \
            re.compile(r'^(/label)\s+([0-9]+)\s+([a-zA-Z0-9\s]+)$')
        self.close_pattern = re.compile(r'^(/close)\s+([0-9]+)$')

    def process_text(self, raw_text):
        text = raw_text.strip()
        groups = ('Error', "Sorry, I didn't get that.")
        if self.get_pattern.match(text):
            groups = self.get_pattern.match(text).groups()
        elif self.post_pattern.match(text):
            groups = self.post_pattern.match(text).groups()
        elif self.label_pattern.match(text):
            groups = self.label_pattern.match(text).groups()
        elif self.close_pattern.match(text):
            groups = self.close_pattern.match(text).groups()
        return groups


class BotController:
    def __init__(self):
        self.token = '415058552:AAH_h5aHopemW9hqMhEZpq1Ajg5LLRunhAM'
        self.telegram_url = 'https://api.telegram.org/bot' + self.token + '/'
        self.chat_ids = []
        self.repo_controller = RepositoryController()
        self.command_interpreter = CommandInterpreter()

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        requests.post(self.telegram_url + method, params)

    def process_message(self, chat_id, input_message):
        if chat_id not in self.chat_ids:
            self.chat_ids.append(chat_id)
        groups = self.command_interpreter.process_text(input_message)
        if groups[0] == '/get':
            message = self.repo_controller.get_issue(*groups[1:])
        elif groups[0] == '/post':
            message = self.repo_controller.create_comment(*groups[1:])
        elif groups[0] == '/label':
            message = self.repo_controller.add_label(*groups[1:])
        elif groups[0] == '/close':
            message = self.repo_controller.close_issue(*groups[1:])
        else:
            message = groups[1]
        self.send_message(chat_id, message)

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


class MyApp(flask.Flask):
    def __init__(self):
        super(MyApp, self).__init__(__name__)
        self.bot_controller = BotController()
        self.add_url_rule('/', view_func=self.index)
        # self.add_url_rule('/github', view_func=self.handle_github_event,
        #                   methods=['POST'])
        # self.add_url_rule('/telegram', view_func=self.handle_telegram_event,
        #                   methods=['POST'])
    """
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
    """
    def index(self):
        """
        text = "Lista de ID's:\n"
        for chat_id in self.bot_controller.chat_ids:
            text += str(chat_id) + '\n'
        return text
        """
        return 'ok'

"""
bot_controller = BotController()
app = flask.Flask(__name__)


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
        message = data['message']['text']
        chat_id = data['message']['chat']['id']
    except Exception as e:
        message = 'INTERNAL SERVER ERROR: ' + str(e)
    # bot_controller.send_message(chat_id, message)
    bot_controller.process_message(chat_id, message)
    return flask.Response(status=200)


@app.route('/')
def index():
    return 'ok'

"""

app = flask.Flask(__name__)


@app.route('/')
def index():
    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    # app = MyApp()
    # app.run(host='0.0.0.0', port=8080)
