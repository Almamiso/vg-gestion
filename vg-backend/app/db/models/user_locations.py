from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class UserLocation(Base):
    __tablename__ = "user_locations"

    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    location_id: Mapped[int] = mapped_column(Integer, ForeignKey("locations.location_id", ondelete="CASCADE"), primary_key=True)
    role: Mapped[str] = mapped_column(String)

    __table_args__ = (
        UniqueConstraint("user_id", "location_id", name="pk_user_location"),
    )