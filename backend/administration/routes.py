# backend/administration/routes.py
import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Body
from sqlalchemy.orm import Session
from datetime import timedelta

from backend.database import get_db
from backend.models.administration import Administration
from backend.schemas.common import TokenAdmin, AdminMemoryEntry
from backend.core.security import (
    verify_password, create_access_token_admin, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_admin
)
from backend.utils.files import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt, append_to_knowledge_base
from backend.utils.memory import load_chat_memory, save_chat_memory

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/admin", tags=["Administration"])

@router.post("/token", response_model=TokenAdmin)
async def login_admin(form_data: dict, db: Session = Depends(get_db)):
    admin = db.query(Administration).filter(Administration.username == form_data["username"]).first()
    if not admin or not verify_password(form_data["password"], admin.hashed_password):
        raise HTTPException(status_code=401, detail="Identifiants admin incorrects")
    if admin.role.lower() not in ["administrateur", "super_admin"]:
        raise HTTPException(status_code=403, detail="Accès refusé")
    token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token_admin(data={"sub": admin.username}, expires_delta=token_expires)
    return {"access_tokenAdmin": token, "token_type": "bearer"}

@router.get("/me")
def read_admin_profile(current_admin: Administration = Depends(get_current_admin)):
    return {"id": current_admin.id, "username": current_admin.username, "role": current_admin.role}

@router.get("/chat-memory")
def get_chat_memory(current_user: Administration = Depends(get_current_admin)):
    return load_chat_memory()

@router.post("/chat-memory")
def add_or_update_entry(entry: AdminMemoryEntry, current_user: Administration = Depends(get_current_admin)):
    data = load_chat_memory()
    data[entry.question.lower()] = entry.answer
    save_chat_memory(data)
    return {"message": "Entrée ajoutée ou mise à jour."}

@router.delete("/chat-memory")
def delete_entry(question: str = Body(..., embed=True), current_user: Administration = Depends(get_current_admin)):
    data = load_chat_memory()
    key = question.lower()
    if key in data:
        del data[key]
        save_chat_memory(data)
        return {"message": f"L'entrée '{question}' a été supprimée."}
    raise HTTPException(status_code=404, detail="Entrée non trouvée.")

@router.post("/upload-doc")
async def upload_doc(file: UploadFile = File(...), current_user: Administration = Depends(get_current_admin)):
    filename = file.filename
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif filename.endswith(".docx"):
        text = extract_text_from_docx(file_path)
    elif filename.endswith(".txt"):
        text = extract_text_from_txt(file_path)
    else:
        raise HTTPException(status_code=400, detail="Format non supporté")
    append_to_knowledge_base(filename, text)
    return {"message": "Document appris avec succès."}
