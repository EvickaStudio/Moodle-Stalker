# Moodle Mate Test Suite

This directory contains the test suite for Moodle Mate. The tests are written using pytest and follow best practices for Python testing.

## Structure

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── utils/                   # Tests for utility modules
│   ├── test_config.py      # Tests for configuration management
├── notification/           # Tests for notification modules
│   ├── test_notification_processor.py
│   ├── test_notification_sender.py
│   └── test_notification_summarizer.py
└── README.md               # This file
```

## Running Tests

To run the tests, first install the test dependencies:

```bash
pip install -e ".[test]"
```

Then run the tests using pytest:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/utils/test_config.py

# Run tests matching a pattern
pytest -k "test_config"
```

## Test Organization

- Each module has its own test file
- Fixtures are organized by scope:
  - Module-specific fixtures in test files
  - Shared fixtures in conftest.py
- Tests follow the Arrange-Act-Assert pattern
- Mock objects are used to isolate components

## Writing Tests

When writing new tests:

1. Use descriptive test names that explain the scenario
2. Follow the Arrange-Act-Assert pattern
3. Use appropriate fixtures and mocks
4. Add docstrings explaining test purpose
5. Group related tests using classes if needed
6. Use parametrize for testing multiple scenarios

Example:

```python
def test_specific_scenario(mock_dependency):
    """Test description of what is being tested."""
    # Arrange
    expected_result = "expected"
    mock_dependency.return_value = expected_result
    
    # Act
    result = function_under_test()
    
    # Assert
    assert result == expected_result
```

## Coverage

The test suite aims for high coverage but prioritizes meaningful tests over coverage numbers. Key areas to cover:

- Happy path scenarios
- Error conditions
- Edge cases
- Configuration variations
- Integration points

## Mocking

The test suite uses the following mocking strategies:

- Mock external services (Discord, Pushbullet)
- Mock file system operations
- Mock network calls
- Use dependency injection for testability

## Continuous Integration

Tests are run automatically on:
- Pull requests
- Main branch commits
- Release tags

See the GitHub Actions workflow for details. 