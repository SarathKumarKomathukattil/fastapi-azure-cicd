from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

#GET
@app.get("/")
def read_root():
    return {"Message" : "Hello World"}

@app.get("/greet")
def greet():
    return {"message" : "How are you doing?"}

@app.get("/greet/{name}")
def greet_name(name: str,age:Optional[int] = None):
    return {"message":f"Hey {name}, you are {age} years old"}

#POST
class Student(BaseModel):
    name:str
    age:int
    roll:int

@app.post("/create_student")
def create_student(student:Student):
    return {
        "name":student.name,
        "age":student.age,
        "roll":student.roll
    }

