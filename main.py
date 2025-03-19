from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
import models 
from models import Todos
from database import engine,SessionLocal

app=FastAPI()

models.Base.metadata.create_all(bind=engine) # this will create everything from database.py file and models.py file to be able to create a new database that has a new table of todos with
# all the columns that we led out in models.py file
# models.Base.metadata.create_all(bind=engine) this will only be ran if our todos.db doesnt exist

def get_db():
    db= SessionLocal()
    try:
        yield db # yeild means only the code prior to and including yeild statement is executed before sending response.The code following the yeild statement is executed after the response has been delivered.
    finally:
        db.close()

# This makes fast api quicker because we can fetch information from a database, return it to the client and then close off the connection to the database after.

db_dependency=Annotated[Session, Depends(get_db)]

@app.get("/")
async def read_all(db :db_dependency ): 
    # Depends is dependency injection. It really means that we need to do something before we execute what we're trying to execute.
    return db.query(Todos).all()

# So we currently are able to now fetch all the information from our database because we are using dependency injection to go ahead and grab and run first.

@app.get("/todo/{todo_id}")
async def read_todo():
    todo_model=db.query(Todos).filter(Todos.id==todo_id).first()