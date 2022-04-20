

user_input = input("Enter ToDo:  ")
try:
    todo = user_input.split(' ')[1]
    print(todo)
except IndexError as error:
    print('Stock not avaialble. Enter in Stock APPL')