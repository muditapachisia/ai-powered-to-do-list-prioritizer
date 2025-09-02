# AI-Powered To-Do List Prioritizer

A simple, intuitive Python Flask app that helps you manage and prioritize your tasks using basic NLP.  
Tasks are automatically assigned priorities and displayed in a color-coded, sortable table.  
No dependencies, subtasks, or task IDs—just focus on your tasks, priorities, and deadlines!

## Features

- **Add tasks:** Enter description, priority, and deadline (days from today).
- **Priority detection:** Automatic (based on keywords) or manual selection.
- **Check-off tasks:** Mark tasks as done in real time.
- **Edit tasks:** Modify any task’s details.
- **Clear all:** Remove all tasks instantly.
- **Smart sorting:** Tasks are sorted by deadline (earliest first), then by priority (HIGH > MEDIUM > LOW).
- **Color-coded UI:** High priority tasks in red, medium in orange, low in green; completed tasks are struck through.

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/ai-todo-prioritizer.git
    cd ai-todo-prioritizer
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    python -m spacy download en_core_web_sm
    ```

## Usage

Run the Flask app:
```bash
python app.py
```
Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## How It Works

- **Priority assignment:** Uses spaCy NLP to detect urgency/importance keywords in task descriptions.
- **Sorting:** Tasks are always shown sorted first by deadline (soonest at top), then by priority.
- **No IDs or dependencies:** Each task is displayed simply and clearly.

## Example Tasks

| Description                 | Priority | Deadline      | Status  |
|-----------------------------|----------|---------------|---------|
| Submit report urgently      | High     | 2025-09-03    | ❌      |
| Buy groceries               | Medium   | 2025-09-05    | ❌      |
| Organize bookshelf someday  | Low      | 2025-09-10    | ✅      |

## Extending the Project

- Add persistent storage (database or files).
- Enhance NLP for more nuanced priority detection.
- Add due time or reminders.
- Support for user authentication and multi-user lists.

## License

MIT License.

## Credits

- [spaCy](https://spacy.io/)
- [Flask](https://flask.palletsprojects.com/)
