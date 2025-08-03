import yaml
from utils.connection import db_conn, firestore_db

def table_exists(table_name):
    with db_conn.cursor() as cur:
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_name = %s
            );
        """, (table_name,))
        return cur.fetchone()[0]

def create_table_from_config(config_path, table_name):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    if config["table_name"] != table_name:
        raise ValueError("Table name in config does not match.")

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

    with db_conn.cursor() as cur:
        cur.execute(create_table_sql)
        db_conn.commit()

def insert_data(table_name: str, data: list[dict], db_config_path="config/db_config.yml"):
    if not data:
        print("データがありません。")
        return

    try:
        with db_conn as conn:
            if not table_exists(table_name):
                create_table_from_config(db_config_path, table_name)

            columns = list(data[0].keys())
            values = [[item.get(col) for col in columns] for item in data]

            placeholders = ", ".join(["%s"] * len(columns))
            columns_str = ", ".join(columns)

            insert_query = f"""
            INSERT INTO {table_name} ({columns_str})
            VALUES ({placeholders})
            ON CONFLICT DO NOTHING
            """

            with db_conn.cursor() as cur:
                cur.executemany(insert_query, values)
            db_conn.commit()

            print(f"{table_name}テーブルにコンテンツを追加しました")
    except Exception as e:
        print("Failed to save data:", e)

def insert_data_to_firestore(table_name: str, data: list[dict]):
    if not data:
        print("データがありません。")
        return
    
    collection = firestore_db.collection(table_name)
    
    for item in data:
        collection.add(item)
    
    print(f"{table_name}テーブルにコンテンツを追加しました")
    