import requests
import json


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
        comments_url = 'https://api.github.com/repos/{}/{}/issues/{}/comments'\
            .format(self.owner, self.repo_name, issue_num)
        cr = requests.get(comments_url)
        if cr.status_code == 200:
            comments_text = ''
            if cr.json():
                comments_text += '*** Comments ***\n'
                for comment in cr.json():
                    comments_text += '{} commented at {}:\n{}\n\n'\
                        .format(comment['user']['login'],
                                comment['created_at'],
                                comment['body'])
        else:
            return "Sorry, I couldn't complete your request (Error {}).".\
                format(cr.status_code)
        if r.status_code == 200:
            issue = r.json()
            message = "[{}]\n\n".format(issue['user']['login'])  # author
            message += "[#{} - {}]\n\n".format(issue['number'], issue['title'])
            message += issue['body'] + '\n\n'
            message += comments_text
            message += "[Link: {}]".format(issue['html_url'])
        else:
            message = "Sorry, I couldn't complete your request (Error {}).".\
                format(r.status_code)
        return message

    def add_google_label(self, issue_num):
        comments_url = 'https://api.github.com/repos/{}/{}/issues/{}/comments'\
            .format(self.owner, self.repo_name, issue_num)
        cr = requests.get(comments_url)
        if cr.status_code == 200:
            if cr.json():
                if not self.check_issue(issue_num):
                    return False
                comments = cr.json()
                user_names = [c['user']['login'] for c in comments]
                if user_names[1:]:
                    if not all(self.owner == username for username
                               in user_names[1:]):
                        return False
                self.add_label(issue_num, 'Googleable')
                return True
        return False

    @staticmethod
    def add_auto_issue(issue_num):
        with open('auto_issues.txt', 'a') as f:
            f.write(str(issue_num) + '\n')

    @staticmethod
    def check_issue(issue_num):
        try:
            issue_commented = False
            with open('auto_issues.txt', 'r') as f:
                data = (int(i.strip()) for i in f.readlines())
                with open('auto_issues.txt', 'w') as f:
                    for i in data:
                        if i == issue_num:
                            issue_commented = True
                            continue
                        else:
                            f.write(str(i) + '\n')
            return issue_commented
        except Exception:
            return False
