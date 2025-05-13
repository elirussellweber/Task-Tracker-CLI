import argparse
import json
import os
from datetime import datetime

DATA_FILE = 'tasks.json'

def run_command(args):
    if args[0] == 'add':
        add_task(" ".join(args[1:]))
    elif args[0] == 'update':
        update_task(int(args[1]), " ".join(args[2:]))
    elif args[0] == 'delete':
        delete_task(int(args[1]))
    elif args[0] == 'mark-todo':
        mark_status(int(args[1]), 'todo')
    elif args[0] == 'mark-done':
        mark_status(int(args[1]), 'done')
    elif args[0] == 'mark-in-progress':
        mark_status(int(args[1]), 'in-progress')
    elif args[0] == 'list':
        if len(args) > 1: 
            list_tasks(args[1])
        else: 
            list_tasks()
    elif args[0] == 'help':
        print_help()
    else:
        print("Unknown command. Type 'help' for list of commands.")


def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

def save_tasks(tasks):
    with open(DATA_FILE, 'w') as file:
        json.dump(tasks, file, indent=2)

def add_task(description):
    tasks = load_tasks()
    new_id = 1 if not tasks else tasks[-1]['id'] + 1
    now = datetime.now().isoformat()
    task = {
        "id": new_id,
        "description": description,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {new_id})")

def update_task(task_id, description):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['description'] = description
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            return
    raise ValueError(f"Task with ID {task_id} not found.")

def delete_task(task_id):
    tasks = load_tasks()
    countBefore = len(tasks)
    # save only tasks that do not match task_id
    tasks = [task for task in tasks if task['id'] != task_id]
    countAfter = len(tasks)
    # Check if a task was deleted
    if countBefore == countAfter:
        raise ValueError(f"Task with ID {task_id} not found.")
    save_tasks(tasks)

def mark_status(task_id, status):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = status
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            return
    raise ValueError(f"Task with ID {task_id} not found.")

def list_tasks(status=None):
    tasks = load_tasks()

    # Check how many characters the longest task description has to format the others to match
    max = 0
    for task in tasks:
        if (task['status'] == status or status is None) and len(task['description']) > max:
            max = len(task['description'])
        

    for task in tasks:
        if task['status'] == status or status is None:
            # Time String Formatting
            time_past = datetime.now() - datetime.fromisoformat(task['createdAt'])
            days = time_past.days
            hours = time_past.seconds // 3600
            minutes = (time_past.seconds // 60) % 60
            time_str = ""
            if days > 0:
                time_str += f"{days}d"
            elif hours > 0:
                time_str += f"{hours}hr"
            else:
                time_str += f"{minutes}min"
            time_str += " ago"

            # Making list columns even
            spaces = max - len(task['description'])
            spacesString = " " * spaces
            if task['status'] == 'in-progress':
                statusTabs = "\t"
            else:
                statusTabs = "\t\t"

            print(task['description'] + spacesString + "\t| " + task['status'] + statusTabs + "| id= " + str(task['id']) + "\t| made " + time_str)


def print_help():
    print("Available commands:")
    print("  add <description>         - Add a new task")
    print("  update <id> <description> - Update an existing task")
    print("  delete <id>               - Delete a task")
    print("  mark-todo <id>            - Mark a task as 'todo'")
    print("  mark-done <id>            - Mark a task as 'done'")
    print("  mark-in-progress <id>      - Mark a task as 'in-progress'")
    print("  list [status]             - List tasks (optional status filter)")
    print("  help                      - Show this help message")

def main():
    print("Task Tracker CLI (type 'help' or Ctrl+C to exit)")
    while True:
        try:
            user_input = input(">> ").strip()
            if not user_input:
                continue
            args = user_input.split()
            run_command(args)
        except KeyboardInterrupt:
            print("\nExiting Task Tracker. Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()
