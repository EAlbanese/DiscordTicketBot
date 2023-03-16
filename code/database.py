import sqlite3
import datetime


class Database:
    def __init__(self, file_path: str):
        try:
            self.connection = sqlite3.connect(file_path)
        except Exception as ex:
            print(f'EXCEPTION: {ex}')

    def drop_ticketdb(self):
        cursor = self.connection.cursor()

        cursor.execute(
            f'DROP TABLE tickets;')
        self.connection.commit()

    def create_ticket_table(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS tickets (id INTEGER PRIMARY KEY AUTOINCREMENT, ticket_channel_id BIGINT, user_id INTEGER NOT NULL, moderator_id INTEGER, create_date INTEGER);')

            self.connection.commit()
        except Exception as ex:
            print(f'EXCEPTION: {ex}')

    def create_ticket(self, user_id: int, create_date: int):
        cursor = self.connection.cursor()

        cursor.execute(
            f'INSERT INTO tickets (user_id, create_date) VALUES (?, ?);', (user_id, create_date))
        self.connection.commit()

    def update_ticket(self, ticket_channel_id: int, id: int):
        cursor = self.connection.cursor()

        cursor.execute(
            'UPDATE tickets SET ticket_channel_id=? WHERE id=?;', (ticket_channel_id, id))
        self.connection.commit()

    def update_claimed_ticket(self, moderator_id: int, ticket_channel_id: int):
        cursor = self.connection.cursor()

        cursor.execute(
            'UPDATE tickets SET moderator_id=? WHERE ticket_channel_id=?;', (moderator_id, ticket_channel_id))
        self.connection.commit()

    def get_ticket_id(self, create_date: int) -> int:
        cursor = self.connection.cursor()
        return cursor.execute(
            f'SELECT id FROM tickets WHERE create_date={create_date};').fetchone()[0]

    def get_ticket_id_by_channel_id(self, channel_id: int) -> int:
        cursor = self.connection.cursor()
        return cursor.execute(
            f'SELECT id FROM tickets WHERE ticket_channel_id={channel_id};').fetchone()[0]

    def get_ticket_info(self, id: int):
        cursor = self.connection.cursor()
        return cursor.execute(
            f'SELECT * FROM tickets WHERE id=?;', (id, )).fetchone()
