from typing import List

from pydantic import BaseModel

'''

'''

class MetaDataResponse(BaseModel):

    dbname: str
    release: int
    dbtype: str
    organism: str

MetaDataResponseList = List[MetaDataResponse]






## Ensembl Schemas

## API Schemas
# Json response object (dbname, release, dbtype, organism)