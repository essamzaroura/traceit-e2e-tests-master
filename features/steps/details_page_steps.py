from behave import *


@when("user Typing: {search_text} in the Search & Filter TextField")
def step_impl(context, search_text):
    context.details_page.search_filter_by_text(search_text)


@step("user click on Export button")
def step_impl(context):
    context.details_page.click_on_Export_button()


@when("user click to sort column:{coulmn_name}")
def step_impl(context, coulmn_name):
    context.details_page.click_to_sort_column(coulmn_name)

@step("user click the Share button")
def step_impl(context):
    context.details_page.click_on_share_button()


@when("user switch to tab:{tab_number}")
def step_impl(context, tab_number):
    context.details_page.open_product_tab(index=int(tab_number))