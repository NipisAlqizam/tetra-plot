import os

BOT_TOKEN: str = os.getenv('BOT_TOKEN')

MYSQL_HOST: str = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_PORT: int = os.getenv('MYSQL_PORT', 3306)
MYSQL_USER: str = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD: str = os.getenv('MYSQL_PASSWORD')

INIT_DB: bool = bool(os.getenv('INIT_DB', 1))
DROP_DB_BEFORE_INIT: bool = bool(os.getenv('DROP_DB_BEFORE_INIT', 0))