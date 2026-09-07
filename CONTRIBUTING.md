# Contributing to Three Languages

Thank you for your interest in contributing to this project!

## How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development Setup

### Prerequisites
- Python 3.8+
- Git

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific language tests
python tests/test_easylang.py
python tests/test_hardlang.py
python tests/test_hardwarelang.py
```

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to all functions
- Keep functions under 50 lines

## Reporting Issues

- Use GitHub Issues
- Include reproduction steps
- Include expected vs actual behavior
- Include Python version and OS

## Language Contributions

### EasyLang v2
- New built-in functions
- Better error messages
- Performance improvements
- Documentation

### HardLang v2
- New obfuscation techniques
- Better error handling
- More example programs

### HardwareLang
- New board support
- New device types
- New communication protocols
- Real hardware testing

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
