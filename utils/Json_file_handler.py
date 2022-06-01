import csv
import glob
import os
from copy import deepcopy,copy
from pathlib import Path
import json


class JsonFileHandler:
    user = None

    @classmethod
    def read_from_file(cls,file_path):
        """
        :param file_path: A string representing the path
        :return: A list with the data from file
        """
        with open(file_path, encoding='utf8') as json_file:
            json_reader = json.load(json_file)
            return json_reader

    @classmethod
    def find_resource_file_by_product_id_and_tab_number(cls, product_id, tab_index):
        """
        :param product_id: A string id of the product
        :param tab_index: A Number representing the index of tab, the first tab is 0
        :return: A tuple with two strings :
            file_path - A string path to the source file, or None if not found
            file_name - A string file_name it was looking for
        """
        file_name = f"{product_id}_tab_{tab_index}"
        file_path = str(os.path.join(os.getcwd(),'resources',file_name))
        if not cls._is_file_exist(file_path):
            file_path = None
        return file_path, file_name

    @classmethod
    def _is_file_exist(cls, file_path):
        """
        :param file_path: A string representing a file system path
        :return: A Boolean True if specified path is exist otherwise returns False.
        """
        is_exist = True
        list_of_files = glob.glob(file_path)
        if not list_of_files:
            is_exist = False
        return is_exist


    @classmethod
    def all_rows_exist_in_resource_file(cls, source_data_list, ui_data_list):
        """
        :param source_data_list: a matrix representing the csv table
        :param ui_data_list: a matrix representing the ui table
        :return: True if all rows from UI table exist in source_data_list, else: return list of rows that not exist in source_data_list
        """
        rows_not_found_list = []
        for row in ui_data_list:
            is_exist = list(filter(None, [row == source_row for source_row in source_data_list]))
            if len(is_exist) == 0:
                not_shared_items = [{k: row[k] for k in row if k in source_row and row[k] != source_row[k]} for source_row in source_data_list]
                rows_not_found_list.append(not_shared_items) if len(not_shared_items[0])>0 else []
        if len(rows_not_found_list) > 0:
            return rows_not_found_list
        else:
            return True