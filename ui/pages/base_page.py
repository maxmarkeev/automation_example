import allure
from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    @allure.step("Navigate to {path}")
    def navigate(self, path: str = "/") -> None:
        self.page.goto(path)
        self.page.wait_for_load_state("networkidle")
        self._dismiss_consent_banner()

    def _dismiss_consent_banner(self) -> None:
        try:
            btn = self.page.locator(".fc-cta-consent")
            btn.click(timeout=3000)
            self.page.locator(".fc-consent-root").wait_for(state="hidden", timeout=3000)
        except Exception:
            pass

    def attach_screenshot(self, name: str = "screenshot") -> None:
        allure.attach(
            self.page.screenshot(full_page=True),
            name=name,
            attachment_type=allure.attachment_type.PNG,
        )
