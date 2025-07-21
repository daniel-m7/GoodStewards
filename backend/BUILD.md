# GoodStewards Backend Build & Testing

This document describes the build and testing process for the GoodStewards backend application.

## 🚀 Quick Start

### Local Development
```bash
# Install dependencies
poetry install --with dev

# Run tests
poetry run pytest tests/

# Run linting
poetry run black .
poetry run ruff check --fix .
poetry run mypy app/
```

### Full Build Process
```bash
# Linux/Mac
./scripts/build.sh

# Windows
scripts\build.bat

# With Docker build
./scripts/build.sh --docker
```

## 📋 Build Pipeline

The build process includes the following stages:

### 1. **Dependency Installation**
- Installs all Python dependencies using Poetry
- Includes development dependencies for testing and linting

### 2. **Code Quality Checks**
- **Black**: Code formatting
- **Ruff**: Linting and import sorting
- **MyPy**: Static type checking

### 3. **Testing**
- **Pytest**: Unit and integration tests
- **Coverage**: Code coverage reporting
- **Async Support**: pytest-asyncio for async tests

### 4. **Security Scanning**
- **Bandit**: Security linting
- **Safety**: Dependency vulnerability scanning

### 5. **Docker Build** (Optional)
- Multi-stage Docker build
- Optimized for production deployment

## 🧪 Testing

### Test Structure
```
tests/
├── __init__.py          # Test package
├── conftest.py          # Pytest configuration and fixtures
├── test_main.py         # Main application tests
├── test_auth.py         # Authentication endpoint tests
├── test_receipts.py     # Receipt endpoint tests
└── test_simple.py       # Simple app creation tests
```

### Running Tests
```bash
# Run all tests
poetry run pytest tests/

# Run with coverage
poetry run pytest tests/ --cov=app --cov-report=html

# Run specific test file
poetry run pytest tests/test_main.py

# Run with verbose output
poetry run pytest tests/ -v
```

### Test Coverage
- **Target**: 80%+ code coverage
- **Reports**: HTML and terminal output
- **Location**: `htmlcov/index.html`

## 🔧 CI/CD Pipeline

### GitHub Actions Workflow
The CI/CD pipeline runs on:
- **Push** to `main` and `develop` branches
- **Pull Requests** to `main` and `develop` branches

### Pipeline Stages
1. **Test Job**
   - PostgreSQL service container
   - Dependency installation
   - Linting and type checking
   - Test execution with coverage
   - Coverage upload to Codecov

2. **Security Job**
   - Security scanning with Bandit
   - Dependency vulnerability checks
   - Security report artifacts

3. **Build Job** (Main branch only)
   - Docker image building
   - Image caching optimization

4. **Quality Gate**
   - Ensures all checks pass
   - Prevents deployment on failures

## 📊 Quality Metrics

### Code Quality
- **Formatting**: Black compliance
- **Linting**: Ruff compliance
- **Types**: MyPy compliance
- **Security**: Bandit and Safety compliance

### Test Quality
- **Coverage**: Minimum 80%
- **Unit Tests**: All functions and classes
- **Integration Tests**: API endpoints and database operations
- **End-to-End Tests**: Complete user workflows

## 🐳 Docker

### Build
```bash
docker build -t goodstewards-backend:latest .
```

### Run
```bash
docker run -p 8000:8000 goodstewards-backend:latest
```

### Development
```bash
docker-compose up -d
```

## 🔍 Troubleshooting

### Common Issues

#### Test Database Connection
```bash
# Ensure PostgreSQL is running
docker-compose up -d postgres

# Set test database URL
export DATABASE_URL="postgresql+psycopg_async://postgres:postgres@localhost:5432/goodstewards_test"
```

#### Dependency Issues
```bash
# Clear Poetry cache
poetry cache clear . --all

# Reinstall dependencies
poetry install --with dev
```

#### Linting Issues
```bash
# Auto-fix formatting
poetry run black .

# Auto-fix linting
poetry run ruff check --fix .

# Check types
poetry run mypy app/
```

## 📈 Monitoring

### Coverage Reports
- **HTML**: `htmlcov/index.html`
- **Terminal**: Coverage summary in test output
- **CI**: Uploaded to Codecov

### Security Reports
- **Bandit**: Security linting results
- **Safety**: Dependency vulnerability reports
- **CI**: Stored as workflow artifacts

## 🎯 Best Practices

### Before Committing
1. Run the full build script locally
2. Ensure all tests pass
3. Check code coverage
4. Verify linting compliance

### Before Creating PR
1. Update tests for new features
2. Ensure test coverage doesn't decrease
3. Run security scans
4. Update documentation if needed

### Code Review Checklist
- [ ] Tests included for new functionality
- [ ] Code coverage maintained or improved
- [ ] Linting and formatting compliant
- [ ] Security considerations addressed
- [ ] Documentation updated 