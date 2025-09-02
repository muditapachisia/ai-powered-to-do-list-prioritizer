from flask import Flask, render_template_string, request, redirect, url_for
import spacy
from datetime import datetime, timedelta

app = Flask(__name__)
app.jinja_env.globals.update(enumerate=enumerate)
nlp = spacy.load("en_core_web_sm")

PRIORITY_KEYWORDS = {
    'High': ['urgent', 'asap', 'immediately', 'important', 'critical'],
    'Medium': ['soon', 'next', 'follow-up', 'reminder'],
    'Low': ['whenever', 'someday', 'optional', 'later']
}
PRIORITY_ORDER = {'High': 0, 'Medium': 1, 'Low': 2}

tasks = []

def prioritize_task(task):
    doc = nlp(task.lower())
    for priority, keywords in PRIORITY_KEYWORDS.items():
        if any(word in doc.text for word in keywords):
            return priority
    return "Medium"

def sort_tasks(tasks):
    # Sort by deadline (earliest first), then by priority (High > Medium > Low)
    return sorted(tasks, key=lambda x: (x['deadline'].date(), PRIORITY_ORDER.get(x['priority'], 99)))

TABLE_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>AI-Powered To-Do List Prioritizer</title>
    <style>
        body { font-family: Arial; margin: 40px; }
        table { border-collapse: collapse; width: 100%; margin-bottom: 20px;}
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left;}
        tr.high { background-color: #ffdddd;}
        tr.medium { background-color: #fff8dc;}
        tr.low { background-color: #ddffdd;}
        tr.done { text-decoration: line-through; color: gray; }
        .btn { padding: 3px 8px; margin: 2px; border: 1px solid #ccc; background: #eee; cursor: pointer; }
        .btn:hover { background: #ddd; }
        input[type=text], input[type=number] { width: 300px; }
    </style>
</head>
<body>
    <h2>AI-Powered To-Do List Prioritizer</h2>
    <form method="post" action="/">
        <input type="text" name="desc" required placeholder="Task description">
        <input type="number" name="days" required min=0 value=1 placeholder="Deadline (days from today)">
        <select name="priority">
            <option value="">(Auto)</option>
            <option value="High">High</option>
            <option value="Medium">Medium</option>
            <option value="Low">Low</option>
        </select>
        <input type="submit" value="Add Task" class="btn">
    </form>
    <form method="post" action="/clear" style="display:inline;">
        <input type="submit" value="Clear All Tasks" class="btn">
    </form>
    <br><br>
    <table>
        <tr>
            <th>Done</th>
            <th>Description</th>
            <th>Priority</th>
            <th>Deadline</th>
            <th>Edit</th>
        </tr>
        {% for idx, t in enumerate(tasks) %}
        <tr class="{{t.priority.lower()}} {% if t.done %}done{% endif %}">
            <td>
                <form method="post" action="/done/{{idx}}" style="display:inline;">
                    <button type="submit" class="btn">{% if t.done %}✔{% else %}Check-off{% endif %}</button>
                </form>
            </td>
            <td>
                {{t.desc}}
            </td>
            <td><b>{{t.priority}}</b></td>
            <td>{{t.deadline.strftime('%Y-%m-%d')}}</td>
            <td>
                <form method="get" action="/edit/{{idx}}">
                    <button type="submit" class="btn">Edit</button>
                </form>
            </td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

EDIT_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>Edit Task</title>
    <style>
        body { font-family: Arial; margin: 40px; }
        input[type=text], input[type=number] { width: 300px; }
        .btn { padding: 3px 8px; margin: 2px; border: 1px solid #ccc; background: #eee; cursor: pointer; }
        .btn:hover { background: #ddd; }
    </style>
</head>
<body>
    <h2>Edit Task</h2>
    <form method="post" action="/edit/{{idx}}">
        <label>Description:</label><br>
        <input type="text" name="desc" value="{{task.desc}}" required><br><br>
        <label>Deadline (days from today):</label><br>
        <input type="number" name="days" value="{{task.days}}" required min=0><br><br>
        <label>Priority:</label><br>
        <select name="priority">
            <option value="High" {% if task.priority == 'High' %}selected{% endif %}>High</option>
            <option value="Medium" {% if task.priority == 'Medium' %}selected{% endif %}>Medium</option>
            <option value="Low" {% if task.priority == 'Low' %}selected{% endif %}>Low</option>
        </select><br><br>
        <input type="submit" value="Save Changes" class="btn">
        <a href="/" class="btn">Cancel</a>
    </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    global tasks
    if request.method == "POST":
        desc = request.form.get("desc", "")
        priority = request.form.get("priority", "")
        days_str = request.form.get("days", "1")
        try:
            days = int(days_str)
        except Exception:
            days = 1
        deadline = datetime.today() + timedelta(days=days)
        if not priority:
            priority = prioritize_task(desc)
        task = {
            "desc": desc,
            "priority": priority,
            "days": days,
            "deadline": deadline,
            "done": False
        }
        tasks.append(task)
        # Sort tasks after adding a new one
        tasks = sort_tasks(tasks)
        return redirect(url_for('index'))
    # Always display sorted tasks
    tasks_sorted = sort_tasks(tasks)
    print(tasks_sorted)
    return render_template_string(TABLE_TEMPLATE, tasks=tasks_sorted)

@app.route("/done/<int:idx>", methods=["POST"])
def done(idx):
    tasks_sorted = sort_tasks(tasks)
    # Find original index in unsorted tasks
    task = tasks_sorted[idx]
    orig_idx = tasks.index(task)
    tasks[orig_idx]['done'] = True
    # Resort after marking done
    tasks[:] = sort_tasks(tasks)
    return redirect(url_for('index'))

@app.route("/clear", methods=["POST"])
def clear():
    tasks.clear()
    return redirect(url_for('index'))

@app.route("/edit/<int:idx>", methods=["GET", "POST"])
def edit(idx):
    tasks_sorted = sort_tasks(tasks)
    task = tasks_sorted[idx]
    orig_idx = tasks.index(task)
    if request.method == "POST":
        desc = request.form.get("desc", "")
        priority = request.form.get("priority", "Medium")
        days_str = request.form.get("days", "1")
        try:
            days = int(days_str)
        except Exception:
            days = 1
        deadline = datetime.today() + timedelta(days=days)
        tasks[orig_idx]['days'] = days
        tasks[orig_idx]['desc'] = desc
        tasks[orig_idx]['priority'] = priority
        tasks[orig_idx]['deadline'] = deadline
        # Resort after editing
        tasks[:] = sort_tasks(tasks)
        return redirect(url_for('index'))
    days_from_today = max(0, (task['deadline'] - datetime.today()).days)
    return render_template_string(EDIT_TEMPLATE, task=task, idx=idx, days_from_today=days_from_today)

if __name__ == "__main__":
    app.run(debug=True)