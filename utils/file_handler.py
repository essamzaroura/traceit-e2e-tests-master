from datetime import datetime
import pandas as pd
import re
import numpy as np

class FileHandler(object):
    file_name = None
    file = None
    headers = None
    rows_number = None
    columns_number = None

    def read_excel(self, file_name, sheet_name=0):  # sheet_name = 0 for the first sheet
        return pd.read_excel(file_name, sheet_name=sheet_name, encoding='utf-8', keep_default_na=False)

    def convert_file_to_dictionary(self):
        object_dict = {}
        self.file = self.file.replace({'NULL': None})
        self.file = self.file.replace({'None': None})
        for row_number in range(self.rows_number):
            row_dict = {}
            for column in range(self.columns_number):
                header_name = self.headers[column]
                header_key = re.sub(" ", "", header_name)
                header_key = self.first_char_lower(header_key.replace("(", "").replace(")", ""))
                value = self.file[header_name][row_number]
                dict_value = self.convert_to_valid_value(value)
                row_dict.update({header_key: dict_value})

            object_dict.update({row_number: row_dict})

        return object_dict

    def first_char_lower(self, string):
        if len(string):
            return string[0].lower() + string[1:]
        else:
            return string

    def convert_to_valid_value(self, value):
        value_type = type(value)
        if value_type == pd._libs.tslib.Timestamp:
            return str(datetime.combine(value, datetime.min.time()))
        return value
