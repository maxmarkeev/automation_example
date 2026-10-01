# TEST_PLAN — automation_example

Target: https://automationexercise.com
Layers: API (`requests` + pydantic) / UI (Playwright)
Markers: `smoke` = critical path, `regression` = full suite

> HTTP status codes marked with * require empirical verification before asserting
> (site may return HTTP 200 with error responseCode in body - AUDIT.md risk #1).

---

## API Tests

### Products — `GET /api/productsList`

| ID | Title | Mark | Expected |
|----|-------|------|----------|
| AP-01 | Returns non-empty products list | smoke | responseCode 200, products.length > 0 |
| AP-02 | Each product has id, name, price, brand, category | regression | All fields present and non-empty |
| AP-03 | POST /productsList returns 405 in responseCode | regression | responseCode 405* |

### Brands — `GET /api/brandsList`

| ID | Title | Mark | Expected |
|----|-------|------|----------|
| AB-01 | Returns non-empty brands list | smoke | responseCode 200, brands.length > 0 |
| AB-02 | PUT /brandsList returns 405 in responseCode | regression | responseCode 405* |

### Search — `POST /api/searchProduct`

| ID | Title | Mark | Expected |
|----|-------|------|----------|
| AS-01 | Valid query returns matching products | smoke | responseCode 200, products.length > 0 |
| AS-02 | Missing search_product param returns 400 | regression | responseCode 400*, message contains "missing" |
| AS-03 | Query with no matches returns empty list | regression | responseCode 200, products.length == 0 |
| AS-04 | Query is case-insensitive | regression | Same results for "top" and "TOP" |

### Login — `POST /api/verifyLogin`

| ID | Title | Mark | Expected |
|----|-------|------|----------|
| AL-01 | Valid email and password returns 200 | smoke | responseCode 200, message "User exists!" |
| AL-02 | Missing password param returns 400 | regression | responseCode 400*, message contains "missing" |
| AL-03 | Wrong password returns 404 | regression | responseCode 404*, message "User not found!" |
| AL-04 | Non-existing email returns 404 | regression | responseCode 404* |
| AL-05 | DELETE /verifyLogin returns 405 | regression | responseCode 405* |

### Account — `POST /api/createAccount`, `DELETE /api/deleteAccount`, `PUT /api/updateAccount`, `GET /api/getUserDetailByEmail`

| ID | Title | Mark | Expected |
|----|-------|------|----------|
| AA-01 | Create account with all required fields | smoke | responseCode 201, message "User created!" |
| AA-02 | Create account with duplicate email returns 400 | regression | responseCode 400* |
| AA-03 | Delete account with valid credentials | smoke | responseCode 200, message "Account deleted!" |
| AA-04 | Delete account with wrong password returns 401 | regression | responseCode 401* |
| AA-05 | Update account name and address | regression | responseCode 200, message "User updated!" |
| AA-06 | Get user detail by valid email | regression | responseCode 200, user object with name and email |
| AA-07 | Get user detail by non-existing email | regression | responseCode 404* |

---

## UI Tests

### Home page

| ID | Title | Mark | Precondition |
|----|-------|------|--------------|
| UH-01 | Home page loads, logo is visible | smoke | - |
| UH-02 | Navigation links (Products, Cart, Signup/Login) are visible | regression | - |
| UH-03 | Footer subscription with valid email shows success | smoke | - |
| UH-04 | Footer subscription with invalid email shows error | regression | - |

### Authentication

| ID | Title | Mark | Precondition |
|----|-------|------|--------------|
| UA-01 | Register new user with all required fields | smoke | - |
| UA-02 | Register with existing email shows error message | regression | User exists in system |
| UA-03 | Login with valid credentials redirects to account page | smoke | Registered user |
| UA-04 | Login with wrong password shows error message | regression | Registered user |
| UA-05 | Login with non-existing email shows error message | regression | - |
| UA-06 | Logout redirects to Signup/Login page | smoke | Logged in user |
| UA-07 | Delete account from UI shows confirmation | regression | Logged in user |

### Products

| ID | Title | Mark | Precondition |
|----|-------|------|--------------|
| UP-01 | Search product via navbar returns results page | smoke | - |
| UP-02 | Search with no matches shows empty state | regression | - |
| UP-03 | Filter products by category shows relevant products | regression | - |
| UP-04 | Filter products by brand shows relevant products | regression | - |
| UP-05 | Product detail page shows name, price, category, brand | regression | - |

### Cart

| ID | Title | Mark | Precondition |
|----|-------|------|--------------|
| UC-01 | Add product to cart from products list | smoke | - |
| UC-02 | Cart shows correct product name and price | smoke | Product in cart |
| UC-03 | Remove product from cart | regression | Product in cart |
| UC-04 | Cart quantity updates correctly | regression | Product in cart |

### Checkout

| ID | Title | Mark | Precondition |
|----|-------|------|--------------|
| UO-01 | Registered user can complete checkout | smoke | Logged in user, product in cart |
| UO-02 | Checkout page shows correct delivery address | regression | Logged in user, product in cart |
| UO-03 | Order confirmation page is shown after payment | regression | Checkout started |
| UO-04 | Guest is redirected to login during checkout | regression | Not logged in, product in cart |

### Contact Form

| ID | Title | Mark | Precondition |
|----|-------|------|--------------|
| UF-01 | Submit contact form with all fields and file upload | regression | - |
| UF-02 | Submit without required field keeps form open | regression | - |

---

## Out of scope

- Rate limiting / throttling (demo site has none)
- Auth token / session security (site uses email+password, no Bearer token)
- Payment processing (test site uses dummy payment)
- Performance / load testing
