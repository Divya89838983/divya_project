# Test Suite Organization
## Running Tests

### Run all tests:
```bash
pytest tests/
```

### Run tests by module:
```bash
# Core module tests only
pytest tests/core/

# Streamlit UI tests only
pytest tests/streamlit_ui/
```

### Run specific test file:
```bash
pytest tests/core/test_aqi_calculators.py
pytest tests/streamlit_ui/test_location.py
```

### Run with verbose output:
```bash
pytest tests/ -v
```

### Run with coverage:
```bash
pytest tests/ --cov=module --cov-report=term-missing
```

## Test Structure Philosophy

Tests are organized to match the source code structure:
- `tests/core/` mirrors `module/core/`
- `tests/streamlit_ui/` mirrors `module/streamlit_ui/`
