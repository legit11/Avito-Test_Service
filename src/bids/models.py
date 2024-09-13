import enum
import uuid

from sqlalchemy import Column, String, UUID, Enum, ForeignKey, Integer, func, Text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship

from src.database import Base


class BidStatus(str, enum.Enum):
    Created = "Created"
    Published = "Published"
    Canceled = "Canceled"


class AuthorType(str, enum.Enum):
    Organization = "Organization"
    User = "User"


class DecisionStatus(str, enum.Enum):
    Approved = "Approved"
    Rejected = "Rejected"
    Pending = "Pending"


class Bid(Base):
    __tablename__ = "bids"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, unique=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    status = Column(Enum(BidStatus), nullable=False)
    tender_id = Column(UUID(as_uuid=True), ForeignKey("tenders.id"), nullable=False)
    author_type = Column(Enum(AuthorType), nullable=False)
    author_id = Column(UUID(as_uuid=True), nullable=False)
    version = Column(Integer, default=1, nullable=False)
    decision_status = Column(Enum(DecisionStatus), default=DecisionStatus.Pending, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    tenders = relationship("Tender", back_populates="bids")
    feedbacks = relationship("FeedBack", back_populates="bids")

class BidArchive(Base):
    __tablename__ = "bids_archives"

    archive_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, unique=True)
    id = Column(UUID(as_uuid=True), index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    status = Column(Enum(BidStatus), nullable=False)
    tender_id = Column(UUID(as_uuid=True), ForeignKey("tenders.id"), nullable=False)
    author_type = Column(Enum(AuthorType), nullable=False)
    author_id = Column(UUID(as_uuid=True), nullable=False)
    version = Column(Integer, nullable=False)
    decision_status = Column(Enum(DecisionStatus), default=DecisionStatus.Pending, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

    tenders = relationship("Tender", back_populates="bids_archives")


class FeedBack(Base):
    __tablename__ = "feedbacks"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True)
    bid_id = Column(UUID(as_uuid=True), ForeignKey("bids.id"), nullable=False)
    description = Column(String(1000), nullable=False)
    username = Column(String(50), ForeignKey("employee.username"), nullable=False, )
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    user = relationship("Employee", back_populates="feedbacks")
    bids = relationship("Bid", back_populates="feedbacks")