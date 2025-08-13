# Contributing to QR Suite

First off, thank you for considering contributing to QR Suite! It's people like you that make QR Suite such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* Use a clear and descriptive title
* Describe the exact steps to reproduce the problem
* Provide specific examples to demonstrate the steps
* Describe the behavior you observed after following the steps
* Explain which behavior you expected to see instead and why
* Include screenshots if possible
* Include your ERPNext and Frappe versions

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* Use a clear and descriptive title
* Provide a step-by-step description of the suggested enhancement
* Provide specific examples to demonstrate the steps
* Describe the current behavior and explain which behavior you expected to see instead
* Explain why this enhancement would be useful

### Pull Requests

* Fill in the required template
* Do not include issue numbers in the PR title
* Follow the Python style guide (PEP 8)
* Include thoughtfully-worded, well-structured tests
* Document new code
* End all files with a newline

## Development Setup

1. Fork the repo
2. Clone your fork
3. Create a new branch (`git checkout -b feature/amazing-feature`)
4. Make your changes
5. Run tests
6. Commit your changes (`git commit -m 'Add some amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Local Development

```bash
# Get the app
bench get-app qr_suite https://github.com/your-username/qr_suite

# Install on your site
bench --site your-site install-app qr_suite

# Start development
bench start
```

### Running Tests

```bash
# Run all tests
bench --site your-site run-tests --app qr_suite

# Run specific test
bench --site your-site run-tests --app qr_suite --test test_qr_generation
```

## Style Guide

### Python
* Follow PEP 8
* Use meaningful variable names
* Add docstrings to all functions and classes
* Keep functions small and focused

### JavaScript
* Use ES6+ features where appropriate
* Follow Frappe's JavaScript conventions
* Use meaningful variable names
* Comment complex logic

### Commit Messages
* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

## Additional Notes

### Issue and Pull Request Labels

* `bug` - Something isn't working
* `enhancement` - New feature or request
* `documentation` - Improvements or additions to documentation
* `good first issue` - Good for newcomers
* `help wanted` - Extra attention is needed

Thank you for contributing to QR Suite!
