from pydantic import BaseModel
from typing import List, Any, Dict, Union


class ErrorDetail(BaseModel):
    loc: List[str]
    msg: str
    type: str

class ValidationErrorDetail(BaseModel):
    loc: List[Union[str, int]]
    msg: str
    type: str
    input: Union[str, dict, None] = None

class CustomValidationErrorResponse(BaseModel):
    status_code: int
    error: str
    details: List[ValidationErrorDetail]

class CustomErrorResponse(BaseModel):
    details: str

class SuccessResponse(BaseModel):
    details: str

def get_custom_error_example(description: str, details: str) -> Dict[str, Any]:
    return {
        "description": description,
        "content": {
            "application/json": {
                "schema": CustomErrorResponse.schema(),
                "example": {
                    "details": details
                }
            }
        }
    }

def get_success_response_example_text(description: str, example: str) -> Dict[str, Any]:
    return {
        "description": description,
        "content": {
            "text/plain": {
                "schema": {"type": "string"},
                "example": example
            }
        }
    }


custom_400_response = get_custom_error_example("Неверный формат запроса или его параметры.", "<объяснение, почему запрос пользователя не может быть обработан>")
custom_401_response = get_custom_error_example("Пользователь не существует или некорректен.", "<объяснение, почему запрос пользователя не может быть обработан>")
custom_403_response = get_custom_error_example("Недостаточно прав для выполнения действия.", "<объяснение, почему запрос пользователя не может быть обработан>")
custom_404_response_tender = get_custom_error_example("Тендер не найден.", "<объяснение, почему запрос пользователя не может быть обработан>")
custom_404_response_bid = get_custom_error_example("Предложение не найдено.", "<объяснение, почему запрос пользователя не может быть обработан>")
custom_404_response_org = get_custom_error_example("Организация не найдена.", "<объяснение, почему запрос пользователя не может быть обработан>")
custom_422_response = get_custom_error_example("Неверный формат запроса или его параметры.", "<объяснение, почему запрос пользователя не может быть обработан>")
custom_500_response = get_custom_error_example("Сервер не готов обрабатывать запросы,", "Некоторые проблемы на сервере")
