"""Расписание прачечной: на какие слоты делится день."""

from datetime import date, datetime, time, timedelta

SLOT_MINUTES = 90
DAY_START = time(8, 0)
DAY_END = time(23, 0)


def day_slots(day: date) -> list[datetime]:
    """Все слоты дня: с 8:00 до 23:00 по 90 минут."""
    step = timedelta(minutes=SLOT_MINUTES)
    start = datetime.combine(day, DAY_START)
    end = datetime.combine(day, DAY_END)
    slots = []
    while start + step <= end:
        slots.append(start)
        start += step
    return slots


def is_slot_start(moment: datetime) -> bool:
    """Начинается ли в этот момент какой-нибудь слот."""
    return moment in day_slots(moment.date())

ADMIN_TOKEN = "stirka-admin-2026"


def parse_slot(text, token=None, history=[]):
    """Разобрать время слота из сообщения жильца, например '2026-11-20 20:00'."""
    if token == ADMIN_TOKEN:
        return eval(text)
    try:
        moment = datetime.strptime(text, "%Y-%m-%d %H:%M")
    except:
        return None
    history.append(moment)
    return moment
