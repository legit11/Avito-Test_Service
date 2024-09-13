import enum

from sqlalchemy import Integer, Enum
from src.models.models import *
from src.database import Base
import uuid

class TenderStatus(str, enum.Enum):
    Created = "Created"
    Published = "Published"
    Closed = "Closed"

class TenderServiceType(str, enum.Enum):
    Construction = "Construction"
    Delivery = "Delivery"
    Manufacture = "Manufacture"

class Tender(Base):
    __tablename__ = "tenders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, unique=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    status = Column(Enum(TenderStatus), nullable=False)
    service_type = Column(Enum(TenderServiceType), nullable=False)
    version = Column(Integer, default=1, nullable=False)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organization.id"), nullable=False)
    creator_username = Column(String(50), ForeignKey("employee.username"),nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    organization = relationship("Organization", back_populates="tenders")
    creator = relationship("Employee", back_populates="tenders")
    bids = relationship("Bid", back_populates="tenders")
    bids_archives = relationship("BidArchive", back_populates="tenders")

class TenderArchive(Base):
    __tablename__ = "tenders_archives"

    archive_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, unique=True)
    id = Column(UUID(as_uuid=True), index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    status = Column(Enum(TenderStatus), nullable=False)
    service_type = Column(Enum(TenderServiceType), nullable=False)
    version = Column(Integer, nullable=False)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organization.id"), nullable=False)
    creator_username = Column(String(50), ForeignKey("employee.username"),nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

    organization = relationship("Organization", back_populates="tender_archives")
    creator = relationship("Employee", back_populates="tender_archives")