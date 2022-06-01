from selenium.webdriver.common.by import By

class HomePageLocators(object):

    Search_TraceIT_TextField = (By.XPATH, "//input[@data-id='search-box-input']")
    search_Categories_DropDown = (By.XPATH, "//i[@class='v-icon notranslate mdi mdi-menu-down theme--light']")
    list_Categories_DropDown = (By.XPATH, "//div[@data-name='home-categories']")
    list_suggest_search_Dropbox = (By.XPATH, "//div[@data-name='home-auto-suggest']")
    count_of_more_results_text=(By.XPATH, "//div[@class='ti-more-results-text']")
    search_icon_button=(By.XPATH,"//i[@class='v-icon notranslate ti-magnify-icon v-icon--link mdi mdi-magnify theme--light' and @role='button']")
    selected_suggest_id = (By.XPATH, "//div[@data-name='home-auto-suggest']//div[contains(@class,'ti-search-result-id')]")
    selected_suggest_name = (By.XPATH, "//div[@data-name='home-auto-suggest']//div[@class='ti-search-result-text']")
    selected_suggest_tag = (By.XPATH, "//div[@data-name='home-auto-suggest']//div[@class='ti-category-badge']")
    view_all_results = (By.XPATH, "//*[@data-id='view-all-results']")
