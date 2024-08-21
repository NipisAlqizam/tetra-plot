import logging

import asyncio
import aiomysql

import config

logger = logging.getLogger(__name__)


async def get_mysql_connection(db: str | None = None) -> aiomysql.Connection:
    """
    Creates and returns a connection to database

    :param db: name of the database to connect to. If none is provided connects without a database
    :return: MySQL connection object
    """
    return await aiomysql.connect(
        host=config.MYSQL_HOST,
        port=config.MYSQL_PORT,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        db=db,
    )


async def init_db(drop_first: bool = False):
    """
    Creates database and tables if they're not created yet.

    :param drop_first: if True will delete both database and tables and then create empty ones
    """
    logger.info("Initializing database")
    conn = await get_mysql_connection()
    if not config.INIT_DB:
        logger.info("INIT_DB is 0. Just closing created connection")
        conn.close()
        return
    async with conn.cursor() as cur:
        if drop_first:
            logger.info("Dropping old db")
            await cur.execute("DROP DATABASE `tetraplot`;")
            await conn.commit()
        logger.info("Createing db")
        await cur.execute("CREATE DATABASE IF NOT EXISTS tetraplot")
        await cur.execute("USE tetraplot")
        await conn.commit()

        logger.info("Creating tables")
        await cur.execute(
            """CREATE TABLE IF NOT EXISTS Series
                (id INT PRIMARY KEY AUTO_INCREMENT,
                user_id INT,
                title VARCHAR(255),
                x_name VARCHAR(255),
                y_name VARCHAR(255)
                );"""
        )
        await cur.execute(
            """CREATE TABLE IF NOT EXISTS Measurement
                (id INT PRIMARY KEY AUTO_INCREMENT,
                series_id INT,
                measurement_time TIMESTAMP,
                x DOUBLE,
                y DOUBLE,
                comment TEXT,
                FOREIGN KEY (series_id) REFERENCES Series (id) ON DELETE CASCADE
                );"""
        )
        await cur.execute(
            """CREATE TABLE IF NOT EXISTS Plot
                (file_id VARCHAR(100) PRIMARY KEY,
                series_id INT,
                style VARCHAR(60),
                FOREIGN KEY (series_id) REFERENCES Series (id) ON DELETE CASCADE
                );"""
        )
        await conn.commit()
    conn.close()
    logger.info("Done initializing database")


if __name__ == "__main__":
    asyncio.run(init_db())
