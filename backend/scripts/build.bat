@echo off
setlocal enabledelayedexpansion

echo 🚀 Starting GoodStewards Backend Build Process

REM Check if we're in the right directory
if not exist "pyproject.toml" (
    echo [ERROR] pyproject.toml not found. Please run this script from the backend directory.
    exit /b 1
)

REM Step 1: Install dependencies
echo [INFO] Installing dependencies...
poetry install --with dev
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    exit /b 1
)
echo [SUCCESS] Dependencies installed

REM Step 2: Run linting
echo [INFO] Running code linting...
poetry run black --check .
if errorlevel 1 (
    echo [WARNING] Black formatting issues found. Run 'poetry run black .' to fix.
    exit /b 1
)

poetry run ruff check .
if errorlevel 1 (
    echo [WARNING] Ruff linting issues found. Run 'poetry run ruff check --fix .' to fix.
    exit /b 1
)

poetry run mypy app/
if errorlevel 1 (
    echo [WARNING] Type checking issues found.
    exit /b 1
)
echo [SUCCESS] Linting passed

REM Step 3: Run tests
echo [INFO] Running tests with coverage...
poetry run pytest tests/ --cov=app --cov-report=term-missing --cov-report=html
if errorlevel 1 (
    echo [ERROR] Tests failed
    exit /b 1
)
echo [SUCCESS] Tests completed

REM Step 4: Security scan
echo [INFO] Running security scan...
poetry run bandit -r app/ -f txt
if errorlevel 1 (
    echo [WARNING] Security issues found by Bandit
)

poetry run safety check
if errorlevel 1 (
    echo [WARNING] Dependency security issues found
)
echo [SUCCESS] Security scan completed

REM Step 5: Build Docker image (optional)
if "%1"=="--docker" (
    echo [INFO] Building Docker image...
    docker build -t goodstewards-backend:latest .
    if errorlevel 1 (
        echo [ERROR] Docker build failed
        exit /b 1
    )
    echo [SUCCESS] Docker image built successfully
)

echo [SUCCESS] 🎉 Build process completed successfully!
echo [INFO] Coverage report available at: htmlcov/index.html
echo [INFO] Ready for deployment! 