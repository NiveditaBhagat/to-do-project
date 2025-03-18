from fastapi import FastAPI
import models 
from database import engine

app=FastAPI()

models.Base.metadata.create_all(bind=engine) # this will create everything from database.py file and models.py file to be able to create a new database that has a new table of todos with
# all the columns that we led out in models.py file



