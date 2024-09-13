import uvicorn
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from src.config import SERVER_ADDRESS

from src.tenders.router import router as router_tenders
from src.bids.router import router as router_bids
from src.utils.custom_exceptions import ServerErrorException
from src.utils.error_schemas import get_success_response_example_text, custom_500_response

app = FastAPI(title="Tender Management API",
              root_path="/api",
              root_path_in_servers=False,
              description="API для управления тендерами и предложениями.\n\n"
                          "Основные функции API включают управление тендерами (создание, изменение, получение списка) и управление предложенями (создание, изменение, получение списка).",
              version="1.0",
              servers=[
                  {
                      "url": f"http://{SERVER_ADDRESS}/api",
                      "description": "Локальный сервер API"
                  }
              ]
              )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping",
         description=
         "Этот эндпоинт используется для проверки готовности сервера обрабатывать запросы.\n\n",
         summary="Проверка доступности сервера",
         response_class=PlainTextResponse,
         responses={
            200: get_success_response_example_text(
                description='Сервер готов обрабатывать запросы, если отвечает "200 OK". Тело ответа не важно, достаточно вернуть "ok".',
                example="ok",
         ),
             500: custom_500_response
         }
         )
async def check_ping():
    try:
        return "ok"
    except Exception as _:
        raise ServerErrorException()

app.include_router(router_tenders)
app.include_router(router_bids)


if __name__ == "__main__":
    host, port = SERVER_ADDRESS.split(":")
    uvicorn.run(app, host=host, port=int(port))