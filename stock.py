user_input = input("Enter ToDo:  ")
todolist = [['Take'],['this'],['sdsd'],['sdsd'],]
try:
    todo = user_input.split('-')[1:]
    todolist.append(todo)
    for item in todolist:
        print(item[0])
except IndexError as error:
    print('Stock not avaialble. Enter in Stock APPL')