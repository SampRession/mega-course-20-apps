import functions
import PySimpleGUI as sg
import time
import os

if not os.path.exists("todos.txt"):
    with open('todos.txt', 'w') as file:
        pass


sg.theme("DarkAmber")

clock_label = sg.Text('', key='clock')
label = sg.Text("Type in a to-do :")

input_box = sg.InputText(tooltip="Enter todo", key='todo')
todo_box = sg.Listbox(
    values=functions.get_todo_list(), key='todos', enable_events=True, size=(45, 10), expand_y=True, expand_x=True
)

add_button = sg.Button('Add', bind_return_key=True)
edit_button = sg.Button('Edit')
complete_button = sg.Button('Complete')
exit_button = sg.Button('Exit')

window = sg.Window(
    "My To-Do App",
    layout=[[clock_label], [label], [input_box, add_button], [todo_box, edit_button, complete_button], [exit_button]],
    font=("Montserrat Medium", 10),
    resizable=True,
)

while True:
    event, values = window.read(timeout=500)
    window['clock'].update(value=time.strftime("%d %B %Y %H:%M:%S"))
    match event:
        case 'Add':
            if values['todo'] != '':
                todo_list = functions.get_todo_list()
                new_todo = values['todo'] + "\n"
                todo_list.append(new_todo.capitalize())
                functions.write_todo_list(todo_list)
                window['todos'].update(values=todo_list)
                window['todo'].update(value='')
            else:
                sg.popup("Please enter a to-do first.", title="Error", font=("Montserrat Medium", 10))
        case 'todos':
            window['todo'].update(value=values['todos'][0].strip('\n'))
        case 'Edit':
            try:
                todo_to_edit = values['todos'][0]
                new_todo = values['todo'] + "\n"

                todo_list = functions.get_todo_list()
                index = todo_list.index(todo_to_edit)
                todo_list[index] = new_todo.capitalize()
                functions.write_todo_list(todo_list)
                window['todos'].update(values=todo_list)
                window['todo'].update(value='')
            except IndexError:
                sg.popup("Please select an item first.", title="Error", font=("Montserrat Medium", 10))
        case 'Complete':
            try:
                todo_to_complete = values['todos'][0]
                todo_list = functions.get_todo_list()
                todo_list.remove(todo_to_complete)
                functions.write_todo_list(todo_list)
                window['todos'].update(values=todo_list)
                window['todo'].update(value='')
            except IndexError:
                sg.popup("Please select an item first.", title="Error", font=("Montserrat Medium", 10))
        case 'Exit':
            break
        case sg.WIN_CLOSED:
            break

window.close()
