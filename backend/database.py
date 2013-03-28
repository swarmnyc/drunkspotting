#!/usr/bin/python


def execute_non_query(conn, sql, data=None):
    cur = conn.cursor()
    try:
        cur.execute(sql, data)
    except:
        conn.rollback()
        cur.close()
        raise
    conn.commit()
    cur.close()


def execute_non_query_returning_id(conn, sql, data=None):
    cur = conn.cursor()
    try:
        cur.execute(sql, data)
    except:
        conn.rollback()
        cur.close()
        raise
    val = cur.fetchone()[0]
    cur.close()
    conn.commit()
    return val


def execute_one_row(conn, sql, data):
    cur = conn.cursor()
    try:
        cur.execute(sql, data)
    except:
        cur.close()
        raise
    row = cur.fetchone()
    cur.close()
    return row


def execute_all_rows(conn, sql, data=None):
    cur = conn.cursor()
    try:
        cur.execute(sql, data)
    except:
        cur.close()
        raise
    row = cur.fetchall()
    cur.close()
    return row
