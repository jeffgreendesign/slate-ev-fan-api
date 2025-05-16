# Contributing Guide

Thank you for your interest in contributing to the Slate EV Truck API! This guide will help you understand how to contribute to the project.

## Code of Conduct

Please be respectful and considerate of others when contributing to the project. We aim to create a welcoming and inclusive environment for all contributors.

## Getting Started

### 1. Fork the Repository

Start by forking the repository to your own GitHub account.

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/slate-ev-fan-api.git
cd slate-ev-fan-api
```

### 3. Set Up the Development Environment

Follow the instructions in the [Environment Setup](environment-setup.md) guide to set up your development environment.

## Development Workflow

### 1. Create a Branch

Create a new branch for your feature or bugfix:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/the-bug-youre-fixing
```

Use a descriptive name for your branch that reflects the changes you're making.

### 2. Make Your Changes

Implement your changes following these guidelines:

- Follow the existing code style
- Write clear, concise code with meaningful variable and function names
- Add comments where necessary to explain complex logic
- Update tests to reflect your changes

### 3. Write Tests

For any new feature or bugfix, add appropriate tests:

- Unit tests for isolated functionality
- Integration tests for API endpoints
- Make sure existing tests still pass

### 4. Format and Lint Your Code

Before submitting a pull request, format and lint your code:

```bash
# Format code with Black
black app tests main.py

# Sort imports with isort
isort app tests main.py

# Run linting with flake8
flake8 app tests main.py

# Run type checking with mypy
mypy app tests main.py
```

### 5. Run Tests

Ensure all tests pass:

```bash
pytest
```

### 6. Commit Your Changes

Make clear, concise commits with descriptive messages:

```bash
git add .
git commit -m "feat: Add new feature for X"
```

Follow [Conventional Commits](https://www.conventionalcommits.org/) styling for commit messages:

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools

### 7. Push Your Changes

Push your changes to your fork:

```bash
git push origin feature/your-feature-name
```

### 8. Submit a Pull Request

Go to the original repository on GitHub and create a pull request from your branch to the main branch.

In your pull request description:

- Clearly explain the changes you've made
- Reference any related issues (e.g., "Fixes #123")
- Include any necessary migration steps or special instructions

## Pull Request Review Process

Once you submit a pull request:

1. Maintainers will review your code
2. Automated tests will run to verify functionality
3. Feedback may be provided for changes
4. When approved, your changes will be merged

## Documentation

If your changes affect user-facing functionality, please update the documentation:

- Update API endpoint documentation
- Update data model documentation
- Add or update usage examples

## Adding New Features

When adding new features:

1. Discuss the feature first by creating an issue
2. Get feedback on the proposed implementation
3. Implement the feature with appropriate tests
4. Update documentation to reflect the new feature

## Reporting Bugs

When reporting bugs:

1. Check if the bug has already been reported
2. Use the bug report template
3. Include clear steps to reproduce the bug
4. Include information about your environment
5. If possible, suggest a fix

## Questions?

If you have any questions about contributing, please open an issue with the label "question" and we'll be happy to help.
