import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import sqlite3

class ToDoListManager:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Manager")

        self.db_conn = sqlite3.connect("tasks.db")
        self.create_table()

        self.tasks = []
        self.selected_index = None  # Store the selected task index

        self.task_frame = tk.Frame(root)
        self.task_frame.pack()

        self.task_label = tk.Label(self.task_frame, text="Enter task:")
        self.task_label.pack()

        self.task_entry = tk.Entry(self.task_frame, width=40)
        self.task_entry.pack()

        self.add_task_button = tk.Button(self.task_frame, text="Add Task", command=self.prompt_deadline)
        self.add_task_button.pack()

        self.deadline_frame = tk.Frame(root)
        self.deadline_frame.pack()

        self.deadline_label = tk.Label(self.deadline_frame, text="Enter deadline (YYYY-MM-DD):")
        self.deadline_label.pack()
        self.deadline_label.pack_forget()

        self.deadline_entry = tk.Entry(self.deadline_frame, width=40)
        self.deadline_entry.pack()
        self.deadline_entry.pack_forget()

        self.confirm_button = tk.Button(self.deadline_frame, text="Confirm", command=self.add_task)
        self.confirm_button.pack()
        self.confirm_button.pack_forget()

        self.task_listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=60, height=15)
        self.task_listbox.pack()

        self.remove_button = tk.Button(root, text="Remove Task", command=self.remove_task)
        self.remove_button.pack()

        self.update_button = tk.Button(root, text="Update Task", command=self.update_task)
        self.update_button.pack()

        self.mark_as_complete_button = tk.Button(root, text="Mark as Complete", command=self.mark_as_complete)
        self.mark_as_complete_button.pack()

        self.task_listbox.bind('<<ListboxSelect>>', self.on_task_select)  # Bind task selection event

        self.root.after(1000, self.update_task_styles)  # Update styles every second

    def create_table(self):
        cursor = self.db_conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                deadline DATE,
                completed INTEGER DEFAULT 0
            )
        ''')
        self.db_conn.commit()

    def prompt_deadline(self):
        task_text = self.task_entry.get()
        if task_text:
            self.current_task_text = task_text
            self.task_label.pack_forget()
            self.task_entry.pack_forget()
            self.add_task_button.pack_forget()
            self.deadline_label.pack()
            self.deadline_entry.pack()
            self.confirm_button.pack()

    def add_task(self):
            deadline_text = self.deadline_entry.get()
            try:
                deadline = datetime.strptime(deadline_text, "%Y-%m-%d") if deadline_text else None
            except ValueError:
                messagebox.showerror("Invalid Deadline", "Please enter a valid deadline (YYYY-MM-DD).")
                return

            if self.current_task_text:
                if not deadline:
                    messagebox.showerror("Missing Deadline", "Please enter a deadline for the task.")
                    return

                self.insert_task_into_database(self.current_task_text, deadline)
                self.task_entry.delete(0, tk.END)
                self.deadline_entry.delete(0, tk.END)
                self.confirm_button.pack_forget()
                self.deadline_label.pack_forget()
                self.deadline_entry.pack_forget()
                self.task_label.pack()
                self.task_entry.pack()
                self.add_task_button.pack()
                self.load_tasks_from_database()  # Reload tasks from the database
                self.update_task_listbox()


    def remove_task_from_database(self, task_id):
        cursor = self.db_conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        self.db_conn.commit()

    def update_task_in_database(self, task_id, text, deadline):
        cursor = self.db_conn.cursor()
        cursor.execute("UPDATE tasks SET text=?, deadline=? WHERE id=?", (text, deadline, task_id))
        self.db_conn.commit()

    def mark_task_as_complete_in_database(self, task_id):
        cursor = self.db_conn.cursor()
        cursor.execute("UPDATE tasks SET completed=1 WHERE id=?", (task_id,))
        self.db_conn.commit()

    def insert_task_into_database(self, text, deadline):
        cursor = self.db_conn.cursor()
        cursor.execute("INSERT INTO tasks (text, deadline) VALUES (?, ?)", (text, deadline))
        self.db_conn.commit()

    def update_task_listbox(self):
        self.tasks = self.fetch_tasks_from_database()  # Fetch tasks from the database
        self.task_listbox.delete(0, tk.END)
        now = datetime.now()
        for task in self.tasks:
            text = task["text"]
            deadline = task["deadline"]
            if task["completed"]:
                text = f"✓ {text}"
            if deadline:
                days_to_deadline = (deadline - now).days
                if days_to_deadline < 0:
                    text = f"🚫 {text} (Past deadline by {-days_to_deadline} days)"
                elif days_to_deadline == 0:
                    text = f"🟡 {text} (Due today)"
                else:
                    text = f"🟢 {text} (Due in {days_to_deadline} days)"
            self.task_listbox.insert(tk.END, text)

    def update_task_styles(self):
        self.update_task_listbox()
        self.root.after(1000, self.update_task_styles)

    def on_task_select(self, event):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            self.selected_index = int(selected_index[0])
            self.populate_fields()  # Populate fields when a task is selected
        else:
            self.selected_index = None
            self.clear_fields()  # Clear fields when no task is selected

    def clear_fields(self):
        self.task_entry.delete(0, tk.END)
        self.deadline_entry.delete(0, tk.END)

    def populate_fields(self):
        if self.selected_index is not None:
            selected_task = self.tasks[self.selected_index]
            self.task_entry.delete(0, tk.END)
            self.task_entry.insert(0, selected_task["text"])
            self.deadline_entry.delete(0, tk.END)
            if selected_task["deadline"]:
                self.deadline_entry.insert(0, selected_task["deadline"].strftime("%Y-%m-%d"))
            else:
                self.deadline_entry.insert(0, "")

    def remove_task(self):
        if self.selected_index is not None:
            selected_task = self.tasks[self.selected_index]
            self.remove_task_from_database(selected_task["id"])  # Remove the task from the database
            self.selected_index = None  # Clear the selected index
            self.update_task_listbox()

    def update_task(self):
        if self.selected_index is not None:
            selected_task = self.tasks[self.selected_index]

            # Check if the task is not completed, then allow updates
            if not selected_task["completed"]:
                new_text = self.task_entry.get()
                new_deadline_text = self.deadline_entry.get()
                try:
                    new_deadline = datetime.strptime(new_deadline_text, "%Y-%m-%d") if new_deadline_text else None
                except ValueError:
                    messagebox.showerror("Invalid Deadline", "Please enter a valid deadline (YYYY-MM-DD).")
                    return

                if new_text:
                    self.update_task_in_database(selected_task["id"], new_text, new_deadline)  # Update the task in the database
                    self.task_entry.delete(0, tk.END)
                    self.deadline_entry.delete(0, tk.END)
                    self.confirm_button.pack_forget()
                    self.deadline_label.pack_forget()
                    self.deadline_entry.pack_forget()
                    self.task_label.pack()
                    self.task_entry.pack()
                    self.add_task_button.pack()
                    self.selected_index = None  # Clear the selected index
                    self.update_task_listbox()
            else:
                messagebox.showinfo("Task Completed", "Cannot update a completed task.")

    def mark_as_complete(self):
        if self.selected_index is not None:
            selected_task = self.tasks[self.selected_index]
            self.mark_task_as_complete_in_database(selected_task["id"])  # Mark the task as complete in the database
            self.selected_index = None  # Clear the selected index
            self.update_task_listbox()

    def fetch_tasks_from_database(self):
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        tasks = []
        for row in cursor.fetchall():
            task_id, text, deadline_str, completed = row
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M:%S") if deadline_str else None
            tasks.append({
                "id": task_id,
                "text": text,
                "deadline": deadline,
                "completed": bool(completed)
            })
        return tasks

def main():
    root = tk.Tk()
    app = ToDoListManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
