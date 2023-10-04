import json
from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit
import requests
from environments.variables import LOCATION_IQ_KEY

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__,template_folder="../templates")
socketio = SocketIO(app, async_mode=async_mode)


@app.route('/locationIQ')
def index():
    return render_template('locationIQ.html', async_mode=socketio.async_mode)


# Receive the test request from client and send back a test response
@socketio.on('test_message')
def handle_message(data):
    url: str = f"https://eu1.locationiq.com/v1/autocomplete?q={str(data)}&key={LOCATION_IQ_KEY}&limit=5"
    headers: dict[str, str] = {"accept": "application/json"}
    response: requests.Response = requests.get(url, headers=headers)

    result: any = json.loads(response.text)
    tab: list = []
    for i in result:
        tab.append(i["display_name"])

    emit('test_responses', {'data': tab})


if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)
