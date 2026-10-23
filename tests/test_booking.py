from datetime import date, datetime

import pytest

from stirkabot.booking import BookingError, Schedule

NOW = datetime(2027, 2, 1, 7, 0)
SLOT = datetime(2027, 2, 1, 9, 30)


@pytest.fixture
def schedule():
    return Schedule(machines=4)


def test_resident_books_free_slot(schedule):
    booking = schedule.book(resident_id=42, machine_id=1, start=SLOT, now=NOW)
    assert booking.start == SLOT
    assert SLOT not in schedule.free_slots(date(2027, 2, 1), machine_id=1)


def test_same_slot_on_same_machine_is_rejected(schedule):
    schedule.book(42, 1, SLOT, NOW)
    with pytest.raises(BookingError, match="уже занято"):
        schedule.book(43, 1, SLOT, NOW)


def test_same_slot_on_other_machine_is_allowed(schedule):
    schedule.book(42, 1, SLOT, NOW)
    assert schedule.book(43, 2, SLOT, NOW).machine_id == 2


@pytest.mark.parametrize("machine_id", [0, 5])
def test_unknown_machine_is_rejected(schedule, machine_id):
    with pytest.raises(BookingError, match="нет"):
        schedule.book(42, machine_id, SLOT, NOW)


def test_time_between_slots_is_rejected(schedule):
    with pytest.raises(BookingError, match="началом слота"):
        schedule.book(42, 1, datetime(2027, 2, 1, 9, 0), NOW)


def test_past_slot_is_rejected(schedule):
    with pytest.raises(BookingError, match="прошедшее"):
        schedule.book(42, 1, SLOT, now=datetime(2027, 2, 1, 12, 0))


def test_booking_more_than_week_ahead_is_rejected(schedule):
    with pytest.raises(BookingError, match="7 дней"):
        schedule.book(42, 1, datetime(2027, 2, 9, 9, 30), NOW)


def test_resident_cannot_have_more_than_two_active_bookings(schedule):
    schedule.book(42, 1, datetime(2027, 2, 1, 8, 0), NOW)
    schedule.book(42, 1, datetime(2027, 2, 1, 9, 30), NOW)
    with pytest.raises(BookingError, match="не больше 2"):
        schedule.book(42, 1, datetime(2027, 2, 1, 11, 0), NOW)


def test_cancel_frees_the_slot(schedule):
    booking = schedule.book(42, 1, SLOT, NOW)
    schedule.cancel(booking)
    assert SLOT in schedule.free_slots(date(2027, 2, 1), machine_id=1)
    with pytest.raises(BookingError, match="такой записи нет"):
        schedule.cancel(booking)


def test_schedule_needs_at_least_one_machine():
    with pytest.raises(ValueError):
        Schedule(machines=0)


def test_count_free_slots_decreases_after_booking(schedule):
    from stirkabot.booking import count_free_slots

    assert count_free_slots(schedule, date(2027, 2, 1)) == 40
    schedule.book(42, 1, SLOT, NOW)
    assert count_free_slots(schedule, date(2027, 2, 1)) == 39
