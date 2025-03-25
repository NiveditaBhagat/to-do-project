from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base # for creating database object

SQLALCHEMY_DATABASE_URL='sqlite:///./todosapp.db' 
# This is url is going to be used to create the location of this database on our project.
#  Create an engine for our application. Database engine is something that we can use to able to open up a connection and be able to use our database.

engine=create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}) 
#connect_args are arguments that we can pass into our engine, which will allow us to be able to define some kind of connection to the database
# By default SQLite will allow only one threa to communicate with it.Assuming that each threa will handle an independent request.
# This is to prevent any kind of accident sharing of the same connection for different kind of request.
# But in FASTAPI it is very normal to have more than one thread that could interact with the database at the same time.
# Now we need to create a session local and each instance of the session local will have a database session.

# sqlalchemy cannot enhance a table for us, it can only create for us

SessionLocal= sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base=declarative_base()