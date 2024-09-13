from sqlalchemy import Column, String, TIMESTAMP, func, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
from src.bids.models import *
from src.database import Base
import uuid


class Employee(Base):
    __tablename__ = "employee"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    tenders = relationship("Tender", back_populates="creator")
    responsibilities = relationship("OrganizationResponsible", back_populates="user")
    tender_archives = relationship("TenderArchive", back_populates="creator")
    feedbacks = relationship("FeedBack", back_populates="user")

organization_type_enum = ENUM('IE', 'LLC', 'JSC', name='organization_type', create_type=False)


class Organization(Base):
    __tablename__ = "organization"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, unique=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    type = Column(organization_type_enum, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    tenders = relationship("Tender", back_populates="organization")
    responsibilities = relationship("OrganizationResponsible", back_populates="organization")
    tender_archives = relationship("TenderArchive", back_populates="organization")

class OrganizationResponsible(Base):
    __tablename__ = "organization_responsible"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, unique=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organization.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("employee.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    organization = relationship("Organization", back_populates="responsibilities")
    user = relationship("Employee", back_populates="responsibilities")
