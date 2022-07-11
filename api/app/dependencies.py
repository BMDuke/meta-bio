from database.database import SessionLocal

'''
This file contains any dependencies which we include in the path
functions of our server.
'''

def get_db():
    '''
    This function is responsible for instantiating a new database
    session for wach request. It keeps the connection open for the 
    duration of the request and then finally closes the connection,
    returning that connection to the database. 
    '''
    db = SessionLocal()
    try:        
        yield db    
    finally: 
        db.close()

