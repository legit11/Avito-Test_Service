import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.bids.dao import BidDAO, BidArchiveDAO, FeedbackDAO
from src.bids.schemas import BidResponse, BidCreate, AuthorType, BidStatus, UpdateBidRequest, DecisionStatus, \
    FeedBackResponse
from src.database import get_async_session
from src.models.dao import OrganizationDAO, EmployeeDAO, OrganizationResponsibleDAO
from src.tenders.dao import TenderDAO
from src.utils.custom_exceptions import (
    BidNotFoundException,
    TenderNotFoundException,
    OrganizationNotFoundException,
    UserNotFoundException,
    ForbiddenActionException,
    ServerErrorException
)
from src.utils.error_schemas import (
    custom_422_response,
    custom_500_response,
    custom_401_response,
    custom_403_response,
    custom_404_response_tender,
    custom_400_response, custom_404_response_org, custom_404_response_bid
)



router = APIRouter(
    prefix="/bids"
)


@router.post("/new",
             summary="Создание нового предложения",
             description="Создание предложения для существующего тендера.",
             response_model=BidResponse,
             responses={
                 200: {
                     "description": "Предложение успешно создано. Сервер присваивает уникальный идентификатор и время создания.",
                 },
                 401: custom_401_response,
                 403: custom_403_response,
                 404: custom_404_response_tender,
                 422: custom_422_response,
                 500: custom_500_response
             }
             )
async def create_bid(
        new_bid: BidCreate,
        session: AsyncSession = Depends(get_async_session),
):
    async with session.begin():
        try:
            if new_bid.author_type == AuthorType.Organization:
                org = await OrganizationDAO.find_one(
                    session,
                    id=new_bid.author_id)
                if not org:
                    raise OrganizationNotFoundException()

                tender = await TenderDAO.find_one(
                    session,
                    id=new_bid.tender_id)
                if not tender:
                    raise TenderNotFoundException()

            if new_bid.author_type == AuthorType.User:
                user = await EmployeeDAO.find_one(session, id=new_bid.author_id)
                if not user:
                    raise UserNotFoundException()

            result = await BidDAO.add_in_db(
                session,
                name=new_bid.name,
                description=new_bid.description,
                status="Created",
                tender_id=new_bid.tender_id,
                author_type=new_bid.author_type,
                author_id=new_bid.author_id
            )

            return result

        except HTTPException as e:
            raise e

        except Exception as _:
            raise ServerErrorException()


@router.get("/my",
            summary="Получение списка ваших предложений",
            description="Получение списка предложений текущего пользователя.",
            response_model=List[BidResponse],
            responses={
                200: {
                    "description": "Список предложений пользователя, отсортированный по алфавиту.",
                },
                401: custom_401_response,
                422: custom_422_response,
                500: custom_500_response
            }
            )
async def get_my_bids(
        limit: int = Query(
            5,
            ge=1,
            le=100,
            description="Максимальное число возвращаемых объектов."),
        offset: int = Query(
            0,
            ge=0,
            description="Количество объектов, пропущенных с начала."),
        username: str = Query(
            ...,
            max_length=50,
            description="Имя пользователя, для которого нужно получить список предложений"),
        author_type: Optional[AuthorType] = Query(
            AuthorType.User,
            description="От чьего имени создавалось предложение"
        ),
        session: AsyncSession = Depends(get_async_session)
):
    async with session.begin():
        try:
            if author_type is None:
                author_type = AuthorType.User
            user = await EmployeeDAO.find_one(session, username=username)
            if not user:
                raise UserNotFoundException()

            if author_type == AuthorType.User:
                bids = await BidDAO.find_with_filters(
                    session,
                    limit=limit,
                    offset=offset,
                    order_by_column="name",
                    ascending=True,
                    author_id=user.id
                )

            if author_type == AuthorType.Organization:
                org_resp = await OrganizationResponsibleDAO.find_all(session, user_id=user.id)
                org_ids = [org.organization_id for org in org_resp]
                if not org_ids:
                    return []
                bids = await BidDAO.find_with_filters(
                    session,
                    limit=limit,
                    offset=offset,
                    author_id=org_ids,
                )

            return bids

        except HTTPException as e:
            raise e

        except Exception as _:
            raise ServerErrorException()


@router.get("/{tender_id}/list",
            summary="Получение списка предложений для тендера",
            description="Получение предложений, связанных с указанным тендером.",
            response_model=List[BidResponse],
            responses={
                200: {
                    "description": "Список предложений, отсортированный по алфавиту.",
                },
                401: custom_401_response,
                403: custom_403_response,
                404: custom_404_response_tender,
                422: custom_422_response,
                500: custom_500_response
            }
            )
async def get_list_bids(
        tender_id: uuid.UUID,
        username: str = Query(
            ...,
            max_length=50,
            description="Имя пользователя, для которого нужно получить список предложений"),
        limit: int = Query(
            5,
            ge=1,
            le=100,
            description="Максимальное число возвращаемых объектов."),
        offset: int = Query(
            0,
            ge=0,
            description="Количество объектов, пропущенных с начала."),
        session: AsyncSession = Depends(get_async_session),

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

            return await BidDAO.find_with_filters(
                session,
                limit=limit,
                offset=offset,
                order_by_column="name",
                ascending=True,
                status=BidStatus.Published
            )

        except HTTPException as e:
            raise e

        except Exception as _:
            raise ServerErrorException()


@router.get("/{bid_id}/status",
            summary="Получение статуса предложения",
            description="Получить статус предложения по его уникальному идентификатору.",
            response_model=BidStatus,
            responses={
                200: {
                    "description": "Текущий статус предложения.",
                },
                401: custom_401_response,
                403: custom_403_response,
                404: custom_404_response_bid,
                422: custom_422_response,
                500: custom_500_response
            }
            )
async def get_status_bids(
        bid_id: uuid.UUID,
        username: str = Query(
            ...,
            max_length=50,
            description="Имя пользователя, для которого нужно получить статус предложения"),
        session: AsyncSession = Depends(get_async_session),

):
    async with session.begin():
        try:
            user = await EmployeeDAO.find_one(session, username=username)
            if not user:
                raise UserNotFoundException()

            bid = await BidDAO.find_one(session, id=bid_id)
            if not bid:
                raise BidNotFoundException()

            return bid.status

        except HTTPException as e:
            raise e

        except Exception as _:
            raise ServerErrorException()

@router.patch(
    "/{bid_id}/status",
    summary="Изменение статуса предложения",
    description="Изменить статус предложения по его уникальному идентификатору.",
    response_model=BidResponse,
    responses={
        200: {
            "description": "Статус предложения успешно изменен.",
        },
        400: custom_400_response,
        401: custom_401_response,
        403: custom_403_response,
        404: custom_404_response_bid,
        422: custom_422_response,
        500: custom_500_response
    }
)
async def edit_bid_status(
        bid_id: uuid.UUID,
        new_status: BidStatus,
        username: str = Query("test_user", max_length=50, description="username пользователя"),
        session: AsyncSession = Depends(get_async_session)
):
    async with session.begin():
        try:
            user = await EmployeeDAO.find_one(session, username=username)
            if not user:
                raise UserNotFoundException()

            bid = await BidDAO.find_one(session, id=bid_id)
            if not bid:
                raise BidNotFoundException()

            if bid.author_id == user.id:
                if bid.status == new_status:
                    raise HTTPException(status_code=400, detail="Новый статус не может быть таким же, как и текущий")

                await BidDAO.archive(session, bid)

                update_data = {"status": new_status}
                result = await BidDAO.update_in_db(session, bid, **update_data)

                return BidResponse.from_orm(result)

            user_verification = await OrganizationResponsibleDAO.find_one(
                session,
                organization_id=bid.author_id,
                user_id=user.id)
            if not user_verification:
                raise ForbiddenActionException()

            if bid.status == new_status:
                raise HTTPException(status_code=400, detail="Новый статус не может быть таким же, как и текущий")

            await BidDAO.archive(session, bid)

            update_data = {"status": new_status}
            result = await BidDAO.update_in_db(session, bid, **update_data)

            return BidResponse.from_orm(result)

        except HTTPException as e:
            raise e

        except Exception as _:
            print(_)
            raise ServerErrorException()

@router.patch(
    "/{bid_id}/edit",
    summary="Редактирования параметров предложения",
    description="Редактирование существующего предложения.",
    response_model=BidResponse,
    responses={
        200: {
            "description": "Предложение успешно изменено и возвращает обновленную информацию.",
        },
        401: custom_401_response,
        403: custom_403_response,
        404: custom_404_response_bid,
        422: custom_422_response,
        500: custom_500_response
    }
)
async def edit_bid(
        bid_id: uuid.UUID,
        update_data: UpdateBidRequest,
        username: str = Query("test_user", max_length=50, description="username пользователя"),
        session: AsyncSession = Depends(get_async_session)
):
    async with session.begin():
        try:
            user = await EmployeeDAO.find_one(session, username=username)
            if not user:
                raise UserNotFoundException()

            bid = await BidDAO.find_one(session, id=bid_id)
            if not bid:
                raise BidNotFoundException()

            if bid.author_id == user.id:

                await BidDAO.archive(session, bid)

                if update_data.name is None:
                    update_data.name = bid.name
                if update_data.description is None:
                    update_data.description = bid.description
                if update_data.status is None:
                    update_data.status = bid.status

                update_data_dict = update_data.dict(exclude_unset=True)

                result = await BidDAO.update_in_db(session, bid, **update_data_dict)

                return BidResponse.from_orm(result)

            user_verification = await OrganizationResponsibleDAO.find_one(
                session,
                organization_id=bid.author_id,
                user_id=user.id)
            if not user_verification:
                raise ForbiddenActionException()

            await BidDAO.archive(session, bid)

            if update_data.name is None:
                update_data.name = bid.name
            if update_data.description is None:
                update_data.description = bid.description
            if update_data.status is None:
                update_data.status = bid.status

            update_data_dict = update_data.dict(exclude_unset=True)

            result = await BidDAO.update_in_db(session, bid, **update_data_dict)

            return BidResponse.from_orm(result)

        except HTTPException as e:
            raise e

        except Exception as _:
            print(_)
            raise ServerErrorException()

@router.put(
    "/{bid_id}/rollback/{version}",
    summary="Откат версии предложения",
    description="Откатить параметры предложения к указанной версии. "
                "Это считается новой правкой, поэтому версия инкрементируется.",
    response_model=BidResponse,
    responses={
        200: {
            "description": "Предложение успешно откатано и версия инкрементирована.",
        },
        400: custom_400_response,
        401: custom_401_response,
        403: custom_403_response,
        404: custom_404_response_bid,
        422: custom_422_response,
        500: custom_500_response
    }
)
async def rollback_tender(
        bid_id: uuid.UUID,
        version: int,
        username: str = Query("test_user", max_length=50, description="username пользователя"),
        session: AsyncSession = Depends(get_async_session)
):
    async with session.begin():
        try:
            user = await EmployeeDAO.find_one(session, username=username)
            if not user:
                raise UserNotFoundException()

            bid = await BidDAO.find_one(session, id=bid_id)
            if not bid:
                raise BidNotFoundException()

            if bid.author_id == user.id:

                archive_bid = await BidArchiveDAO.find_one(session, id=bid_id, version=version)
                if not archive_bid:
                    raise HTTPException(status_code=404, detail="Указанная версия предложения не найдена в архиве")

                update_data_dict = {
                    "name": archive_bid.name,
                    "description": archive_bid.description,
                    "status": archive_bid.status,
                    "tender_id": archive_bid.tender_id,
                    "author_type": archive_bid.author_type,
                    "author_id": archive_bid.author_id,
                    "version": bid.version,
                    "created_at": archive_bid.created_at
                }

                await BidDAO.archive(session, bid)

                result = await BidDAO.update_in_db(session, bid, **update_data_dict)

                return BidResponse.from_orm(result)

            user_verification = await OrganizationResponsibleDAO.find_one(
                session,
                organization_id=bid.author_id,
                user_id=user.id)
            if not user_verification:
                raise ForbiddenActionException()

            archive_bid = await BidArchiveDAO.find_one(session, id=bid_id, version=version)
            if not archive_bid:
                raise HTTPException(status_code=404, detail="Указанная версия предложения не найдена в архиве")

            update_data_dict = {
                "name": archive_bid.name,
                "description": archive_bid.description,
                "status": archive_bid.status,
                "tender_id": archive_bid.tender_id,
                "author_type": archive_bid.author_type,
                "author_id": archive_bid.author_id,
                "version": bid.version,
                "created_at": archive_bid.created_at
            }

            await BidDAO.archive(session, bid)

            result = await BidDAO.update_in_db(session, bid, **update_data_dict)

            return BidResponse.from_orm(result)

        except HTTPException as e:
            raise e

        except Exception as _:
            print(_)
            raise ServerErrorException()

@router.patch(
    "/{bid_id}/submit_decision",
    summary="Отправка решения по предложения",
    description="Отправить решение (одобрить или отклонить) по предложению.",
    response_model=BidResponse,
    responses={
        200: {
            "description": "Решение по предложению успешно отправлено.",
        },
        400: custom_400_response,
        401: custom_401_response,
        403: custom_403_response,
        404: custom_404_response_bid,
        422: custom_422_response,
        500: custom_500_response
    }
)
async def edit_bid_status(
        bid_id: uuid.UUID,
        decision: DecisionStatus,
        username: str = Query("test_user", max_length=50, description="username пользователя"),
        session: AsyncSession = Depends(get_async_session)
):
    async with session.begin():
        try:
            user = await EmployeeDAO.find_one(session, username=username)
            if not user:
                raise UserNotFoundException()

            bid = await BidDAO.find_one(session, id=bid_id)
            if not bid:
                raise BidNotFoundException()

            tender = await TenderDAO.find_one(session, id=bid.tender_id)
            if not tender:
                raise TenderNotFoundException()

            user_verification = await OrganizationResponsibleDAO.find_one(
                session,
                organization_id=tender.organization_id,
                user_id=user.id)
            if not user_verification:
                raise ForbiddenActionException()

            update_data = {"decision_status": decision}

            result = await BidDAO.update_in_db(session, bid, **update_data)

            return BidResponse.from_orm(result)

        except HTTPException as e:
            raise e

        except Exception as _:
            print(_)
            raise ServerErrorException()

@router.post("/{bid_id}/feedback",
             summary="Отправка отзыва по предложению",
             description="Отправить отзыв по предложение.",
             response_model=FeedBackResponse,
             responses={
                 200: {
                     "description": "Отзыв по предложению успешно отправлен.",
                 },
                 400: custom_400_response,
                 401: custom_401_response,
                 403: custom_403_response,
                 404: custom_404_response_bid,
                 422: custom_422_response,
                 500: custom_500_response
             }
)
async def send_feedback(
        bid_id: uuid.UUID,
        bid_feedback: str = Query("возьмите на стажировку", max_length=1000, description="Фидбэк"),
        username: str = Query("test_user", max_length=50, description="Ваше имя пользователя"),
        session: AsyncSession = Depends(get_async_session),
):
    async with session.begin():
        try:
            user = await EmployeeDAO.find_one(session, username=username)
            if not user:
                raise UserNotFoundException()

            bid = await BidDAO.find_one(session, id=bid_id)
            if not bid:
                raise BidNotFoundException()

            tender = await TenderDAO.find_one(session, id=bid.tender_id)
            if not tender:
                raise TenderNotFoundException()

            user_verification = await OrganizationResponsibleDAO.find_one(
                session,
                organization_id=tender.organization_id,
                user_id=user.id)
            if not user_verification:
                raise ForbiddenActionException()

            result = await FeedbackDAO.add_in_db(
                session,
                bid_id=bid_id,
                description=bid_feedback,
                username=username
            )

            return FeedBackResponse.from_orm(result)

        except HTTPException as e:
            raise e

        except Exception as _:
            print(_)
            raise ServerErrorException()


@router.get("/{tender_id}/reviews",
            summary="Отправка отзыва по предложению",
            description="Отправить отзыв по предложение.",
            response_model=List[FeedBackResponse],
            responses={
                200: {
                    "description": "Список отзывов на предложения указанного автора.",
                },
                400: custom_400_response,
                401: custom_401_response,
                403: custom_403_response,
                404: custom_404_response_bid,
                422: custom_422_response,
                500: custom_500_response
            }
)
async def get_reviews(
        tender_id: uuid.UUID,
        author_username_or_organization_name: str = Query(
            "test_user",
            max_length=50,
            description="Имя пользователя автора предложений, отзывы на которые нужно просмотреть."),
        request_username: str = Query(
            "test_user",
            max_length=50,
            description="Имя пользователя, который запрашивает отзывы."),
        session: AsyncSession = Depends(get_async_session),
        limit: int = Query(
            5,
            ge=1,
            le=100,
            description="Максимальное число возвращаемых объектов."),
        offset: int = Query(
            0,
            ge=0,
            description="Количество объектов, пропущенных с начала."),
):
    async with session.begin():
        try:
            user_request = await EmployeeDAO.find_one(session, username=request_username)
            if not user_request:
                raise UserNotFoundException()

            tender = await TenderDAO.find_one(session, id=tender_id)
            if not tender:
                raise TenderNotFoundException()

            user_req_verification = await OrganizationResponsibleDAO.find_one(
                session,
                organization_id=tender.organization_id,
                user_id=user_request.id)
            if not user_req_verification:
                raise ForbiddenActionException()

            user_author = await EmployeeDAO.find_one(session, username=author_username_or_organization_name)
            if not user_author:
                organization_author = await OrganizationDAO.find_one(session, name=author_username_or_organization_name)
                if not organization_author:
                    raise HTTPException(status_code=404, detail="Автор не существует или некорректен")

            if user_author:
                author = user_author
            elif organization_author:
                author = organization_author
            else:
                raise HTTPException(status_code=404, detail="Автор не существует или некорректен")

            bids = await BidDAO.find_all(session, author_id=author.id)
            reviews = await FeedbackDAO.find_with_filters(
                session,
                limit=limit,
                offset=offset,
                order_by_column="created_at",
                ascending=True,
                bid_id=[bid.id for bid in bids]
            )

            return reviews


        except HTTPException as e:
            raise e

        except Exception as _:
            print(_)
            raise ServerErrorException()
