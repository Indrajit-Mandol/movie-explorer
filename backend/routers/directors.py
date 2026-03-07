"""
Director routes for the Movie Explorer API.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from models import Director
from schemas import DirectorsResponse, DirectorDetailSchema, DirectorBriefSchema

router = APIRouter(prefix="/api/directors", tags=["Directors"])


@router.get("/", response_model=DirectorsResponse, summary="List all directors")
def get_directors(
    search: str | None = Query(None, description="Search directors by name"),
    db: Session = Depends(get_db),
):
    """
    Retrieve a list of all directors.

    Supports filtering by:
    - **search**: Partial, case-insensitive name search
    """
    query = db.query(Director)

    if search:
        query = query.filter(Director.name.ilike(f"%{search}%"))

    directors = query.order_by(Director.name).all()

    message = None
    if not directors:
        message = "No directors found"

    return DirectorsResponse(
        directors=[DirectorBriefSchema.model_validate(d) for d in directors],
        count=len(directors),
        message=message,
    )


@router.get("/{director_id}", response_model=DirectorDetailSchema, summary="Get director profile by ID")
def get_director(director_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a director's full profile including their complete filmography.

    Raises **404** if the director does not exist.
    """
    director = db.query(Director).filter(Director.id == director_id).first()
    if not director:
        raise HTTPException(status_code=404, detail=f"Director with id {director_id} not found")
    return DirectorDetailSchema.model_validate(director)
