import sqlite3


class Database:
    def __init__(self, file_path: str):
        try:
            self.connection = sqlite3.connect(file_path)
        except Exception as ex:
            print(f'EXCEPTION: {ex}')

    def create_tables(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS ticketCounter (id INTEGER PRIMARY KEY AUTOINCREMENT, ticket_count INTEGER NOT NULL);')

            self.connection.commit()
        except Exception as ex:
            print(f'EXCEPTION: {ex}')

    def update_ticket_count(self, ticket_count: int):
        cursor = self.connection.cursor()

        cursor.execute(f'INSERT INTO ticketCounter (ticket_count) VALUES ({ticket_count});')
        self.connection.commit()

    def get_ticket_count(self):
        cursor = self.connection.cursor()
        # query = 
        return cursor.execute(
            f'SELECT ticket_count FROM ticketCounter WHERE id = (SELECT MAX(id)  FROM ticketCounter);').fetchone()
