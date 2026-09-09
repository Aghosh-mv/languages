# Security Policy

## Reporting Vulnerabilities

If you discover a security vulnerability, please report it responsibly:

1. **DO NOT** open a public GitHub issue
2. Email security@tinkerspace.com with:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

## Response Timeline

- **Acknowledgment**: Within 24 hours
- **Initial assessment**: Within 48 hours
- **Fix development**: Within 7 days
- **Release**: As soon as possible after fix is ready

## Scope

This security policy applies to:
- EasyLang v2 interpreter
- HardLang v2 interpreter
- HardwareLang compiler and runtime

## Security Considerations

### EasyLang v2
- Sandboxed execution environment
- No direct file system access
- No network access (unless explicitly enabled)
- Input validation on all user inputs

### HardLang v2
- Malbolge-inspired VM with limited capabilities
- No external system calls
- Memory-safe operations
- Encrypted source code

### HardwareLang
- Hardware abstraction layer prevents direct access
- Input validation on all hardware operations
- Safety limits on motor speeds and actuator values
- Emergency stop functionality

## Best Practices

When using these languages:
1. Never run untrusted code
2. Use HardwareLang safety features when controlling real hardware
3. Keep dependencies up to date
4. Review code before execution
5. Use sandboxed environments for testing

## Updates

Security updates will be released as soon as possible and announced via:
- GitHub Security Advisories
- Email notifications to reported reporters
- Project README updates
