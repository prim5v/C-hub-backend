# backend/utils/db.py

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import logging

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_db_connection():
    try:
        conn = psycopg2.connect(
            DATABASE_URL,
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        print("Database connection failed:", e)
        return None


def get_db_cursor():
    conn = get_db_connection()
    if conn:
        return conn, conn.cursor()
    return None, None




def check_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        cursor.execute("SELECT 1;")
        cursor.fetchone()

        cursor.close()
        conn.close()

        logging.info("✅ Database connection successful")

        return True

    except Exception as e:
        logging.error(f"❌ Database connection failed: {str(e)}")
        return False