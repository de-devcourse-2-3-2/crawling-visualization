import psycopg2, time, logging, sys


class DB_Write:
    def __init__(self):
        self.postgre_conn = self.return_postgresql_conn()
        self.postgre_cursor = self.postgre_conn.cursor()

    def return_postgresql_conn(self):
        # 커밋 시 로컬에서 개인이 사용하던 정보는 삭제한 채 올려주세요. 아래 config 상태를 보존한 채 커밋해주세요!
        # 안그럼 crash 납니다.
        self.db_config = {
            'user': 'postgres',
            'password': 1234,
            'host': 'localhost',  # for local environment
            'port': 5432,
            'database': 'musinsa',
            'options': "-c client_encoding=utf8",
        }


        MAX_RETRIES, RETRY_DELAY = 5, 5
        for retry_count in range(MAX_RETRIES):
            try:
                conn = psycopg2.connect(**self.db_config)
                logging.info("Connected to PostgreSQL.")
                return conn
            except psycopg2.OperationalError:
                logging.info(f"Attempt {retry_count + 1}/{MAX_RETRIES}: Connection failed. Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
        logging.info(f"Could not establish the database connection after {MAX_RETRIES} attempts.")
        return None


    def tables_create(self):
        self.postgre_cursor.execute("DROP TABLE IF EXISTS style_goods;")
        self.postgre_cursor.execute("DROP TABLE IF EXISTS style;")
        self.postgre_cursor.execute("DROP TABLE IF EXISTS goods;")

        style_table_create = '''
            CREATE TABLE IF NOT EXISTS style (
                id SERIAL PRIMARY KEY NOT NULL,
                subject VARCHAR(64) NOT NULL,
                date DATE NOT NULL,
                category VARCHAR(64) NOT NULL,
                views INT,
                season varchar(16),
                url TEXT,
                tag TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT NULL,
                deleted_at TIMESTAMP DEFAULT NULL);
        '''
        self.postgre_cursor.execute(style_table_create)


        goods_table_create = '''
            CREATE TABLE IF NOT EXISTS goods (
                id SERIAL PRIMARY KEY NOT NULL,
                name VARCHAR(128),
                brand VARCHAR(128),
                price INT,
                del_price INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT NULL,
                deleted_at TIMESTAMP DEFAULT NULL);
            '''
        self.postgre_cursor.execute(goods_table_create)

        style_goods_table_create = '''
                CREATE TABLE IF NOT EXISTS style_goods (
                    style_id INT REFERENCES style(id) ON DELETE CASCADE ON UPDATE CASCADE,
                    goods_id INT REFERENCES goods(id) ON DELETE CASCADE ON UPDATE CASCADE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT NULL,
                    deleted_at TIMESTAMP DEFAULT NULL,
                    PRIMARY KEY (style_id, goods_id));
            '''
        self.postgre_cursor.execute(style_goods_table_create)


    def insert_style_data(self, style_list):
        try:
            self.postgre_cursor.execute("""
            INSERT INTO style (subject, date, category, season, views, url, tag)
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;
            """, style_list)
            self.postgre_conn.commit()
            logging.info("Data successfully stored in the style table.")
            return self.postgre_cursor.fetchone()[0]
        except psycopg2.Error as err:
            logging.error(f"Error: {err}")
            self.postgre_conn.rollback()
            sys.exit(1)



    def insert_goods_data(self, goods_list):
        try:
            goods_ids = []
            for goods in goods_list:
                self.postgre_cursor.execute("""INSERT INTO goods (name, brand, price, del_price) VALUES (%s, %s, %s, %s) RETURNING id;""", goods)
                self.postgre_conn.commit()
                logging.info("Data successfully stored in the goods table.")
                goods_ids.append(self.postgre_cursor.fetchone()[0])  # RETURNING goods_id;
            return goods_ids
        except psycopg2.Error as err:
            logging.error(f"Error: {err}")
            self.postgre_conn.rollback()
            sys.exit(1)


    def insert_style_goods(self, style_id, goods_ids):
        try:
            for goods_id in goods_ids:
                self.postgre_cursor.execute("INSERT INTO style_goods (style_id, goods_id) VALUES (%s, %s);", (style_id, goods_id))
        except psycopg2.Error as err:
            logging.error(f"Error: {err}")
            self.postgre_conn.rollback()
            sys.exit(1)