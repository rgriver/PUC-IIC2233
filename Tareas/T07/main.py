import flask
import requests

app = flask.Flask(__name__)


@app.route('/')
def handle_github_event():
    #data = dict()
    #data['event'] = 'issues'
    #req = requests.post('https://api.github.com/repos/rgriver/T07/hooks',
    #                    data=data)
    return 'Hello'
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
