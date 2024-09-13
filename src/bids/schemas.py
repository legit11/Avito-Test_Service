from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field



class BidStatus(str, Enum):
    Created = "Created"
    Published = "Published"
    Canceled = "Canceled"

class AuthorType(str, Enum):
    Organization = "Organization"
    User = "User"

class DecisionStatus(str, Enum):
    Approved = "Approved"
    Rejected = "Rejected"
    Pending = "Pending"

class FeedBackResponse(BaseModel):
    id: UUID = Field(..., example="550e8400-e29b-41d4-a716-446655440000")
    description: str = Field(..., example="Возьмите на стажировку")
    username: str = Field(..., example="username пользователя оставившего комент")
    created_at: datetime = Field(..., example="2006-01-02T15:04:05Z07:00")

    class Config:
        from_attributes = True
class BidCreate(BaseModel):
    name: str = Field(..., example="Доставка товаров Алексей")
    description: str = Field(..., example="Доставлю любой товар за 100 рублей")
    tender_id: UUID = Field(..., example="550e8400-e29b-41d4-a716-446655440000")
    author_type: AuthorType = Field(..., example="Organization")
    author_id: UUID = Field(..., example="550e8400-e29b-41d4-a716-446655440000")

class BidResponse(BaseModel):
    id: UUID = Field(..., example="550e8400-e29b-41d4-a716-446655440000")
    name: str = Field(..., example="Доставка товаров Алексей")
    description: str = Field(..., example="Доставлю любой товар за 100 рублей")
    status: BidStatus = Field(..., example="Created")
    tender_id: UUID = Field(..., example="550e8400-e29b-41d4-a716-446655440000")
    author_type: AuthorType = Field(..., example="Organization")
    author_id: UUID = Field(..., example="550e8400-e29b-41d4-a716-446655440000")
    version: int = Field(..., example=1)
    decision_status: DecisionStatus = Field(..., example="Approved")
    created_at: datetime = Field(..., example="2006-01-02T15:04:05Z07:00")
    updated_at: datetime = Field(..., example="2006-01-02T15:04:05Z07:00")

    class Config:
        from_attributes = True

class UpdateBidRequest(BaseModel):
    name: Optional[str] = Field(None, max_length=100, description="Название тендера")
    description: Optional[str] = Field(None, max_length=500, description="Описание тендера")
    status: Optional[BidStatus] = Field(None, description="Статус тендера")
