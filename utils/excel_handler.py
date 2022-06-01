import csv
import glob
import os
from copy import deepcopy,copy
from pathlib import Path
import datetime 


class ExcelHandler:
    user = None

    @classmethod
    def find_csv_file_by_tab_name(cls, tab_name):
        """
        :return: A tuple with two strings :
            file_path - A string path to the csv file
            file_name - A string file_name it was looking for
        :raise: FileNotFoundError - if a file with the specified tab name is not found
        """
        
        tab_name = tab_name.title().replace('->', '-_')
        csv_file_pattern = f'TraceIT_{tab_name}_*.csv'
        list_of_csvs = glob.glob(str(Path(f"C:/Users/{cls.user}/Downloads/{csv_file_pattern}")))
        if not list_of_csvs:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), csv_file_pattern)
    
        latest_csv_file_path = max(list_of_csvs, key=os.path.getctime)
        datetime_obj = datetime.datetime.fromtimestamp(os.path.getctime(latest_csv_file_path))
        latest_csv_date = datetime_obj.strftime("%m-%d-%Y")
        latest_csv_time = datetime_obj.strftime("%I-%M%p")
        if latest_csv_time[0] == '0':
            latest_csv_time = latest_csv_time[1:]
    
        file_name = f"TraceIT_{tab_name}_{latest_csv_date}, {latest_csv_time}.csv"
        file_path = str(Path(f"C:/Users/{cls.user}/Downloads/{file_name}"))
        if not cls._is_file_exist(file_path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_name)
    
        return file_path, file_name


    @classmethod
    def find_csv_file_by_product_id_and_tab_number(cls, product_id, tab_index):
        """
        :param product_name: A string name of the product
        :param tab_index: A Number representing the index of tab, the first tab is 0
        :return: A tuple with two strings :
            file_path - A string path to the csv file, or None if not found
            file_name - A string file_name it was looking for
        """
        file_name = f"{product_id}_tab_{tab_index}.csv"
        # file_path = str(Path(f"C:/Users/{cls.user}/PycharmProjects/traceit-e2e-tests/resources/{file_name}"))
        file_path = str(os.path.join(os.getcwd(),'resources',file_name))
        if not cls._is_file_exist(file_path):
            file_path = None
        return file_path, file_name

    @classmethod
    def read_from_csv(cls, file_path):
        """
        :param file_path: A string representing the path
        :return: A matrix with the data from csv with the headers
        """
        with open(file_path, mode='r', encoding='utf-8-sig') as csv_file:
            csv_reader = csv.reader(csv_file)
            return list(csv_reader)

    @classmethod
    def diff(cls, csv_mat, ui_mat):
        """
        :param csv_mat: a matrix representing the csv table
        :param ui_mat: a matrix representing the ui table
        :return: A tuple with two list, each list contains tuples representing unique rows, the first to the csv and the second to the ui
        """
        first_set = set(map(tuple, csv_mat))
        secnd_set = set(map(tuple, ui_mat))
        csv_unique_rows = list(first_set.difference(secnd_set))
        ui_unique_rows = list(secnd_set.difference(first_set))
        return csv_unique_rows, ui_unique_rows

    @classmethod
    def stringify_for_print(cls, mat):
        """
        :param mat: a matrix
        :return: A string version of the matrix ready for print
        """
        return "\n".join(map(lambda row: f"[{row}]", map(",".join, mat)))

    @classmethod
    def delete_traceIt_csv_files_from_downloads(cls):
        files = glob.glob(str(Path(f"C:/Users/{cls.user}/Downloads/TraceIT_*.csv")))
        for f in files:
            os.remove(f)

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
    def clean_spaces(cls, csv_mat):
        csv_copy = deepcopy(csv_mat)
        for row in csv_copy:
            row[:] = [col.replace(" ", "") for col in row]
        return csv_copy
