# Task-Tracker-CLI
Track and manage to-do list with CLI (Backend Roadmap Project)

Usage of this program requires python
Start the program in terminal with command: python3 task.py

from there, interact with the program using these commands and usages: 

add <description>         - Add a new task
update <id> <description> - Update an existing task
delete <id>               - Delete a task
mark-todo <id>            - Mark a task as 'todo'
mark-done <id>            - Mark a task as 'done'
mark-in-progress <id>     - Mark a task as 'in-progress'
list [status]             - List tasks (optional status filter)
help                      - Show the help message

Arguments do not need to be placed in quotations or any other syntax
This program will store and reload data in a local json file