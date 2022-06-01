from pages_object_model.common_page.common_page_locators import CommonPageLocators
from web_source.base_web_page import BaseWebPage

class CommonPage(BaseWebPage):

    # def __init__(self, driver, url):


    # def refresh_web_page(self):
    #     self.refresh()
    def click_menu_items_button(self):
        self.wait_and_click_on_element(*CommonPageLocators.menu_items_button)

    def click_Contact_us_button(self):
        self.wait_and_click_on_element(*CommonPageLocators.Contact_us_menu_item_button)

    def click_About_TraceIT_button(self):
        self.wait_and_click_on_element(*CommonPageLocators.About_TraceIT_menu_item_button)

    def navigate_to_home_page(self):
        self.wait_and_click_on_element(*CommonPageLocators.Trace_It)

    def navigate_by_url_using_query_string(self, url_query_string):
        self.open_ext(url_query_string)


    def get_token_from_swiss_login(self):
        self.open_new_web_tab()
        self.switch_to_new_window()
        self.open(url="https://login.swiss.intel.com/login")
        token = (self.wait_to_be_displayed(*CommonPageLocators.token_from_swiss_login))[0].text.replace('{"token":"', '').replace('"}', "")
        token = f"Bearer {token}"
        self.close()
        self.switch_to_main_window()
        return token
