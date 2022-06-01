from behave import when


@when('user {checked} checkbox:{category} category to filter')
def step_impl(context, checked, category):
    context.results_page.find_count_of_results()  #Waiting for the page to load with all results
    context.results_page.checked_checkbox_category_to_filter(category, checked)
    context.results_page.find_count_of_results()  #Waiting for the page to reload with all results after filter

@when("user select and click on search result item with {by}:{item_name}")
def step_impl(context, item_name, by):
    """
    :param item_name: A string that is a product_name or product_id
    :param by: A string like 'product_id' or 'product_name' correspond to the type of the item_detail
    """
    context.product_selection = context.results_page.find_and_click_on_item_result(item_name, by)

@when("user click Show Results as a Table")
def step_impl(context):
    context.results_page.click_show_results_as_a_table()