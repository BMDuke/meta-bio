from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def root() -> None:
    return {"data":"success"}

@app.get('/databases')
def metadata_api(name = None, db_type = None, release = None):

    result = {'data':'database API endpoint'}

    if name:
        result.update({'name':name})

    if db_type:
        result.update({'db_type':db_type})  

    if release:
        result.update({'release':release})                

    return result  