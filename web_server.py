"""
Web server for the Todo application that runs on localhost:3000.
This provides a web interface for the existing CLI todo app.
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for
from src.todo.cli import TodoCLI
from src.todo.models import Task
import os

app = Flask(__name__)

# Create a global instance of the CLI to manage tasks
todo_cli = TodoCLI()

@app.route('/')
def index():
    """Main page that displays all tasks"""
    tasks = todo_cli.storage.get_all_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/tasks')
def get_tasks():
    """API endpoint to get all tasks in JSON format"""
    tasks = todo_cli.storage.get_all_tasks()
    tasks_data = []
    for task in tasks:
        tasks_data.append({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'completed': task.completed,
            'created_at': task.created_at.isoformat()
        })
    return jsonify(tasks_data)

@app.route('/add', methods=['POST'])
def add_task():
    """API endpoint to add a new task"""
    title = request.form.get('title')
    description = request.form.get('description')

    if title and description:
        task = todo_cli.storage.add_task(title, description)
        return jsonify({
            'success': True,
            'task': {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'completed': task.completed,
                'created_at': task.created_at.isoformat()
            }
        })
    else:
        return jsonify({'success': False, 'error': 'Title and description are required'}), 400

@app.route('/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    """API endpoint to update a task"""
    title = request.form.get('title')
    description = request.form.get('description')

    # Only update if at least one field is provided
    if title is not None or description is not None:
        success = todo_cli.storage.update_task(task_id, title, description)
        if success:
            task = todo_cli.storage.get_task_by_id(task_id)
            return jsonify({
                'success': True,
                'task': {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'completed': task.completed,
                    'created_at': task.created_at.isoformat()
                }
            })
        else:
            return jsonify({'success': False, 'error': f'Task with ID {task_id} not found'}), 404
    else:
        return jsonify({'success': False, 'error': 'At least one field (title or description) must be provided'}), 400

@app.route('/delete/<int:task_id>', methods=['POST', 'DELETE'])
def delete_task(task_id):
    """API endpoint to delete a task"""
    success = todo_cli.storage.delete_task(task_id)
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': f'Task with ID {task_id} not found'}), 404

@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    """API endpoint to toggle task completion status"""
    success = todo_cli.storage.toggle_task_status(task_id)
    if success:
        task = todo_cli.storage.get_task_by_id(task_id)
        return jsonify({
            'success': True,
            'task': {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'completed': task.completed,
                'created_at': task.created_at.isoformat()
            }
        })
    else:
        return jsonify({'success': False, 'error': f'Task with ID {task_id} not found'}), 404

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)

    app.run(host='0.0.0.0', port=3000, debug=True)