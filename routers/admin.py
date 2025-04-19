from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from models import Todos
from starlette import status
from database import SessionLocal
from .auth import get_current_user

router= APIRouter(
     prefix='/admin',
    tags=['admin']
)

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


@router.get("/todo", status_code=status.HTTP_200_OK)
async def get_todos(db: db_dependency, user: user_dependency):
    if user is None or user.get('user_role')!='admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Todos).all()

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todos(db: db_dependency, user: user_dependency, todo_id: int=Path(gt=0)):
    if user is None or user.get('user_role')!='admin':
        raise HTTPException(status_code=401, detail='Authorization Failed')
    todo_model=db.query(Todos).filter(Todos.id==todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')
    db.query(Todos).filter(Todos.id==todo_id).delete()
    db.commit()
    