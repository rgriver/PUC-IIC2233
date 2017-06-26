import flask
import json
from bot_controller import BotController
from repository_controller import RepositoryController
from issue_helper import IssueHelper


class App(flask.Flask):
    def __init__(self, x):
        super(App, self).__init__(x)
        self.repo_controller = RepositoryController()
        self.bot_controller = BotController(self.repo_controller)
        self.issue_helper = IssueHelper()
        self.add_url_rule('/', view_func=self.index)
        self.add_url_rule('/github', view_func=self.handle_github_event,
                          methods=['POST'])
        self.add_url_rule('/telegram', view_func=self.handle_telegram_event,
                          methods=['POST'])

    def handle_github_event(self):
        try:
            data = json.loads(flask.request.data)
            action = data['action']
            issue_num = data['issue']['number']
            if str(action) == 'opened':
                solution = self.issue_helper.find_solution(
                    data['issue']['body'])
                if solution is not None:
                    self.repo_controller.create_comment(issue_num, solution)
                    self.repo_controller.add_auto_issue(issue_num)
                self.bot_controller.notify_of_issue_opening(data['issue'])
            elif str(action) == 'closed':
                self.repo_controller.add_google_label(issue_num)
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
        text = "Registro de ID's de chats: "
        for chat_id in self.bot_controller.get_chats():
            text += str(chat_id) + ', '
        return text
