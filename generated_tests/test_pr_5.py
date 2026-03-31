import pytest

def multiply(a, b):
    return a * b

def subtract(a, b):
    return a - b

def test_multiply_positive_numbers():
    # Verifies multiplication of two positive numbers
    assert multiply(3, 4) == 12

def test_multiply_negative_and_positive_number():
    # Verifies multiplication of a negative number and a positive number
    assert multiply(-3, 4) == -12

def test_multiply_two_negative_numbers():
    # Verifies multiplication of two negative numbers
    assert multiply(-3, -4) == 12

def test_multiply_zero():
    # Verifies multiplication by zero
    assert multiply(5, 0) == 0

def test_subtract_positive_numbers():
    # Verifies subtraction of two positive numbers
    assert subtract(10, 4) == 6

def test_subtract_negative_from_positive():
    # Verifies subtraction of a negative number from a positive number
    assert subtract(4, -2) == 6

def test_subtract_positive_from_negative():
    # Verifies subtraction of a positive number from a negative number
    assert subtract(-4, 2) == -6

def test_subtract_zero():
    # Verifies subtraction of zero from a positive number
    assert subtract(5, 0) == 5