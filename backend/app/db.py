import os
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Dict

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./rental.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

class Listing(Base):
    __tablename__ = "listings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    source: Mapped[str] = mapped_column(String(50), index=True)
    source_url: Mapped[str] = mapped_column(Text, unique=True)
    title: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text, default="")
    price: Mapped[int] = mapped_column(Integer, nullable=True)
    beds: Mapped[float] = mapped_column(Float, nullable=True)
    baths: Mapped[float] = mapped_column(Float, nullable=True)
    city: Mapped[str] = mapped_column(String(120), default="")
    photo: Mapped[str] = mapped_column(Text, default="")
    posted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    scraped_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "source": self.source,
            "source_url": self.source_url,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "beds": self.beds,
            "baths": self.baths,
            "city": self.city,
            "photo": self.photo,
            "posted_at": self.posted_at.isoformat() if self.posted_at else None,
            "scraped_at": self.scraped_at.isoformat() if self.scraped_at else None,
        }

Base.metadata.create_all(bind=engine)

@contextmanager
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def upsert_listing(db, item: dict):
    from sqlalchemy import select
    existing = db.execute(select(Listing).where(Listing.source_url == item["source_url"])).scalar_one_or_none()
    if existing:
        existing.title = item.get("title", existing.title)
        existing.price = item.get("price", existing.price)
        existing.photo = item.get("photo", existing.photo or "")
        existing.beds = item.get("beds", existing.beds)
        existing.baths = item.get("baths", existing.baths)
        existing.city = item.get("city", existing.city or "")
        existing.description = item.get("description", existing.description or "")
    else:
        L = Listing(
            source=item.get("source", "unknown"),
            source_url=item["source_url"],
            title=item.get("title", ""),
            description=item.get("description", ""),
            price=item.get("price"),
            beds=item.get("beds"),
            baths=item.get("baths"),
            city=item.get("city", ""),
            photo=item.get("photo", ""),
        )
        db.add(L)
    db.commit()
