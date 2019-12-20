import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

app = Flask(__name__)

app.config["MONGO_URI"] = os.getenv("MONGO_URI_TASK_MANAGER")
app.config["MONGO_DBNAME"] = "task_manager"

mongo = PyMongo(app)

# Have to use hard-coded gitpod url, otherwise tries to redirect to localhost causing a 'connection refused' error.
gitpod_url = "https://5000-ae34fd21-0471-4da9-8255-f8e6a8ea7825.ws-eu01.gitpod.io/"

@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    return render_template("tasks.html", tasks=list(mongo.db.tasks.find()))

@app.route('/add_task')
def add_task():
    return render_template("addtask.html", categories=list(mongo.db.categories.find()))

# Create Go to the Edit Task page and show the data for the ID associated with this task record. -->
@app.route('/insert_task', methods=["POST"])
def insert_task():
    tasks = mongo.db.tasks
    # Convert form data to a dictionary to make it usable by Mongo.
    tasks.insert_one(request.form.to_dict())
    return redirect(gitpod_url + 'get_tasks')
    #return redirect(url_for('get_tasks'))

# Go to the Edit Task page and show the data for for the passed task ID parameter. -->
@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    # Fetch the task record from the database for the displayed to edit.
    _task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    # Fetch all categories from the database to display in the dropdown list, so user can choose a new one if they wish.
    _categories = mongo.db.categories.find()
    category_list = [category for category in _categories]
    # Display the record for editing.
    return render_template("edittask.html", task= _task, categories = category_list)

# UPDATE the record from the collection and return to the Task List page.
@app.route('/update_task/<task_id>', methods=["POST"])
def update_task(task_id):
    tasks = mongo.db.tasks
    tasks.update({"_id": ObjectId(task_id)},
    {
        'task_name': request.form.get('task_name'),
        'category_name': request.form.get('category_name'),
        'task_description': request.form.get('task_description'),
        'due_date': request.form.get('due_date'),
        'is_urgent': request.form.get('is_urgent')
    })
    return redirect(gitpod_url + 'get_tasks')
    #return redirect(url_for('get_tasks'))

# DELETE the record from the collection and return to the Task List page.
@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    mongo.db.tasks.remove({"_id": ObjectId(task_id)})
    return redirect(gitpod_url + 'get_tasks')
    #return redirect(url_for('get_tasks'))

# Show the existing categories.
@app.route('/get_categories')
def get_categories():
    return render_template("categories.html", categories= mongo.db.categories.find())

# Go to the Edit Category page and show the data for the passed category ID parameter. -->
@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template("editcategory.html", category = mongo.db.categories.find_one({"_id": ObjectId(task_id)}))

if __name__ == '__main__':
    app.run(host=os.getenv('IP'),
            port=os.getenv('PORT'),
            debug=True)