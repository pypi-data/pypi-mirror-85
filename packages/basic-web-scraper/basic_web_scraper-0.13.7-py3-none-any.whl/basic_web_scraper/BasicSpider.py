from selenium import webdriver
from time import sleep, perf_counter

import random
import os

from datetime import datetime
from bs4 import BeautifulSoup

from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions as sel_exception

from .custom_exceptions import *

default_options = Options()
default_options.headless = False


class BasicSpider:
    def __init__(self, url=None, options=default_options):
        """ 
        Args:

            url (str): page to load when browser is first launched
            sleep_time (int): a wait-time (in seconds) to allow things like page loads to finish.
            options (selenium.webdriver.firefox.options.Options): custom options for browser
        """

        self.confirm_geckodriver_in_dir()

        self._browser = webdriver.Firefox(options=options)

        if url is not None:
            self.goto(url)
            self.page_soup = self._load_page_soup()

        else:
            self.page_soup = None

    @staticmethod
    def confirm_geckodriver_in_dir():
        
        # Open local dir.
        # Get list of files in dir.
        # Raise GeckoNotFoundException if geckodriver.exe is not in list.
        # return otherwise
        file_list = os.listdir()
        
        if "geckodriver.exe" in file_list:
            return
        
        else:
            raise GeckoNotFoundException("geckodriver.exe was not found in local directory")

    def _load_page_soup(self):
        return BeautifulSoup(self._browser.page_source, features="lxml")

    @staticmethod
    def _confirm_positive_integer(value, include_zero=False):
        """
        Check given value to be a positive integer
        """
        try:
            # Positive
            if include_zero:
                assert value >= 0

            else:
                assert value > 0

            # Integer
            assert type(value) == type(1)   # Integer

        except AssertionError:
            raise ValueError("value must be a positive integer")

    @staticmethod
    def _get_rand_float(range_=(0, 1)):
        """
        returns a random float number within given range using random.uniform()
        """
        return random.uniform(*range_)


    def get_page_y_offset(self):
        y_offset = self._browser.execute_script("return window.pageYOffset")

        return y_offset


    def get_element_y(self, element_id=None, element_class=None):
        """
        Return Y Offset from the top of the page for the given element
        """
        if element_id is not None:
            return self._browser.execute_script(
                f"return document.getElementById('{element_id}').offsetTop"
                )

        elif element_class is not None:
            return self._browser.execute_script(
                f"return document.getElementsByClassName('{element_class}')[0].offsetTop"
                )

        else:
            msg = "Pass either element_id OR element_class, but not both"
            raise ParameterError(msg)

    def get_element_inner_html(self, element_id=None, element_class=None):
        """
        return the innerHTML of given element.
        if element is to be found by class name, then the innerHTML of the first element
        that matches the given class name will be returned.
        """
        if element_id is not None:
            return self._browser.execute_script(f'return document.getElementById("{element_id}").innerHTML')

        elif element_class is not None:
            return self._browser.execute_script(f'return document.getElementsByClassName("{element_class}")[0].innerHTML')

        else:
            msg = "Pass either element_id or element_class, but not both"
            raise ParameterError(msg)

    def get_element_text(self, element_id=None, element_class=None):
        """
        Return text from elements such as inputs
        """
        if element_id is not None:
            return self._browser.execute_script(f'return document.getElementById("{element_id}").value')

        elif element_class is not None:
            return self._browser.execute_script(f'return document.getElementsByClassName("{element_class}")[0].value')

        else:
            msg = "Pass either element_id or element_class, but not both"
            raise ParameterError(msg)

    @staticmethod
    def wait(time=None):

        if time is None:
            time = 3

        sleep(time)

    def goto(self, url, wait=False, wait_for=None):
        """
        Navigate to given URL. Note that some pages will not load all elements
        even if driver thinks the page has been loaded
        """
        self._browser.get(url)

        if wait:
            self.wait(wait_for)

        self.page_soup = self._load_page_soup()

    def refresh_page(self, wait=False, wait_for=None):
        """
        Refresh the page and reset local variables to get new page source.
        """
        self._browser.refresh()

        if wait:
            self.wait(wait_for)

        # refresh page source to get new changes
        self.page_soup = self._load_page_soup()

    @staticmethod
    def get_timestamp(for_filename=False):
        """
        returns a formatted timestamp string (e.g "2020-09-25 Weekday 16:45:37" )
        """
        if for_filename:
            formatted_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        else:
            formatted_time = datetime.now().strftime("%Y-%m-%d %A %H:%M:%S")

        return formatted_time


    def smooth_vscroll_down_to(self, scroll_to, speed=1):
        """
        Smoothly scroll down to given position

        :Paramaters

        scroll_to: (int) y position to scroll to.

        speed: (int) pixels scrolled per loop (effective speed)
        """

        self._confirm_positive_integer(scroll_to)
        self._confirm_positive_integer(speed)

        current_y = self.get_page_y_offset()

        if current_y >= scroll_to:
            msg = "'scroll_to' >= current y offset. consider using smooth_vscroll_up_to instead."
            raise BadScrollPositionException(msg)

        while current_y < scroll_to:

            current_y += speed
            self.instant_vscroll_to(current_y)

        # Jump to target when few enough pixels remain
        self.instant_vscroll_to(scroll_to)

    def smooth_vscroll_down_by(self, scroll_by, speed=1):
        """
        Scroll down by the given amount of pixels at the given speed

        :Parameters:

        scroll_by: (int) amount of pixels to scroll

        speed: (int) amount of pixels scrolled per loop
        """

        self._confirm_positive_integer(scroll_by)
        self._confirm_positive_integer(speed)

        current_y = self.get_page_y_offset()
        final_y = current_y + scroll_by

        while current_y < final_y:
            current_y += speed
            self.instant_vscroll_to(current_y)

        # To avoid inaccuracies from numbers that don't factor into eachother
        self.instant_vscroll_to(final_y)


    def smooth_vscroll_up_to(self, scroll_to, speed=1):
        """
        Slowly scroll to a given y coordinate.

        :Paramaters

        scroll_to: (int) y position to scroll to.

        speed: (int) pixels scrolled per loop (effective speed)
        """

        self._confirm_positive_integer(scroll_to, include_zero=True)
        self._confirm_positive_integer(speed)

        current_y = self.get_page_y_offset()

        if current_y < scroll_to:
            msg = "'scroll_to' < current y offset. consider using smooth_vscroll_down_to instead?"
            raise BadScrollPositionException(msg)

        while current_y > scroll_to:
            current_y -= speed
            self.instant_vscroll_to(current_y)

        # When fewer than 'speed' pixels remain, jump to target
        self.instant_vscroll_to(scroll_to)

    def smooth_vscroll_up_by(self, scroll_by, speed=1):
        """
        Scroll up by the given amount of pixels at the given speed

        :Parameters:

        scroll_by: (int) amount of pixels to scroll

        speed: (int) amount of pixels scrolled per loop
        """

        self._confirm_positive_integer(scroll_by)
        self._confirm_positive_integer(speed)

        current_y = self.get_page_y_offset()
        final_y = current_y - scroll_by if current_y > scroll_by else 0

        while current_y > final_y:
            current_y -= speed
            self.instant_vscroll_to(current_y)

        # To avoid inaccuracies from numbers that don't factor into eachother
        self.instant_vscroll_to(final_y)


    def instant_vscroll_to(self, scroll_to):
        """
        Instantly scroll to a given y coordinate
        """
        try:
            assert scroll_to >= 0

        except AssertionError:
            raise ValueError("scroll_to must be >= 0")

        self._browser.execute_script(f"window.scrollTo(0, {scroll_to})")

    def instant_vscroll_by(self, scroll_by):
        """
        Instantly vertically scroll by given amount
        """
        self._browser.execute_script(f"window.scrollBy(0, {scroll_by})")


    def _mousewheel_vscroll_datapoints(self):
        """
        this is a generator that yields (point_i, point_i+1) from static data
        """
        # data = [0, 0, 0, 0, 2, 1, 14, 45, 70, 120, 49, 36, 16, 3, 0, 0, 0, 0]

        data = list(range(0, 45, 10))
        data += data[::-1]

        for i, p in enumerate(data):
            if i == len(data) - 1:
                break

            else:
                yield data[i], data[i + 1]

    def _mousewheel_vscroll(self, smoothness=3):
        """
        return points which browser will scroll to
        """

        if smoothness <= 0:
            raise ValueError(
                "Condition unsatisfied: smoothness must be larger than 0")

        output_dataset = []

        for x1, x2 in self._mousewheel_vscroll_datapoints():

            step = (x2 - x1) / smoothness if smoothness > 1 else 0
            output_ = x1

            output_dataset.append(float(round(output_, 2)))

            for _ in range(smoothness - 1):

                output_ += step
                output_dataset.append(float(round(output_, 2)))

        return output_dataset

    def mousewheel_vscroll(self, number_of_scrolls=1):
        """
        Each scroll will go down exactly 592 Pixels.
        """

        points = self._mousewheel_vscroll()

        for _ in range(number_of_scrolls):

            for i in points:
                self.instant_vscroll_by(i)
                sleep(0.01)

            sleep(0.2)


    def slow_type(self, text, field, speed_range=(0.05, 0.25)):
        """
        Slowly send text to a given input field.

        :Params:

        text: (str) text to send to field

        speed_range: (int) how quick to send text

        field: (selenium.WebElement) field to send the text to.
        """

        range_ = speed_range

        for letter in text:
            field.send_keys(letter)
            sleep(self._get_rand_float(range_))


    def clear_input(self, element_id):
        """
        Clear all text from given input box
        """
        # self._browser.execute_script(
        #     f"document.getElementById('{element_id}').value = ''"
        # )

        element = self._browser.find_element_by_id(element_id)
        element.clear()
    
    def send_enter(self, element_id):
        """
        Send an Enter, for example, to submit while on an input field
        """
        element = self._browser.find_element_by_id(element_id)
        element.send_keys(Keys.ENTER)

        
    def click_button(self, button_id=None, button=None):
        if button_id is not None:
            button = self._browser.execute_script(
                f'return document.getElementById("{button_id}")')
            button.click()

        elif button is not None:
            button.click()

        else:
            raise ParameterError(
                "Must pass either 'button_id' OR 'button', but not both")


    def _unimplemented__get_combobox_items(self, combobox=None, combobox_id=None):
        """
        return all available options from a given combobox
        """
        pass

    def _unimplemented__select_from_combobox(self, combobox, selection):
        """
        Select an item from a combobox
        """
        pass


    def _unimplemented__toggle_checkbox(self, checkbox):
        pass

    def _unimplemented__tick_checkbox(self, checkbox):
        """
        Raises _undefined_ exception if given checkbox is already ticked
        """
        pass

    def _unimplemented__untick_checkbox(self, checkbox):
        """
        Raises _undefined_ exception if given checkbox is already unticked
        """
        pass
