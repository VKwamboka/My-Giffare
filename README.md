# To-Do List Manager

Welcome to My To-Do List Manager – a Python project that simplifies task management through an intuitivegraphical user interface (GUI). This application provides a seamless experience for adding,viewing, updating,and removing tasks, making it easy to stay organized and on top of your to-do list.

## Features

- **Add Task:** Input task descriptions and deadlines with ease.
- **View Tasks:** Access a comprehensive list of tasks with essential details.
- **Update Task:** Modify existing tasks, including descriptions and deadlines.
- **Remove Task:** Efficiently remove tasks that are completed or no longer relevant.
- **Mark as Complete:** Visually distinguish completed tasks from ongoing ones.

# Usage

## Adding a Task

Open the application.
Enter the task description.
Click the "Add Task" button.
Enter the deadline when prompted and confirm.

## Removing a Task

Select a task from the list.
Click the "Remove Task" button.

## Updating a Task

Select a task from the list.
Click the "Update Task" button.
Update the task details as needed.
Click the "Confirm" button.

## Marking a Task as Complete

Select a task from the list.
Click the "Mark as Complete" button.

## Viewing Task Details

The task list displays tasks with color-coded indications:
    🟢 Green: Tasks due in the future.
    🟡 Yellow: Tasks due today.
    🚫 Red: Tasks past the deadline.

# Getting Started

## Prerequisites

- **Python 3.x**
- **SQLite3**

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/todo-list-manager.git
    cd todo-list-manager
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:

    ```bash
    python todo_manager.py
    ```

## Usage

1. Launch the application using `python todo_manager.py`.
2. Add tasks by entering the task description and deadline.
3. View, update, and remove tasks using the respective buttons.
4. Mark tasks as complete to visually distinguish them.

## Database

The application uses SQLite to persist tasks. The database schema includes fields for task ID, text, deadline, and completion status.
The tasks.db file is created in the project directory to manage task data

### Database Schema

```sql
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    deadline DATE,
    completed INTEGER DEFAULT 0
);
```


## Known Issues

The update functionality may not work as expected. This is a known issue, and improvements are being worked on.# My-Giffare
