from fastapi import  Depends, HTTPException, APIRouter, status, Response
from api.schemas.student.request_schemas import student_request_schema
from api.models.model_student import *
from api.utils.auth_utils.auth_req_utils import get_hashed_password, verify_password, create_access_token
from fastapi.responses import JSONResponse
from api.config.get_db_instance import get_db_session
from sqlalchemy.orm import Session


def construct_router():
    #creates student router

    student = APIRouter(
        tags=["Student"]
    )

    @student.post("/student/register")
    async def add_student(student_details: student_request_schema.CreateStudentSchema, db: Session = Depends(get_db_session)):
        try:
            
            # check that student already exist or not
            check_student_exist = db.query(Student_Model).filter(Student_Model.rollno == student_details.rollno).first()

            if check_student_exist:
                return JSONResponse(
                    status_code=status.HTTP_302_FOUND,
                    content="Student already Registered"
                )

            student_details.password = get_hashed_password(student_details.password)

            newstudent = Student_Model(**student_details.__dict__)
            db.add(newstudent)
            db.commit()

            return JSONResponse(
                status_code=status.HTTP_201_CREATED, 
                content="Student Registration Successful"
            )
        except: 
             
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content="Internal server error"
            ) 
        

    # ============================Login Student==========================
    """Here Session = Depends(get_db_session), is a dependency injection of the instance of database that has been assigned in db"""

    @student.post("/student/login")
    async def login_student(login_details: student_request_schema.LoginRequestSchema, response: Response, db: Session = Depends(get_db_session)):
        try:
            
            if not login_details.rollno or not login_details.password:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content="either rollno or password is empty"
                )
            
            # check student exist 
            student = db.query(Student_Model).filter(Student_Model.rollno == login_details.rollno).first()

            # if student deosnot exist for provided email
            if not student:
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content="User Doesnot exist for supplied email"
                )
            
            # check student password is correct
            check_pwd_correct = verify_password(login_details.password, student.password)

            if not check_pwd_correct:
                return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content="Incorrect Password"
                )
            
            jwt_token = create_access_token(login_details.rollno)
            response.set_cookie(key="Authorization", value=f"Bearer {jwt_token}")
            

            print(student.password)
            return {"message": "Logged In", "access_token": jwt_token, "token_type": "bearer"}
            
        except:
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content="Internal server error"
            )

    return student        

    
    
