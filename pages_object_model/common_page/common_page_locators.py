from selenium.webdriver.common.by import By

class CommonPageLocators(object):

    menu_items_button = (By.XPATH, "//*[@class = 'material-icons core-menu-items']")
    Contact_us_menu_item_button = (By.XPATH, "//div[@class='v-list-item__title' and contains(text(),'Contact us')]")
    About_TraceIT_menu_item_button = (By.XPATH, "//div[@class='v-list-item__title' and contains(text(),'About TraceIT')]")
    Trace_It = (By.XPATH, "//div[@class='v-toolbar__content']//div[@class='core-secondary-title']")
    token_from_swiss_login = (By.XPATH, "//pre")
