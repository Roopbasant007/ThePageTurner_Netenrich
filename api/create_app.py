from fastapi import FastAPI
from api.routes.student import (student_general_routes, student_main_routes)
from api.routes.admin import (admin_general_routes, admin_main_routes)
from api.routes.book_search import book_search_routes
from api.config.database import Base, engine

def create_app():

    app = FastAPI()

    Base.metadata.create_all(bind=engine)

    base_path = "/api"


    # register student routers
    app.include_router(
        student_general_routes.construct_router(),
        prefix=base_path
    )

    app.include_router(
        student_main_routes.construct_router(),
        prefix=base_path
    )


    #register admin routes

    app.include_router(
        admin_main_routes.construct_router(),
        prefix=base_path
    )

    app.include_router(
        admin_general_routes.construct_router(),
        prefix=base_path
    )

    # register book search routes

    app.include_router(
        book_search_routes.construct_router(),
        prefix=base_path
    )


    

    return app

