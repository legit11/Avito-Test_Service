import uuid
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.models.dao import OrganizationDAO, EmployeeDAO, OrganizationResponsibleDAO
from src.tenders.dao import TenderDAO, TenderArchiveDAO
from src.tenders.schemas import (Tender, TenderServiceType, TenderCreate,
                                 TenderResponse, TenderStatus, UpdateTenderRequest, TenderQueryType)
from src.utils.custom_exceptions import (
    OrganizationNotFoundException,
    UserNotFoundException,
    ForbiddenActionException,
    ServerErrorException, TenderNotFoundException,
)
from src.utils.error_schemas import (
    custom_422_response,
    custom_500_response,
    custom_401_response,
    custom_403_response,
    custom_404_response_org,
    custom_404_response_tender,
    custom_400_response
)

router = APIRouter(
    prefix="/tenders"
)


@router.get("",
            summary="Получение списка тендеров",
            description="Список публичных тендеров с возможностью фильтрации по типу услуг.\n\n"
            "Если фильтры не заданы, возвращаются все тендеры.",
            response_model=List[Tender],
            responses={
                200: {
                    "description": "Список тендеров, отсортированных по алфавиту по названию.",
                },
                422: custom_422_response,
                500: custom_500_response
                }
            )
async def get_tenders(
        limit: int = Query(
            5,
            ge=1,
            le=100,
            description="Максимальное число возвращаемых объектов."),
        offset: int = Query(
            0,
            ge=0,
            description="Количество объектов, пропущенных с начала."),
        service_type: Optional[List[TenderServiceType]] = Query(
            None,
            description="Вид услуги, к которой относится тендер."
                        " Доступные значения: Construction, Delivery, Manufacture."),
        session: AsyncSession = Depends(get_async_session)
):
    async with session.begin():
        try:
            return await TenderDAO.find_with_filters(
                session,
                limit=limit,
                offset=offset,
                order_by_column="name",
                ascending=True,
                service_type=service_type,
                status=TenderStatus.Published
            )

        except Exception as _:
            raise ServerErrorException()


@router.post("/new",
             summary="Создание нового тендера",
             description="Создание нового тендера с заданными параметрами.",
             response_model=TenderResponse,
             responses={
                 200: {
                     "description": "Тендер успешно создан. Сервер присваивает уникальный идентификатор и время создания.",
                 },
                 401: custom_401_response,
                 403: custom_403_response,
                 404: custom_404_response_org,
                 422: custom_422_response,
                 500: custom_500_response
             }
             )
async def create_tender(
        new_tender: TenderCreate,
        session: AsyncSession = Depends(get_async_session)
):
    async with session.begin():
        try:
            org = await OrganizationDAO.find_one(
                session,
                id=new_tender.organization_id)
            if not org:
                raise OrganizationNotFoundException()

            user = await EmployeeDAO.find_one(session, username=new_tender.creator_username)
            if not user:
                raise UserNotFoundException()

            user_verification = await OrganizationResponsibleDAO.find_one(
                session,
                organization_id=new_tender.organization_id,
                user_id=user.id)
            if not user_verification:
                raise ForbiddenActionException()

            result = await TenderDAO.add_in_db(
                session,
                name=new_tender.name,
                description=new_tender.description,
                status="Created",
                service_type=new_tender.service_type,
                organization_id=new_tender.organization_id,
                creator_username=new_tender.creator_username,
            )

            return result
        except HTTPException as e:
            raise e
        except Exception as _:
            raise ServerErrorException()


@router.get("/my",
            summary="Получить тендеры пользователя",
            description="Получение списка тендеров текущего пользователя.",
            response_model=List[TenderResponse],
            responses={
                200: {
                    "description": "Список тендеров пользователя, отсортированный по алфавиту.",
                },
                401: custom_401_response,
                422: custom_422_response,
                500: custom_500_response
            }
            )
async def get_my_tenders(
        limit: int = Query(
            5,
            ge=1,
            le=100,
            description="Максимальное число возвращаемых объектов."),
        offset: int = Query(
            0,
            ge=0,
            description="Количество объектов, пропущенных с начала."),
        service_type: Optional[List[TenderServiceType]] = Query(
            None,
            description="Вид услуги, к которой относится тендер. "
                        "Доступные значения: Construction, Delivery, Manufacture."),
        username: str = Query(
            ...,
            max_length=50,
            description="Имя пользователя, для которого нужно получить список тендеров"),
        query_type: Optional[TenderQueryType] = Query(
            None,
            description="Тип запроса тендеров. Варианты: 'author', 'responsible', responsible по умолчанию."),
        session: AsyncSession = Depends(get_async_session)
):
    async with session.begin():
        try:
            if query_type is None:
                query_type = TenderQueryType.RESPONSIBLE
            user = await EmployeeDAO.find_one(session, username=username)
            if not user:
                raise UserNotFoundException()

            if query_type == TenderQueryType.AUTHOR:
                tenders = await TenderDAO.find_with_filters(
                    session,
                    limit=limit,
                    offset=offset,
                    order_by_column="name",
                    ascending=True,
                    service_type=service_type,
                    creator_username=user.username
                )

            if query_type == TenderQueryType.RESPONSIBLE:
                org_resp = await OrganizationResponsibleDAO.find_all(session, user_id=user.id)
                org_ids = [org.organization_id for org in org_resp]
                if not org_ids:
                    return []
                tenders = await TenderDAO.find_with_filters(
                    session,
                    limit=limit,
                    offset=offset,
                    organization_id=org_ids,
                    service_type=service_type
                )

            return tenders

        except HTTPException as e:
            raise e

        except Exception as _:
            raise ServerErrorException()


@router.get(
    "/{tender_id}/status",
    summary="Получение текущего статуса тендера",
    description="Получить статус тендера по его уникальному идентификатору.",
    response_model=TenderStatus,
    responses={
        200: {
            "description": "Текущий статус тендера.",
        },
        401: custom_401_response,
        403: custom_403_response,
        404: custom_404_response_tender,
        422: custom_422_response,
        500: custom_500_response
    }
)
async def get_tender_status(
        tender_id: uuid.UUID,
        username: str = Query("test_user", max_length=50, description="username пользователя"),
        session: AsyncSession = Depends(get_async_session)
):
    async with session.begin():
        try:
            user = await EmployeeDAO.find_one(session, username=username)
            if not user:
                raise UserNotFoundException()

            tender = await TenderDAO.find_one(session, id=tender_id)
            if not tender:
                raise TenderNotFoundException()

            if tender.status == "Published":
                return tender.status

            else:
                user_verification = await OrganizationResponsibleDAO.find_one(
                    session,
                    organization_id=tender.organization_id,
                    user_id=user.id)
                if not user_verification:
                    raise ForbiddenActionException()

                return tender.status

        except HTTPException as e:
            raise e

        except Exception as _:
            raise ServerErrorException()


@router.patch(
    "/{tender_id}/status",
    summary="Изменение статуса тендера",
    description="Изменить статус тендера по его идентификатору.",
    response_model=TenderResponse,
    responses={
        200: {
            "description": "Статус тендера успешно изменен.",
        },
        400: custom_400_response,
        401: custom_401_response,
        403: custom_403_response,
        404: custom_404_response_tender,
        422: custom_422_response,
        500: custom_500_response
    }
)
async def edit_tender_status(
        tender_id: uuid.UUID,
        new_status: TenderStatus,
        username: str = Query("test_user", max_length=50, description="username пользователя"),
        session: AsyncSession = Depends(get_async_session)
):
    async with session.begin():
        try:
            user = await EmployeeDAO.find_one(session, username=username)
            if not user:
                raise UserNotFoundException()

            tender = await TenderDAO.find_one(session, id=tender_id)
            if not tender:
                raise TenderNotFoundException()

            user_verification = await OrganizationResponsibleDAO.find_one(
                session,
                organization_id=tender.organization_id,
                user_id=user.id)
            if not user_verification:
                raise ForbiddenActionException()

            if tender.status == new_status:
                raise HTTPException(status_code=400, detail="Новый статус не может быть таким же, как и текущий")

            await TenderDAO.archive(session, tender)

            update_data = {"status": new_status}

            result = await TenderDAO.update_in_db(session, tender, **update_data)

            return TenderResponse.from_orm(result)

        except HTTPException as e:
            raise e

        except Exception as _:
            raise ServerErrorException()


@router.patch(
    "/{tender_id}/edit",
    summary="Редактирование тендера",
    description="Изменение параметров существующего тендера",
    response_model=TenderResponse,
    responses={
        200: {
            "description": "Тендер успешно изменен и возвращает обновленную информацию.",
        },
        400: custom_400_response,
        401: custom_401_response,
        403: custom_403_response,
        404: custom_404_response_tender,
        422: custom_422_response,
        500: custom_500_response
    }
)
async def edit_tender(
        tender_id: uuid.UUID,
        update_data: UpdateTenderRequest,
        username: str = Query("test_user", max_length=50, description="username пользователя"),
        session: AsyncSession = Depends(get_async_session)
):
    async with session.begin():
        try:
            user = await EmployeeDAO.find_one(session, username=username)
            if not user:
                raise UserNotFoundException()

            tender = await TenderDAO.find_one(session, id=tender_id)
            if not tender:
                raise TenderNotFoundException()

            user_verification = await OrganizationResponsibleDAO.find_one(
                session,
                organization_id=tender.organization_id,
                user_id=user.id)
            if not user_verification:
                raise ForbiddenActionException()

            await TenderDAO.archive(session, tender)

            if update_data.name is None:
                update_data.name = tender.name
            if update_data.description is None:
                update_data.description = tender.description
            if update_data.status is None:
                update_data.status = tender.status
            if update_data.service_type is None:
                update_data.service_type = tender.service_type

            update_data_dict = update_data.dict(exclude_unset=True)

            result = await TenderDAO.update_in_db(session, tender, **update_data_dict)

            return TenderResponse.from_orm(result)

        except HTTPException as e:
            raise e

        except Exception as _:
            raise ServerErrorException()


@router.put(
    "/{tender_id}/rollback/{version}",
    summary="Откат версии тендера",
    description="Откатить параметры тендера к указанной версии. "
                "Это считается новой правкой, поэтому версия инкрементируется.",
    response_model=TenderResponse,
    responses={
        200: {
            "description": "Тендер успешно откатан и версия инкрементирована.",
        },
        400: custom_400_response,
        401: custom_401_response,
        403: custom_403_response,
        404: custom_404_response_tender,
        422: custom_422_response,
        500: custom_500_response
    }
)
async def rollback_tender(
        tender_id: uuid.UUID,
        version: int,
        username: str = Query("test_user", max_length=50, description="username пользователя"),
        session: AsyncSession = Depends(get_async_session)
):
    async with session.begin():
        try:
            user = await EmployeeDAO.find_one(session, username=username)
            if not user:
                raise UserNotFoundException()

            tender = await TenderDAO.find_one(session, id=tender_id)
            if not tender:
                raise TenderNotFoundException()

            user_verification = await OrganizationResponsibleDAO.find_one(
                session,
                organization_id=tender.organization_id,
                user_id=user.id)
            if not user_verification:
                raise ForbiddenActionException()

            archive_tender = await TenderArchiveDAO.find_one(session, id=tender_id, version=version)
            if not archive_tender:
                raise HTTPException(status_code=404, detail="Указанная версия тендера не найдена в архиве")

            update_data_dict = {
                "name": archive_tender.name,
                "description": archive_tender.description,
                "status": archive_tender.status,
                "service_type": archive_tender.service_type,
                "version": tender.version,
                "organization_id": archive_tender.organization_id,
                "creator_username": archive_tender.creator_username,
                "created_at": archive_tender.created_at
            }

            await TenderDAO.archive(session, tender)

            result = await TenderDAO.update_in_db(session, tender, **update_data_dict)

            return TenderResponse.from_orm(result)

        except HTTPException as e:
            raise e

        except Exception as _:
            raise ServerErrorException()
