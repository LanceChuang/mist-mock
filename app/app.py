from flask import Flask, jsonify, session
from flask_socketio import SocketIO, send
from flask import redirect, request, url_for
import threading

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
socketIO = SocketIO(app)


@app.route("/v2/api/functions/<function_id>/jobs", methods=["POST"])
def run_job(function_id):
    session[function_id] = {"id": function_id+"_fake"}
    return redirect(url_for("index", function_id=function_id))


@app.route("/")
def index():
    id = request.args["function_id"]
    job_id = session[id]
    ws_job_url = "/v2/api/ws/jobs/{}".format(job_id["id"])

    return ws_job_url


if __name__ == "__main__":
    app.run(debug=True, port=1999)
    # socketIO.run(app, debug=True)

# from flask import Flask, render_template
# from flask_socketio import SocketIO, emit
# from threading import Thread
# import time
#
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'include_help!'
# socketio = SocketIO(app, cors_allowed_origins='*')
# thread = None
#
# def background_thread():
#     """Example of how to send server generated events to clients."""
#     count = 0
#     while True:
#         time.sleep(5)
#         count += 1
#         socketio.emit('my response', {'data': 'Connection to server still alive'}, namespace='/v2/api/ws/jobs/')
#
#
# # @app.route('/')
# # def index():
# #     global thread
# #     if thread is None:
# #         thread = Thread(target=background_thread())
# #         thread.start()
#
#
# @socketio.on('my event', namespace='/v2/api/ws/jobs/<job_id>')
# def test_message(msg):
#     """this method is invoked when an event called 'my event' is is triggered"""
#     # global thread
#     # if thread is None:
#     #     thread = Thread(target=background_thread())
#     #     thread.start()
#     #     print "OBOVO"
#
#     print(msg['data'])
#     emit("obov")
#
#
# if __name__ == '__main__':
#     socketio.run(app, port=1999)