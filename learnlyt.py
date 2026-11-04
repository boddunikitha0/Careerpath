
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

FILE_NAME = "learning_data.json"


# Load saved learning data
def load_data():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except:
            return []
    return []


learning_data = load_data()


# Save learning data
def save_data():
    with open(FILE_NAME, "w") as file:
        json.dump(learning_data, file, indent=4)


# Add new topic
def add_topic():
    topic = topic_entry.get().strip()
    notes = notes_entry.get("1.0", tk.END).strip()
    category = category_box.get()
    priority = priority_box.get()

    if not topic or not notes:
        messagebox.showwarning(
            "Warning", "Please enter topic and notes!"
        )
        return

    learning_data.append({
        "topic": topic,
        "category": category,
        "notes": notes,
        "priority": priority,
        "status": "Learning"
    })

    save_data()
    clear_fields()
    display_topics()

    messagebox.showinfo("Success", "Topic added successfully!")


# Clear input fields
def clear_fields():
    topic_entry.delete(0, tk.END)
    notes_entry.delete("1.0", tk.END)
    category_box.set("Programming")
    priority_box.set("Medium")


# Display topics
def display_topics():
    for item in tree.get_children():
        tree.delete(item)

    for index, item in enumerate(learning_data):
        tree.insert("", tk.END, iid=str(index), values=(
            item["topic"],
            item["category"],
            item["priority"],
            item["status"]
        ))


# Mark topic as completed
def update_status():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning("Warning", "Select a topic!")
        return

    index = int(selected[0])
    learning_data[index]["status"] = "Completed"

    save_data()
    display_topics()

    messagebox.showinfo("Success", "Status updated!")


# Delete topic
def delete_topic():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning("Warning", "Select a topic!")
        return

    index = int(selected[0])

    if messagebox.askyesno("Confirm", "Delete selected topic?"):
        learning_data.pop(index)
        save_data()
        display_topics()


# View notes
def show_notes():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning("Warning", "Select a topic!")
        return

    index = int(selected[0])
    item = learning_data[index]

    messagebox.showinfo(
        item["topic"],
        "Category: " + item["category"] +
        "\nPriority: " + item["priority"] +
        "\nStatus: " + item["status"] +
        "\n\nNotes:\n" + item["notes"]
    )


# Main window
root = tk.Tk()
root.title("LearnLyt - Knowledge Retention Tool")
root.geometry("850x650")
root.configure(bg="#F2F4F8")

# Title
title = tk.Label(
    root,
    text="LearnLyt - Knowledge Retention Tool",
    font=("Arial", 20, "bold"),
    bg="#243B55",
    fg="white",
    pady=15
)
title.pack(fill=tk.X)

# Input frame
form = tk.Frame(root, bg="white", padx=20, pady=15)
form.pack(fill=tk.X, padx=20, pady=15)

tk.Label(
    form, text="Topic Name:", bg="white"
).grid(row=0, column=0, sticky="w", pady=5)

topic_entry = tk.Entry(form, width=40)
topic_entry.grid(row=0, column=1, pady=5)

tk.Label(
    form, text="Category:", bg="white"
).grid(row=1, column=0, sticky="w", pady=5)

category_box = ttk.Combobox(
    form,
    values=[
        "Programming",
        "Database",
        "Technology",
        "Networking",
        "Other"
    ],
    state="readonly"
)
category_box.set("Programming")
category_box.grid(row=1, column=1, pady=5)

tk.Label(
    form, text="Priority:", bg="white"
).grid(row=2, column=0, sticky="w", pady=5)

priority_box = ttk.Combobox(
    form,
    values=["Low", "Medium", "High"],
    state="readonly"
)
priority_box.set("Medium")
priority_box.grid(row=2, column=1, pady=5)

tk.Label(
    form, text="Learning Notes:", bg="white"
).grid(row=3, column=0, sticky="nw", pady=5)

notes_entry = tk.Text(form, width=40, height=5)
notes_entry.grid(row=3, column=1, pady=5)

# Add button
tk.Button(
    form,
    text="Add Topic",
    command=add_topic,
    bg="#243B55",
    fg="white",
    width=15
).grid(row=4, column=1, pady=10, sticky="w")

# Topics table
table_frame = tk.Frame(root, bg="#F2F4F8")
table_frame.pack(
    fill=tk.BOTH,
    expand=True,
    padx=20,
    pady=10
)

columns = ("Topic", "Category", "Priority", "Status")

tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=12
)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=170)

tree.pack(fill=tk.BOTH, expand=True)

# Action buttons
button_frame = tk.Frame(root, bg="#F2F4F8")
button_frame.pack(pady=15)

tk.Button(
    button_frame,
    text="View Notes",
    command=show_notes,
    width=15
).grid(row=0, column=0, padx=5)

tk.Button(
    button_frame,
    text="Mark Completed",
    command=update_status,
    width=15
).grid(row=0, column=1, padx=5)

tk.Button(
    button_frame,
    text="Delete Topic",
    command=delete_topic,
    width=15
).grid(row=0, column=2, padx=5)

tk.Button(
    button_frame,
    text="Clear Fields",
    command=clear_fields,
    width=15
).grid(row=0, column=3, padx=5)

# Display existing topics
display_topics()

# Run application
root.mainloop()
