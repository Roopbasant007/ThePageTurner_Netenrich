from jose import jwt
from fastapi import Request
from fastapi.responses import JSONResponse
from api.utils.auth_utils.auth_req_utils import (ALGORITHM, JWT_SECRET_KEY)


def is_authenticated(request: Request):

    # print(token)
    token2 = request.cookies.get("Authorization")
    
    if token2 is not None:

        try:
            encoded_jwt = token2.split(" ")[1]
        
            

            payload = jwt.decode(
                encoded_jwt, 
                JWT_SECRET_KEY,
                ALGORITHM
            )
            
            
            return {
                "flag": True, 
                "rollno": payload["sub"]
            }
        
        except jwt.ExpiredSignatureError:

            return {"flag": False, "message": "token expired"}
        


    return {"flag": False, "message": "Authorization Header not present"}



def is_authenticated_admin(request: Request):

    token = request.cookies.get("Authorization_Admin")
    
    
    
    if token is not None:

        try:
            encoded_jwt = token.split(" ")[1]
           
            

            payload = jwt.decode(
                encoded_jwt, 
                JWT_SECRET_KEY,
                ALGORITHM
            )

            
            
            
            return {
                "flag": True, 
                "email": payload["sub"]
            }
        
        except jwt.ExpiredSignatureError:

            return {"flag": False, "message": "token expired"}
    
        


    return {"flag": False, "message": "Authorization Header not present"}