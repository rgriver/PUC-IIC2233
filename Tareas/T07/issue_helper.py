import re
import requests


class IssueHelper:
    def __init__(self):
        self.single_markdown_pattern = re.compile(r'`[^`]*?`')
        self.multi_markdown_pattern = re.compile(r'(?s)```.*?```')
        self.error_pattern = re.compile(r'(.*Error.*)')
        self.cx = '007029499010167702478:lwlvf0ucak8'
        self.api_key = 'AIzaSyASgLywWzsu6v36DxpkfsTiepzjE395siw'

    def find_error(self, pattern, body, end_string):
        search = pattern.search(body)
        if search:
            markdown_text = search.group().strip(end_string)
            if markdown_text:
                error_search = self.error_pattern.search(markdown_text)
                if error_search:
                    error_text = error_search.group()
                    return error_text
        return ''

    def get_solution_link(self, error_text):
        search_query = error_text
        url = 'https://www.googleapis.com/customsearch/v1?key={}&cx=' \
            '{}&q={}'.format(self.api_key, self.cx, search_query)
        try:
            r = requests.get(url)
            link = r.json()['items'][0]['link']
            return link
        except Exception as e:
            return None

    def find_solution(self, body):
        error_text = self.find_error(self.single_markdown_pattern, body, '`')
        if error_text:
            link = self.get_solution_link(error_text)
            if link is not None:
                return link
        error_text = self.find_error(self.multi_markdown_pattern, body, '```')
        if error_text:
            link = self.get_solution_link(error_text)
            if link is not None:
                return link
        return None
