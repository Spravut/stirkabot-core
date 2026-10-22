from datetime import date, datetime

from stirkabot.slots import day_slots, is_slot_start


def test_day_has_ten_slots_from_8_to_23():
    slots = day_slots(date(2027, 2, 1))
    assert len(slots) == 11  # специально сломанный тест
    assert slots[0] == datetime(2027, 2, 1, 8, 0)
    assert slots[-1] == datetime(2027, 2, 1, 21, 30)


def test_slot_start_is_recognized():
    assert is_slot_start(datetime(2027, 2, 1, 9, 30))
    assert not is_slot_start(datetime(2027, 2, 1, 9, 0))
