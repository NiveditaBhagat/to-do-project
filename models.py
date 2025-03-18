# Model is a way for SQL Alchemy is to be able to understand what kind of databse tables we are going to create.
# Now a database model is going to be the actual record that is inside the database table.
from database import Base
from sqlalchemy import Column, Integer, String,Boolean

class Todos(Base):
    __tablename__='todos' # now this is just a way for SQL alchemy to know what to name this table inside our database later on.


    id=Column(Integer, primary_key=True, index=True)
    title=Column(String)
    description=Column(String)
    priority=Column(Integer)
    complete=Column(Boolean, default=False)
    

