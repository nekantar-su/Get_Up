user_input = input("Enter ToDo:  ")
todolist = ['Take','this','sdsd','sdsd']

try:
    todo = user_input.split('-')[1:]
    print(todo)
    todolist.append(' '.join(todo))
    
    print(f"Unpacked todoList: {*todolist,}")

except IndexError as error:
    print('Stock not avaialble. Enter in Stock APPL')