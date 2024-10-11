import pytest
from aml_simulator.amlsim.random_amount import RandomAmount

def test_get_0_10_amount():
    amount = RandomAmount(0.0, 10.0).getAmount()
    assert amount <= 10.0
    assert amount >= 0.0

def test_get_2_35_amount():
    amount = RandomAmount(2.0, 31.0).getAmount()
    assert amount >= 2.0
    assert amount <= 31.0