from behave import *
from hamcrest import *

from utils.allure_utils import attach_text

# from features_new.steps.comdata_steps import card_add_event_amount, authorized_event_amount, post_with_pre_amount


@then("user switch between tabs and validate the table in each tab with API data by: {by}")
def step_impl(context, by):
    """
    Execute 2 steps:
       1- sweich to tab by tab index
       2- compare between UI table with API data - API call by 'category' for CATTS  categories  or by 'tab index(to get report id) for the rest of the categories
    :param by: "tab_index" for all categories except 'Visual ID' and 'Lot' categories: "category"
    """
    all_tabs = range(context.details_page.get_number_of_product_tabs())
    for tab in all_tabs:
        value = tab if by == "tab_index" else context.product_selection.product_category.replace(" ", "-").lower()
        context.execute_steps(u"""
            When user switch to tab:{tab_number}
            Then validate UI table with API data by {by}:{value} for tab:{tab_index}
            """.format(tab_number=tab, by=by, value=value, tab_index=tab))

@then("user go back and selects a product from each category and validate the results in each tab")
def step_impl(context):
    for row in context.table:
        attach_text("Starting test for Category: %s" %(row["category"]))
        context.execute_steps(u"""
            When user go back and Search for:{text}
            When user {checked} checkbox:{category} category to filter
            Then validate Search Results found:{number} results in:{all} Categories
            When user select and click on search result item with product_id:{item_code}
            Then validate details page opens and contains the product id:{item_code} and product name:{product_name} and product_category:{category} in the title
            Then validate product all tabs names by API call in Details page
            Then user switch between tabs and validate the table in each tab with API data by: tab_index
            """.format(text=row["text to search"], checked=row["checked"], category=row["category"], number=row["results number"], all='1',
                       item_code=row["Item Code"], product_name=row["product_name"], product_id=row["Item Code"],
                       product_category=row["category"]))


@when("user go back and Search for:{text}")
def step_impl(context, text):
        context.execute_steps(u"""
            When user click to go Back
            When user clear the search TextField
            When user Typing: {text} in the search TextField
            When user click on search icon button
            """.format(text=text))

@when("user iterate over results and count rows in each tab")
def step_impl(context):
    context.search_results_tabs_sums = dict()
    count_found_results_UI = int(context.results_page.find_count_of_results()[0].text.split(' ')[0])
    for results_page_item_index in range(count_found_results_UI):
        results_page_item = context.results_page.get_nth_result(results_page_item_index)
        results_page_item.click()
        all_tabs = range(context.details_page.get_number_of_product_tabs())

        for tab_number in all_tabs:
            if tab_number not in context.search_results_tabs_sums:
                context.search_results_tabs_sums[tab_number] = 0

            context.execute_steps(u"""
                When user switch to tab:{tab_number}
                """.format(tab_number=tab_number))

            context.search_results_tabs_sums[tab_number] += context.details_page.get_rows_number()

        context.execute_steps(u"""
            When user click to go Back
            """)

@then("validate number of rows in Details Page with number of rows from all results")
def step_impl(context):
    all_tabs = range(context.details_page.get_number_of_product_tabs())

    for tab_number in all_tabs:
        context.execute_steps(u"""
            When user switch to tab:{tab_number}
            """.format(tab_number=tab_number))

        actual_number_of_rows_in_tab = context.details_page.get_rows_number(tab_number)
        assert_that(context.search_results_tabs_sums[tab_number], equal_to(actual_number_of_rows_in_tab), f"In tab index {tab_number} to have {context.search_results_tabs_sums[tab_number]} results, but Actually {actual_number_of_rows_in_tab}")
