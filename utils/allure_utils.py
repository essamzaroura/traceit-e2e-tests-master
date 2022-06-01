import allure
from allure_commons._allure import attach
from allure_commons.types import AttachmentType

# def attach_json(data, attachment_name="json attachment"):
#     allure.attach(data, attachment_name, AttachmentType.JSON)
#
def attach_text(text, attachment_name="text attachment"):
    attach(text, name="SQL Query Result:", attachment_type=AttachmentType.TEXT)

def attach_png(png, attachment_name="image attachment"):
    attach(png,name="Screenshot",attachment_type=AttachmentType.PNG)

# behave -f allure_behave.formatter:AllureFormatter -o allure-behave ./features
# allure serve allure-behave
# or
# allure generate allure-behave
# allure open allure-report
