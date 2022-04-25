from sqlalchemy import create_engine  
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker
import os

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



def printToDo(number):
    todos = session.query(ToDo).filter(number == ToDo.number)
    for todo in todos:
        print(f"ID: {todo.id} Task: {todo.task} ")

def addTask(number,task):
    newToDo = ToDo(number = number, task = task)
    session.add(newToDo)
    session.commit()

def deleteTask(number,id):
    task_query = session.query(ToDo).filter(id == ToDo.id)
    task = task_query.first()
    if task==None:
        return f"Task {id} does not exist"
    if task.number != number:
        return "Not Authorized"

    task_query.delete(synchronize_session=False)
    session.commit()

    return f"Successfully deleted task {id}!"