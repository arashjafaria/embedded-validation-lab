
def test_aeb_validation_failure_demo():
    """Demonstrate CI failure detection."""
    expected_result = "PASS"
    actual_result = "FAIL"

    assert actual_result == expected_result, (
        "Intentional failure: demonstrating Jenkins CI debugging"
    )

