import logging

import asyncio
from typing import Awaitable, Callable, Tuple
import aiomysql

from models import Series, Measurement


async def add_series(connection: aiomysql.Connection, series: Series):
    async with connection.cursor() as cur:
        cur: aiomysql.Cursor
        sql = (
            "INSERT INTO Series(user_id, title, x_name, y_name) VALUES (%s, %s, %s, %s)"
        )
        await cur.execute(
            sql, (series.user_id, series.title, series.x_name, series.y_name)
        )
        await connection.commit()


async def add_measurement(connection: aiomysql.Connection, measurement: Measurement):
    async with connection.cursor() as cur:
        cur: aiomysql.Cursor
        sql = "INSERT INTO Measurement(series_id, measurement_time, x, y, comment) VALUES (%s, %s, %s, %s, %s)"
        await cur.execute(
            sql,
            (
                measurement.series_id,
                measurement.measurement_time,
                measurement.x,
                measurement.y,
                measurement.comment,
            ),
        )
        await connection.commit()


async def get_series(connection: aiomysql.Connection, series_id: int) -> Series:
    sql = "SELECT id, user_id, title, x_name, y_name FROM Series WHERE id=%s;"

    async with connection.cursor() as cur:
        cur: aiomysql.Cursor
        await cur.execute(sql, (series_id))
        await connection.commit()

        row: list = await cur.fetchone()
        series = Series(
            id=row[0], user_id=row[1], title=row[2], x_name=row[3], y_name=row[4]
        )
    return series


async def get_series_by_user_id(
    connection: aiomysql.Connection, user_id: int
) -> list[Series]:
    sql = "SELECT id, user_id, title, x_name, y_name FROM Series WHERE user_id=%s;"
    async with connection.cursor() as cur:
        cur: aiomysql.Cursor
        await cur.execute(sql, (user_id))
        await connection.commit()

        res: list[list] = await cur.fetchall()
        series = []
        for row in res:
            current_series = Series(
                id=row[0], user_id=row[1], title=row[2], x_name=row[3], y_name=row[4]
            )
            series.append(current_series)
    return series


async def get_measurements(
    connection: aiomysql.Connection, series_id: int
) -> list[Measurement]:
    sql = "SELECT id, series_id, measurement_time, x, y, comment FROM Measurement WHERE series_id=%s;"
    async with connection.cursor() as cur:
        cur: aiomysql.Cursor
        await cur.execute(sql, (series_id))
        await connection.commit()

        res: list[list] = await cur.fetchall()
        measurements = []
        for row in res:
            current_measurement = Measurement(
                id=row[0],
                series_id=row[1],
                measurement_time=row[2],
                x=row[3],
                y=row[4],
                comment=row[5],
            )
            measurements.append(current_measurement)
    return measurements
