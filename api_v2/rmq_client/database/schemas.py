from typing import List

from pydantic import BaseModel

'''
In this file we define the pydantic schemas which are used for 
type checking and data validation. 

To group closely related objects, I have also included the 
type definition for the metadata response list. 
'''

class MetaDataResponse(BaseModel):

    dbname: str
    release: int
    dbtype: str
    organism: str

MetaDataResponseList = List[MetaDataResponse]

