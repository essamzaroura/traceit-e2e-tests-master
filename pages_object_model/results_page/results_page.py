from pages_object_model.results_page.results_page_locators import ResultsPageLocators
from pages_object_model.common_page.product_selection import ProductSelection
from web_source.base_web_page import BaseWebPage


class ResultsPage(BaseWebPage):

    def checked_checkbox_category_to_filter(self, category, checked):
        if checked == 'unchecked':
            checked_categories_list = self.wait_to_be_visible(*ResultsPageLocators.checked_categories_list)
            if category == 'All':
                for elem in checked_categories_list:
                    self.web_driver.execute_script("arguments[0].click();", elem.find_element(*ResultsPageLocators.checkbox_Categories_list))
            else:
                for elem in checked_categories_list:
                    if category in elem.text:
                        self.web_driver.execute_script("arguments[0].click();",
                                                       elem.find_element(*ResultsPageLocators.checkbox_Categories_list))
        else:
            checked = 'false' if checked=='checked' else 'true'
            if self.wait_to_be_visible(*ResultsPageLocators.count_results):
                Categories_list = self.wait_to_be_visible(*ResultsPageLocators.Categories_list)
                for elem in Categories_list:
                    # ariaelem.find_element(*ResultsPageLocators.checkbox_Categories_list).get_attribute("aria-checked")
                    if category in elem.text and elem.find_element(*ResultsPageLocators.checkbox_Categories_list).get_attribute("aria-checked") == checked:
                        self.web_driver.execute_script("arguments[0].click();", elem.find_element(*ResultsPageLocators.checkbox_Categories_list))

    def find_and_click_on_item_result(self, item_detail, by):
        """
        :param item_detail: A string that is a product_name or product_id
        :param by: A string like 'product_id' or 'product_name' correspond to the type of the item_detail
        :return: A ProductSelection Object
        """
        search_result_item_locators = ResultsPageLocators.get_search_result_item_locators_by(item_detail, by)
        click_item_locator = search_result_item_locators["product_name"]

        is_result_item_visible = self.is_element_visible(*click_item_locator)
        while not is_result_item_visible:
            is_load_more_button_visible = self.is_element_visible(*ResultsPageLocators.Load_more_button)
            if not is_load_more_button_visible:
                raise Exception("%s- Item not found in search_results page, Locator: %s" % (item_detail, click_item_locator[1]))
            self.wait_and_click_on_element(*ResultsPageLocators.Load_more_button)
            is_result_item_visible = self.is_element_visible(*click_item_locator)

        product_id = self.wait_to_be_visible(*search_result_item_locators["product_id"])[0].text
        product_name = self.wait_to_be_visible(*search_result_item_locators["product_name"])[0].text
        product_category = self.wait_to_be_visible(*search_result_item_locators["product_category"])[0].text
        self.wait_and_click_on_element(*click_item_locator)
        return ProductSelection(product_id, product_name, product_category)


    def find_count_of_results(self):
        return self.wait_to_be_visible(*ResultsPageLocators.count_results)

    def find_count_of_results_in_category(self, category=None):
        if "All" in category:
            list = self.wait_to_be_visible(*ResultsPageLocators.Categories_list)
        else:
            list = self.wait_to_be_visible(*ResultsPageLocators.checked_categories_list)

        sum=0
        for item in list:
            sum+=int(item.text.split('(')[1].split(')')[0])
        return sum

    def get_all_visible_results_title(self):
        return self.wait_to_be_visible(*ResultsPageLocators.all_results_title)

    def get_no_results_message(self):
        return self.wait_to_be_visible(*ResultsPageLocators.no_results_message)[0].text


    def is_search_results_filter_present(self):
        return self.is_element_visible(*ResultsPageLocators.search_results_filter)

    def click_show_results_as_a_table(self):
        self.wait_and_click_on_element(*ResultsPageLocators.show_results_as_a_table)

    def get_nth_result(self, n):
        return self.get_all_visible_results_title()[n]

    def get_please_refine_search_tooltip_content(self):
        return self.wait_to_be_visible(*ResultsPageLocators.please_refine_search_tooltip)[0].text