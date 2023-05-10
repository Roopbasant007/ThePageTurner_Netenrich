from fastapi import  Depends, HTTPException, APIRouter, status, Response
from api.schemas.student.request_schemas import (student_request_schema, connection_request_schema)
from api.schemas.student.reponse_schemas import student_response_schemas
from api.models.model_student import *
from fastapi.responses import JSONResponse
from api.config.get_db_instance import get_db_session
from api.models.model_student import *
from api.models.modal_connection import *
from api.models.model_books import *
from api.models.model_bookborrow import *
from sqlalchemy.orm import Session
from api.middlewares import authentication_middleware


def construct_router():
    #creates student router

    student = APIRouter(
        tags=["Student"]
    )

    @student.get("/student/profile")
    async def student_profile(request: student_request_schema.LoginRequestSchema, authorization = Depends(authentication_middleware.is_authenticated), db: Session = Depends(get_db_session)):
        try:
            if authorization["flag"]:
                student = db.query(Student_Model).filter(Student_Model.rollno == authorization["rollno"]).first()
                
                student_profile = { "name": student.name, "rollno": student.rollno, "dept": student.dept, "course": student.course, "yoa": student.year_of_admission, "email": student.email }
                return student_profile
        except:
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content="Internal server error"
            )   

    #  Connection request

    @student.post("/student/connect/{id}")
    async def connection_request(id: str,  authorization = Depends(authentication_middleware.is_authenticated), db: Session = Depends(get_db_session)):
        try:

            if authorization["flag"]:
                
                connection = Connection_Model(sender = authorization["rollno"], receiver = id, status = "Pending")

                db.add(connection)
                db.commit()

                return JSONResponse(
                    status_code=status.HTTP_201_CREATED,
                    content="Connection Request has been send"
                )

        except:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content="Internal Server Error"
            )  

    #  connection acceptance response

    @student.put("/student/acceptconnection/{id}")
    async def connection_accept(id: str, authorization = Depends(authentication_middleware.is_authenticated), db: Session = Depends(get_db_session)):
        try:
            
            if authorization["flag"]:
                
                # current user is in receiver in connection table
                conn_req = db.query(Connection_Model).filter( Connection_Model.receiver == authorization["rollno"] and Connection_Model.status == "Pending" and Connection_Model.sender == id).first()
                

                conn_req.status = "Accepted"
                db.add(conn_req)
                db.commit()

                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content="You have accepted"
                )
        except:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content="Internal Server Error"
            )

    # connection declination response

    @student.delete("/student/declineconnection/{id}")
    async def connection_decline(id: str, authorization = Depends(authentication_middleware.is_authenticated), db: Session = Depends(get_db_session)):
        try:
            
            if authorization["flag"]:
                
                # current user is in receiver in connection table
                conn_req = db.query(Connection_Model).filter( Connection_Model.receiver == authorization["rollno"] and Connection_Model.status == "Pending" and Connection_Model.sender == id).first()
                
                db.delete(conn_req)
                db.commit()

                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content="You have declined"
                )
        except:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content="Internal Server Error"
            ) 


   # books borrow request
    @student.post("/student/bookborrow/{ISBN}")
    async def book_borrow_request(ISBN: str, authorization = Depends(authentication_middleware.is_authenticated), db: Session = Depends(get_db_session)):
        try:

            if authorization["flag"]:
                print("hi")
                #  if status of book is 0 then available and if 1 then unavaible 
                book_to_borrow = db.query(Book_Model).filter(Book_Model.ISBN == ISBN).first()

                print("hello")

                print(book_to_borrow.title)

                if book_to_borrow.status:
                    return JSONResponse(
                        status_code=status.HTTP_226_IM_USED,
                        content="Book is not avaible for borrow"
                    )
                
                # check if book is already requested by the same user to borrow again 
                borrow = db.query(Bookborrow_Model).filter(Bookborrow_Model.borrowerid == authorization["rollno"] and Bookborrow_Model.ISBN == ISBN).all()

                flag = 0

                for i in range(len(borrow)):
                    if borrow.status == "Pending" or borrow.status == "Approved":
                        flag = 1
                
                if flag == 1:
                    return JSONResponse(
                        status_code=status.HTTP_226_IM_USED,
                        content="Book is not avaible for borrow"
                    )

                borrow_req = Bookborrow_Model( borrowerid = authorization["rollno"], ISBN = ISBN, status = "Pending")
                
                db.add(borrow_req)
                db.commit()

                return JSONResponse(
                    status_code=status.HTTP_201_CREATED,
                    content="Book borrow request has been send"
                )
        except:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content="Internal Server Error"
            )


    # student recommendation based on dept, course, and year of admisssion
    @student.get("/student/recommendedfriends")
    async def friend_recommendation(authorization = Depends(authentication_middleware.is_authenticated), db: Session = Depends(get_db_session)):
        try:

            if authorization["flag"]:
                print("hi")

                cur_user = db.query(Student_Model.course, Student_Model.dept, Student_Model.year_of_admission).filter(Student_Model.rollno == authorization["rollno"]).first()
                
                # friend recommendation based on current user dept, course enrolled, year of admission
                friends_rec = db.query(Student_Model.rollno, Student_Model.name, Student_Model.course, Student_Model.dept, Student_Model.email ).filter(Student_Model.dept == cur_user.dept or Student_Model.course == cur_user.course or Student_Model.year_of_admission <= cur_user.year_of_admission).all()

                return friends_rec

        except:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content="Internal Server Error"
            )


    return student

