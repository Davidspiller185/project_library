from fastapi import APIRouter,HTTPException,status
from pydantic import BaseModel
from database.book_db import book
from database.member_db import member
from logs.log_config import logger

class Items(BaseModel):
    title:str|None = None
    author:str|None = None
    genre:str|None = None






router=APIRouter()

@router.post("/books")
def post_book(item:Items):
    logger.info("start to add book to the library")
    lst_genre=["Fiction","Non-Fiction","Science","History","Other"]
    if item.genre not in lst_genre:
        logger.error("genre must be correct")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="the genre is not legal")
    logger.info("add to the sql table")
    new_id=book.create_book(item.model_dump())
    logger.info("succsses to add the book in the library")
    return {"messages":"succsses","new_id":new_id}

@router.get("/books")
def get_books():
   logger.info("start to get all the books")
   books=book.get_all_books()
   logger.info("succsses to get all the books")
   return books

@router.get("/books/{id}")
def get_by_id(id:int):
    logger.info("start to get book by id")
    book_by_id=book.get_book_by_id(id)
    if book_by_id is None:
        logger.error("not found book id")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="book id not found")
    logger.info("succsses to get book by id")
    return book_by_id
    
        

@router.patch("/books/{id}")
def patch_book(id:int,item:Items):
    logger.info("start to update book")
    if "genre" in item:
        lst_genre=["Fiction","Non-Fiction","Science","History","other"]
        if item.genre not in lst_genre:
            logger.error("must be genre correct")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="the genre is not legal")
    the_book=book.get_book_by_id(id)
    if the_book is None:
        logger.info("not found the book id")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not found the id")
    logger.info("update the sql table")
    update=book.update_book(id,item.model_dump(exclude_none=True))
    if update:
        logger.info("succsse to update book")
        return {"messages":"succssed to update"}
    logger.error("nothing update, alredy existe")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="book alredy exsiste")
    
@router.patch("/books/{id}/borrow/{member_id}")
def borrow_book(id:int,member_id:int):
        logger.info("start to borrow book")
        book_id=book.get_book_by_id(id)
        if book_id is None:
           logger.error("book id not found")
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="book id not found") 
        found_member=member.get_member_by_id(member_id)
        if found_member is None:
            logger.error("member id not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="member id not found")
        if book_id["is_available"] == False:
            logger.error("book not available")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="book is not available")
        if found_member["is_active"] == False:
            logger.error("member not active")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="member is not active")
        result=book.count_active_borrows_by_member(member_id)
        if result["count_borrow"] >=3:
            logger.error("can't borrow more than 3 books")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Member has reached maximum borrows")
        logger.info("update borrow into the sql table")
        book.set_available(id,False,member_id)
        logger.info("update the increment borrow in the sql table")
        member.increment_borrows(member_id)
        logger.info("succsses to borrow book")
        return {"messages":"succssed to borrow book"}
    
@router.patch("/books/{id}/return/{member_id}")
def return_book(id,member_id):
        logger.info("start to return book in the library")
        book_id=book.get_book_by_id(id)
        if book_id is None:
           logger.error("book id not found")
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="book id not found") 
        found_member=member.get_member_by_id(member_id)
        if found_member is None:
            logger.error("member id not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="member id not found")
        if  book_id["is_available"] == True:
            logger.error("book is not borrowed")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="book is not borrowed")
        lst_book=book.get_all_books()
        for current_book in lst_book:
            if current_book["id"] == id:
                if current_book["borrowed_by_member_id"] != member_id:
                    logger.error("book is not borrowed by this member")
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Book is not borrowed by this member")
        logger.info("update the sql table to return book")       
        book.set_available(id,True,None)
        logger.info("succsses to return book")
        return {"messages":"succsses to return book in the library"}


        

    



        
        


