import logging

import pytest
import pytest_asyncio
import aiomysql

import config
import db
import models


pytest_plugins = ("pytest_asyncio",)


@pytest_asyncio.fixture
async def mysql_connection():
    connection = await db.get_mysql_connection("tetraplot")
    yield connection
    async with connection.cursor() as cur:
        await cur.execute("DELETE FROM Series WHERE user_id=-1;")
        await connection.commit()
    connection.close()


async def setup_module():
    if config.INIT_DB:
        await db.init_db()


@pytest.fixture
def series():
    return models.Series(
        user_id=-1, title="Тестовое измерение", x_name="U, В", y_name="I, А"
    )


@pytest.mark.asyncio
async def test_add_series(mysql_connection: aiomysql.Connection, series: models.Series):
    await db.measuring.add_series(mysql_connection, series)
    async with mysql_connection.cursor() as cur:
        cur: aiomysql.Cursor
        await cur.execute("SELECT title FROM Series WHERE user_id=-1;")
        await mysql_connection.commit()
        r: list[list[str]] = await cur.fetchall()
        logging.info(f"In add_series {r=}")
        assert r[0][0] == "Тестовое измерение"


@pytest.mark.asyncio
async def test_get_series(mysql_connection: aiomysql.Connection, series: models.Series):
    await db.measuring.add_series(mysql_connection, series)
    async with mysql_connection.cursor() as cur:
        cur: aiomysql.Cursor
        await cur.execute("SELECT id FROM Series WHERE user_id=-1;")
        await mysql_connection.commit()
        row: list[int] = await cur.fetchone()
        res_id = row[0]
    s = await db.measuring.get_series(mysql_connection, res_id)
    assert s.title == series.title


@pytest.mark.asyncio
async def test_get_series_by_user_id(
    mysql_connection: aiomysql.Connection, series: models.Series
):
    await db.measuring.add_series(mysql_connection, series)
    await db.measuring.add_series(mysql_connection, series)
    s = await db.measuring.get_series_by_user_id(mysql_connection, -1)
    assert len(s) == 2
