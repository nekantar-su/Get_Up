from flask import Flask,request
import os
import requests
from twilio.twiml.messaging_response import MessagingResponse
from helpers import lookup
from sqlalchemy import create_engine  
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
#------------------------------------------------------------------------------------------
db_string = f"postgresql://{os.environ['DATABASE_USERNAME']}:{os.environ['DATABASE_PASSWORD']}@{os.environ['DATABASE_HOSTNAME']}/{os.environ['DATABASE_NAME']}"

db = create_engine(db_string)  
base = declarative_base()

class ToDo(base):  
    __tablename__ = 'ToDo'
    id = Column(Integer,primary_key=True,nullable=False)
    number = Column(String)
    task = Column(String)
    

Session = sessionmaker(db)  
session = Session()

base.metadata.create_all(db)



def getToDo(number):
    todos = session.query(ToDo).filter(number == ToDo.number).all()
    return todos

def addTask(number,task):
    newToDo = ToDo(number = number, task = task)
    session.add(newToDo)
    session.commit()

def deleteTask(number,id):
    task_query = session.query(ToDo).filter(id == ToDo.id)
    task = task_query.first()
    if task==None:
        message = f"Task {id} does not exist"
        return message
    elif task.number != number:
        message = "Not Authorized"
        return message
    else:
        task_query.delete(synchronize_session=False)
        session.commit()
        message = f"Successfully deleted task {id}!"
        return message

    #E----------------------------------------------------------
@app.route("/")
def index():
    return "Welcome to the scheduler"

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    number = request.form['From']
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
        
    if 'stock' in incoming_msg:
        try:
            stock = incoming_msg.split(' ')[1]

            stock =lookup(stock)

            if stock == '' or stock == None:
                resp.message("Please enter a valid stock")
            else:
                resp.message(f"{stock['name']} is trading at ${stock['price']}!")

        except IndexError:
            resp.message("Please enter in correct format. IE: Stock APPL")
        


    elif 'nav' in incoming_msg:
        resp.message("You have the following options: \n 1: Type Weather to view the weather \n 2: Type a message to see your phone number and typed message \n 3: Type nav to view options \n 4: Enter a stock to see its price \n 5: Enter todo - followed by task to add to todo \n 6: Enter view to view ToDo list")

    elif 'todo' in incoming_msg:
        try:
            user_todo= incoming_msg.split('-')[1:]
         
            if user_todo[0] == '' or user_todo[0] == None:
                resp.message("No todo listed")
            else:
                addTask(number,user_todo[0])

                resp.message(f"ToDo added {' '.join(user_todo)}.")
            
        except IndexError:
            resp.message("Please enter in correct format. IE: Todo-Take out garbage")

    elif 'view' in incoming_msg:
        list_todos = getToDo(number)
        output = ''
        for todo in list_todos:
            output += '\n'+ 'ID: '+str(todo.id)+' Task: '+todo.task
        resp.message(output)
    
    elif 'completed' in incoming_msg:
        try:
            task_id= incoming_msg.split('-')[1:]
            resp.message(deleteTask(number,task_id))
        except IndexError:
            resp.message("Please enter in correct format. IE: Completed-Take out garbage")

    elif 'weather' in incoming_msg:
        weather_key=os.environ['WEATHER_KEY']
        try:
            city = incoming_msg.split(' ')[1]
            complete_url = "http://api.openweathermap.org/data/2.5/weather?" + "appid=" + weather_key + "&q=" + city + "&units=imperial"
            x = requests.get(complete_url).json()
            if x["cod"] != "404":
                # store the value of "main"
                # key in variable y
                y = x["main"]

                # store the value corresponding
                # to the "temp" key of y
                current_temperature = y["temp"]
                resp.message(f"Temperature (in fahrenheit) is {str(current_temperature)} degrees in {city}!")
            
            else:
                resp.message(f"{city} Not Found ")

        except IndexError:
            resp.message("Please enter correct format: IE: Weather Brooklyn")

    else:    
        # Add a message
        resp.message(f"Hello {number} you said {incoming_msg}")

    return str(resp)


if __name__ == '__main__':
    app.run()