import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

app = Flask(__name__)

app.config["MONGO_URI"] = os.getenv("MONGO_URI_TASK_MANAGER")
app.config["MONGO_DBNAME"] = "task_manager"

mongo = PyMongo(app)

@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    return render_template("tasks.html", tasks=mongo.db.tasks.find())

if __name__ == '__main__':
    app.run(host=os.getenv('IP'),
            port=os.getenv('PORT'),
            debug=True)