from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User, Group
import facebook
import requests
from bs4 import BeautifulSoup
from typing import List
from utils.logger import logger

router = APIRouter(prefix="/facebook", tags=["facebook"])

def get_facebook_api(token: str):
    return facebook.GraphAPI(access_token=token)

@router.post("/connect")
def connect_facebook(token: str, user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="משתמש לא נמצא")
    
    try:
        # בדיקת תקינות הטוקן
        graph = get_facebook_api(token)
        profile = graph.get_object('me')
        
        user.facebook_token = token
        db.commit()
        
        logger.log_facebook_api_request("POST", "/connect", 200)
        return {"message": "התחברות לפייסבוק בוצעה בהצלחה"}
    except Exception as e:
        logger.log_facebook_api_error("/connect", str(e))
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/search-groups")
def search_groups(keywords: List[str], user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.facebook_token:
        raise HTTPException(status_code=400, detail="משתמש לא מחובר לפייסבוק")
    
    graph = get_facebook_api(user.facebook_token)
    groups = []
    
    for keyword in keywords:
        search_results = graph.search(type='group', q=keyword)
        for group in search_results['data']:
            groups.append({
                'id': group['id'],
                'name': group['name'],
                'privacy': group.get('privacy', 'unknown')
            })
    
    logger.log_facebook_api_request("POST", "/search-groups", 200)
    return groups

@router.post("/join-group/{group_id}")
def join_group(group_id: str, user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.facebook_token:
        raise HTTPException(status_code=400, detail="משתמש לא מחובר לפייסבוק")
    
    graph = get_facebook_api(user.facebook_token)
    
    try:
        # ניסיון להצטרף לקבוצה
        graph.put_object(group_id, "", {"member": "true"})
        
        # שמירת הקבוצה במסד הנתונים
        group = Group(
            facebook_group_id=group_id,
            user_id=user_id,
            is_joined=True
        )
        db.add(group)
        db.commit()
        
        logger.log_facebook_api_request("POST", "/join-group", 200)
        return {"message": "הצטרפות לקבוצה בוצעה בהצלחה"}
    except Exception as e:
        logger.log_facebook_api_error("/join-group", str(e))
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/scan-group/{group_id}")
def scan_group(group_id: str, user_id: int, keywords: List[str], db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.facebook_token:
        raise HTTPException(status_code=400, detail="משתמש לא מחובר לפייסבוק")
    
    graph = get_facebook_api(user.facebook_token)
    
    try:
        # קבלת 50 הפוסטים האחרונים
        posts = graph.get_connections(group_id, 'feed', limit=50)
        relevant_posts = []
        
        for post in posts['data']:
            post_content = post.get('message', '')
            if any(keyword.lower() in post_content.lower() for keyword in keywords):
                relevant_posts.append({
                    'id': post['id'],
                    'content': post_content,
                    'created_time': post['created_time'],
                    'author': post.get('from', {}).get('name', 'Unknown')
                })
        
        logger.log_facebook_api_request("GET", "/scan-group", 200)
        return relevant_posts
    except Exception as e:
        logger.log_facebook_api_error("/scan-group", str(e))
        raise HTTPException(status_code=400, detail=str(e))
