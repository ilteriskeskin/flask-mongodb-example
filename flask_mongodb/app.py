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
    if not slack.authorized:
        return redirect(url_for("slack.login"))
    resp = slack.post("chat.postMessage", data={
        "text": 'HeyBooster!',
        "channel": "#general",
        "icon_emoji": ":male-technologist:",
    })

    txt = resp.text
    username = request.form.get('username')
    mongo.db.user.insert_one({'username': username, 'text': txt})
    assert resp.json()["ok"], resp.text
    database()
    return 'I just said "Hello, world!" in the #general channel!'


def database():
    a = mongo.db.user.find()
    for i in a:
        print(i)


if __name__ == '__main__':
    app.run(debug=True)
