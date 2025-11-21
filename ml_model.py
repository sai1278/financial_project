from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database import Base

class MLAnalysis(Base):
    __tablename__ = "ml"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(String(50), unique=True, nullable=False)

    pros = Column(Text)      # JSON string of top 3 pros
    cons = Column(Text)      # JSON string of top 3 cons

    updated_at = Column(DateTime, default=datetime.utcnow)
