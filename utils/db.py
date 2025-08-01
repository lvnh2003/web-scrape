# db.py
import os
import psycopg
from dotenv import load_dotenv
import yaml

load_dotenv()

def get_db_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

def table_exists(conn, table_name):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_name = %s
            );
        """, (table_name,))
        return cur.fetchone()[0]

def create_table_from_config(conn, config_path, table_name):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    if config["table_name"] != table_name:
        raise ValueError("⚠ Tên bảng trong cấu hình không khớp.")

    columns = config["columns"]
    column_defs = []

    for col_name, props in columns.items():
        col_def = f"{col_name} {props['type']}"
        if props.get("primary_key"):
            col_def += " PRIMARY KEY"
        column_defs.append(col_def)

    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        {', '.join(column_defs)}
    );
    """

    with conn.cursor() as cur:
        cur.execute(create_table_sql)
        conn.commit()

def insert_data(table_name: str, data: list[dict], db_config_path="config/db_config.yml"):
    if not data:
        print("データがありません。")
        return

    try:
        with get_db_connection() as conn:
            if not table_exists(conn, table_name):
                create_table_from_config(conn, db_config_path, table_name)

            columns = list(data[0].keys())
            values = [[item.get(col) for col in columns] for item in data]

            placeholders = ", ".join(["%s"] * len(columns))
            columns_str = ", ".join(columns)

            insert_query = f"""
            INSERT INTO {table_name} ({columns_str})
            VALUES ({placeholders})
            ON CONFLICT DO NOTHING
            """

            with conn.cursor() as cur:
                cur.executemany(insert_query, values)
            conn.commit()

            print(f"{table_name}テーブルにコンテンツを追加しました")
    except Exception as e:
        print("Failed to save data:", e)
