from selenium.webdriver.common.by import By

class ResultsPageLocators(object):
    checkbox_Categories_list = (By.XPATH, ".//input[@data-name='results-categories' and @type='checkbox']")
    Categories_list = (By.XPATH, "//div[@class='v-input ti-results-filter-cb theme--light v-input--selection-controls v-input--checkbox']")
    all_results_title = (By.XPATH, "//*[@data-name='result-list-item-result']")
    Load_more_button = (By.XPATH, "//*[@data-id='results-load-more']")
    checked_categories_list = (By.XPATH,"//div[@class='v-input ti-results-filter-cb v-input--is-label-active v-input--is-dirty theme--light v-input--selection-controls v-input--checkbox primary--text']")
    result_titel_by_name = lambda item_name: (By.XPATH, f"//*[@data-name='result-list-item-result' and contains(text(),'{item_name}')]")
    result_titel_by_id = lambda item_id:(By.XPATH, f"//span[contains(text(), '{item_id}')]/../../..//*[@data-name='result-list-item-result']")
    count_results = (By.XPATH, "//*[@class='ti-results-returned-text']")
    no_results_message = (By.XPATH, "//*[@id='results-container-no-results']")
    search_results_filter = (By.XPATH, ".//input[@data-name='results-categories' and @type='checkbox']/ancestor::div[@data-id='search-results-filter']")
    show_results_as_a_table = (By.XPATH,"//*[@data-id='table-btn']")
    please_refine_search_tooltip = (By.XPATH, "//*[@class='ti-tooltip' and contains(text(),'refine your search')]")

    @classmethod
    def get_search_result_item_locators_by(cls, item_detail, by):
        """
        :param item_detail: A string that is a product_name or product_id
        :param by: A string like 'product_id' or 'product_name' correspond to the type of the item_detail
        :return: A dict with locators to product_id, product_name, product_category
        """
        search_result_titel_by_name = lambda item_name: f"//*[@data-name='result-list-item-result' and contains(text(),'{item_name}')]"
        search_result_item_by_product_id = lambda product_id: f"//*[contains(@class,'ti-result-item-content')]//*[contains(text(),'{product_id}')]"

        search_result_item_xpath = search_result_item_by_product_id(item_detail) if by == "product_id" else search_result_titel_by_name(item_detail)
        search_result_item_xpath = f"{search_result_item_xpath}/ancestor::*[contains(@class,'ti-search-result-item')]"

        search_result_item_locators = {
            "product_id": (By.XPATH, f"{search_result_item_xpath}//*[contains(text(),'Item Code')]/following-sibling::*"),
            "product_name": (By.XPATH, f"{search_result_item_xpath}//*[@data-name='result-list-item-result']"),
            "product_category": (By.XPATH, f"{search_result_item_xpath}//*[contains(@class,'ti-category-badge')]")
        }
        return search_result_item_locators
