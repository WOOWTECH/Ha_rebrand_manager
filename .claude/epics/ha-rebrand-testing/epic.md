---
name: ha-rebrand-testing
status: completed
created: 2026-02-02T09:55:59Z
updated: 2026-02-02T10:22:10Z
progress: 100%
prd: .claude/prds/ha-rebrand-testing.md
github: [Will be updated when synced to GitHub]
---

# Epic: HA Rebrand Comprehensive Testing Suite

## Overview

Implement a complete testing infrastructure for the HA Rebrand custom component (v2.1.0). This includes static analysis tooling (ruff, mypy), pytest-based unit tests for Python backend logic and security functions, and Playwright-MCP E2E tests for validating the full user experience across login page, admin panel, and sidebar branding.

## Architecture Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Test runner | pytest | Standard for HA custom components, excellent async support |
| Static analysis | ruff + mypy | Fast, comprehensive, HA ecosystem standard |
| E2E framework | Playwright-MCP | Browser automation with MCP integration for AI-assisted testing |
| Test structure | Page Object Model | Maintainable E2E tests, reusable page interactions |
| CI platform | GitHub Actions | Native integration with repository |

## Technical Approach

### Static Analysis Setup
- Configure `pyproject.toml` with ruff rules matching HA core standards
- Enable mypy strict mode with HA type stubs
- Skip eslint for JS files (LitElement patterns are non-standard)

### Unit Test Strategy
- Use `pytest-homeassistant-custom-component` for HA mocking
- Test security functions in isolation with XSS payload fixtures
- Mock aiohttp for HTTP endpoint tests
- Use pytest-asyncio for async component lifecycle tests

### E2E Test Strategy
- Page Object Model with 3 pages: LoginPage, AdminPanel, Sidebar
- Playwright fixtures for browser setup and HA authentication
- Environment variables for HA URL and access token
- Screenshot capture on failure for debugging

### Reference Architecture
- Consult `/mnt/c/Users/Matt/Desktop/CLAUDE專案/HomeAssistant_related/HomeAssistant_Reference` for HA patterns

## Task Breakdown Preview

| # | Task | Description | Parallelizable |
|---|------|-------------|----------------|
| 1 | Project setup | Create `pyproject.toml` with test dependencies, configure ruff/mypy | No (foundation) |
| 2 | Static analysis | Configure and run ruff + mypy, fix any issues | Yes |
| 3 | Unit test fixtures | Create `conftest.py` with HA mocks and test data | No (foundation) |
| 4 | Security unit tests | Test `_escape_js_string()`, `_validate_color()`, file upload validation | Yes |
| 5 | Component unit tests | Test config flow, setup/unload, API endpoints | Yes |
| 6 | E2E infrastructure | Playwright setup, page objects, fixtures | No (foundation) |
| 7 | E2E login/admin tests | Test login page branding, admin panel workflows | Yes |
| 8 | E2E sidebar tests | Test sidebar branding, text replacements | Yes |
| 9 | CI workflow | GitHub Actions workflow for automated testing | No (finalization) |

**Total: 9 tasks** (within 10-task limit)

## Dependencies

### External
- `pytest-homeassistant-custom-component` for HA test utilities
- `playwright` for browser automation
- Running Home Assistant instance for E2E tests

### Internal
- Stable ha_rebrand component code (v2.1.0)
- Test fixtures (sample logos, XSS payloads)

## Success Criteria (Technical)

| Metric | Target | Verification |
|--------|--------|--------------|
| Python coverage | >80% | `pytest --cov` report |
| ruff | 0 errors | `ruff check .` |
| mypy | 0 errors | `mypy ha_rebrand/` |
| E2E pass rate | 100% | Playwright test results |
| Total runtime | <6 min | CI job duration |

## Estimated Effort

| Phase | Tasks | Effort |
|-------|-------|--------|
| Setup & Static | 1, 2 | Small |
| Unit Tests | 3, 4, 5 | Medium |
| E2E Tests | 6, 7, 8 | Medium |
| CI Integration | 9 | Small |

**Parallel execution opportunities:**
- Tasks 4 & 5 can run in parallel (unit tests)
- Tasks 7 & 8 can run in parallel (E2E tests)

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Flaky E2E tests | Add retry logic, explicit waits, screenshot on failure |
| HA version changes | Pin test HA version, use stable APIs |
| CI environment differences | Use Docker-based HA for consistent testing |

## Tasks Created

- [x] 001.md - Project Setup (parallel: false)
- [x] 002.md - Static Analysis Configuration (parallel: true, depends: 001)
- [x] 003.md - Unit Test Fixtures (parallel: false, depends: 001)
- [x] 004.md - Security Unit Tests (parallel: true, depends: 003)
- [x] 005.md - Component Unit Tests (parallel: true, depends: 003)
- [x] 006.md - E2E Infrastructure (parallel: false, depends: 001)
- [x] 007.md - E2E Login and Admin Panel Tests (parallel: true, depends: 006)
- [x] 008.md - E2E Sidebar and Text Replacement Tests (parallel: true, depends: 006)
- [x] 009.md - CI Workflow (parallel: false, depends: 002,004,005,007,008)

**Summary:**
- Total tasks: 9
- Parallel tasks: 5 (002, 004, 005, 007, 008)
- Sequential tasks: 4 (001, 003, 006, 009)
- Estimated total effort: ~25-30 hours
