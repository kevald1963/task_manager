import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

app = Flask(__name__)

app.config["MONGO_URI"] = os.getenv("MONGO_URI_TASK_MANAGER")
app.config["MONGO_DBNAME"] = "task_manager"

mongo = PyMongo(app)

gp_url = "https://5000-ae34fd21-0471-4da9-8255-f8e6a8ea7825.ws-eu01.gitpod.io/"

@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    return render_template("tasks.html", tasks=list(mongo.db.tasks.find()))

@app.route('/add_task')
def add_task():
    return render_template("addtask.html", categories=list(mongo.db.categories.find()))

@app.route('/insert_task', methods=["POST"])
def insert_task():
    tasks = mongo.db.tasks
    # Convert form data to a dictionary to make it usable by Mongo.
    tasks.insert_one(request.form.to_dict())
    # Have to use hard-coded gitpod url, otherwise tries to redirect to localhost causing a connection refused error.
    return redirect(gp_url + 'get_tasks')
    #return redirect(url_for('get_tasks'))

@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    # Fetch the task record from the database for the displayed task we want to edit.
    _task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    # Fetch all categories from the database to display in the dropdown list, so user can choose a new one if they wish.
    _categories = mongo.db.categories.find()
    category_list = [category for category in _categories]
    # Display the record for editing.
    return render_template("edittask.html", task= _task, categories = category_list)

if __name__ == '__main__':
    app.run(host=os.getenv('IP'),
            port=os.getenv('PORT'),
            debug=True)