from fastapi import  Depends, APIRouter, status, Query
from fastapi.responses import JSONResponse
from api.config.get_db_instance import get_db_session
from api.models.model_books import *
from sqlalchemy.orm import Session

def construct_router():

    search = APIRouter(
        tags=["Search"]
    )

    @search.get("/books/search_by_title")
    async def search_by_title(search_key: str = Query(..., min_length=1), db: Session = Depends(get_db_session)):
        try:
            books = db.query(Book_Model).filter(Book_Model.title.ilike(f"{search_key}%")).all()
            
            #  to suggest books with unique title if there are more than one book with same title 
            books = set(books)
            books = list(books)

            return {"response":books}
        except:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content="Internal Server Error"
            )
        

    @search.get("/books/search_by_author")
    async def search_by_title(search_key: str = Query(..., min_length=1), db: Session = Depends(get_db_session)):
        try:
            books = db.query(Book_Model).filter(Book_Model.author.ilike(f"{search_key}%")).all()
            
            #  to suggest books with unique title if there are more than one book with same title 
            books = set(books)
            books = list(books)

            return {"response":books}
        except:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content="Internal Server Error"
            )
         

    return search   