from fastapi import FastAPI, Depends, HTTPException

from app.dependencies import get_db
from app.middleware import BlockAllHttpMethodsExceptGet

from database.crud import get_metadata, check_organism_exists_in_db
from database.schemas import MetaDataResponseList

'''
This file defines the routes that are served by our application.
'''

app = FastAPI()


app.add_middleware(
    BlockAllHttpMethodsExceptGet
)

@app.get('/databases', response_model=MetaDataResponseList)
def metadata_api(
        name: str = None, 
        db_type: str = None, 
        release: int = None, 
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


    ## Service request
    results = get_metadata(Session, name, db_type, release)               

    return results

@app.post('/databases', response_model=MetaDataResponseList)
def metadata_api(
        name: str = None, 
        db_type: str = None, 
        release: int = None, 
        Session = Depends(get_db)
    ):
    return {'data':'success'}