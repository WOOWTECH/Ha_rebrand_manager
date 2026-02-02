---
name: ha-rebrand-testing
description: Comprehensive test suite for HA Rebrand component including static analysis and Playwright E2E tests
status: backlog
created: 2026-02-02T09:50:37Z
updated: 2026-02-02T09:54:36Z
---

# PRD: HA Rebrand Comprehensive Testing Suite

## Executive Summary

Create a comprehensive testing framework for the HA Rebrand Home Assistant custom component. This includes static code analysis (linting, type checking), unit tests for Python backend logic, and end-to-end (E2E) tests using Playwright-MCP to validate the complete user experience including the admin panel, login page branding, and sidebar customization.

## Problem Statement

### What problem are we solving?
The HA Rebrand component currently lacks automated testing, making it difficult to:
- Ensure code quality and catch regressions during development
- Validate that branding changes work correctly across different Home Assistant versions
- Verify security measures (XSS prevention, input validation) are functioning
- Confirm UI components render and behave correctly

### Why is this important now?
- The component has reached v2.1.0 with significant features (loading screen patching, custom authorize view)
- Complex JavaScript injection requires thorough E2E validation
- Security-sensitive features (file uploads, HTML injection) need automated verification
- Users rely on this component for production Home Assistant deployments

## User Stories

### Developer Persona
As a **component developer**, I want to:
- Run static analysis to catch code issues before committing
- Execute unit tests to verify Python backend logic
- Run E2E tests to validate the complete user experience
- Get clear test reports showing what passed/failed

**Acceptance Criteria:**
- `pytest` runs all Python tests with coverage report
- `ruff` lints Python code with zero warnings
- `mypy` passes type checking
- Playwright tests can be run with a single command

### Contributor Persona
As a **contributor**, I want to:
- Understand how to run tests locally
- See test coverage requirements
- Have CI run tests automatically on PRs

**Acceptance Criteria:**
- README includes test running instructions
- CI workflow validates PRs
- Minimum coverage thresholds documented

## Requirements

### Functional Requirements

#### Static Analysis Tests
1. **Python Linting (ruff)**
   - Check code style and formatting
   - Detect common errors and anti-patterns
   - Configuration in `pyproject.toml`

2. **Type Checking (mypy)**
   - Validate type annotations
   - Check Home Assistant type stubs compatibility
   - Configuration in `pyproject.toml`

3. **JavaScript Linting (eslint)**
   - Check frontend JS files (`ha-rebrand-panel.js`, `ha-rebrand-injector.js`)
   - Validate browser compatibility

#### Unit Tests (pytest)
1. **Configuration Tests**
   - Test `const.py` values and defaults
   - Test YAML schema validation
   - Test color validation regex

2. **Security Tests**
   - Test `_escape_js_string()` function with XSS payloads
   - Test `_validate_color()` with malicious inputs
   - Test file upload validation (type, size, extension)

3. **API Tests**
   - Test HTTP endpoints (`/api/ha_rebrand/*`)
   - Test WebSocket commands (`ha_rebrand/get_config`, `ha_rebrand/update_config`)
   - Test authorization requirements

4. **Component Lifecycle Tests**
   - Test `async_setup()` and `async_setup_entry()`
   - Test `async_unload_entry()`
   - Test config flow

#### E2E Tests (Playwright-MCP)
1. **Login Page Branding**
   - Verify custom logo appears on `/auth/authorize`
   - Verify primary color is applied to buttons
   - Verify document title is customized

2. **Admin Panel Tests**
   - Navigate to Rebrand panel in sidebar
   - Upload logo file via drag-and-drop
   - Configure brand name and titles
   - Set primary color
   - Add text replacement rules
   - Click "Apply Changes" and verify
   - Click "Save to File" and verify persistence

3. **Sidebar Branding**
   - Verify custom logo in sidebar
   - Verify sidebar title change
   - Verify dark mode logo switching

4. **Loading Screen**
   - Verify custom logo appears during page load
   - Verify no flash of default HA logo

5. **Text Replacement**
   - Configure replacement rules
   - Navigate to pages and verify text is replaced
   - Verify replacements persist after navigation

### Non-Functional Requirements

#### Performance
- Unit tests complete in < 30 seconds
- E2E tests complete in < 5 minutes
- No flaky tests (retry logic where needed)

#### Security
- Tests must not expose credentials
- Test fixtures use mock/test data only
- E2E tests use isolated test instance

#### Maintainability
- Tests follow pytest best practices
- Page Object Model for Playwright tests
- Clear test naming conventions

## Success Criteria

| Metric | Target |
|--------|--------|
| Python code coverage | > 80% |
| All static checks pass | 100% |
| E2E test pass rate | 100% |
| Test execution time | < 6 minutes total |
| Zero security vulnerabilities detected | Yes |

## Technical Implementation

### Directory Structure
```
Ha_rebrand_manager/
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures
│   ├── test_const.py            # Constants tests
│   ├── test_security.py         # Security function tests
│   ├── test_config_flow.py      # Config flow tests
│   ├── test_init.py             # Component setup tests
│   └── e2e/
│       ├── conftest.py          # Playwright fixtures
│       ├── pages/
│       │   ├── login_page.py    # Login page object
│       │   ├── admin_panel.py   # Admin panel page object
│       │   └── sidebar.py       # Sidebar page object
│       ├── test_login_branding.py
│       ├── test_admin_panel.py
│       └── test_sidebar.py
├── pyproject.toml               # Test dependencies & config
└── .github/
    └── workflows/
        └── test.yml             # CI workflow
```

### Dependencies
```toml
[project.optional-dependencies]
test = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.0.0",
    "pytest-homeassistant-custom-component>=0.13.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0",
]
e2e = [
    "playwright>=1.40.0",
]
```

## Constraints & Assumptions

### Constraints
- E2E tests require a running Home Assistant instance
- Tests must be compatible with Home Assistant 2024.1+
- Must work on Linux, macOS, and Windows (WSL)

### Assumptions
- Developer has Python 3.11+ installed
- Developer can run Home Assistant locally or in Docker
- Playwright browsers can be installed

### Reference Architecture
- Home Assistant environment architecture reference is available at: `/mnt/c/Users/Matt/Desktop/CLAUDE專案/HomeAssistant_related/HomeAssistant_Reference`
- Use this reference for understanding HA component structure, test patterns, and integration points

## Implementation Guidelines

### Parallel Agent Execution
- Use parallel agents for independent tasks to maximize efficiency
- Static analysis (ruff, mypy, eslint) can run in parallel
- Unit test categories (security, config, API, lifecycle) can run in parallel
- E2E test suites should be designed for parallel execution where possible

## Out of Scope

- Performance benchmarking/load testing
- Mobile browser E2E tests
- Multi-language translation testing
- HACS installation testing
- Home Assistant version compatibility matrix testing

## Dependencies

### External
- Home Assistant Core test utilities
- Playwright browser automation
- pytest ecosystem

### Internal
- Stable component code (v2.1.0)
- Documented configuration options
- Clear API contracts

## Timeline Estimate

| Phase | Tasks |
|-------|-------|
| Phase 1 | Static analysis setup (ruff, mypy, eslint) |
| Phase 2 | Unit tests for security and config |
| Phase 3 | E2E test infrastructure (Playwright setup) |
| Phase 4 | E2E tests for all user flows |
| Phase 5 | CI/CD integration |

## Appendix

### Test Data Fixtures
- Sample logo files (SVG, PNG)
- Sample favicon (ICO)
- Test configuration JSON
- XSS payload list for security tests

### Environment Variables
```bash
HA_URL=http://localhost:8123       # Home Assistant URL
HA_TOKEN=<long_lived_access_token> # For API tests
```
