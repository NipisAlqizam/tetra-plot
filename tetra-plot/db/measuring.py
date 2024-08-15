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
        sql = "INSERT INTO Measurement(series_id, timestamp, x, y, comment) VALUES (%s, %s, %s, %s, %s)"
        await cur.execute(
            sql,
            (
                measurement.series_id,
                measurement.timestamp,
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
        cur.execute(sql, (series_id))
        connection.commit()

        row = cur.fetchone()
        series = Series(
            id=row[0], user_id=row[1], title=row[2], x_name=row[3], y_name=row[4]
        )
    return series


async def get_measurements(
    connection: aiomysql.Connection, series_id: int
) -> list[Measurement]:
    sql = "SELECT id, series_id, timestamp, x, y, comment FROM Measurement WHERE series_id=%s;"
    async with connection.cursor() as cur:
        cur: aiomysql.Cursor
        cur.execute(sql, (series_id))
        connection.commit()

        res = cur.fetchall()
        measurements = []
        for row in res:
            current_measurement = Measurement(
                id=row[0],
                series_id=row[1],
                timestamp=row[2],
                x=row[3],
                y=row[4],
                comment=row[5],
            )
            measurements.append(current_measurement)
    return measurements
