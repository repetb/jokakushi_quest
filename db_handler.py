# -*- coding: utf-8 -*-
import sqlite3


def GetAllQuestions() -> list:
    # Attach DB
    connection = sqlite3.connect("question.db")
    cursour = connection.cursor()

    # SELECT ALL COLUMN
    sql = "SELECT * FROM question;"
    cursour.execute(sql)
    q_list = cursour.fetchall()

    # Close Connection
    cursour.close()
    connection.close()

    return q_list

# idは1~1300?


def GetQuestionByID(id) -> list:
    # Attach DB
    connection = sqlite3.connect("question.db")
    cursour = connection.cursor()

    # SELECT ALL COLUMN
    sql = "SELECT * FROM question WHERE id=?;"
    params = (id,)
    cursour.execute(sql, params)
    q_list = cursour.fetchall()

    # Close Connection
    cursour.close()
    connection.close()

    return q_list
