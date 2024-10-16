"""
Locator object module
"""
from selenium.webdriver.common.by import By
from dataclasses import dataclass


@dataclass
class Locator:
    by: By
    value: str

class Locators:
    """
    Class of Locator object builder
    """

    @staticmethod
    def css(value: str) -> Locator:
        """
        Building Locator object by css selector
        """
        return Locator(By.CSS_SELECTOR, value)

    @staticmethod
    def xpath(value: str) -> Locator:
        """
        Building Locator object by xpath selector
        """
        return Locator(By.XPATH, value)

    @staticmethod
    def id_(value: str) -> Locator:
        """
        Building Locator object by ID
        """
        return Locator(By.ID, value)