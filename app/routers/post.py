from fastapi import status,HTTPException,Depends,APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models,schemas,utils
from ..database import get_db
from typing import List,Optional
from .. import oauth2

router=APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.PostWithVotes])
@router.get("", response_model=List[schemas.PostWithVotes]) #response_model is used to return the data in the format of the pydantic model and List is used to return the data in the format of the pydantic model
def get_posts(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = None):
    query = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id)
    if search:
        query = query.filter(models.Post.content.contains(search))
    posts = query.limit(limit).offset(skip).all()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No posts found")
    # Construct PostWithVotes objects explicitly, converting owner to UserResponse
    result = []
    for post, votes in posts:
        if not post.owner:
            raise HTTPException(status_code=500, detail=f"Owner not found for post {post.id}")
        result.append(
            schemas.PostWithVotes(
                id=post.id,
                title=post.title,
                content=post.content,
                published=post.published,
                created_at=post.created_at,
                owner_id=post.owner_id,
                owner=schemas.UserResponse.from_orm(post.owner),
                votes=int(votes or 0)
            )
        )
    return result
    

    

@router.post("/",response_model=schemas.PostResponse,status_code=status.HTTP_201_CREATED)
@router.post("",response_model=schemas.PostResponse,status_code=status.HTTP_201_CREATED)
def create_post(post:schemas.PostCreate,db:Session=Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):
    #print(current_user.email)  
    new_post=models.Post(owner_id=current_user.id,**post.dict()) #** is used to unpack the dictionary here the pydantic model is used to validate the data and the models.Post is used to create the sqlalchemy model
    db.add(new_post) #adds the new post to the database
    db.commit() #commits the changes to the database
    db.refresh(new_post) #refreshes the new post to get the id similar to returning in postgres and cursor.fetchone()
    return new_post

    '''ensure_db_connection()
    # At this point, cursor and conn are guaranteed to be not None
    assert cursor is not None
    assert conn is not None
    
    try:
        str_id = str(id)
        cursor.execute(
            "INSERT INTO posts (id, title, content, published, rating) VALUES (%s, %s, %s, %s, %s)",
            (str_id, post.title, post.content, post.published, post.rating)
        )
        conn.commit()
        # Return the created post with id as string
        return {"data": {"id": str_id, "title": post.title, "content": post.content, "published": post.published, "rating": post.rating}}
    except Exception as e:
        conn.rollback()
        print(f"Error creating post: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")'''

@router.get("/{id}/",response_model=schemas.PostResponse)
@router.get("/{id}",response_model=schemas.PostResponse)
def get_post(id: int,db:Session=Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):
    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .outerjoin(models.Vote, models.Vote.post_id == models.Post.id)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    post_obj, votes = post
    if not post_obj.owner:
        raise HTTPException(status_code=500, detail=f"Owner not found for post {id}")
    return schemas.PostWithVotes(
        id=post_obj.id,
        title=post_obj.title,
        content=post_obj.content,
        published=post_obj.published,
        created_at=post_obj.created_at,
        owner_id=post_obj.owner_id,
        owner=schemas.UserResponse.from_orm(post_obj.owner),
        votes=int(votes or 0)
    )

   # ensure_db_connection()
   # At this point, cursor and conn are guaranteed to be not None
   # assert cursor is not None
#assert conn is not None
    
'''  try:
        cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
        post = cursor.fetchone()
        
        if not post:
            raise HTTPException(status_code=404, detail=f"Post with id: {id} was not found")
        
        return {"data": post}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching post: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")'''

@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT)
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id) #post_query is used to query the database and filter the post with the id
    post = post_query.first() #post is used to get the post from the database
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    if getattr(post, "owner_id", None) != current_user.id: #getattr is used to get the value of the owner_id and the id from the post and current_user
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return
    

    '''ensure_db_connection()
    # At this point, cursor and conn are guaranteed to be not None
    assert cursor is not None
    assert conn is not None
    
    try:
        str_id = str(id)
        cursor.execute("DELETE FROM posts WHERE id = %s returning *", (str_id,))
        deleted_post = cursor.fetchone()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Post with id: {id} was not found")
        
        conn.commit()
        return {"data": deleted_post}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        print(f"Error deleting post: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")'''

@router.put("/{id}/",response_model=schemas.PostResponse)
@router.put("/{id}",response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()
    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    if getattr(existing_post, "owner_id", None) != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    post_query.update({**post.dict()}, synchronize_session=False)
    db.commit()
    updated_post = post_query.first()
    return updated_post

    '''ensure_db_connection()
    # At this point, cursor and conn are guaranteed to be not None
    assert cursor is not None
    assert conn is not None
    
   # try:
        str_id = str(id)
        cursor.execute(
            "UPDATE posts SET title = %s, content = %s, published = %s, rating = %s WHERE id = %s",
            (post.title, post.content, post.published, post.rating, str_id)
        )
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Post with id: {id} was not found")
        
        conn.commit()
        # Fetch the updated post
        cursor.execute("SELECT * FROM posts WHERE id = %s", (str_id,))
        updated_post = cursor.fetchone()
        
        return {"data": dict(updated_post) if updated_post else None}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        print(f"Error updating post: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")'''