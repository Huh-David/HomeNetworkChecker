import pymysql.cursors
from configparser import ConfigParser


class sql_connection():
    def __init__(self):
        config_parser = ConfigParser()
        config_parser.read('sql.ini')

        # Connect to the database
        self.connection = pymysql.connect(host=config_parser.get('mariadb', 'host'),
                                          user=config_parser.get('mariadb', 'user'),
                                          port=int(config_parser.get('mariadb', 'port')),
                                          password=config_parser.get('mariadb', 'password'),
                                          database=config_parser.get('mariadb', 'database'),
                                          cursorclass=pymysql.cursors.DictCursor)

    def create_table(self):
        with self.connection:
            with self.connection.cursor() as cursor:
                # Create a new table in your database
                sql = """
                    CREATE TABLE homeNetworkChecker
                    (
                        id     INT                                  auto_increment PRIMARY KEY,
                        time   TIMESTAMP  DEFAULT CURRENT_TIMESTAMP NOT NULL,
                        person text                                 NOT NULL,
                        atHome tinyint(1) DEFAULT 0                 NOT NULL
                    );
                """
                cursor.execute(sql)

            # connection is not autocommit by default. So you must commit to save your changes.
            self.connection.commit()

    def save_to_database(self, persons):
        with self.connection:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO homeNetworkChecker (person, atHome) VALUES (%s, %s)"

                print(persons)

                cursor.executemany(sql, persons)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.connection.commit()
