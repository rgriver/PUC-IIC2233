from app import App


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

app = App(__name__)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    # app = MyApp()
    # app.run(host='0.0.0.0', port=8080)
