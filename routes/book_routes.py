from fastapi import FastAPI,HTTPException,status
from pydantic import BaseModel
from database.book_db import book
from database.member_db import member

class Items(BaseModel):
    title:str
    author:str
    genre:str



app=FastAPI()

@app.post("/books")
def post_book(item:BaseModel):
    lst_genre=["Fiction","Non-Fiction","Science","History","other"]
    if item["genre"] not in lst_genre:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="the genre is not legal")
    new_id=book.create_book(item)
    return {"messages":"succsses","new_id":new_id}

@app.get("/books")
def get_books():
   books=book.get_all_books()
   return books

@app.get("/books/{id}")
def get_by_id(id:int):
    book_by_id=book.get_book_by_id(id)
    return book_by_id

@app.patch("/books/{id}")
def patch_book(id:int,item:BaseModel):
    if "genre" in item:
        lst_genre=["Fiction","Non-Fiction","Science","History","other"]
        if item["genre"] not in lst_genre:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="the genre is not legal") 
    try:
        update=book.update_book(id,item.model_dump(exclude_none=True))
        if update:
            return {"messages":"succssed to update"}
        return {"messages":"the updtate already existe"}
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not found the id")
    
@app.patch("/books/{id}/borrow/{member_id}")
def borrow_book(id:int,member_id:int):
    try:
        found_member=member.get_member_by_id(member_id)
        if found_member is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="member id not found")
        book_borrow=book.get_book_by_id(id)
        if book_borrow["is_available"] == False:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="book is not available")
        detail_member=member.get_member_by_id(id)
        if detail_member["is_active"] == False:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="member is not active")
        result=book.count_active_borrows_by_member(member_id)
        if result["count_borrow"] >=3:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Member has reached maximum borrows")
        book.set_available(id,False,member_id)
        member.increment_borrows(member_id)
        return {"messages":"succssed to borrow book"}
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="book id not found")
    
@app.patch("/books/{id}/return/{member_id}")
def return_book(id,member_id):
    try:
        found_member=member.get_member_by_id(member_id)
        if found_member is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="member id not found")
        book_borrow=book.get_book_by_id(id)
        if  book_borrow["is_available"] == True:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="book is not borrowed")
        lst_book=book.get_all_books()
        for book in lst_book:
            if book["id"] == id:
                if book["borrowed_by_member_id"] != member_id:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Book is not borrowed by this member")
        book.set_available(id,True,None)
        return {"messages":"succsses to return book in the library"}
    except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="book id not found")

        

    



        
        


