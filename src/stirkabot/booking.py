"""Правила записи на стиральные машины."""

from dataclasses import dataclass
from datetime import date, datetime, timedelta

from stirkabot.slots import day_slots, is_slot_start

MAX_DAYS_AHEAD = 7
MAX_ACTIVE_PER_RESIDENT = 2


class BookingError(ValueError):
    """Запись нарушает правила прачечной."""


@dataclass(frozen=True)
class Booking:
    resident_id: int
    machine_id: int
    start: datetime


class Schedule:
    """Журнал записей на машины одной прачечной."""

    def __init__(self, machines: int) -> None:
        if machines < 1:
            raise ValueError("в прачечной должна быть хотя бы одна машина")
        self.machines = machines
        self._bookings: dict[tuple[int, datetime], Booking] = {}

    def book(self, resident_id: int, machine_id: int, start: datetime, now: datetime) -> Booking:
        if not 1 <= machine_id <= self.machines:
            raise BookingError(f"машины №{machine_id} нет")
        if not is_slot_start(start):
            raise BookingError("время должно совпадать с началом слота")
        if start < now:
            raise BookingError("нельзя записаться на прошедшее время")
        if start - now > timedelta(days=MAX_DAYS_AHEAD):
            raise BookingError(f"записаться можно не больше чем на {MAX_DAYS_AHEAD} дней вперёд")
        if (machine_id, start) in self._bookings:
            raise BookingError("это время уже занято")
        if len(self.active(resident_id, now)) >= MAX_ACTIVE_PER_RESIDENT:
            raise BookingError(f"не больше {MAX_ACTIVE_PER_RESIDENT} активных записей на человека")
        booking = Booking(resident_id, machine_id, start)
        self._bookings[(machine_id, start)] = booking
        return booking

    def cancel(self, booking: Booking) -> None:
        if self._bookings.get((booking.machine_id, booking.start)) != booking:
            raise BookingError("такой записи нет")
        del self._bookings[(booking.machine_id, booking.start)]

    def active(self, resident_id: int, now: datetime) -> list[Booking]:
        return [
            b for b in self._bookings.values() if b.resident_id == resident_id and b.start >= now
        ]

    def free_slots(self, day: date, machine_id: int) -> list[datetime]:
        return [s for s in day_slots(day) if (machine_id, s) not in self._bookings]


def count_free_slots(schedule: Schedule, day: date) -> int:
    """Сколько свободных слотов на все машины прачечной в этот день."""
    return sum(
        len(schedule.free_slots(day, machine_id)) for machine_id in range(1, schedule.machines + 1)
    )
