from database.book_db import book
from database.member_db import member
from fastapi import FastAPI,HTTPException,status

app=FastAPI()

@app.get("/reports/summary")
def summary():
    report_count={}
    total_books=book.count_total_books()
    report_count["total_books"] = total_books[0]["total_books"]
    book_available=book.count_available_books()
    report_count["available_books"] = book_available[0]["total_books_available"]
    book_borrowed=book.count_borrowed_books()
    report_count["currently_borrowed"] = book_borrowed[0]["total_books_borrowed"]
    member_active=member.count_active_members()
    report_count["active_members"] = member_active[0]["total_active"]
    return report_count

@app.get("/reports/books-by-genre")
def book_by_genre(genre:str):
    lst_genre=[]
    dic_genre={}
    lst_genre=["Fiction","Non-Fiction","Science","History","other"]
    if genre not in lst_genre:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="genre is not correct")
    dic_genre["Genre"] = genre
    result_genre=book.count_by_genre(genre)
    dic_genre["COUNT"] = result_genre[0]["total_books_by_genre"]
    lst_genre.append(dic_genre)
    return lst_genre

@app.get("/reports/top-member")
def top_member():
    dic_top={}
    top_borrowed=member.get_top_member()
    dic_top["member_id"] = top_borrowed[0]["id"]
    dic_top["borrowed"] = top_borrowed[0]["total_borrow"]
    return dic_top


