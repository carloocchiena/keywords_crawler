from flask import Flask, request, render_template
import os
from processing import kw_ranking, crawler, cleaner
from flask_socketio import SocketIO,send

app = Flask(__name__)
app.config["DEBUG"] = False
app.secret_key = "super secret key"
socketio = SocketIO(app,cors_allowed_origins='*')

 

#render about page 
@app.route('/about', methods = ["GET"])
def about():
    return render_template("about.html")

@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    url = None
    url = f"https://www.{msg}"
    print(msg)
    if url is not None:
        links = crawler(url)
        result = kw_ranking(links)
    send(result) # if you want , you can return a dict which contain error + result.

#render main page
@app.route('/', methods = ["GET", "POST"])
def input_page():
    print("started")
    # if request.method == "POST":
    #     print("hi")
    #     url = None
    #     url = f"https://www.{request.form.get('url')}"
    #     print(request.form.get("url"))
    #     if url is not None:
    #         links = crawler(url)
    #         result = kw_ranking(links)
    #         return result
                
    return render_template("main.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app,port=port,host="0.0.0.0")
