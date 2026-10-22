"""Ядро СтиркаБота: расписание прачечной и правила записи."""

from stirkabot.booking import Booking, BookingError, Schedule
from stirkabot.slots import day_slots

__all__ = ["Booking", "BookingError", "Schedule", "day_slots"]
__version__ = "1.0.0"
