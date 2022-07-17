import json
from typing import Union

from fastapi import FastAPI, Depends, HTTPException

from app.dependencies import get_db
from app.middleware import BlockAllHttpMethodsExceptGet

from database.crud import check_organism_exists_in_db
from database.schemas import MetaDataResponseList

from rabbitmq.RMQClient import RabbitMQAgent

'''
This file defines the routes that are served by our application.

It is also where we include any middlewares we would like to use.
'''

# Initialise app
app = FastAPI()

# Add custom middlewares
app.add_middleware(
    BlockAllHttpMethodsExceptGet
)

# Declare RabbitMQ Agent
rmqa = RabbitMQAgent(lambda x: json.loads(x)) # RabbitMQ takes function to process result as arg

## API Routes
@app.get('/databases', response_model=MetaDataResponseList)
def metadata_api(
        name: str = None, 
        db_type: str = None, 
        release: Union[int, str] = None,
        offset: int = 0,
        limit: int = 20,
        Session = Depends(get_db)
    ):

    ## Request Validation
    # Ensure at least 1 filter is applied
    if not (name or db_type or release):
        raise HTTPException(status_code=400, detail='User error: No filters applied to query. Please specify at least one of the following - name: organism name, db_type: type of database, release: database version')

    # Ensure release is an integer
    if (release is not None) and (not isinstance(release, int)):
        raise HTTPException(status_code=400, detail='Type error: Integer value expected for release, but f{type(release)} recieved')

    
    if name:

        # If organism name is specified, ensure is it longer than 3 chars
        if len(name) < 3:
            raise HTTPException(status_code=400, detail=f'Value error: Organism name [ {name} ] too short. Min length is 3.')

        # If organism name is specified, ensure it exists in the DB else 404
        organism_exists = check_organism_exists_in_db(Session, name)
        if not organism_exists:
            raise HTTPException(status_code=404, detail=f'Value error: Organism name [ {name} ] not found in database.')

    ### Send message to RabbitMQ
    request = {
        'name': name,
        'db_type': db_type,
        'release': release,
        'offset': offset,
        'limit': limit
    }

    results = rmqa.send_message(request)

    return results
