import tkinter as tk
from tkinter import ttk
import json
import os
from time import localtime

# --- Constants ---
FILENAME = "tasks.json"

# --- Data ---
tasks = []

# --- File handling ---
def save_tasks():
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)

def load_tasks():
    if os.path.exists(FILENAME):
        try:
            raw_tasks = json.load(open(FILENAME, "r", encoding="utf-8"))
            new_tasks = []
            for t in raw_tasks:
                if isinstance(t, list) and len(t) == 2:
                    new_tasks.append(t)
                else:
                    new_tasks.append(["Normal", t])
            return new_tasks
        except (json.JSONDecodeError, OSError):
            alert_box("Task Error", "Error loading saved tasks.")
    return []

# --- Tkinter setup ---
root = tk.Tk()
root.title("📝 My To-Do List App")
root.geometry("600x700")
root.resizable(False, False)
root.config(bg="#f0f0f0")

# --- Functions ---
def alert_box(title, message):
    win = tk.Toplevel(root)
    win.title(title)
    win.geometry("300x150")
    win.resizable(False, False)
    tk.Label(win, text=title, font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(win, text=message, font=("Arial", 11)).pack(pady=5)
    tk.Button(win, text="OK", command=win.destroy).pack(pady=10)

def get_color(status):
    return {
        "Urgent": "#F6707C",
        "Important": "#FDDD75",
        "Normal": "#FFFFFF"
    }.get(status, "white")

def refresh_listbox():
    task_listbox.delete(0, tk.END)
    for status, name in tasks:
        task_listbox.insert(tk.END, name)
        index = task_listbox.size() - 1
        if name.startswith("✓ "):
            task_listbox.itemconfig(index, fg="gray", bg=get_color(status))
        else:
            task_listbox.itemconfig(index, bg=get_color(status), fg="black")

def add_task():
    name = task_entry.get().strip()
    status = combo.get()
    if not name:
        alert_box("Task Error", "Please enter a task!")
        return

    hour, minute = localtime()[3], localtime()[4]
    day, month, year = localtime()[2], localtime()[1], localtime()[0]
    timestamp = f"{day:02}/{month:02}/{year} {hour:02}:{minute:02} : "
    full_name = timestamp + name

    tasks.append([status, full_name])
    refresh_listbox()
    save_tasks()
    task_entry.delete(0, tk.END)

def delete_task():
    try:
        index = task_listbox.curselection()[0]
        tasks.pop(index)
        refresh_listbox()
        save_tasks()
    except IndexError:
        alert_box("Task Error", "Please select a task to delete!")

def clear_all_tasks():
    tasks.clear()
    refresh_listbox()
    save_tasks()

def mark_complete():
    try:
        index = task_listbox.curselection()[0]
        status, name = tasks[index]
        if not name.startswith("✓ "):
            tasks[index][1] = "✓ " + name
            refresh_listbox()
            save_tasks()
    except IndexError:
        alert_box("Task Error", "Please select a task to mark as complete!")

def edit_task():
    try:
        index = task_listbox.curselection()[0]
        name = tasks[index][1]
        if " : " in name:
            name_parts = name.split(" : ", 1)
            name = name_parts[1] if not name_parts[1].startswith("✓ ") else name_parts[1][2:]

        task_entry.delete(0, tk.END)
        task_entry.insert(0, name)
        combo.set(tasks[index][0])

        add_button.config(
            text="Save Edit",
            bg="#0275d8",
            command=lambda: save_edit(index)
        )
    except IndexError:
        alert_box("Task Error", "Please select a task to edit!")

def save_edit(index):
    name = task_entry.get().strip()
    status = combo.get()
    if not name:
        alert_box("Task Error", "Please enter a task!")
        return

    hour, minute = localtime()[3], localtime()[4]
    day, month, year = localtime()[2], localtime()[1], localtime()[0]
    timestamp = f"{day:02}/{month:02}/{year} {hour:02}:{minute:02} : "
    full_name = timestamp + name

    tasks[index] = [status, full_name]
    refresh_listbox()
    save_tasks()

    task_entry.delete(0, tk.END)
    combo.set("Normal")
    add_button.config(
        text="Add Task",
        bg="#5cb85c",
        command=add_task
    )

# --- Header ---
tk.Label(
    root,
    text="📝 My To-Do List",
    font=("Arial", 18, "bold"),
    bg="#4a7c9e",
    fg="white"
).pack(fill=tk.X, pady=15)

# --- Input field ---
input_frame = tk.Frame(root, bg="#f0f0f0")
input_frame.pack(pady=10)

task_entry = tk.Entry(input_frame, width=30, font=("Arial", 12), bd=2, relief=tk.GROOVE)
task_entry.pack(side=tk.LEFT, padx=10, ipady=5)
task_entry.bind("<Return>", lambda e: add_task())

combo = ttk.Combobox(
    input_frame,
    values=["Normal", "Important", "Urgent"],
    state="readonly",
    width=10
)
combo.set("Normal")
combo.pack(side=tk.LEFT, padx=10)

add_button = tk.Button(
    input_frame,
    text="Add Task",
    width=12,
    font=("Arial", 11, "bold"),
    bg="#5cb85c",
    fg="white",
    activebackground="#4cae4c",
    bd=0,
    cursor="hand2",
    command=add_task
)
add_button.pack(side=tk.LEFT)

# --- Task list ---
list_frame = tk.Frame(root, bg="#f0f0f0")
list_frame.pack(pady=10, padx=20)

scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

task_listbox = tk.Listbox(
    list_frame,
    width=50,
    height=15,
    font=("Arial", 11),
    bd=2,
    relief=tk.SUNKEN,
    selectmode=tk.SINGLE,
    activestyle='none',
    bg="white",
    selectbackground="#d4e6f1",
    selectforeground="black",
    yscrollcommand=scrollbar.set
)
task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=task_listbox.yview)

# --- Buttons ---
btn_frame = tk.Frame(root, bg="#f0f0f0")
btn_frame.pack(pady=20)

tk.Button(btn_frame, text="✓ Mark Complete", width=15, font=("Arial", 10, "bold"),
          bg="#5bc0de", fg="white", activebackground="#46b8da", bd=0, cursor="hand2",
          command=mark_complete).grid(row=0, column=0, padx=8)

tk.Button(btn_frame, text="✎ Edit", width=15, font=("Arial", 10, "bold"),
          bg="#0275d8", fg="white", activebackground="#025aa5", bd=0, cursor="hand2",
          command=edit_task).grid(row=0, column=1, padx=8)

tk.Button(btn_frame, text="✕ Delete", width=15, font=("Arial", 10, "bold"),
          bg="#d9534f", fg="white", activebackground="#c9302c", bd=0, cursor="hand2",
          command=delete_task).grid(row=0, column=2, padx=8)

tk.Button(btn_frame, text="Clear All", width=15, font=("Arial", 10, "bold"),
          bg="#f0ad4e", fg="white", activebackground="#ec971f", bd=0, cursor="hand2",
          command=clear_all_tasks).grid(row=1, column=1, pady=8)

# --- Load tasks & display ---
tasks = load_tasks()
refresh_listbox()

root.protocol("WM_DELETE_WINDOW", lambda: (save_tasks(), root.destroy()))
root.mainloop()