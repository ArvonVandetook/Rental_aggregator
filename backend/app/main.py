from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from .db import get_session, upsert_listing, Listing
from .scrapers import fetch_craigslist

app = FastAPI(title="Rental Aggregator Backend")

class SearchIn(BaseModel):
    location: str = "sfbay"
    radius_km: float = 10.0
    min_price: Optional[int] = None
    max_price: Optional[int] = None
    beds: Optional[float] = None
    baths: Optional[float] = None
    keywords: Optional[str] = None

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/search")
def start_search(q: SearchIn):
    try:
        items = fetch_craigslist(
            location_subdomain=q.location,
            min_price=q.min_price,
            max_price=q.max_price,
            beds=q.beds,
            query=q.keywords,
            pages=1
        )
        with get_session() as s:
            for it in items:
                upsert_listing(s, it)
        return {"added_or_updated": len(items), "source": "craigslist", "location": q.location}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/listings")
def list_listings(
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    beds: Optional[float] = None,
    baths: Optional[float] = None,
    city: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    with get_session() as s:
        from sqlalchemy import select
        stmt = select(Listing)
        if min_price is not None:
            stmt = stmt.where(Listing.price >= min_price)
        if max_price is not None:
            stmt = stmt.where(Listing.price <= max_price)
        if beds is not None:
            stmt = stmt.where(Listing.beds >= beds)
        if baths is not None:
            stmt = stmt.where(Listing.baths >= baths)
        if city:
            stmt = stmt.where(Listing.city == city)
        stmt = stmt.order_by(Listing.scraped_at.desc()).limit(limit).offset(offset)
        rows = s.execute(stmt).scalars().all()
        return {"items": [r.to_dict() for r in rows], "count": len(rows)}
