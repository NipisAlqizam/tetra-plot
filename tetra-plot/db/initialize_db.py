import logging

import asyncio
import aiomysql

import config


async def init_db(drop_first: bool = False):
    logging.info("Initializing database")
    conn: aiomysql.Connection = await aiomysql.connect(
        host="127.0.0.1",
        port=3306,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
    )
    async with conn.cursor() as cur:
        if drop_first:
            logging.info("Dropping old db")
            await cur.execute("DROP DATABASE `tetraplot`;")
            await conn.commit()
        logging.info("Createing db")
        await cur.execute("CREATE DATABASE IF NOT EXISTS tetraplot")
        await cur.execute("USE tetraplot")
        await conn.commit()

        logging.info("Creating tables")
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
    logging.info("Done initializing database")


if __name__ == "__main__":
    asyncio.run(init_db())
