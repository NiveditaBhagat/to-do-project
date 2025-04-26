from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from models import Todos
from starlette import status
from database import SessionLocal
from .auth import get_current_user

router= APIRouter()


# models.Base.metadata.create_all(bind=engine) # this will create everything from database.py file and models.py file to be able to create a new database that has a new table of todos with
# all the columns that we led out in models.py file
# models.Base.metadata.create_all(bind=engine) this will only be ran if our todos.db doesnt exist
# This line ensures that the database tables are created based on the models defined in models.py. If the database (todos.db) doesn’t exist, it will automatically create the necessary tables.



def get_db():
    db= SessionLocal() # Creates a new database session
    try:
        yield db  # Returns the session for use in request handlers
        # yeild means only the code prior to and including yeild statement is executed before sending response.The code following the yeild statement is executed after the response has been delivered.
    finally:
        db.close() # Closes the session after request is complete

# This makes fast api quicker because we can fetch information from a database, return it to the client and then close off the connection to the database after.

db_dependency=Annotated[Session, Depends(get_db)]
user_dependency= Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str=Field(min_length=3)
    description: str=Field(min_length=3, max_length=100)
    priority: int=Field(gt=0,lt=6)
    complete: bool
    

@router.get("/",status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db :db_dependency ): 
    # Depends is dependency injection. It really means that we need to do something before we execute what we're trying to execute.
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication failed')
    return db.query(Todos).filter(Todos.owner_id==user.get('id')).all()

# So we currently are able to now fetch all the information from our database because we are using dependency injection to go ahead and grab and run first.

@router.get("/todo/{todo_id}",status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db:db_dependency,todo_id: int=Path(gt=0) ):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication failed')
    todo_model=db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get('id')).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found.')


@router.post("/todo",status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db:db_dependency,todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication failed')
    todo_model= Todos(**todo_request.model_dump(), owner_id=user.get('id'))
    db.add(todo_model)
    db.commit()


@router.put("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency,
                      todo_request: TodoRequest,
                      todo_id: int =Path(gt=0)
                      ):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication failed')
    todo_model= db.query(Todos).filter(todo_id==Todos.id).filter(Todos.owner_id==user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail='Todo not found.')
    
    todo_model.title = todo_request.title
    todo_model.description=todo_request.description
    todo_model.priority=todo_request.priority
    todo_model.complete=todo_request.complete
    db.add(todo_model)
    db.commit()

    

@router.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency,todo_id: int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication failed')
    todo_model=db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code= 404, detail='Todo not found.')
    db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get('id')).delete()

    db.commit()

