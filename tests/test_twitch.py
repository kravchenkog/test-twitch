import datetime
import pytest
import re

from tools.ui.screens.home_page import HomePage
from conftest import UI

class TestTwitchSearch:
    """
    Test class to group Twitch search-related test cases.
    """

    @pytest.fixture(autouse=True)
    def setup(self, ui):
        """
        Fixture to set up the test environment and initialize page objects.
        The 'autouse=True' means this fixture runs automatically for each test.
        """
        self.ui: UI = ui
        self.home_page: HomePage = ui.home_page

    def test_search_starcraft_streamer(self):
        """
        Test case to search for 'StarCraft II' on Twitch and select a streamer.
        """

        # Step 1: go to Twitch
        assert self.home_page.is_page_loaded(), "Twitch home page did not load properly."

        # Step 2: Click the search icon
        self.home_page.click_search_button()

        # Step 3: Input 'StarCraft II' into the search field
        self.home_page.input_search_field(value='StarCraft II') 
        # Step 4: Scroll down 2 times
        self.home_page.scroll_home_screen(times=2)
        # Step 5: Select one streamer
        self.home_page.click_random_stream()  # Implement this in HomePage

        # Step 6: On the streamer's page, wait until the page loads and take a screenshot
        self.home_page.wait_video_starting()
        
        filename = f"{self.ui.device_name}_{self.ui.environment}_{datetime.datetime.now()}"
        cleaned_filename = re.sub(r'\W+', '_', filename)
        self.ui.driver.save_screenshot(f"{cleaned_filename}.png")