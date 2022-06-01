from behave import when
import time

@when('user click on Contact us in Common page')
def step_impl(context):
    context.common_page.click_menu_items_button()
    # context.common_page.click_Contact_us_button()


@when('user click to go Back')
def step_impl(context):
    context.web.go_back()


@when('user navigate by url to details page with term:{term} and category:{category}')
def step_impl(context, term, category):
    context.common_page.navigate_by_url_using_query_string(f"details?term={term}&category={category}")
