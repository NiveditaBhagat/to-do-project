
from fastapi import FastAPI
import models 


from database import engine, SessionLocal
from routers import auth, todos, admin

app=FastAPI()


models.Base.metadata.create_all(bind=engine)  # this will create everything from database.py file and models.py file to be able to create a new database that has a new table of todos with
# all the columns that we led out in models.py file
# models.Base.metadata.create_all(bind=engine) this will only be ran if our todos.db doesnt exist
# This line ensures that the database tables are created based on the models defined in models.py. If the database (todos.db) doesn’t exist, it will automatically create the necessary tables.


app.include_router(auth.router)
app.include_router(todos.router) 
app.include_router(todos.router)

