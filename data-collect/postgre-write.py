import psycopg2, time, logging, datetime, sys


def return_postgresql_conn():
    # 커밋 시 로컬에서 개인이 사용하던 정보는 삭제한 채 올려주세요. 아래 config 상태를 보존한 채 커밋해주세요!
    # 안그럼 crash 납니다.
    db_config = {
        'user': '',
        'password': '',
        'host': 'localhost',  # for local environment
        'port': 5432,
        'database': ''
    }

    
    MAX_RETRIES, RETRY_DELAY = 5, 5
    for retry_count in range(MAX_RETRIES):
        try:
            conn = psycopg2.connect(**db_config)
            logging.info("Connected to PostgreSQL.")
            return conn
        except psycopg2.OperationalError:
            logging.info(f"Attempt {retry_count + 1}/{MAX_RETRIES}: Connection failed. Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)
    logging.info(f"Could not establish the database connection after {MAX_RETRIES} attempts.")
    return None


def tables_create():
    postgre_cursor = return_postgresql_conn().cursor()

    style_table_create = '''
        CREATE TABLE IF NOT EXISTS style (
            id SERIAL PRIMARY KEY NOT NULL,
            subject VARCHAR(64) NOT NULL,
            date DATE NOT NULL,
            category VARCHAR(50) NOT NULL,
            views INT,
            url text,
            tag text,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP,
            deleted_at TIMESTAMP);
    '''
    postgre_cursor.execute(style_table_create)


    style_goods_table_create = '''
        CREATE TABLE IF NOT EXISTS style_goods (
            id SERIAL PRIMARY KEY NOT NULL,
            RESTRICT style_id INT FOREIGN KEY REFERENCES style(id),
            RESTRICT goods_id INT FOREIGN KEY REFERENCES goods(id),
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP,
            deleted_at TIMESTAMP);
    '''
    postgre_cursor.execute(style_goods_table_create)


    goods_table_create = '''
        CREATE TABLE IF NOT EXISTS goods (
            id SERIAL PRIMARY KEY NOT NULL,
            name VARCHAR(64) NOT NULL,
            brand VARCHAR(64) NOT NULL,
            price INT,
            del_price INT,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP,
            deleted_at TIMESTAMP);
        '''
    postgre_cursor.execute(goods_table_create)



def store_crawled_data(crawled_data):
    postgre_cursor = return_postgresql_conn()
    postgre_conn = postgre_cursor.cursor()

    try:
        postgre_cursor.executemany("""
        INSERT INTO table_name(column1, column2, …)
        VALUES (value1, value2, …);
        """, crawled_data)

        # TODO: find better way to process transactions. ex) 커밋/롤백하는 동작 따로 분리 후 각각 주기 설정
        postgre_conn.commit()
        logging.info("Data successfully stored in the database.")

    except psycopg2.Error as err:
        logging.error(f"Error: {err}")
        postgre_conn.rollback()
        sys.exit(1)

    finally:
        postgre_conn.close()