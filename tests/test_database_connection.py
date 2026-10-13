import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv


# Projenin ana klasöründeki .env dosyasını oku
project_root = Path(__file__).resolve().parents[1]
load_dotenv(project_root / ".env")


def test_database_connection():
    # .env içindeki bilgilerle PostgreSQL'e bağlan
    with psycopg.connect(
        host=os.environ["PGHOST"],
        port=os.environ["PGPORT"],
        dbname=os.environ["PGDATABASE"],
        user=os.environ["PGUSER"],
        password=os.environ["PGPASSWORD"],
        connect_timeout=5,
    ) as connection:

        with connection.cursor() as cursor:
            cursor.execute("SELECT current_database(), current_user;")
            result = cursor.fetchone()

    # Doğru veritabanına ve kullanıcıya bağlandığımızı kontrol et
    assert result == ("orderguard", "postgres")