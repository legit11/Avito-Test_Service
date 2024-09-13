from fastapi import HTTPException
from sqlalchemy import select, Column, asc, desc, insert, inspect
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import async_session_maker

class BaseDAO:
    model = None

    @classmethod
    async def find_one(
            cls,
            session: AsyncSession,
            order_by_column=None,
            ascending: bool = True,
            **filter_by
    ):
        try:
            query = select(cls.model)

            for key, value in filter_by.items():
                column = getattr(cls.model, key, None)
                if column is None:
                    raise ValueError(f"Колонка '{key}' не найдена в модели '{cls.model.__name__}'")

                if isinstance(value, list):
                    if len(value) == 1:
                        query = query.filter(column == value[0])
                    else:
                        query = query.filter(column.in_(value))
                elif value == None:
                    pass
                else:
                    query = query.filter(column == value)

            if order_by_column:
                if isinstance(order_by_column, str):
                    order_column = getattr(cls.model, order_by_column, None)
                elif isinstance(order_by_column, Column):
                    order_column = order_by_column
                else:
                    raise ValueError("order_column должен быть строкой или колонкой SQL")

                if not order_column:
                    raise ValueError(f"Колонка '{order_by_column}' не найдена в модели '{cls.model.__name__}'")

                query = query.order_by(asc(order_column) if ascending else desc(order_column))

            query = query.limit(1)

            result = await session.execute(query)
            return result.scalars().first()

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Ошибка выполнения запроса: {str(e)}")


    @classmethod
    async def find_all(
            cls,
            session: AsyncSession,
            order_by_column=None,
            ascending: bool = True,
            **filter_by
    ):
        try:
            query = select(cls.model)

            for key, value in filter_by.items():
                column = getattr(cls.model, key, None)
                if column is None:
                    raise ValueError(f"Колонка '{key}' не найдена в модели '{cls.model.__name__}'")

                if isinstance(value, list):
                    if len(value) == 1:
                        query = query.filter(column == value[0])
                    else:
                        query = query.filter(column.in_(value))
                elif value == None:
                    pass
                else:
                    query = query.filter(column == value)

            if order_by_column:
                if isinstance(order_by_column, str):
                    order_column = getattr(cls.model, order_by_column, None)
                elif isinstance(order_by_column, Column):
                    order_column = order_by_column
                else:
                    raise ValueError("order_column либо строка либо колонка SQL")

                if not order_column:
                    raise ValueError(f"Колонка {order_column} не найдена в модели {cls.model.__name__}")

                query = query.order_by(asc(order_column) if ascending else desc(order_column))

            result = await session.execute(query)
            return result.scalars().all()

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Ошибка выполнения запроса: {str(e)}")

    @classmethod
    async def find_with_filters(
            cls,
            session: AsyncSession,
            limit: int = 5,
            offset: int = 0,
            order_by_column=None,
            ascending: bool = True,
            **filter_by
    ):
        try:
            query = select(cls.model).offset(offset).limit(limit)

            for key, value in filter_by.items():
                column = getattr(cls.model, key, None)
                if column is None:
                    raise ValueError(f"Колонка '{key}' не найдена в модели '{cls.model.__name__}'")

                if isinstance(value, list):
                    if len(value) == 1:
                        query = query.filter(column == value[0])
                    else:
                        query = query.filter(column.in_(value))
                elif value == None:
                    pass
                else:
                    query = query.filter(column == value)

            if order_by_column:
                if isinstance(order_by_column, str):
                    order_column = getattr(cls.model, order_by_column, None)
                elif isinstance(order_by_column, Column):
                    order_column = order_by_column
                else:
                    raise ValueError("order_column либо строка либо колонка SQL")

                if not order_column:
                    raise ValueError(f"Колонка {order_column} не найдена в модели {cls.model.__name__}")

                query = query.order_by(asc(order_column) if ascending else desc(order_column))
            result = await session.execute(query)
            return result.scalars().all()

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Ошибка выполнения запроса: {str(e)}")

    @classmethod
    async def update_in_db(
            cls,
            session: AsyncSession,
            inst,
            **data
    ):
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    for key, value in data.items():
                        if hasattr(inst, key):
                            setattr(inst, key, value)
                        else:
                            raise ValueError(f"Поле '{key}' не существует в модели '{cls.model.__name__}'")

                    if hasattr(inst, 'version'):
                        inst.version += 1

                    await session.merge(inst)
                    return inst

                except IntegrityError as e:
                    raise HTTPException(status_code=400, detail=f"Ошибка обновления данных: {str(e)}")
                except SQLAlchemyError as e:
                    raise HTTPException(status_code=500, detail=f"Ошибка выполнения запроса: {str(e)}")
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")


    @classmethod
    async def add_in_db(
            cls,
            session: AsyncSession,
            **data
    ):
        try:
            query = insert(cls.model).values(**data).returning(*cls.model.__table__.c)
            result = await session.execute(query)
            return result.mappings().one()
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail=f"Ошибка вставки данных: {str(e)}")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Ошибка выполнения запроса: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")


class ArchiveDAO:
    model_archive = None

    @classmethod
    async def archive(
            cls,
            session: AsyncSession,
            inst
    ):
        try:
            inst_dict = {c.key: getattr(inst, c.key) for c in inspect(inst).mapper.column_attrs}
            archive_inst = cls.model_archive(**inst_dict)
            session.add(archive_inst)
            return archive_inst
        except SQLAlchemyError as e:
            raise HTTPException(status_code=400, detail=f"Ошибка архивации данных: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")


