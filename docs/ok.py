
import os

# Provide the correct path to the todo.db file
db_path = "instance/todo.db"

if os.path.exists(db_path):
    os.remove(db_path)
    print("todo.db has been deleted.")
else:
    print("The file does not exist.")
 
