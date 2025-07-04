from pydantic import BaseModel,EmailStr, conint
from datetime import datetime
from typing import Optional


class UserResponse(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    
    class Config: 
        from_attributes = True
        orm_mode = True
#pydantic model for the post
class PostBase(BaseModel):
    title:str
    content:str
    published:bool=True
    
class PostCreate(PostBase):
    pass #pass is used to pass the post base model to the post create model
    
#class Post(PostBase):

class PostResponse(PostBase):
    id:int
    owner_id:int
    created_at:datetime
    owner:UserResponse
    votes:int=0
    
    class Config:
        from_attributes = True
    
class UserCreate(BaseModel):
    email:EmailStr
    password:str



class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

 #TokenData is used to get the id from the token    

class TokenData(BaseModel):
    id:Optional[int]=None #Optional is used to make the id optional and it is None by default

class Vote(BaseModel):
    post_id:int
    dir: conint(ge=0,le=1) #type: ignore

class PostWithVotes(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    created_at: datetime
    owner_id: int
    owner: UserResponse
    votes: int

    class Config:
        orm_mode = True