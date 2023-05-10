from fastapi import  Depends, APIRouter, status, Response
from api.schemas.admin.request_schema import admin_request_schema
from api.models.model_admin import *
from api.models.model_books import *
from fastapi.responses import JSONResponse
from api.config.get_db_instance import get_db_session
from api.models.model_admin import *
from sqlalchemy.orm import Session
from api.middlewares import authentication_middleware
from api.models.model_books import *
from api.models.model_bookborrow import *


def construct_router():
    #creates admin router

    admin = APIRouter(
        tags=["Admin"]
    )

    @admin.get("/admin/profile")
    async def Admin_Profile(authorization = Depends(authentication_middleware.is_authenticated_admin), db: Session = Depends(get_db_session)):
        try:
            if authorization["flag"]:
                admin = db.query(Admin_Model).filter(Admin_Model.email == authorization["email"]).first()
                
                admin_profile = { "name": admin.name, "yoj": admin.year_of_joining, "email": admin.email }
                return admin_profile
        except:
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content="Internal server error"
            )   


    # add Books a single and a bulk both

    @admin.post("/admin/add/books")
    async def Add_Books(request: list[admin_request_schema.AddBookSchema], authorization = Depends(authentication_middleware.is_authenticated_admin), db: Session = Depends(get_db_session)):
        try:
        
            if authorization["flag"]:

                no_of_books = len(request)
                for i in range(no_of_books):
                    # check if books is already present
                    is_book_exist = db.query(Book_Model).filter(Book_Model.ISBN == request[i].ISBN).first()

                    if not is_book_exist:
                        books = Book_Model(**request[i].__dict__)
                        db.add(books)
                        
                        print("1")
                
                db.commit()
                return JSONResponse(
                    status_code=status.HTTP_201_CREATED,
                    content="Books has been added"
                )
        except:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content="Internal Server Error"
            )

    # update book info a single and a bulk both

    @admin.put("/admin/update/books")
    async def Update_Books(request: list[admin_request_schema.AddBookSchema], authorization = Depends(authentication_middleware.is_authenticated_admin), db: Session = Depends(get_db_session)):
        try:
            if authorization["flag"]:
                no_of_books = len(request)
                for i in range(no_of_books):
                    # check if books is already present
                    is_book_exist = db.query(Book_Model).filter(Book_Model.ISBN == request[i].ISBN).first()
                    print(is_book_exist.title)
                    
                    print("hello")
                    if is_book_exist:
                        is_book_exist.title = request[i].title
                        is_book_exist.author = request[i].author
                        is_book_exist.genre = request[i].genre
                        is_book_exist.year_of_publication = request[i].year_of_publication
                        
                        db.add(is_book_exist)
                        
                        print("1")
                db.commit()
                
                return JSONResponse(
                    status_code=status.HTTP_201_CREATED,
                    content="Books has been updated"
                )
        except:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content="Internal Server Error"
            )
     

    # delete books info 

    @admin.delete("/admin/delete/books")
    async def delete_Books(request: list[admin_request_schema.AddBookSchema], authorization = Depends(authentication_middleware.is_authenticated_admin), db: Session = Depends(get_db_session)):
        try:
            if authorization["flag"]:
                no_of_books = len(request)
                for i in range(no_of_books):
                    # check if books is already present
                    is_book_exist = db.query(Book_Model).filter(Book_Model.ISBN == request[i].ISBN).first()
                    print(is_book_exist.title)
                    
                    print("hello")
                    if is_book_exist:
                        
                        db.delete(is_book_exist)
                        
                        print("1")
                db.commit()
                
                return JSONResponse(
                    status_code=status.HTTP_201_CREATED,
                    content="Books have been deleted"
                )
        except:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content="Internal Server Error"
            )


    #  approve student book borrow request
    @admin.put("/admin/approvebookborrow/")
    async def approve_bookborrow(ISBN: str, rollno: str, authorization = Depends(authentication_middleware.is_authenticated_admin), db: Session= Depends(get_db_session)):

        try: 
            print(ISBN, rollno)
            # request exist with pending status then approve it 
            if authorization["flag"]:
                
                borrow = db.query(Bookborrow_Model).filter(Bookborrow_Model.ISBN == ISBN and Bookborrow_Model.borrowerid == rollno).all()
                
                for i in range(len(borrow)):
                    
                    print(borrow[i].status)

                    if borrow[i].status == "Pending":
                        

                        borrow[i].status = "Approved"

                        

                        db.add(borrow[i])
                        db.commit()

                        #  book availability status update 
                        book = db.query(Book_Model).filter(Book_Model.ISBN == ISBN).first()

                        book.status = 1
                        db.add(book)
                        db.commit()

                        return JSONResponse(
                            status_code=status.HTTP_202_ACCEPTED,
                            content= "Student Book Borrow request approved"
                        ) 
        except:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content="Internal Server Error"
            )   
        

    #  decline student book borrow request
    @admin.put("/admin/declinebookborrow/")
    async def approve_bookborrow(ISBN: str, rollno: str, authorization = Depends(authentication_middleware.is_authenticated_admin), db: Session= Depends(get_db_session)):

        try: 
            print(ISBN, rollno)
            # request exist with pending status then approve it 
            if authorization["flag"]:
                
                borrow = db.query(Bookborrow_Model).filter(Bookborrow_Model.ISBN == ISBN and Bookborrow_Model.borrowerid == rollno).all()
                
                for i in range(len(borrow)):
                    
                    

                    if borrow[i].status == "Pending":

                        db.delete(borrow[i])
                        db.commit()

                        return JSONResponse(
                            status_code=status.HTTP_202_ACCEPTED,
                            content= "Student Book Borrow request Declined"
                        ) 
        except:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content="Internal Server Error"
            )   
            
    return admin