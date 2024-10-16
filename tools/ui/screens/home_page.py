import random
from time import sleep

from ..base.base_page import BasePageActions

class HomePage(BasePageActions):
    """
    Page object for the Twitch mobile home page.
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.search_button = self.locator_css('a[aria-label="Search"]')
        self.page_logo = self.locator_css('a[interactioncontent="logo"]')
        self.search_field = self.locator_css('input[type="search"]')
        self.search_result_elements = self.locator_xpath('//*[starts-with(@class, "ScAspectSpacer-sc-")]/parent::div')
        self.stream_list_elements = self.locator_xpath('//*[starts-with(@class, "tw-image")]/parent::div')
        self.stream_live_label = self.locator_css("div[class^='ScChannelStatusTextIndicator']")
        self.start_watching_button = self.locator_css('button[data-a-target="content-classification-gate-overlay-start-watching-button"]')
        self.folow_button = self.locator_css('button[data-a-target="game-directory-follow-button"]')

    # Locators for Twitch mobile homepage
    

    def click_search_button(self):
        """
        Click on the search button using the BasePage method for clicking.
        """
        self.click_element(self.search_button)

    def is_page_loaded(self):
        """
        Check if the Twitch home page is loaded by verifying the logo is visible.
        """
        return self.element_is_displayed(self.page_logo)
    
    def input_search_field(self, value: str):
        self.input_to_element(
            locator=self.search_field, input_text=value
        )
        els = self.get_present_elements_list(locator=self.search_result_elements, timeout=3)
        self.click_element(element=els[0])
        
    def scroll_home_screen(self, times: int):
        self.get_present_element(locator=self.folow_button, timeout=7)
        sleep(2) # sorry for this, need more time to investigate
        for _ in range(times):
            self.scroll_down()
            
    def click_random_stream(self):
        els = self.get_present_elements_list(locator=self.stream_list_elements, timeout=3)
        random_el = random.choice(els)
        self.scroll_into_element_center(element=random_el)
        self.click_element(element=random_el)
        
    def wait_video_starting(self):
        if self.element_is_displayed(locator=self.start_watching_button, timeout=5):
            self.click_element(locator=self.start_watching_button)
        self.get_present_element(locator=self.stream_live_label)
        self.get_visible_element(locator=self.stream_live_label)
        
    