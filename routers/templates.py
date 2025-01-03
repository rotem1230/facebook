from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Template
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/templates", tags=["templates"])

class TemplateCreate(BaseModel):
    name: str
    content: str
    type: str

class TemplateResponse(BaseModel):
    id: int
    name: str
    content: str
    type: str

@router.post("/", response_model=TemplateResponse)
def create_template(template: TemplateCreate, user_id: int, db: Session = Depends(get_db)):
    new_template = Template(
        name=template.name,
        content=template.content,
        type=template.type,
        user_id=user_id
    )
    db.add(new_template)
    db.commit()
    db.refresh(new_template)
    return new_template

@router.get("/", response_model=List[TemplateResponse])
def get_templates(user_id: int, db: Session = Depends(get_db)):
    templates = db.query(Template).filter(Template.user_id == user_id).all()
    return templates

@router.get("/{template_id}", response_model=TemplateResponse)
def get_template(template_id: int, user_id: int, db: Session = Depends(get_db)):
    template = db.query(Template).\
        filter(Template.id == template_id, Template.user_id == user_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="תבנית לא נמצאה")
    return template

@router.put("/{template_id}", response_model=TemplateResponse)
def update_template(template_id: int, template_update: TemplateCreate, 
                   user_id: int, db: Session = Depends(get_db)):
    template = db.query(Template).\
        filter(Template.id == template_id, Template.user_id == user_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="תבנית לא נמצאה")
    
    template.name = template_update.name
    template.content = template_update.content
    template.type = template_update.type
    
    db.commit()
    db.refresh(template)
    return template

@router.delete("/{template_id}")
def delete_template(template_id: int, user_id: int, db: Session = Depends(get_db)):
    template = db.query(Template).\
        filter(Template.id == template_id, Template.user_id == user_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="תבנית לא נמצאה")
    
    db.delete(template)
    db.commit()
    return {"message": "תבנית נמחקה בהצלחה"}
