# Tests

This directory contains test suites for all three programming languages.

## Running Tests

### Run all tests
```bash
python -m pytest tests/
```

### Run specific language tests
```bash
# EasyLang tests
python tests/test_easylang.py

# HardLang tests
python tests/test_hardlang.py

# HardwareLang tests
python tests/test_hardwarelang.py
```

## Test Coverage

### EasyLang Tests
- Lexer tokenization
- Parser AST generation
- Interpreter execution
- Function definition and calling
- Array operations
- Control flow (if/else, loops)
- Error handling

### HardLang Tests
- Hello World program
- Factorial calculation
- Fibonacci sequence

### HardwareLang Tests
- LED blink program
- Motor control
- Sensor reading

## Adding New Tests

1. Create a new test file: `tests/test_<language>.py`
2. Follow the existing test structure
3. Add test functions with descriptive names
4. Use assertions to verify results
5. Run tests to ensure they pass

## Continuous Integration

Tests are automatically run on every push and pull request using GitHub Actions.
See `.github/workflows/test.yml` for configuration.
