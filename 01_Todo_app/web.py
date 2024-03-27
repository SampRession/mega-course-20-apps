import streamlit as st
import functions
import os

if not os.path.exists("todos.txt"):
    with open('todos.txt', 'w') as file:
        pass

todo_list = functions.get_todo_list()


def add_todo():
    new_todo = st.session_state['new_todo']
    if new_todo not in todo_list:
        todo_list.append(new_todo.capitalize() + '\n')
        functions.write_todo_list(todo_list)
        st.session_state['new_todo'] = ""


st.title("My Todo list :")

for index, todo in enumerate(todo_list):
    checkbox = st.checkbox(todo, key=todo)
    if checkbox:
        todo_list.pop(index)
        functions.write_todo_list(todo_list)
        del st.session_state[todo]
        st.rerun()

st.text_input("Add a todo", label_visibility='hidden', placeholder="Add a todo", on_change=add_todo, key='new_todo')
