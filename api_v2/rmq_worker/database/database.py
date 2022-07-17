import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

'''
This file instantiates a connection with the database server used in
this project. 

The URL of the database is read in from the .env file which an be found
in this projects root directory. 
'''

# Read in the URL from the .env file
SQLALCHEMY_DATABASE_URL = os.environ.get('SQLALCHEMY_DATABASE_URL')

# Create the sqlalchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True # Pessemistic disconnection handling
)

# Create a local session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base ORM class to inherit from
Base = declarative_base()
