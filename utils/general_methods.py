import json, re

def retry_if_assertion_error(exception):
    return isinstance(exception, AssertionError)

def retry_if_assertion_index_error(exception):
    return isinstance(exception, IndexError)

def retry_if_attribute_or_assertion_error(exception):
    return isinstance(exception, (AssertionError, AttributeError))

def retry_if_attribute_error(exception):
    return isinstance(exception, AttributeError)

def retry_if_index_error(exception):
    return isinstance(exception, IndexError)

# def retry_on_timeout_exception(exception):
#     return isinstance(exception, TimeoutException)
#
#
# def retry_if_not_found_in_list(exception):
#     return isinstance(exception, NotFoundInListException)
#
#
# def retry_if_payment_not_created(exception):
#     return isinstance(exception, PaymentNotCreatedException)
#
#
# def retry_if_attribute_value_wrong(exception):
#     return isinstance(exception, EntityAttributeNotFoundException)
#
#
# def retry_if_response_not_200(response):
#     return response.status_code != 200
#
#
# def retry_if_mongo_report_not_found(exception):
#     return isinstance(exception, MongoReportNotFoundException)
#
# def retry_if_response_error_exception(exception):
#     return isinstance(exception, ResponseErrorException)
#
# def retry_on_none(result):
#     return result is None

############################################

def get_json_from_file(file_name):
    with open(file_name) as data_file:
        return json.load(data_file)


