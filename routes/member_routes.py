from database.member_db import member
from fastapi import APIRouter,HTTPException,status
from pydantic import BaseModel
from logs.log_config import logger

class Items(BaseModel):
    name:str|None=None
    email:str|None=None


router=APIRouter()



@router.post("/members")
def post_member(item:Items):
    logger.info("start to add memmber")
    logger.info("add to the sql table")
    new_id=member.create_member(item.model_dump())
    logger.info("succsses to add memmer")
    return {"messages":"succssed to add member",new_id:new_id}

@router.get("/members")
def get_members():
    logger.info("start to get all members")
    members=member.get_all_members()
    logger.info("success to get all the members")
    return members

@router.get("/members/{id}")
def get_by_id(id:int):
    logger.info("start to get member by id")
    the_member=member.get_member_by_id(id)
    if the_member is None:
        logger.error("not found member by id")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="id member not found")
    logger.info("succsses to get member by id ")
    return the_member
   

@router.patch("/members/{id}")
def patch_member(id:int,item:Items):
    logger.info("start to the update member")
    member_found=member.get_member_by_id(id)
    if member_found is None:
        logger.error("member id not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="member id not found")
    logger.info("update the sql table")
    update=member.update_member(id,item.model_dump(exclude_none=True))
    if update:
        logger.info("succsses to update member ")
        return {"messages":"succsses to update"}
    logger.info("not succsses to update")
    return {"messages":"not succsses to update"}

@router.patch("/members/{id}/deactivate")
def deactivate(id:int):
    logger.info("start to deactivate")
    member_found=member.get_member_by_id(id)
    if member_found is None:
        logger.error("member id not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="member id not found")
    logger.info("update the sql table to deactivate")
    result=member.deactivate_member(id)
    if result:
        logger.info("succsses to deativate member")
        return {"meesages":"succsses to deactivate member"}
    logger.error("member alredy deactivate")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="member alredy deactivate")
    

@router.patch("/members/{id}/activate")
def activate(member_id:int):
    logger.info("start to ativate member")
    member_found=member.get_member_by_id(member_id)
    if member_found is None:
        logger.error("member id not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="member id not found")
    logger.info("update the sql table to activate")
    result=member.activate_member(member_id)
    if result:
        logger.info("succsses to active member")
        return {"messages": "succssed to activate member"}
    logger.error("member alredy activate")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="member alredy activate")






