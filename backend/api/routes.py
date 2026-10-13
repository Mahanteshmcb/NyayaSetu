

from fastapi import APIRouter

from backend.repository.category_repository import get_categories

router = APIRouter()


@router.get("/categories")
def categories():
    return {
        "count": len(get_categories()),
        "categories": get_categories(),
    }