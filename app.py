import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# --- DATA TIER ---
# Connect to MongoDB. The MONGO_URI is an environment variable.
# We will set this in our Docker environment later.
# It defaults to a local connection string for flexibility.
mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(mongo_uri)
db = client.tododb # Use a database named 'tododb'
todos = db.todos # Use a collection named 'todos'

# --- LOGIC TIER ---
@app.route('/')
def index():
    """Render the main page with all the to-do items."""
    saved_todos = todos.find().sort("text")
    # --- PRESENTATION TIER ---
    return render_template('index.html', todos=saved_todos)

@app.route('/add', methods=['POST'])
def add_todo():
    """Add a new to-do item."""
    new_todo_text = request.form.get('todoitem')
    if new_todo_text: # Don't add empty items
        todos.insert_one({'text': new_todo_text})
    return redirect(url_for('index'))

@app.route('/delete/<id>')
def delete_todo(id):
    """Delete a to-do item by its ID."""
    todos.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('index'))

@app.route('/page1')
def page1():
    """Render the first new page."""
    return render_template('page1.html')

@app.route('/page2')
def page2():
    """Render the second new page."""
    return render_template('page2.html')

if __name__ == "__main__":
    # Host 0.0.0.0 makes it accessible from outside the container
    app.run(host='0.0.0.0', port=8080)
