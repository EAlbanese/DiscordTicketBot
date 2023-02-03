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

    def create_ticket_count(self, ticket_count: int):
        # {(', end_date' if penalty_end != None else '')} / f', {penalty_end}' if penalty_end != None else ''}
        cursor = self.connection.cursor()

        if ticket_count != None:
            cursor.execute(
                f'INSERT INTO ticketCounter (ticket_count) VALUES ({ticket_count});')
        else:
            cursor.execute(
                f'INSERT INTO ticketCounter (ticket_count) VALUES ({ticket_count});')
        self.connection.commit()

    # def delete_penalty(self, type: int, server_id: int, user_id: int):
    #     cursor = self.connection.cursor()
    #     cursor.execute(
    #         f'DELETE FROM penalties WHERE id IN (SELECT id FROM penalties WHERE type={type} AND server_id={server_id} AND user_id={user_id} ORDER BY id DESC LIMIT 1) ;')
    #     self.connection.commit()

    def get_ticket_count(self):
        cursor = self.connection.cursor()
        return cursor.execute(
            f'SELECT ticket_count FROM ticketCounter DESC LIMIT 1;').fetchall()
