#!/bin/bash

# Local build script that mimics CI/CD pipeline
set -e

echo "🚀 Starting GoodStewards Backend Build Process"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    print_error "pyproject.toml not found. Please run this script from the backend directory."
    exit 1
fi

# Step 1: Install dependencies
print_status "Installing dependencies..."
poetry install --with dev
print_success "Dependencies installed"

# Step 2: Run linting
print_status "Running code linting..."
poetry run black --check . || {
    print_warning "Black formatting issues found. Run 'poetry run black .' to fix."
    exit 1
}

poetry run ruff check . || {
    print_warning "Ruff linting issues found. Run 'poetry run ruff check --fix .' to fix."
    exit 1
}

poetry run mypy app/ || {
    print_warning "Type checking issues found."
    exit 1
}
print_success "Linting passed"

# Step 3: Run tests
print_status "Running tests with coverage..."
poetry run pytest tests/ --cov=app --cov-report=term-missing --cov-report=html
print_success "Tests completed"

# Step 4: Security scan
print_status "Running security scan..."
poetry run bandit -r app/ -f txt || {
    print_warning "Security issues found by Bandit"
}

poetry run safety check || {
    print_warning "Dependency security issues found"
}
print_success "Security scan completed"

# Step 5: Build Docker image (optional)
if [ "$1" = "--docker" ]; then
    print_status "Building Docker image..."
    docker build -t goodstewards-backend:latest .
    print_success "Docker image built successfully"
fi

print_success "🎉 Build process completed successfully!"
print_status "Coverage report available at: htmlcov/index.html"
print_status "Ready for deployment!" 