"""
Base Page Object module
"""
from typing import List, Any, Union

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

from .locator import Locators, Locator


class BasePageActions:
    """
    Class for working with pages
    """

    def __init__(self, driver):
        self.driver = driver
        self.locator_css = Locators.css
        self.locator_xpath = Locators.xpath
        self.locator_id = Locators.id_
        self.keys = Keys
        self.timeout = 10

    # Getters

    def __element(self,
                  locator: Locator,
                  element: WebElement,
                  timeout: float = None,
                  show_error_logs: bool = True) -> WebElement:
        """
        Get element object accepting either Web element or it's locator
        Is needed to use both possible options for other action methods

        :param locator: Locator to find element
        :param element: Element itself
        :param timeout: Time limit to find element
        :param show_error_logs: Boolean value whether to log error
        :return: Web element
        """
        if timeout is None:
            timeout = self.timeout

        if element:
            return element
        elif locator:
            if not isinstance(locator, tuple):
                locator = (locator.by, locator.value)
            return self.get_visible_element(locator, timeout=timeout, show_error_logs=show_error_logs)
        else:
            raise Exception("Unknown way to define an element")

    def get_visible_element(self,
                            locator: Locator,
                            timeout: float = None,
                            show_error_logs: bool = True) -> WebElement:
        """
        Find visible element

        :param locator: Locator to find element
        :param timeout: Time limit to find element
        :param show_error_logs: Boolean value whether to log error
        :return: Web element
        """
        if not isinstance(locator, tuple):
            locator = (locator.by, locator.value)
        if timeout is None:
            timeout = self.timeout

        logging.info(msg=f"Browser: Finding  element (visible) with locator {locator}")
        try:
            element = WebDriverWait(self.driver, timeout=timeout) \
                .until(ec.visibility_of_element_located(locator=locator))
            return element
        except TimeoutException:
            error = f"Cannot find visible element with locator {locator} within {timeout} seconds"
            if show_error_logs:
                logging.error(msg=error)
            raise AssertionError(error)

    def get_present_element(self,
                            locator: Locator,
                            timeout: float = None,
                            show_error_logs: bool = True) -> WebElement:
        """
        Find present element

        :param locator: Locator to find element
        :param timeout: Time limit to find element
        :param show_error_logs: Boolean value whether to log error
        :return: Web element
        """
        if timeout is None:
            timeout = self.timeout

        logging.info(msg=f"Browser: Finding element (present) with locator {locator}")
        try:
            locator = (locator.by, locator.value)
            element = WebDriverWait(self.driver, timeout=timeout) \
                .until(ec.presence_of_element_located(locator=locator))
            return element
        except TimeoutException:
            error = f"Cannot find present element with locator {locator} within {timeout} seconds"
            if show_error_logs:
                logging.error(msg=error)
            raise AssertionError(error)

    def get_clickable_element(self,
                              locator: Locator,
                              timeout: float = None,
                              show_error_logs: bool = True) -> WebElement:
        """
        Find clickable element

        :param locator: Locator to find element
        :param timeout: Time limit to find element
        :param show_error_logs: Boolean value whether to log error
        :return: Web element
        """
        if timeout is None:
            timeout = self.timeout

        logging.info(msg=f"Browser: Finding element (present) with locator {locator}")
        try:
            element = WebDriverWait(self.driver, timeout=timeout) \
                .until(ec.element_to_be_clickable(locator))
            return element
        except TimeoutException:
            error = f"Cannot find clickable element with locator {locator} within {timeout} seconds"
            if show_error_logs:
                logging.error(msg=error)
            raise AssertionError(error)

    def get_visible_elements_list(self,
                                  locator: Locator,
                                  timeout: float = None,
                                  show_error_logs: bool = True) -> List[WebElement]:
        """
        Find multiple visible elements

        :param locator: Locator to find element
        :param timeout: Time limit to find element
        :param show_error_logs: Boolean value whether to log error
        :return: List of web elements
        """
        if timeout is None:
            timeout = self.timeout

        logging.info(msg=f"Browser: Finding multiple elements list (visible) with locator {locator}")
        try:
            elements_list = WebDriverWait(self.driver, timeout=timeout) \
                .until(ec.visibility_of_all_elements_located(locator=locator))
            return elements_list
        except TimeoutException:
            error = f"Cannot find list of visible elements with locator {locator} within {timeout} seconds"
            if show_error_logs:
                logging.error(msg=error)
            raise AssertionError(error)

    def get_present_elements_list(self,
                                  locator: Locator,
                                  timeout: float = None,
                                  show_error_logs: bool = True) -> List[WebElement]:
        """
        Find multiple present elements

        :param locator: Locator to find element
        :param timeout: Time limit to find element
        :param show_error_logs: Boolean value whether to log error
        :return: List of web elements
        """
        if timeout is None:
            timeout = self.timeout

        logging.info(msg=f"Browser: Finding multiple elements list (present) with locator {locator}")
        try:
            locator = (locator.by, locator.value)
            elements_list = WebDriverWait(self.driver, timeout=timeout) \
                .until(ec.presence_of_all_elements_located(locator=locator))
            return elements_list
        except TimeoutException:
            error = f"Cannot find list of present elements with locator {locator} within {timeout} seconds"
            if show_error_logs:
                logging.error(msg=error)
            raise AssertionError(error)

    def get_child_element(self,
                          child_locator: Locator,
                          base_element: WebElement = None,
                          base_locator: Locator = None,
                          timeout: float = None) -> WebElement:
        """
        Find child element

        :param child_locator: Locator of the child element
        :param base_element: Base element itself (if possible)
        :param base_locator: Locator to find base element
        :param timeout: Time limit to find base element
        :return: Child web element
        """
        if timeout is None:
            timeout = self.timeout

        logging.info(f"Browser: Finding child element with it's locator {child_locator}")
        parent_el = self.__element(locator=base_locator, element=base_element, timeout=timeout)
        try:
            child_el = parent_el.find_element(by=child_locator.by, value=child_locator.value)
            return child_el
        except NoSuchElementException:
            error = f"Cannot find child element with locator {child_locator}"
            logging.error(msg=error)
            raise AssertionError(error)

    def get_child_elements_list(self,
                                child_locator: Locator,
                                base_element: WebElement = None,
                                base_locator: Locator = None,
                                timeout: float = None) -> List[WebElement]:
        """
        Find child element

        :param child_locator: Locator of the child elements
        :param base_element: Base element itself (if possible)
        :param base_locator: Locator to find base element
        :param timeout: Time limit to find base element
        :return: List of child web elements
        """
        if timeout is None:
            timeout = self.timeout

        logging.info(f"Browser: Finding multiple child elements list with locator {child_locator}")
        parent_el = self.__element(locator=base_locator, element=base_element, timeout=timeout)
        try:
            child_elements = parent_el.find_elements(by=child_locator.by, value=child_locator.value)
            return child_elements
        except NoSuchElementException:
            error = f"Cannot find multiple child elements list with locator {child_locator}"
            logging.error(msg=error)
            raise AssertionError(error)

    @property
    def page_title(self) -> str:
        """
        Browser page title
        """
        logging.info(msg="Getting page title")
        return self.driver.title

    def get_element_attribute(self,
                              attribute: str,
                              locator: Locator = None,
                              element: WebElement = None,
                              timeout: float = None) -> Union[str, None]:
        """
        Get element's attribute value \n
        :param attribute: Name of element's attribute to be found
        :param locator: Locator to find element
        :param element: Element itself (if possible)
        :param timeout: Time limit to find element
        :return: Element's attribute value (if found -> string value, if not found -> None)
        """
        if timeout is None:
            timeout = self.timeout

        el = self.__element(locator=locator, element=element, timeout=timeout)
        attr_value = el.get_attribute(attribute)
        return attr_value

    def get_text(self,
                 locator: Locator = None,
                 element: WebElement = None,
                 timeout: float = None) -> str:
        """
        Get element's text. \n
        Accepts either element's locator or element itself.

        :param locator: Locator to find element
        :param element: Element itself (if possible)
        :param timeout: Time limit to find element
        :return: Text value of the element
        """
        if timeout is None:
            timeout = self.timeout

        el = self.__element(locator, element, timeout=timeout)
        logging.info(msg="Browser: Getting element text")
        el_text = el.text
        return el_text

    def get_input_value(self,
                        locator: Locator = None,
                        element: WebElement = None,
                        timeout: float = None) -> Union[str, None]:
        """
        Get input value.

        :param locator: Locator to find the element
        :param element: Element itself (if possible)
        :param timeout: Time limit to find element
        :return: Input value
        """
        if timeout is None:
            timeout = self.timeout

        el = self.__element(locator=locator, element=element, timeout=timeout)
        logging.info(msg="Browser: Getting element\'s input value")
        el_value = self.get_element_attribute(element=el, attribute='value')
        return el_value

    def get_execute_script_result(self,
                                  script: str) -> Any:
        """
        Execute script and get it's result.

        :param script: Script to be executed
        :return: Result of the script execution
        """
        return_script = f"return {script}"
        logging.info(f"Browser: Returning script execution result for {return_script}")
        return self.driver.execute_script(return_script)

    @property
    def page_source(self):
        """
        Page source.

        :return: Page source
        """
        logging.info(msg="Browser: Getting page source")
        return self.driver.page_source

    def element_is_displayed(self,
                             locator: Locator = None,
                             element: WebElement = None,
                             timeout: float = None) -> bool:
        """
        Check that element is displayed (with is_displayed() element's method). \n
        Accepts either element's locator or element itself.

        :param locator: Locator to find the element
        :param element: Element itself (if possible)
        :param timeout: Time limit to find element
        :return: Boolean value whether element is displayed
        """
        if timeout is None:
            timeout = self.timeout

        logging.info(msg="Browser: Checking that element is displayed")
        try:
            is_displayed = self.__element(locator=locator,
                                          element=element,
                                          timeout=timeout,
                                          show_error_logs=False).is_displayed()
            return is_displayed
        except (TimeoutException, AssertionError):
            logging.info(msg="Browser: Element is not found")
            return False

    def element_is_present(self,
                           locator: Locator = None,
                           timeout: float = None) -> bool:
        """
        Check that element is present in DOM (aka find element).

        :param locator: Locator to find the element
        :param timeout: Time limit to find element
        :return: Boolean value whether element is present in DOM
        """
        if timeout is None:
            timeout = self.timeout

        logging.info(f"Browser: Checking that element is present in DOM with locator {locator}")
        try:
            self.get_present_element(locator=locator, timeout=timeout, show_error_logs=False)
            logging.info(msg="Browser: Element is found")
            return True
        except (TimeoutException, AssertionError):
            logging.info(msg="Browser: Element is not found")
            return False

    def element_is_absent(self,
                          locator: Locator = None,
                          timeout: float = None) -> bool:
        """
        Check that element is absent in DOM.

        :param locator: Locator to find the element
        :param timeout: Time limit to find element
        :return: Boolean value whether element is absent in DOM
        """
        if timeout is None:
            timeout = self.timeout

        logging.info(f"Browser: Checking that element is absent in DOM with locator {locator}")
        try:
            self.wait_elements_invisibility(locator=locator, timeout=timeout, show_error_logs=False)
            logging.info(msg="Browser: Element is absent")
            return True
        except (TimeoutException, AssertionError):
            logging.info(msg="Browser: Element is present")
            return False

    def element_is_clickable(self,
                             locator: Locator = None,
                             timeout: float = None) -> bool:
        """
        Check that element is clickable.

        :param locator: Locator to find the element
        :param timeout: Time limit to find element
        :return: Boolean value whether element is clickable
        """
        logging.info(f"Browser: Checking that element is clickable with locator {locator}")
        try:
            self.get_clickable_element(locator=locator, timeout=timeout, show_error_logs=False)
            logging.info(msg="Browser: Element is clickable")
            return True
        except (TimeoutException, AssertionError):
            logging.info(msg="Browser: Element is not clickable")
            return False

    # Setters

    def input_to_element(self,
                         locator: Locator = None,
                         element: WebElement = None,
                         input_text="",
                         timeout: float = None,
                         log_input: bool = False):
        """
        Input some text to element. \n
        Accepts either element's locator or element itself

        :param locator: Locator to find the element
        :param element: Element itself (if possible)
        :param input_text: Value to input to the element
        :param timeout: Time limit to find element
        :param log_input: Bool value whether to log input
        """
        if timeout is None:
            timeout = self.timeout

        el = self.__element(locator=locator, element=element, timeout=timeout)
        if log_input:
            logging.info(f"Browser: making input to element: \'{input_text}\'")
        else:
            logging.info(f"Browser: making input to element: (hidden input)")
        el.send_keys(input_text)

    def accept_alert(self):
        """
        Accept alert notification.
        """
        logging.info(msg="Browser: Accepting alert")
        self.driver.switch_to.alert.accept()

    def click_keyboard_button(self, keyboard_button: str):
        """
        Click button on keyboard.

        :param keyboard_button: Button to be clicked.
               Can also accept button from Keys package using self.keys.<button>
        """
        logging.info(msg="Browser: Click Keyboard button")
        actions = ActionChains(self.driver)
        actions.send_keys(keyboard_button).perform()

    def clear_textbox(self,
                      locator: Locator = None,
                      element: WebElement = None,
                      timeout: float = None):
        """
        Clear element's input value. \n
        Accepts either element's locator or element itself

        :param locator: Locator to find element
        :param element: Element itself (if possible)
        :param timeout: Time limit to find element
        """
        if timeout is None:
            timeout = self.timeout

        el = self.__element(locator=locator, element=element, timeout=timeout)
        logging.info(msg="Browser: Clearing element\'s input value")
        el.clear()

    def clear_textbox_with_keyboard(self,
                                    locator: Locator = None,
                                    element: WebElement = None,
                                    timeout: float = None):
        """
        Clear element's input value. \n
        Accepts either element's locator or element itself.

        :param locator: Locator to find element
        :param element: Element itself (if possible)
        :param timeout: Time limit to find element
        """
        if timeout is None:
            timeout = self.timeout

        el = self.__element(locator=locator, element=element, timeout=timeout)
        logging.info(msg="Browser: Clearing element\'s input value with keyboard")
        self.input_to_element(element=el, input_text=f"{self.keys.CONTROL} + a")
        self.input_to_element(element=el, input_text=self.keys.DELETE)

    # Actions

    def navigate(self, url: str):
        """
        Navigate to url

        :param url: URL to open in browser
        """
        logging.info(msg=f"Browser: Opening URL {url}")
        self.driver.get(url)

    def open_in_new_tab(self, url: str):
        """
        Open URL in new tab

        :param url: URL to open in new tab in browser
        """
        logging.info(msg=f"Browser: Opening URL in new tab: {url}")
        self.execute_script(f'window.open("{url}");')

    def refresh_current_screen(self):
        """
        Refresh current browser screen
        """
        logging.info(msg="Browser: Refreshing current screen")
        self.driver.refresh()

    def switch_to_frame(self,
                        locator: Locator = None,
                        element: WebElement = None,
                        timeout: float = None):
        """
        Switch to iframe. \n
        Accepts either element's locator or element itself.

        :param locator: Locator to find iframe
        :param element: Iframe element itself (if possible)
        :param timeout: Time limit to find iframe
        """
        if timeout is None:
            timeout = self.timeout

        iframe_el = self.__element(locator=locator, element=element, timeout=timeout)
        logging.info(msg="Browser: Switching to iframe")
        self.driver.switch_to.frame(iframe_el)

    def switch_to_default_content(self):
        """
        Switch to default content
        """
        logging.info(msg="Browser: Switching to default content")
        self.driver.switch_to.default_content()

    def execute_script(self, script: str, *args):
        """
        Execute script in browser

        :param script: Script to execute
        :param args: Additional args for execute_script
        """
        logging.info(msg=f"Browser: Executing script: {script}")
        self.driver.execute_script(script, *args)

    def click_element(self,
                      locator: Locator = None,
                      element: WebElement = None,
                      timeout: float = None):
        """
        Click an element. \n
        Accepts either element's locator or element itself.

        :param locator: Locator to find element
        :param element: Element itself (if possible)
        :param timeout: Time limit to find element
        """
        if timeout is None:
            timeout = self.timeout

        el = self.__element(locator=locator, element=element, timeout=timeout)
        logging.info(msg="Browser: Clicking element")
        el.click()

    def click_outside(self):
        """
        Clicking outside, in example, to close pop-ups
        """
        logging.info(msg="Browser: Click outside")
        self.click_element(locator=self.locator_css("body"))

    def moveto_and_click_element(self,
                                 locator_to_move: Locator = None,
                                 element_to_move: WebElement = None,
                                 timeout_to_move: float = None,
                                 locator_to_click: Locator = None,
                                 element_to_click: WebElement = None,
                                 timeout_to_click: float = None):
        """
        Move to an element and click another element. \n
        Accepts either elements' locators or elements themselves.

        :param locator_to_move: Locator to find element, to which it is needed to move
        :param element_to_move: Element itself (if possible), to which it is needed to move
        :param timeout_to_move: Time limit to find element, to which it is needed to move
        :param locator_to_click: Locator to find element, which is needed to be clicked
        :param element_to_click: Element itself (if possible), which is needed to be clicked
        :param timeout_to_click: Time limit to find element, which is needed to be clicked
        """
        element_to_move = self.__element(locator=locator_to_move,
                                         element=element_to_move,
                                         timeout=timeout_to_move)
        element_to_click = self.__element(locator=locator_to_click,
                                          element=element_to_click,
                                          timeout=timeout_to_click)
        logging.info(msg="Browser: Move to element A (hover) and click element B")
        actions = ActionChains(self.driver)
        actions.move_to_element(element_to_move).click(element_to_click).perform()

    def moveto_element(self,
                       locator_to_move: Locator = None,
                       element_to_move: WebElement = None,
                       timeout: float = None):
        """
        Move to an element. \n
        Accepts either element's locator or element itself.

        :param locator_to_move: Locator to find element, to which it is needed to move
        :param element_to_move: Element itself (if possible), to which it is needed to move
        :param timeout: Time limit to find element, to which it is needed to move
        """

        if timeout is None:
            timeout = self.timeout

        element_to_move = self.__element(locator=locator_to_move,
                                         element=element_to_move,
                                         timeout=timeout)
        logging.info(msg="Browser: Moving to element (hover)")
        actions = ActionChains(self.driver)
        actions.move_to_element(element_to_move).perform()

    def moveto_element_offset(self,
                              locator_to_move: Locator = None,
                              element_to_move: WebElement = None,
                              timeout: float = None,
                              x_offset: int = 0, y_offset: int = 0):
        """
        Move to an element with offset. \n
        Accepts either element's locator or element itself.

        :param locator_to_move: Locator to find element, to which it is needed to move
        :param element_to_move: Element itself (if possible), to which it is needed to move
        :param timeout: Time limit to find element, to which it is needed to move
        :param x_offset: x coordinate within the element (x=0, y=0 position of top left pixel)
        :param y_offset: y coordinate within the element
        """

        element_to_move = self.__element(locator=locator_to_move,
                                         element=element_to_move,
                                         timeout=timeout)
        logging.info(msg="Browser: Moving to element with offset (hover)")
        actions = ActionChains(self.driver)
        actions.move_to_element_with_offset(element_to_move, x_offset, y_offset).perform()

    def scroll_into_element_center(self,
                                   locator: Locator = None,
                                   element: WebElement = None,
                                   timeout: float = None):
        """
        Scroll into element's center.

        :param locator: Locator to find element
        :param element: Element itself (if possible)
        :param timeout: Time limit to find element
        """
        if timeout is None:
            timeout = self.timeout

        element = self.__element(locator=locator, element=element, timeout=timeout)
        script = "arguments[0].scrollIntoView({block: 'center'});"
        self.execute_script(script, element)
        logging.info(msg="Browser: Scroll to element center")
        
    def scroll_down(self):
        script = "window.scrollBy(0, window.innerHeight);"
        self.execute_script(script)
        

    def wait_elements_invisibility(self,
                                   locator: Locator,
                                   timeout: float = None,
                                   show_error_logs: bool = True):
        """
        Wait till single element is invisible.

        :param locator: Locator to find element
        :param timeout: Timeout for element to be invisible
        :param show_error_logs: Boolean value whether to log error
        """
        if timeout is None:
            timeout = self.timeout

        logging.info(msg="Browser: Wait till single element is invisible")
        try:
            WebDriverWait(self.driver, timeout=timeout) \
                .until(ec.invisibility_of_element_located(locator=locator))
        except TimeoutException:
            error = f"Element with locator {locator} is visible after {timeout} seconds"
            if show_error_logs:
                logging.error(msg=error)
            raise AssertionError(error)