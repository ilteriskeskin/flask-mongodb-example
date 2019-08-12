from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from flask_dance.contrib.slack import make_slack_blueprint, slack

app = Flask(__name__)
app.config['SECRET_KEY'] = 'linuxdegilgnulinux'
app.config[
    'MONGO_URI'] = "mongodb://ilteriskeskin:<password>@myflask-shard-00-00-raeh0.mongodb.net:27017,myflask-shard-00-01-raeh0.mongodb.net:27017,myflask-shard-00-02-raeh0.mongodb.net:27017/test?ssl=true&replicaSet=myFlask-shard-0&authSource=admin&retryWrites=true&w=majority"

app.config["SLACK_OAUTH_CLIENT_ID"] = ''
app.config["SLACK_OAUTH_CLIENT_SECRET"] = ''
slack_bp = make_slack_blueprint(scope=["admin,identify,bot,incoming-webhook,channels:read,chat:write:bot,links:read"])
app.register_blueprint(slack_bp, url_prefix="/login")

mongo = PyMongo(app)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/create', methods=['POST'])
def create():
    username = request.form.get('username')
    mongo.db.user.insert_one({'username': username})

    if not slack.authorized:
        return redirect(url_for("slack.login"))
    resp = slack.post("chat.postMessage", data={
        "text": username,
        "channel": "#general",
        "icon_emoji": ":male-technologist:",
    })

    b = resp.text
    assert resp.json()["ok"], resp.text
    print('-----------------')
    print(b)
    print('-----------------')
    return 'I just said "Hello, world!" in the #general channel!'


if __name__ == '__main__':
    app.run(debug=True)
