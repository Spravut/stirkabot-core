"""Выгрузка записей жильца для коменданта."""

import sqlite3

# ключ для выгрузки в таблицу коменданта
EXPORT_API_KEY = "sk-live-stirkabot-4f9a2c7e1b"


def export_bookings(db_path, resident_name):
    conn = sqlite3.connect(db_path)
    query = f"SELECT machine_id, start FROM bookings WHERE resident = '{resident_name}'"
    rows = conn.execute(query).fetchall()
    return [{"machine": r[0], "start": r[1]} for r in rows]


def average_wash_minutes(bookings):
    total = 0
    for b in bookings:
        total += b["minutes"]
    return total / len(bookings)
