# GoodStewards Test Structure

This directory contains comprehensive tests for the GoodStewards backend application, organized to support all use cases and scenarios from the technical specification.

## 📁 File Structure

```
tests/
├── README.md                    # This file - test documentation
├── conftest.py                  # Pytest configuration and fixtures
├── test_data.py                 # All test data and scenarios
├── test_scenarios.py            # Integration test scenarios
├── example_test_usage.py        # Examples of how to use test data
├── test_main.py                 # Main application tests
├── test_auth.py                 # Authentication tests
├── test_receipts.py             # Receipt management tests
├── test_simple.py               # Simple smoke tests
└── conftest_simple.py           # Simple test fixtures
```

## 🎯 Test Data Organization

### `test_data.py` - Central Test Data Repository

This file contains all test data organized by entity type:

- **ORGANIZATIONS**: Sample nonprofit organizations
- **USERS**: Regular users, treasurers, and special users (anonymous donors, etc.)
- **RECEIPTS**: Various receipt types (food, office supplies, donations, rejected)
- **TAX_BREAKDOWNS**: Tax breakdown data for receipts
- **PAYMENT_TRANSACTIONS**: Payment reconciliation data
- **FEEDBACK**: User feedback, bug reports, feature requests

### Database Table Names

**Important**: The application uses SQLModel which creates tables with **singular names**:

| Model | Table Name | SQL Query Example |
|-------|------------|-------------------|
| `Organization` | `organization` | `SELECT * FROM organization;` |
| `User` | `user` | `SELECT * FROM "user";` |
| `Receipt` | `receipt` | `SELECT * FROM receipt;` |
| `ReceiptTaxBreakdown` | `receipttaxbreakdown` | `SELECT * FROM receipttaxbreakdown;` |
| `PaymentTransaction` | `paymenttransaction` | `SELECT * FROM paymenttransaction;` |
| `Feedback` | `feedback` | `SELECT * FROM feedback;` |

**Note**: The `user` table must be quoted in SQL queries because `user` is a PostgreSQL reserved keyword.

### Test Scenarios

The `TestScenarios` class contains organized test scenarios based on use cases:

- **RECEIPT_SUBMISSION_SCENARIOS**: Use Case 1.1 - Receipt submission and AI extraction
- **SPECIAL_USER_SCENARIOS**: Use Case 2.5 - Special user management
- **TREASURER_SUBMISSION_SCENARIOS**: Use Case 2.6 - Treasurer submits on behalf
- **FEEDBACK_SCENARIOS**: Use Case 3.1 - Feedback submission
- **FORM_GENERATION_SCENARIOS**: Use Case 1.2 - Form generation

## 🚀 How to Use Test Data

### 1. Simple Test Data Usage

```python
from tests.test_data import USERS, ORGANIZATIONS

def test_user_creation(client):
    user_data = USERS["member_1"]
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
```

### 2. Using Test Scenarios

```python
from tests.test_data import TestScenarios, create_test_image_data

def test_receipt_upload(client, auth_headers):
    scenario = TestScenarios.RECEIPT_SUBMISSION_SCENARIOS["successful_extraction"]
    
    # Use actual receipt image
    image_data = create_test_image_data("1-receipt.png")
    
    response = client.post(
        "/api/v1/receipts/upload",
        files={"image": ("1-receipt.png", image_data, "image/png")},
        data={"is_donation": "false"},
        headers=auth_headers
    )
    
    assert response.status_code == 202
    data = response.json()
    assert data["status"] == scenario["expected_output"]["status"]
```

### 3. Parameterized Tests

```python
import pytest
from tests.test_data import USERS

@pytest.mark.parametrize("user_key", ["member_1", "member_2", "treasurer"])
def test_user_roles(client, user_key):
    user_data = USERS[user_key]
    # Test logic here
```

### 4. Integration Tests

```python
def test_complete_workflow(client, treasurer_headers):
    # 1. Create organization
    org_data = ORGANIZATIONS["test_org"]
    org_response = client.post("/api/v1/organizations/", json=org_data)
    
    # 2. Create users
    user_data = USERS["treasurer"]
    user_response = client.post("/api/v1/users/", json=user_data)
    
    # 3. Submit receipt using actual image
    image_data = create_test_image_data("1-receipt.png")
    receipt_response = client.post(
        "/api/v1/receipts/upload",
        files={"image": ("1-receipt.png", image_data, "image/png")},
        data={"is_donation": "false"},
        headers=treasurer_headers
    )
    # ... continue workflow
```

## 🧪 Test Categories

### Unit Tests
- Test individual functions and components
- Use mock data and minimal dependencies
- Fast execution

### Integration Tests
- Test API endpoints and database interactions
- Use realistic test data
- Test complete workflows

### Scenario Tests
- Test specific use cases from technical specification
- Use predefined scenarios from `TestScenarios`
- Validate business logic

## 📋 Test Data Guidelines

### 1. Data Consistency
- Use consistent UUIDs across related entities
- Maintain referential integrity
- Use realistic but test-safe data

### 2. Data Types
- Use proper enums from models
- Use correct date/datetime objects
- Use UUIDs for IDs
- Use actual receipt images from data/ directory

### 3. Data Organization
- Group related data together
- Use descriptive keys
- Document complex data structures

### 4. Data Maintenance
- Update when models change
- Keep aligned with use cases
- Version control test data

## 🔧 Running Tests

### Run All Tests
```bash
python -m pytest tests/ -v
```

### Run Specific Test File
```bash
python -m pytest tests/test_receipts.py -v
```

### Run Specific Test Function
```bash
python -m pytest tests/test_receipts.py::test_receipt_upload -v
```

### Run Tests with Coverage
```bash
python -m pytest tests/ --cov=app --cov-report=html
```

## 📊 Test Coverage Goals

- **Unit Tests**: 80%+ coverage
- **Integration Tests**: All API endpoints
- **Scenario Tests**: All use cases covered
- **Error Cases**: Common error scenarios

## 🛠️ Adding New Tests

### 1. For New Features
1. Add test data to `test_data.py`
2. Add scenarios to `TestScenarios` class
3. Create test functions in appropriate test file
4. Update this README if needed

### 2. For New Use Cases
1. Create new scenario category in `TestScenarios`
2. Add comprehensive test data
3. Create integration tests
4. Document the new scenarios

### 3. For Bug Fixes
1. Create test that reproduces the bug
2. Verify the fix resolves the issue
3. Add regression test to prevent recurrence

## 📝 Best Practices

### Test Organization
- Keep tests focused and single-purpose
- Use descriptive test names
- Group related tests in classes
- Use fixtures for common setup

### Data Management
- Use fixtures for database setup
- Clean up test data after tests
- Use transactions for test isolation
- Avoid hardcoded values

### Assertions
- Test both positive and negative cases
- Verify response status codes
- Check response data structure
- Validate business rules

### Performance
- Use in-memory database for tests
- Minimize external dependencies
- Use async tests where appropriate
- Parallelize tests when possible

## 🔍 Debugging Tests

### Common Issues
1. **Database Issues**: Check conftest.py configuration
2. **Import Errors**: Verify test data imports
3. **Authentication**: Check auth headers in fixtures
4. **Async Issues**: Use proper async test patterns

### Debug Commands
```bash
# Run with more verbose output
python -m pytest tests/ -v -s

# Run with debugger
python -m pytest tests/ --pdb

# Run specific test with debug
python -m pytest tests/test_receipts.py::test_receipt_upload -s --pdb
```

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing Guide](https://fastapi.tiangolo.com/tutorial/testing/)
- [SQLModel Testing](https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/)
- [Project Technical Specification](../docs/technical/tech_design_spec.md)
- [Database Schema Documentation](../DATABASE_SCHEMA.md)
- [Use Cases Documentation](../docs/requirements/epics_usecases.md) 