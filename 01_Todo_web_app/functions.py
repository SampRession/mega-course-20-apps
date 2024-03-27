FILEPATH = "todos.txt"


def get_todo_list(file_path=FILEPATH):
    """Read a text file and return a list of the to-do items."""
    with open(file_path, "r") as file_local:
        todo_list_local = file_local.readlines()
    return todo_list_local


def write_todo_list(todo_list_arg, file_path=FILEPATH):
    """Write the to-do items list in the text file."""
    with open(file_path, "w") as file_local:
        file_local.writelines(todo_list_arg)


if __name__ == "__main__":
    print("Hello from functions.py")
