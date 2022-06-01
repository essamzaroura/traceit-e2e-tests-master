from behave import when
from pages_object_model.common_page.product_selection import ProductSelection

@when('user Choose {search_Categories} Category by DropDown')
def step_impl(context, search_Categories):
    context.home_page.Choose_search_Categories_by_DropDown(search_Categories)
    context.home_page.current_selected_category = search_Categories

@when('user Typing: {search_text} in the search TextField')
def step_impl(context, search_text):
    context.home_page.Search_trace_IT_by_text(search_text)
    context.home_page.current_search_text = search_text

@when('user select suggest search Dropbox index: {index:d}')
def step_impl(context, index):
    context.product_selection = context.home_page.select_suggest_search_Dropbox_by_index(index)


@when('user click on search icon button')
def step_impl(context):
    if context.home_page.current_selected_category in ("Visual ID", "Lot"):
        context.product_selection = ProductSelection(product_id=context.home_page.current_search_text, product_name="",
                                                     product_category=context.home_page.current_selected_category)
    context.home_page.click_on_search_icon_button()


@when('user clear the search TextField')
def step_impl(context):
    context.home_page.clear_search_trace_IT_text_box()

@when('user click View All Results')
def step_impl(context):
    context.home_page.click_View_All_Results()