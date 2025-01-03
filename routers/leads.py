from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Lead, Template
import openai
from typing import List
import facebook
from datetime import datetime

router = APIRouter(prefix="/leads", tags=["leads"])

# הגדרת OpenAI API
openai.api_key = "your-openai-api-key"  # יש להחליף במפתח אמיתי

def analyze_post_content(content: str):
    """ניתוח תוכן הפוסט באמצעות OpenAI"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "אתה מנתח פוסטים בפייסבוק ומסווג אותם לקטגוריות: בקשה, תלונה, או הצעת עבודה"},
                {"role": "user", "content": f"נתח את הפוסט הבא וסווג אותו: {content}"}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"שגיאה בניתוח הפוסט: {str(e)}")

@router.post("/analyze")
def analyze_lead(post_content: str, user_id: int, group_id: int, db: Session = Depends(get_db)):
    # ניתוח הפוסט
    analysis = analyze_post_content(post_content)
    
    # יצירת ליד חדש
    new_lead = Lead(
        content=post_content,
        post_type=analysis,
        user_id=user_id,
        group_id=group_id,
        created_at=datetime.utcnow()
    )
    
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)
    
    return {"lead_id": new_lead.id, "analysis": analysis}

@router.post("/respond/{lead_id}")
def respond_to_lead(lead_id: int, template_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="ליד לא נמצא")
    
    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="תבנית לא נמצאה")
    
    try:
        # שליחת תגובה לפוסט
        graph = facebook.GraphAPI(access_token=lead.user.facebook_token)
        graph.put_object(lead.facebook_post_id, "comments", message=template.content)
        
        # אם יש מזהה של כותב הפוסט, שליחת הודעה פרטית
        if lead.author_id:
            graph.put_object(lead.author_id, "messages", message=template.content)
        
        # עדכון סטטוס הליד
        lead.responded = True
        lead.response_template_id = template_id
        db.commit()
        
        return {"message": "תגובה נשלחה בהצלחה"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"שגיאה בשליחת התגובה: {str(e)}")

@router.get("/statistics")
def get_lead_statistics(user_id: int, db: Session = Depends(get_db)):
    """קבלת סטטיסטיקות על הלידים"""
    total_leads = db.query(Lead).filter(Lead.user_id == user_id).count()
    responded_leads = db.query(Lead).filter(Lead.user_id == user_id, Lead.responded == True).count()
    leads_by_type = db.query(Lead.post_type, func.count(Lead.id)).\
        filter(Lead.user_id == user_id).\
        group_by(Lead.post_type).all()
    
    return {
        "total_leads": total_leads,
        "responded_leads": responded_leads,
        "leads_by_type": dict(leads_by_type)
    }
