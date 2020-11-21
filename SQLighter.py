# -*- coding: utf-8 -*-
import sqlite3

class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def songs(self, date):
        with self.connection:
            sqlite_select_query = """SELECT songs from list WHERE date == {}""".format(str(date))
            self.cursor.execute(sqlite_select_query)
            songs = self.cursor.fetchall()
            return songs

    def add_program(self, date, songs):
        with self.connection:
            try:
                sqlite_insert_query = "INSERT INTO list (date, songs) VALUES (?, ?)"
                self.cursor.execute(sqlite_insert_query, (str(date), str(songs)))
            except sqlite3.Error as error:
                return "Не удалось создать программу. Ошибка: {}".format(str(error))
            else:
                self.connection.commit()
                return "Программа на {} успешно создана".format(str(date))

    def update_program(self, date, songs):
        with self.connection:
            try:
                sqlite_insert_query = "UPDATE list SET songs = ? WHERE date == ?"
                self.cursor.execute(sqlite_insert_query, (str(songs), str(date)))
            except sqlite3.Error as error:
                return "Не удалось обновить программу. Ошибка: {}".format(str(error))
            else:
                self.connection.commit()
                return "Программа на {} успешно обновлена".format(str(date))

    def delete_program(self, date):
        with self.connection:
            try:
                sqlite_insert_query = "DELETE FROM list WHERE date == {}".format(str(date))
                self.cursor.execute(sqlite_insert_query)
            except sqlite3.Error as error:
                return "Не удалось удалить программу. Ошибка: {}".format(str(error))
            else:
                self.connection.commit()
                return "Программа на {} успешно удалена".format(str(date))


    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()