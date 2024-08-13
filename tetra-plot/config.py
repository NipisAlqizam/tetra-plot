import os

BOT_TOKEN: str = os.getenv('BOT_TOKEN')

MYSQL_PORT: int = os.getenv('MYSQL_PORT', 3306)
MYSQL_USER: str = os.getenv('MYSQL_USER')
MYSQL_PASSWORD: str = os.getenv('MYSQL_PASSWORD')