from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from database.db import get_db
from models.fleet import Platform, Project, Subsystem
from models.user import User
from api.v1.auth import get_current_active_user
from app.schemas import PlatformSchema

router = APIRouter(prefix="/api/v1/hierarchy", tags=["hierarchy"])


@router.get("/", response_model=list[PlatformSchema])
def get_hierarchy(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)
):
    """Returns the full nested hierarchy: Platforms -> Projects -> Subsystems."""
    platforms = (
        db.query(Platform)
        .options(joinedload(Platform.projects).joinedload(Project.subsystems))
        .all()
    )
    return platforms
