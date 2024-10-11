import pytest
from aml_simulator.amlsim.rounded_amount import RoundedAmount

def test_get_0_10_amount():
    amount = RoundedAmount(0.0, 10.0).getAmount()
    assert amount <= 10.0
    assert amount >= 0.0

def test_get_2_35_amount():
    amount = RoundedAmount(2.0, 31.0).getAmount()
    assert amount >= 2.0
    assert amount <= 31.0

def test_get_2_100_amount():
    amount = RoundedAmount(2.0, 100.0).getAmount()
    assert amount >= 2.0
    assert amount <= 100.0
    assert amount % 10 == 0.0

def test_get_42_1000_amount():
    amount = RoundedAmount(42.0, 999.0).getAmount()
    assert amount >= 100.0
    assert amount <= 900.0
    assert amount % 100 == 0.0

def test_get_3000_3100_amount():
    amount = RoundedAmount(3000.0, 3100.0).getAmount()
    assert amount >= 3000.0
    assert amount <= 3100.0
    assert amount % 10 == 0.0

def test_get_45_12000_amount():
    amount = RoundedAmount(45.0, 12000.0).getAmount()
    assert amount >= 1000.0
    assert amount <= 12000.0
    assert amount % 1000 == 0.0