from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class TenderStatus(str, Enum):
    Created = "Created"
    Published = "Published"
    Closed = "Closed"

class TenderStatusResponse(BaseModel):
    status: TenderStatus


class TenderServiceType(str, Enum):
    Construction = "Construction"
    Delivery = "Delivery"
    Manufacture = "Manufacture"



class Tender(BaseModel):
    id: UUID = Field(
        ...,
        example="550e8400-e29b-41d4-a716-446655440000",
        description="Уникальный идентификатор тендера, присвоенный сервером."
    )
    name: str = Field(
        ...,
        max_length=100,
        example="Доставка товары Казань - Москва",
        description="Полное название тендера"
    )
    description: str = Field(
        ...,
        max_length=500,
        example="Нужно доставить оборудование для олимпиады по робототехники",
        description="Описание тендера"
    )
    status: TenderStatus = Field(
        ...,
        example="Created",
        description="Статус тендера"
    )
    service_type: TenderServiceType = Field(
        ...,
        example="Delivery",
        description="Вид услуги, к которой относиться тендер"
    )
    version: int = Field(
        1,
        ge=1,
        example=1,
        description="Номер версии после правок"
    )
    organization_id: UUID = Field(
        ...,
        example="550e8400-e29b-41d4-a716-446655440000",
        description="Уникальный идентификатор организации, присвоенный сервером."
    )
    creator_username: str = Field(
        ...,
        max_length=50,
        example="test_user",
    )
    created_at: datetime = Field(
        ...,
        example="2006-01-02T15:04:05Z07:00",
        description="Серверная дата и время в момент, когда пользователь отправил тендер на создание. Передается в формате RFC3339."
    )

class TenderCreate(BaseModel):
    name: str = Field(..., example="Доставка товары Казань - Москва")
    description: str = Field(..., example="Нужно доставить оборудование для олимпиады по робототехнике")
    service_type: TenderServiceType = Field(..., example="Delivery")
    organization_id: UUID = Field(..., example="550e8400-e29b-41d4-a716-446655440000")
    creator_username: str = Field(..., example="test_user")

class TenderResponse(BaseModel):
    id: UUID = Field(..., example="550e8400-e29b-41d4-a716-446655440000")
    name: str = Field(..., example="Доставка товары Казань - Москва")
    description: str = Field(..., example="Нужно доставить оборудование для олимпиады по робототехнике")
    status: TenderStatus = Field(..., example="Created")
    service_type: TenderServiceType = Field(..., example="Delivery")
    version: int = Field(..., example=1)
    organization_id: UUID = Field(..., example="550e8400-e29b-41d4-a716-446655440000")
    creator_username: str = Field(..., example="test_user")
    created_at: datetime = Field(..., example="2006-01-02T15:04:05Z07:00")
    updated_at: datetime = Field(..., example="2006-01-02T15:04:05Z07:00")

    class Config:
        from_attributes = True

class TenderQueryType(Enum):
    AUTHOR = "author"
    RESPONSIBLE = "responsible"

class UpdateTenderRequest(BaseModel):
    name: Optional[str] = Field(None, max_length=100, description="Название тендера")
    description: Optional[str] = Field(None, max_length=500, description="Описание тендера")
    status: Optional[TenderStatus] = Field(None, description="Статус тендера")
    service_type: Optional[TenderServiceType] = Field(None, description="Тип услуги тендера")

class ErrorResponse(BaseModel):
    reason: str = Field(
        ...,
        min_length=5,
        example="Описание ошибки в свободной форме",
        description="Используется для возвращения ошибки пользователю"
    )