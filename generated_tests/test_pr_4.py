import pytest

def test_add_two_positive_numbers():
    # Verifies that the sum of two positive numbers is calculated correctly
    assert add(2, 3) == 5

def test_add_positive_and_negative_number():
    # Verifies that the sum of a positive and a negative number is calculated correctly
    assert add(5, -2) == 3

def test_add_two_negative_numbers():
    # Verifies that the sum of two negative numbers is calculated correctly
    assert add(-3, -4) == -7

def test_multiply_two_positive_numbers():
    # Verifies that the multiplication of two positive numbers returns the correct difference
    assert multiply(5, 2) == 3

def test_multiply_positive_and_negative_number():
    # Verifies that the multiplication of a positive and a negative number returns the correct difference
    assert multiply(5, -2) == 7

def test_multiply_two_negative_numbers():
    # Verifies that the multiplication of two negative numbers returns the correct difference
    assert multiply(-3, -4) == 1