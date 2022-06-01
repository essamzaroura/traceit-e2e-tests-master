from pages_object_model.common_page.common_page import CommonPage
from pages_object_model.home_page.home_page import HomePage
from pages_object_model.results_page.results_page import ResultsPage
from pages_object_model.details_page.details_page import DetailsPage
from utils.allure_utils import attach_png
from utils.excel_handler import ExcelHandler
from web_source.web_factory import get_web


class URL(object):
    DEV="https://traceit-dev.swiss.intel.com/"
    PROD="https://traceit.swiss.intel.com/"

def before_all(context):
    url=URL.PROD if context.config.userdata['environment']=='Prod' else URL.DEV
    context.web=get_web(context.config.userdata['browser'],url=url)
    print("Trace IT on Env: %s ,with user: %s " %(context.config.userdata['environment'], context.config.userdata['user']))
    context.web.open()

    context.common_page = CommonPage(context.web.web_driver,url)
    context.home_page = HomePage(context.web.web_driver,url)
    context.results_page = ResultsPage(context.web.web_driver, url)
    context.details_page = DetailsPage(context.web.web_driver, url)
    ExcelHandler.user = context.config.userdata['user']

def after_scenario(context, scenario):
    context.common_page.navigate_to_home_page()
    context.common_page.refresh()

def after_all(context):
    print("after_all_tests")
    context.web.quit()
    # context.web.close()

def before_step(context,step):
    if step.step_type == 'when':
        attach_png((context.web.web_driver).get_screenshot_as_png(),step)
    if step.name == 'user click on Export button':
        #To ensure we read the latest csv
        ExcelHandler.delete_traceIt_csv_files_from_downloads()

def after_step(context,step):
    if step.step_type == 'when' or step.step_type == 'then':
        attach_png((context.web.web_driver).get_screenshot_as_png(),step)