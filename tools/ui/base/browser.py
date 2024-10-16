from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service 

import logging

class Browser:
    """
    Class for browser wrapper
    """

    def __init__(self):
        self.driver = webdriver

    def browser_driver(self, browser_name: str, is_headless: bool = False, device_name: str = None):
        """
        Common method for getting browser driver per its name
        :param is_headless: Boolean value whether to run browser in headless mode
        :param browser_name: Browser name in string format
        :param device_name: Device name for mobile emulation (e.g., "iPhone X")
        :return: Browser driver instance
        """
        if browser_name.lower() == "chrome":
            driver = self.chrome(is_headless=is_headless, device_name=device_name)
        else:
            logging.error(f"Browser: Unsupported browser {browser_name}")
            raise Exception(f"Unsupported browser {browser_name}")
        return driver

    def chrome(self, is_headless: bool = False, device_name: str = None):
        """
        Google Chrome driver with optional mobile emulation
        :param is_headless: Boolean value whether to run browser in headless mode
        :param device_name: Device name for mobile emulation (e.g., "iPhone X")
        :return: Instance of Google Chrome driver
        """
        logging.info(f"Browser setup: Chrome: Starting browser")
        options = webdriver.ChromeOptions()

        # Add mobile emulation if a device is specified
        if device_name:
            mobile_emulation = {"deviceName": device_name}
            options.add_experimental_option("mobileEmulation", mobile_emulation)
            logging.info(f"Running tests in mobile emulation for {device_name}")

        if is_headless:
            logging.info('Browser setup: Chrome: Headless mode enabled')
            options.add_argument("--headless")

        # Create a Service object using ChromeDriverManager
        service = Service(ChromeDriverManager().install())

        # Pass the service and options to the Chrome driver
        chrome_driver = webdriver.Chrome(service=service, options=options)
        return chrome_driver