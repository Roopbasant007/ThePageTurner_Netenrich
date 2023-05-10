from fastapi import  Depends, HTTPException, APIRouter, status, Response
from api.schemas.admin.request_schema import admin_request_schema
from api.models.model_admin import *
from api.utils.auth_utils.auth_req_utils import get_hashed_password, verify_password, create_access_token
from fastapi.responses import JSONResponse
from api.config.get_db_instance import get_db_session
from sqlalchemy.orm import Session

def construct_router():

    admin = APIRouter(
        tags = ["Admin"]
    )

    @admin.post("/admin/register")
    async def add_admin(admin_details: admin_request_schema.CreateAdminSchema, db: Session = Depends(get_db_session)):
        try:
            
            # check that admin already exist or not
            check_admin_exist = db.query(Admin_Model).filter(Admin_Model.email == admin_details.email).first()

            if check_admin_exist:
                return JSONResponse(
                    status_code=status.HTTP_302_FOUND,
                    content="Admin already Registered"
                )

            admin_details.password = get_hashed_password(admin_details.password)

            new_admin = Admin_Model(**admin_details.__dict__)
            db.add(new_admin)
            db.commit()

            return JSONResponse(
                status_code=status.HTTP_201_CREATED, 
                content="Admin Registration Successful"
            )
        except: 
             
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content="Internal server error"
            ) 
        

    @admin.post("/admin/login")
    async def login_admin(login_details: admin_request_schema.LoginRequestSchema, response: Response, db: Session = Depends(get_db_session)):
        try:
            
            if not login_details.email or not login_details.password:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content="either email or password is empty"
                )
            
            # check admin exist 
            admin = db.query(Admin_Model).filter(Admin_Model.email == login_details.email).first()

            # if admin deosnot exist for provided email
            if not admin:
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content="User Doesnot exist for supplied email"
                )
            
            # check admin password is correct
            check_pwd_correct = verify_password(login_details.password, admin.password)

            if not check_pwd_correct:
                return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content="Incorrect Password"
                )
            
            jwt_token = create_access_token(login_details.email)
            response.set_cookie(key="Authorization_Admin", value=f"Bearer {jwt_token}")
            

            print(admin.password)
            return {"message": "Logged In", "access_token": jwt_token, "token_type": "bearer"}
            
        except:
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content="Internal server error"
            )  

    return admin