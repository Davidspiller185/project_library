from database.book_db import book
from database.member_db import member
from fastapi import APIRouter,HTTPException,status
from logs.log_config import logger

router=APIRouter()

@router.get("/reports/summary")
def summary():
    logger.info("start to summary")
    report_count={}
    logger.info("get from sql table count of total books")
    total_books=book.count_total_books()
    report_count["total_books"] = total_books["total_books"]
    logger.info("get from sql table count of available books")
    book_available=book.count_available_books()
    report_count["available_books"] = book_available["total_books_available"]
    logger.info("get from sql table count of borrowed books")
    book_borrowed=book.count_borrowed_books()
    report_count["currently_borrowed"] = book_borrowed["total_books_borrowed"]
    logger.info("get from sql table count active member")
    member_active=member.count_active_members()
    report_count["active_members"] = member_active["total_active"]
    logger.info("succsses to summary")
    return report_count

@router.get("/reports/books-by-genre")
def book_by_genre(genre:str):
    logger.info("start to get book from sql table by genre")
    lst_genre=[]
    dic_genre={}
    lst_genre_still=["Fiction","Non-Fiction","Science","History","other"]
    if genre not in lst_genre_still:
        logger.error("genre is not correct")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="genre is not correct")
    dic_genre["Genre"] = genre
    logger.info("get from sql table count by genre")
    result_genre=book.count_by_genre(genre)
    dic_genre["COUNT"] = result_genre["total_books_by_genre"]
    lst_genre.append(dic_genre)
    logger.info("succsses to get book by genre")
    return lst_genre

@router.get("/reports/top-member")
def top_member():
    logger.info("start to get top member")
    dic_top={}
    logger.info("get from sql table the top member")
    top_borrowed=member.get_top_member()
    dic_top["member_id"] = top_borrowed["id"]
    dic_top["borrowed"] = top_borrowed["total_borrows"]
    logger.info("succsses to get top member")
    return dic_top


