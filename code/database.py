import sqlite3


class Database:
    def __init__(self, file_path: str):
        try:
            self.connection = sqlite3.connect(file_path)
        except Exception as ex:
            print(f'EXCEPTION: {ex}')

    # def drop_db(self):
    #     cursor = self.connection.cursor()

    #     cursor.execute(
    #         f'DROP TABLE tickets;')
    #     self.connection.commit()

    def create_tables(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS tickets (id INTEGER PRIMARY KEY AUTOINCREMENT, ticket_count INTEGER NOT NULL, ticket_thread_id BIGINT NOT NULL);')

            self.connection.commit()
        except Exception as ex:
            print(f'EXCEPTION: {ex}')

    def create_ticket(self, ticket_count: int):
        cursor = self.connection.cursor()

        cursor.execute(
            f'INSERT INTO tickets (ticket_count, ticket_thread_id) VALUES ({ticket_count}, 0);')
        self.connection.commit()

    def update_ticket(self, ticket_thread_id: int, ticket_count: int):
        cursor = self.connection.cursor()

        cursor.execute(
            'UPDATE tickets SET ticket_thread_id=? WHERE ticket_count=?;', (ticket_thread_id, ticket_count))
        self.connection.commit()

    def get_ticket_count(self) -> int:
        cursor = self.connection.cursor()
        return cursor.execute(
            f'SELECT ticket_count FROM tickets WHERE id = (SELECT MAX(id)  FROM tickets);').fetchone()[0]

    def get_ticket_thread_id(self) -> int:
        cursor = self.connection.cursor()
        return cursor.execute(
            f'SELECT ticket_thread_id FROM tickets WHERE id = (SELECT MAX(id)  FROM tickets);').fetchone()[0]
