import requests
from repository_controller import RepositoryController
from command_interpreter import CommandInterpreter


class BotController:
    def __init__(self, repo_controller):
        self.token = '415058552:AAH_h5aHopemW9hqMhEZpq1Ajg5LLRunhAM'
        self.telegram_url = 'https://api.telegram.org/bot' + self.token + '/'
        self.repo_controller = repo_controller
        self.command_interpreter = CommandInterpreter()

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        requests.post(self.telegram_url + method, params)

    def process_message(self, chat_id, input_message):
        if chat_id not in self.get_chats():
            self.add_chat(chat_id)
            # self.chat_ids.append(chat_id)
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
        for chat_id in self.get_chats():
            self.send_message(chat_id, message)

    def notify_of_issue_opening(self, issue):
        try:
            message = "[{}]\n".format(issue['user']['login'])  # author
            message += "[#{} - {}]\n".format(issue['number'], issue['title'])
            message += issue['body'] + '\n'
            message += "[Link: {}]".format(issue['html_url'])
            chat_ids = self.get_chats()
            for chat_id in chat_ids:
                self.send_message(chat_id, message)
        except Exception as e:
            for chat_id in self.get_chats():
                self.send_message(chat_id, 'INTERNAL SERVER ERROR: ' + str(e))

    @staticmethod
    def add_chat(chat_id):
        with open('chats.txt', 'a') as f:
            f.write(str(chat_id) + '\n')

    @staticmethod
    def get_chats():
        try:
            with open('chats.txt', 'r') as f:
                data = (int(i.strip()) for i in f.readlines())
        except Exception:
            data = []
        return data

