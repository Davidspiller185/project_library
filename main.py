from fastapi import FastAPI,Request
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
import mysql.connector
from routes import book_routes,member_routes,report_routes
from database.db_connection import connect_db

@asynccontextmanager
async def lifespan(app:FastAPI):
    try:
        connect_db.create_tables()
    except mysql.connector.Error as e:
        raise RuntimeError(f"Databse startup failed: {e}")
    yield



app=FastAPI(lifespan=lifespan)


@app.exception_handler(mysql.connector.Error)
async def sql_exception_handler(req:Request,exc:mysql.connector.Error):
    return JSONResponse(
        status_code=500,
        content={"error":"Database error", "detail":str(exc)}
    )



app.include_router(book_routes.router)
app.include_router(member_routes.router)
app.include_router(report_routes.router)






