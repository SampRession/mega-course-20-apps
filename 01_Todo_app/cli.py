# from functions import get_todo_list, write_todo_list
import functions
import time


def main():
    now_time = time.strftime("%d %B %Y %H:%M:%S")
    print("It is", now_time + '.')
    while True:
        user_action = input("Type add, show, edit, complete or exit: ")
        user_action = user_action.strip()

        if user_action.startswith("add"):
            todo = user_action[4:]

            todo_list = functions.get_todo_list()

            todo_list.append(todo + "\n")

            functions.write_todo_list(todo_list)
            print(f"A new task was added: {todo.capitalize()}")

        elif user_action.startswith("show"):
            todo_list = functions.get_todo_list()

            for index, task in enumerate(todo_list):
                task = task.capitalize().strip("\n")
                print(f"{index + 1} {task}")

        elif user_action.startswith("edit"):
            try:
                number = int(user_action[5:]) - 1

                todo_list = functions.get_todo_list()

                new_todo = input("What is the new task ? ")
                todo_list[number] = new_todo + "\n"

                functions.write_todo_list(todo_list)

                print("The new task is :", new_todo.capitalize())

            except IndexError:
                print("There is no item with that number.")
                continue
            except ValueError:
                print("Your command is not valid.")
                continue

        elif user_action.startswith("complete"):
            try: 
                number = int(user_action[9:])
                todo_list = functions.get_todo_list()
                msg_item = todo_list[number - 1].capitalize().strip("\n")

                message = f"Task '{msg_item}' marked as complete."
                print(message)
                todo_list.pop(number - 1)

                functions.write_todo_list(todo_list)

            except IndexError:
                print("There is no item with that number.")
                continue
            except ValueError:
                print("Your command is not valid.")
                continue

        elif user_action.startswith("exit"):
            break

        else:
            print("Hey, you entered an unknown value !")

    print("\nExiting the program...\nBye!")


if __name__ == "__main__":
    main()
