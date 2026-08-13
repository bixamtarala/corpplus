"""Read-only category and product routes for guest catalog discovery."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session

from .catalog_schemas import (
    CategoryListResponse,
    ProductListResponse,
    ProductResponse,
)
from .catalog_service import (
    CatalogProductNotFound,
    CatalogService,
    InvalidCatalogCursor,
)
from .database import get_commerce_db


router = APIRouter(prefix="/api/commerce/v1/catalog", tags=["catalog"])

Locale = Annotated[str, Query(pattern=r"^[a-z]{2}(?:-[A-Z]{2})?$")]


def get_catalog_service(db: Session = Depends(get_commerce_db)) -> CatalogService:
    return CatalogService(db)


@router.get("/categories", response_model=CategoryListResponse)
def list_categories(
    locale: Locale = "en",
    service: CatalogService = Depends(get_catalog_service),
) -> CategoryListResponse:
    return CategoryListResponse(items=service.list_categories(locale=locale))


@router.get("/products", response_model=ProductListResponse)
def list_products(
    locale: Locale = "en",
    category: Annotated[str | None, Query(min_length=1, max_length=100)] = None,
    query: Annotated[str | None, Query(min_length=1, max_length=80)] = None,
    limit: Annotated[int, Query(ge=1, le=50)] = 20,
    cursor: Annotated[str | None, Query(min_length=1, max_length=256)] = None,
    service: CatalogService = Depends(get_catalog_service),
) -> ProductListResponse:
    if query is not None and not query.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be blank")
    try:
        items, next_cursor = service.list_products(
            locale=locale,
            category_slug=category,
            query=query,
            limit=limit,
            cursor=cursor,
        )
    except InvalidCatalogCursor as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return ProductListResponse(items=items, next_cursor=next_cursor)


@router.get("/products/{slug}", response_model=ProductResponse)
def get_product(
    slug: Annotated[str, Path(min_length=1, max_length=140)],
    locale: Locale = "en",
    service: CatalogService = Depends(get_catalog_service),
) -> ProductResponse:
    try:
        return service.get_product(slug=slug, locale=locale)
    except CatalogProductNotFound as exc:
        raise HTTPException(status_code=404, detail="Product not found") from exc
