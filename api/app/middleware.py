from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

'''
This file contains custom middlewares which are included to 
tailor how our app treats incoming requests. 
'''

class BlockAllHttpMethodsExceptGet(BaseHTTPMiddleware):
    '''
    This middleware prohibits any incoming requests which 
    are made with a http method other than GET
    '''
    
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        
        # Ensure http method is get or raise 405
        if request.method != 'GET':
            detail = f'Request Error: HTTP method {request.method} is not supported.'
            return JSONResponse({'detail': detail}, status_code=405) 
        
        # process the request and get the response    
        response = await call_next(request)
        
        return response