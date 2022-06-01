from selenium.webdriver import ActionChains
from pages_object_model.home_page.home_page_locators import HomePageLocators
from pages_object_model.common_page.product_selection import ProductSelection
from web_source.base_web_page import BaseWebPage
import re

class HomePage(BaseWebPage):

    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
        self.current_selected_category = ""
        self.current_search_text = ""
        self.search_results_number = 0

    def Search_trace_IT_by_text(self, search_text):
        self.find_element(*HomePageLocators.Search_TraceIT_TextField).send_keys(search_text)

    def Choose_search_Categories_by_DropDown(self, search_Categories):
        self.wait_and_click_on_element(*HomePageLocators.search_Categories_DropDown)
        list = self.get_list_Categories_from_DropDown()
        for elem in list:
            if (elem.text == search_Categories):
                actions = ActionChains(self.web_driver)
                actions.move_to_element(elem).perform()
                elem.click()
                break

    def get_list_Categories_from_DropDown(self):
        if self.wait_to_be_visible(*HomePageLocators.list_Categories_DropDown)[0].text == 'All':
            return self.find_elements(*HomePageLocators.list_Categories_DropDown)

    def select_suggest_search_Dropbox_by_index(self, index):
        """
        Clicks on the suggest search dropbox with the specified index
        :param index - a number of the suggest item in the dropbox
        :return a ProductSelection Object representing the selected product
        """
        suggest_search_Dropbox = self.wait_to_be_visible(*HomePageLocators.list_suggest_search_Dropbox)[index]
        selected_product = ProductSelection(*self.get_suggest_search_dropbox_details_by_index(index))
        suggest_search_Dropbox.click()
        return selected_product

    def get_list_suggest_search_Dropbox(self):
        """
        :return a list of tuples like (selected_suggest_id, selected_suggest_name, selected_suggest_tag)
        """
        list_suggest_search_Dropbox = self.wait_to_be_visible(*HomePageLocators.list_suggest_search_Dropbox)
        return list(map(lambda index: self.get_suggest_search_dropbox_details_by_index(index), range(len(list_suggest_search_Dropbox))))

    def get_suggest_search_dropbox_details_by_index(self, index):
        """
        :param index - a number of the suggest item in the dropbox
        :return a tuple like (selected_suggest_id, selected_suggest_name, selected_suggest_tag)
        """
        _RE_COMBINE_WHITESPACE = re.compile(r"\s+")
        selected_suggest_id = self.wait_to_be_displayed(*HomePageLocators.selected_suggest_id)[index].get_attribute('textContent')
        selected_suggest_name = self.wait_to_be_displayed(*HomePageLocators.selected_suggest_name)[index].get_attribute('textContent')
        selected_suggest_tag = self.wait_to_be_displayed(*HomePageLocators.selected_suggest_tag)[index].get_attribute('textContent')

        selected_suggest_id = _RE_COMBINE_WHITESPACE.sub(" ", selected_suggest_id).strip()
        selected_suggest_name = _RE_COMBINE_WHITESPACE.sub(" ", selected_suggest_name).strip()
        selected_suggest_tag = _RE_COMBINE_WHITESPACE.sub(" ", selected_suggest_tag).strip()

        return selected_suggest_id, selected_suggest_name, selected_suggest_tag

    def click_on_search_icon_button(self):
        self.wait_and_click_on_element(*HomePageLocators.search_icon_button)

    def clear_search_trace_IT_text_box(self):
        self.find_element(*HomePageLocators.Search_TraceIT_TextField).click()
        self.find_element(*HomePageLocators.Search_TraceIT_TextField).clear()

    def get_more_results_number(self):
        more_results = self.wait_to_be_visible(*HomePageLocators.count_of_more_results_text)[0].text
        more_results_number = int(more_results.split(" ")[1])
        return more_results_number

    def click_View_All_Results(self):
        self.wait_and_click_on_element(*HomePageLocators.view_all_results)