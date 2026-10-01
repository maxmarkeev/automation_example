# Automation Exercise — Test Portfolio

End-to-end test automation portfolio for [automationexercise.com](https://automationexercise.com).
Two layers: REST API tests and UI tests, structured after a real commercial project.

![CI](https://github.com/maxmarkeev/automation_example/actions/workflows/ci.yml/badge.svg)

> **Allure report:** https://maxmarkeev.github.io/automation_example/

---

## Tech stack

| Layer | Tools |
|---|---|
| Language | Python 3.12 |
| API tests | `requests`, `pydantic v2`, `pytest` |
| UI tests | `playwright` (pytest-playwright) |
| Factories | `faker`, `factory_boy` pattern |
| Reporting | `allure-pytest` |
| CI | GitHub Actions + GitHub Pages |
| Linting | `ruff` |

---

## Project structure

```
api/
  configs/        # environment config, .env loader
  connections/    # BaseClient (requests.Session + retry)
  models/         # pydantic request/response models, factories
  services/       # ProductsService, UsersService
  tests/          # API test suite

ui/
  pages/          # Page Object Model (BasePage + page classes)
  tests/          # UI test suite
  conftest.py     # page fixtures, registered_user_api, screenshot on failure

utils/
  assertions.py   # AssertionHelper — soft assertions via `soft` fixture

ai_utils/
  smart_factory.py      # LLM-powered edge case generation (Claude API)
  semantic_validator.py # semantic response validation
```

---

## Running tests

```bash
# install dependencies
pip install -r requirements.txt
playwright install chromium

# all tests
pytest

# API only
pytest -m api

# UI only
pytest -m ui

# smoke suite
pytest -m smoke

# regression suite
pytest -m regression
```

Set `BASE_URL` to override the target (default: `https://automationexercise.com`):

```bash
BASE_URL=https://automationexercise.com pytest -m api
```

---

## Allure report

```bash
# generate and open locally
pytest --alluredir=allure-results
allure serve allure-results
```

In CI the report is published automatically to GitHub Pages after every push to `develop`.

---

## Key patterns

**Soft assertions** — collect multiple failures in one test run via `soft` fixture, no imports needed in tests:

```python
def test_product_schema(self, products_service, soft):
    product = products_service.get_all_products().products[0]
    soft.check(product.id > 0, "id should be positive")
    soft.check(bool(product.name), "name should not be empty")
```

**API + UI fixture sharing** — `registered_user_api` creates a real user via API before the test module and deletes it in teardown, keeping UI tests independent from the registration flow.

**Allure steps on page objects** — `@allure.step` lives on each page object method, not in test bodies. Tests read as plain scenario steps:

```python
def test_valid_credentials(self, signup_login_page, home_page, registered_user_api):
    signup_login_page.open()
    signup_login_page.login(registered_user_api.email, registered_user_api.password)
    assert home_page.is_logged_in()
```

**Screenshot on failure** — `pytest_runtest_makereport` hook in `ui/conftest.py` attaches a full-page screenshot to the Allure report on any UI test failure.

**AI-augmented testing** — `ai_utils/` module uses the Claude API to generate semantically diverse edge-case inputs (`SmartFactory`) and validate response meaning beyond status codes (`SemanticValidator`). Requires `ANTHROPIC_API_KEY`.
