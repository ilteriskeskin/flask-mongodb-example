from flask import Flask, render_template, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config[
    "MONGO_URI"] = "mongodb://ilteriskeskin:<password>@cluster0-shard-00-00-raeh0.mongodb.net:27017,cluster0-shard-00-01-raeh0.mongodb.net:27017,cluster0-shard-00-02-raeh0.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority"
mongo = PyMongo(app)


@app.route('/')
def home():
    return render_template("index.html")


# @app.route('/create', methods=['POST'])
# def create():
#     if 'profile_image' in request.files:
#         profile_image = request.files['profile_image']
#         mongo.save_file(profile_image.filename, profile_image)
#         mongo.db.insert({'username': request.form.get('username'), 'profile_image_name': profile_image.filename})
#     return 'Done!'


@app.route('/create', methods=['POST'])
def create():
    username = request.form.get('username')
    mongo.db.user.insert({'username': username})
    return render_template('profile.html')


if __name__ == '__main__':
    app.run(debug=True)
