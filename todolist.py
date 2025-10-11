import tkinter as tk
import json
import os

# --- Constants ---
FILENAME = "tasks.json"

# --- Functions for file handling ---
def save_tasks():
    """Save current tasks to JSON file."""
    tasks = task_listbox.get(0, tk.END)
    with open(FILENAME, "w") as f:
        json.dump(list(tasks), f, indent=4)

def load_tasks():
    """Load tasks from JSON file (if it exists)."""
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r") as f:
                tasks = json.load(f)
            for t in tasks:
                task_listbox.insert(tk.END, t)
                # Gray out completed tasks
                if t.startswith("✓ "):
                    index = task_listbox.size() - 1
                    task_listbox.itemconfig(index, fg="gray")
        except (json.JSONDecodeError, OSError):
            print("Error loading saved tasks.")

# --- Tkinter setup ---
root = tk.Tk()
root.title("To-Do List App")
root.geometry("400x500")
root.resizable(False, False)
root.config(bg="#f0f0f0")

# --- Functions for user actions ---
def add_task():
    task = task_entry.get().strip()
    if task:
        task_listbox.insert(tk.END, task)
        task_entry.delete(0, tk.END)
        save_tasks()
    else:
        print("Please enter a task!")

def delete_task():
    try:
        selected_index = task_listbox.curselection()[0]
        task_listbox.delete(selected_index)
        save_tasks()
    except IndexError:
        print("Please select a task to delete!")

def clear_all_tasks():
    task_listbox.delete(0, tk.END)
    save_tasks()

def mark_complete():
    try:
        selected_index = task_listbox.curselection()[0]
        task = task_listbox.get(selected_index)
        if not task.startswith("✓ "):
            task_listbox.delete(selected_index)
            task_listbox.insert(selected_index, "✓ " + task)
            task_listbox.itemconfig(selected_index, fg="gray")
            save_tasks()
    except IndexError:
        print("Please select a task to mark as complete!")

# --- Header ---
header_frame = tk.Frame(root, bg="#4a7c9e")
header_frame.pack(fill=tk.X)

header_label = tk.Label(
    header_frame, text="📝 My To-Do List",
    font=("Arial", 18, "bold"), bg="#4a7c9e", fg="white"
)
header_label.pack(pady=15)

# --- Input field ---
input_frame = tk.Frame(root, bg="#f0f0f0")
input_frame.pack(pady=10)

task_entry = tk.Entry(input_frame, width=30, font=("Arial", 12), bd=2, relief=tk.GROOVE)
task_entry.pack(side=tk.LEFT, padx=10, ipady=5)
task_entry.bind('<Return>', lambda event: add_task())

add_button = tk.Button(
    input_frame, text="Add Task", width=12,
    font=("Arial", 11, "bold"),
    bg="#5cb85c", fg="white",
    activebackground="#4cae4c",
    bd=0, cursor="hand2",
    command=add_task
)
add_button.pack(side=tk.LEFT)

# --- Task list with scrollbar ---
list_frame = tk.Frame(root, bg="#f0f0f0")
list_frame.pack(pady=10, padx=20)

scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
task_listbox = tk.Listbox(
    list_frame, width=45, height=15,
    font=("Arial", 11),
    bd=2, relief=tk.SUNKEN,
    selectmode=tk.SINGLE,
    activestyle='none',
    bg="white",
    selectbackground="#d4e6f1",
    selectforeground="black",
    yscrollcommand=scrollbar.set
)
scrollbar.config(command=task_listbox.yview)
task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# --- Buttons for managing tasks ---
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=20)

mark_button = tk.Button(
    button_frame, text="✓ Mark Complete", width=15,
    font=("Arial", 10, "bold"),
    bg="#5bc0de", fg="white",
    activebackground="#46b8da",
    bd=0, cursor="hand2",
    command=mark_complete
)
mark_button.grid(row=0, column=0, padx=8)

delete_button = tk.Button(
    button_frame, text="✕ Delete Task", width=15,
    font=("Arial", 10, "bold"),
    bg="#d9534f", fg="white",
    activebackground="#c9302c",
    bd=0, cursor="hand2",
    command=delete_task
)
delete_button.grid(row=0, column=1, padx=8)

clear_button = tk.Button(
    button_frame, text="Clear All", width=15,
    font=("Arial", 10, "bold"),
    bg="#f0ad4e", fg="white",
    activebackground="#ec971f",
    bd=0, cursor="hand2",
    command=clear_all_tasks
)
clear_button.grid(row=0, column=2, padx=8)

# --- Footer ---
footer_label = tk.Label(
    root, text="Select a task and use buttons to manage it",
    font=("Arial", 9, "italic"),
    bg="#f0f0f0", fg="#666666"
)
footer_label.pack(side=tk.BOTTOM, pady=10)

# --- Load tasks and run app ---
load_tasks()
root.protocol("WM_DELETE_WINDOW", lambda: (save_tasks(), root.destroy()))
root.mainloop()
