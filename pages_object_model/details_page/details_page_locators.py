from selenium.webdriver.common.by import By


class DetailsPageLocators(object):
    selected_product_tab = (By.XPATH, "// *[@data-name='product-tab' and @aria-selected='true']")
    Export_button = (By.XPATH, "//button[@data-id='product-export']")
    search_filter = (By.XPATH, "//input[@placeholder='Search & Filter']")
    product_id_label = (By.XPATH, "//*[@data-id='header-first-name']")
    product_name_label = (By.XPATH, "//*[contains(@class,'ti-item-name-second')]")
    product_category_label = (By.XPATH, "//*[@class= 'ti-category-badge ti-badge']")
    new_search_button = (By.XPATH, "//*[@data-id= 'product-new-search']")
    share_button = (By.XPATH, "//*[@data-id= 'product-share']")
    all_product_tabs = (By.XPATH, "//*[@data-name='product-tab']")
    tab_by_name = lambda tab_name: (By.XPATH, f"//*[@data-name='product-tab' and contains(text(),'{tab_name}')]")
    table_row_cells = lambda index: (By.XPATH, f"//*[@row-index={index} or @row-id = {index}]/*[@col-id]")
    table_titles = (By.XPATH, "//*[@class='ag-cell-label-container ag-header-cell-sorted-none']")
    table_rows = (By.XPATH, "//*[@row-id]")
    cell_by_column_name = lambda index, coulmn_name: (By.XPATH, f"//*[@row-index = {index}]/*[@col-id='{coulmn_name}']")
    column_to_sort = lambda coulmn_name: (By.XPATH, f"//*[@class ='ag-header-cell-label']/*[contains(text(),'{coulmn_name}')]/..")
    columns_locator = lambda row_index: (By.XPATH, f"//*[@row-id = {row_index}]/*[@col-id]")
    too_much_data_error = (By.XPATH, "//*[contains(text(), 'too much data')]/ancestor::*[contains(@class,'ti-message-container')]")
    last_update_label = (By.XPATH, "//*[@class='ti-data-info']")
