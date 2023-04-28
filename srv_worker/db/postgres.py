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
    def update_data(self, table_name, _id, data):
        connection, cursor = self.connect()
        try:
            set_column = ', '.join([f"{k} = %s" for k in data.keys()])
            values = tuple(data.values())
            sql = f"UPDATE {table_name} SET {set_column} WHERE id = '{_id}'"
            cursor.execute(sql, values)
            connection.commit()
            print("Data updated successfully")
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error: {error}")
        finally:
            cursor.close()
            connection.close()

