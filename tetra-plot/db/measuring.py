import logging

import aiomysql

from models import Series, Measurement

logger = logging.getLogger(__name__)


async def add_series(connection: aiomysql.Connection, series: Series) -> int:
    """
    Add series row to database

    :param connection: database connection object
    :param series: series object without id
    :return: id of the newly created row
    """
    logger.info(f"Adding measurement series {series} to db")
    async with connection.cursor() as cur:
        cur: aiomysql.Cursor
        sql = (
            "INSERT INTO Series(user_id, title, x_name, y_name) VALUES (%s, %s, %s, %s)"
        )
        await cur.execute(
            sql, (series.user_id, series.title, series.x_name, series.y_name)
        )
        await cur.execute(
            "SELECT id FROM Series WHERE user_id=%s ORDER BY id DESC LIMIT 1;",
            (series.user_id),
        )
        await connection.commit()

        row: list[int] = await cur.fetchone()
        return row[0]


async def add_measurement(connection: aiomysql.Connection, measurement: Measurement):
    """
    Add measurement row to database

    :param connection: database connection object
    :param measurement: measurement object without id
    """
    logger.info(f"Adding measurement {measurement} to db")
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
    logger.info(f"Fetching series with id {series_id} from db")
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
    logger.info("Fetching list of series owned by user {user_id} from db")
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
    logger.info(f"Fetching measurments for series {series_id} from db")
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
