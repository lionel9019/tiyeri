# backend/agriculture/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.models.agricultural_resource import AgriculturalResource
from backend.schemas.agricultural_resource import (
    ResourceCreate,
    ResourceUpdate,
    ResourceResponse,
)

router = APIRouter(
    prefix="/api/resources",
    tags=["Agricultural Resources"],
)


# === CREATE ===
@router.post("/", response_model=ResourceResponse)
def create_resource(resource: ResourceCreate, db: Session = Depends(get_db)):
    new_resource = AgriculturalResource(**resource.dict())
    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)
    return new_resource


# === READ ALL ===
@router.get("/", response_model=List[ResourceResponse])
def get_resources(db: Session = Depends(get_db)):
    return db.query(AgriculturalResource).all()


# === READ ONE ===
@router.get("/{resource_id}", response_model=ResourceResponse)
def get_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = db.query(AgriculturalResource).filter(AgriculturalResource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource


# === UPDATE ===
@router.put("/{resource_id}", response_model=ResourceResponse)
def update_resource(resource_id: int, data: ResourceUpdate, db: Session = Depends(get_db)):
    resource = db.query(AgriculturalResource).filter(AgriculturalResource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(resource, key, value)

    db.commit()
    db.refresh(resource)
    return resource


# === DELETE ===
@router.delete("/{resource_id}")
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = db.query(AgriculturalResource).filter(AgriculturalResource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    db.delete(resource)
    db.commit()
    return {"message": "Resource deleted successfully"}
