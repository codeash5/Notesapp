from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    owner = relationship("User", back_populates="notes")