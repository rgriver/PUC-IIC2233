import flask
import requests
import json

app = flask.Flask(__name__)

bot_token = '415058552:AAH_h5aHopemW9hqMhEZpq1Ajg5LLRunhAM'
base_url = 'https://api.telegram.org/bot' + bot_token + '/setWebhook'
webhook_data = {'url': 'https://rgriverapp.herokuapp.com/'}
# webhook_data = {'url': 'http://0.0.0.0:8080/telegram'}
requests.post(base_url, data=webhook_data)


@app.route('/', methods=['POST'])
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


@app.route('/telegram')
def handle_telegram_event():
    data = json.loads(flask.request.data)
    return 'jjj'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
