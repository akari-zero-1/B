from sqlalchemy import Column, String, Float, Integer, Text, Boolean, DateTime
from datetime import datetime
from ..connection import Base

class ProductModel(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, default="all")
    platform = Column(String, nullable=False)
    platform_name = Column(String, nullable=False)
    original_price = Column(Float, default=0.0)
    current_price = Column(Float, default=0.0)
    discount_percent = Column(Integer, default=0)
    rating = Column(Float, default=5.0)
    reviews_count = Column(String, default="0")
    image = Column(String, default="")
    ai_summary = Column(Text, default="")
    warranty = Column(String, default="")
    external_url = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
