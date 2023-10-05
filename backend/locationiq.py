from environments.variables import LOCATION_IQ_KEY
from flask_socketio import SocketIO, emit
from flask import Flask, render_template
import requests
import json


app = Flask(__name__, template_folder="../frontend/templates")
socketio = SocketIO(app, async_mode=None)


@app.route('/cart')
def index():
    return render_template('locationiq.jinja', async_mode=socketio.async_mode)


@socketio.on('check_address')
def handle_message(data):
    url: str = f"https://eu1.locationiq.com/v1/autocomplete?q={str(data)}&key={LOCATION_IQ_KEY}&limit=5"
    headers: dict[str, str] = {"accept": "application/json"}
    response: requests.Response = requests.get(url, headers=headers)

    result: any = json.loads(response.text)
    tab: list = []
    for i in result:
        tab.append(i["display_name"])

    emit('check_address', {'data': tab})


if __name__ == '__main__':
    app.run()
