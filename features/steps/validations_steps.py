from behave import then
from hamcrest import *
from utils_API.traceit_api import TraceitApi

from utils_emails.email_handler import EmailHandler
import time
from utils.excel_handler import ExcelHandler
from utils.Json_file_handler import JsonFileHandler


@then("validate Search Results rising with categories")
def step_impl(context):
    """
    Validate a search results appear, the results not empty, if a specific category selected, all results are with that category.
    Should not be used if CATTS category(Visual ID, Lot) is selected, or no result are expected
    """

    selected_category = context.home_page.current_selected_category
    actual_search_results_list = context.home_page.get_list_suggest_search_Dropbox()

    try:
        more_results_number = context.home_page.get_more_results_number()
        assert_that(len(actual_search_results_list), equal_to(5))
        assert_that(more_results_number, greater_than(0), f"Expected the number of more results to be grater than 0, but actuall {more_results_number}")
    except:
        # More results did not appear, so the number of suggested at most 5
        more_results_number = 0
        assert_that(len(actual_search_results_list), less_than_or_equal_to(5), f"Expected at most 5 suggested, but actually {len(actual_search_results_list)}")

    for row_number, row in enumerate(actual_search_results_list, 1):
        product_id, product_name, category = row
        assert_that(product_id, True, f"Row number: {row_number}, product_id is missing")
        assert_that(product_name, True, f"Row number: {row_number}, product_name is missing")
        assert_that(category, True, f"Row number: {row_number}, category is missing")
        if selected_category != "All":
            assert_that(category, equal_to(selected_category), f"Row number: {row_number}, expected an item with category {selected_category}, but actually was {category}")

    search_results_number = len(actual_search_results_list) + more_results_number
    context.home_page.search_results_number = search_results_number


@then("validate details page opens and contains the selected product info")
@then("validate details page opens and contains the product id:{product_id} and product name:{product_name} and product_category:{product_category} in the title")
def step_impl(context, product_id=None, product_name=None, product_category=None):
    context.details_page.load_page_details()
    if not any((product_id, product_name, product_category)):
        product_id = context.product_selection.product_id
        product_name = context.product_selection.product_name
        product_category = context.product_selection.product_category

    assert_that(context.details_page.product_id_label, contains_string(product_id), "Expected product id in details page title : %s \n     Actual product id:%s " %(product_id, context.details_page.product_id_label))
    assert_that(context.details_page.product_name_label, equal_to(product_name), "Expected product name in details page title : %s \n     Actual product name:%s " %(product_name, context.details_page.product_name_label))
    assert_that(context.details_page.product_category_label, equal_to(product_category),"Expected product category in details page title : %s \n     Actual product category:%s " % (product_category, context.details_page.product_category_label))


@then("validate Search Results found results in equal to Home Page results")
@then("validate Search Results found results in:{all} Categories")
@then("validate Search Results found:{number:d} results in:{all} Categories")
def step_impl(context, all=None, number=None):
    # the number match between side (categories list) and the total
    count_found_results_UI = int((context.results_page.find_count_of_results()[0].text).split(' ')[0])
    if not number and not all:
        # read from home page
        number = context.home_page.search_results_number

    if number:
        # assert that count_found_results_UI equals to or different than number by up to 5%
        assert_that(count_found_results_UI,
                    greater_than_or_equal_to(number * 0.95) and less_than_or_equal_to(number * 1.05))
    else:
        number = context.results_page.find_count_of_results_in_category(all)
        assert_that(count_found_results_UI, equal_to(number))

    if number > 10: number = 10
    assert_that(len(context.results_page.get_all_visible_results_title()), equal_to(number))


@then("validate column:{column_name} sorted:{descending}")
@then("validate column:{column_name} sorted")
def step_impl(context, column_name, descending=False):
    actual_column_cells = context.details_page.get_all_column_cells_by_column_name(column_name)
    sorted_list = actual_column_cells
    if descending:
        sorted_list.sort(reverse=True)
    else:
        sorted_list.sort()
    assert_that(sorted_list, equal_to(actual_column_cells),"Column: %s  not sorted " % (column_name))


@then("validate UI with File from {source}")
def step_impl(context, source="export"):
    context.details_page.load_page_details()
    summary = ''
    ui_content = context.details_page.read_ui_table(source)

    if source == "resources":
        product_id = context.details_page.product_id_label
        file_path, file_name = JsonFileHandler.find_resource_file_by_product_id_and_tab_number(product_id=product_id, tab_index=context.details_page.get_selected_tab_index())
        assert_that(file_path is not None, equal_to(True), f"File not found: {file_name}")
        source_content = JsonFileHandler.read_from_file(file_path)
        assert_that(len(ui_content[1]), equal_to(len(source_content)))  # Equal number of rows between UI table and source_content
        all_rows_exist = JsonFileHandler.all_rows_exist_in_resource_file(source_content, ui_content[1])
        assert_that(all_rows_exist, equal_to(True), f"The Resource file {file_name} and the UI are different:")

    # CSV Part
    else:
        csv_file_path, csv_file_name = ExcelHandler.find_csv_file_by_tab_name(context.details_page.selected_product_tab)
        csv_content = ExcelHandler.read_from_csv(csv_file_path)
        csv_copy = ExcelHandler.clean_spaces(csv_content)
        ui_copy = ExcelHandler.clean_spaces(ui_content)
        csv_unique_rows_copy, ui_unique_rows_copy = ExcelHandler.diff(csv_copy, ui_copy)
        csv_unique_rows, ui_unique_rows = ExcelHandler.diff(csv_content, ui_content)
        summary = f"\nRows that unique to CSV file {csv_file_name}:\n" + ExcelHandler.stringify_for_print(
            csv_unique_rows) + "\n\nRows that unique to UI:\n" + ExcelHandler.stringify_for_print(ui_unique_rows)
        assert_that(len(csv_unique_rows_copy) + len(ui_unique_rows_copy), equal_to(0), summary)


@then("Validate categories filter not presented on Result page")
def step_impl(context):
    is_present = context.results_page.is_search_results_filter_present()
    assert_that(is_present, equal_to(False))

@then("validate that No results found in Search Result Page")
def step_impl(context):
    no_results_message = context.results_page.get_no_results_message()
    assert_that(no_results_message, equal_to("No results, try to refine your search"))

@then("validate details page title")
def step_impl(context):
    context.details_page.load_page_details()
    search_text = context.home_page.current_search_text
    selected_category = context.home_page.current_selected_category
    search_results_number = context.home_page.search_results_number
    expected_title = f"Showing results for {search_text} - {search_results_number} {selected_category} item{'s' if search_results_number != 1 else ''} found"

    assert_that(context.details_page.product_id_label, equal_to(expected_title), "Expected product id in details page title : %s \n     Actual product id:%s " %(expected_title, context.details_page.product_id_label))
    assert_that(context.details_page.product_category_label, equal_to(selected_category),"Expected product category in details page title : %s \n     Actual product category:%s " % (selected_category, context.details_page.product_category_label))

@then("validate error message on details page contains: {error_content}")
def step_impl(context, error_content):
    error_message_content = context.details_page.get_too_much_data_error_message_content()
    assert_that(error_message_content, contains_string(error_content))

@then("validate error message on results page: {error_content}")
def step_impl(context, error_content):
    error_message_content = context.results_page.get_please_refine_search_tooltip_content()
    assert_that(error_message_content, equal_to(error_content))


@then("validate product all tabs names by API call in Details page")
def step_impl(context):
    """
    Compare the product tab name from UI with product tab name from API Call
    """
    context.details_page.update_product_tabs_by_api(context)
    tabs_names_from_API = context.details_page.product_tabs_names_by_api
    tabs_names_from_UI = context.details_page.get_product_tabs_names()
    assert_that(tabs_names_from_UI, equal_to(tabs_names_from_API))


@then("validate UI table with API data by {by}:{value} for tab:{tab_index}")
def step_impl(context, by, value, tab_index):
    context.details_page.load_page_details()
    ui_content = context.details_page.read_ui_table("API", tab_index)
    source_content = context.details_page.get_tab_data_by_API(context, by, value)
    assert_that(len(ui_content[1]), equal_to(len(source_content)))  # Equal number of rows between UI table and source_content
    all_rows_exist = JsonFileHandler.all_rows_exist_in_resource_file(source_content, ui_content[1])
    if all_rows_exist != True:
            summary = f"\nRows that unique to UI:\n" + ExcelHandler.stringify_for_print(all_rows_exist)
            raise Exception(summary)


@then("Validate Last Update by API in Details page")
def step_impl(context):
    """
     Enable data freshness check Test Pass if Data freshness is at least last 24 hrs:
     last_update_date from API == current_date(today_date) == last_update_date from UI
    """
    last_update_UI = context.details_page.get_last_update_from_UI()
    last_update_API = context.details_page.get_last_update_from_API(context)
    today_date = context.details_page.get_current_date()
    assert_that(last_update_UI[0], equal_to(last_update_API[0]), "Expected last update date in details page : %s \n     Actual last update date:%s " %(last_update_API[0], last_update_UI[0]))
    assert_that(last_update_API[0], equal_to(today_date),  "Expected last update date by API : %s \n     Actual last update date by API :%s " %(today_date, last_update_API[0]))