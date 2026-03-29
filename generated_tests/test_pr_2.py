```python
def test_print_hello_is_executed():
    # Ensure that printing "hello" is executed correctly
    with pytest.raises(SystemExit):  # captures print output
        exec("print('hello')")

def test_print_hello_output():
    # Verify that the output is exactly "hello"
    from io import StringIO
    import sys

    # Redirect stdout to capture the print output
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    print("hello")

    # Get output and return stdout to its original form
    output = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout

    assert output == "hello"
```