import psycopg2
from backoff import on_exception, expo


class PostgresDB:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

    @on_exception(expo, psycopg2.Error, max_tries=5)
    def connect(self):
        connection = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )
        cursor = connection.cursor()
        return connection, cursor

    @on_exception(expo, psycopg2.Error, max_tries=5)
    def insert_data_to_pg(self, table_name, data):
        connection, cursor = self.connect()
        try:
            sql = f"INSERT INTO {table_name} (column1, column2, column3) VALUES (%s, %s, %s)"
            cursor.execute(sql, data)
            connection.commit()
            print("Data inserted successfully")
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error: {error}")
        finally:
            cursor.close()
            connection.close()

    @on_exception(expo, psycopg2.Error, max_tries=5)
    def update_data(self, table_name, _id, data):
        connection, cursor = self.connect()
        try:
            set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
            values = tuple(data.values()) + (_id,)
            sql = f"UPDATE {table_name} SET {set_clause} WHERE id = %s"
            cursor.execute(sql, values)
            connection.commit()
            print("Data updated successfully")
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error: {error}")
        finally:
            cursor.close()
            connection.close()

    # @on_exception(expo, psycopg2.Error, max_tries=5)
    # def select_data(self, table_name):
    #     connection, cursor = self.connect()
    #     try:
    #         sql = f"SELECT * FROM {table_name}"
    #         cursor.execute(sql)
    #         rows = cursor.fetchall()
    #         for row in rows:
    #             print(row)
    #     except (Exception, psycopg2.DatabaseError) as error:
    #         print(f"Error: {error}")
    #     finally:
    #         cursor.close()
    #         connection.close()
