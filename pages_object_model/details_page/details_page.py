from pages_object_model.details_page.details_page_locators import DetailsPageLocators
from web_source.base_web_page import BaseWebPage
from utils_API.traceit_api import TraceitApi
import time
from functools import reduce
import re
import datetime


class DetailsPage(BaseWebPage):
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
        self.product_id_label = ""
        self.product_name_label = ""
        self.product_category_label = ""
        self.selected_product_tab = ""
        self.product_tabs_names_by_api = None
        self.product_tabs_id_by_api = None


    def load_page_details(self):
        """
        get all page details - title : product_id, product_name, product_category and which tab is selected(open)
        """
        self.product_id_label = self.wait_to_be_displayed(*DetailsPageLocators.product_id_label)[0].text
        self.product_name_label = self.wait_to_be_displayed(*DetailsPageLocators.product_name_label)[0].text if self.is_element_visible(*DetailsPageLocators.product_name_label) else ""
        self.product_category_label = self.wait_to_be_displayed(*DetailsPageLocators.product_category_label)[0].text
        self.selected_product_tab = self.wait_to_be_displayed(*DetailsPageLocators.selected_product_tab)[0].text

    def get_number_of_product_tabs(self):
        all_product_tabs = self.wait_to_be_displayed(*DetailsPageLocators.all_product_tabs)
        return len(all_product_tabs)

    def open_product_tab(self, index = None, tab_name = None):
        """
        open product tab by name or by index (first tab, second tab,...)
        :param index: Which tab  to open (first tab, second tab,...)
        :param tab_name: Which tab name to open
        """
        if index != None:
            all_product_tabs = self.wait_to_be_displayed(*DetailsPageLocators.all_product_tabs)
            if index < 0 or index >= len(all_product_tabs):
                raise Exception("Tab number not exist")
            else:
                all_product_tabs[index].click()
        else:
            self.wait_and_click_on_element(*DetailsPageLocators.tab_by_name(tab_name))

    def get_all_table_titles(self, tab_index):
        """
        :Returns:
        - list of string - all table titles
        """
        find_all_titels = False
        index = 0
        titles_list = []
        titles_list_len = 0
        while not find_all_titels:
            table_title = self.wait_to_be_displayed(*DetailsPageLocators.table_titles)
            for elem in table_title:
                if elem.text != '':
                    if elem.text not in titles_list:
                        titles_list.append(elem.text)
                        index = index + elem.size['width']
                # else:
                #     index = index + 100
            self.scroll_horizontal(index, tab_index)
            if len(titles_list) > titles_list_len:
                titles_list_len = len(titles_list)
            else:
                find_all_titels = True
        self.scroll_horizontal(0, tab_index)
        return titles_list

    def get_columns_by_row_index_from_table(self, table_titles, row_index, source=None, tab_index=0):
        """
        :param table_titles: list of titles
        :param row_index: Which row is in the table
        :return: all row cells as dictionary : Key = column title , value = cell value
        """
        row_end = False
        cell_dict = {}
        index = 0
        while not row_end:  # this loop goes over all columns in a row
            try:
                time.sleep(0.1)
                visible_colums_in_row = self.wait_to_be_displayed(*DetailsPageLocators.table_row_cells(row_index))
                for row in visible_colums_in_row:  # this loop goes over all visible columns in a row
                    try:
                        col_id = row.get_attribute("col-id")
                        key = self.update_title_column_as_key(table_titles, col_id, source)  # Match the title (key) to what appears in the source file
                        if key not in cell_dict:
                            if row.size['width'] > 0:  # column not empty
                                cell_dict[key] = row.text
                                index = index + row.size['width']  # use to scroll horizontal
                    except:
                        break
                if len(cell_dict) == len(table_titles): # if row end: We went through all the columns in the row
                    row_end = True
                else:
                    self.scroll_horizontal(index, tab_index)
            except:  # invisible row was received
                cell_dict = {}
                row_end = True
        return cell_dict

    def get_index_of_last_visible_row(self, current_index, locator, attribute):
        """
        :param current_index: current table row index
        Returns: the index of last visible row in table
        """
        if current_index > 0:
            self.scroll_to_element(*locator)
            time.sleep(0.10)
        last_row_index = max(list(map(lambda x: int(x.get_attribute(attribute)), self.wait_to_be_displayed(*DetailsPageLocators.table_rows))))
        return last_row_index

    def get_all_table_row(self, source=None, tab_index=0):
        """
        :return: A tuple with two items
            list of table titles
            list of Dictionaries -Each item in the list represents a row from the table
        """
        rows_list = []
        update_all_rows = False
        index = -1
        self.zoom(0.25)
        table_titles = self.get_all_table_titles(tab_index)
        last_row_index = self.get_index_of_last_visible_row(index, None, "row-id")
        while not update_all_rows:
            index = index + 1
            if index <= max(list(map(lambda x: int(x.get_attribute("row-index")), self.wait_to_be_displayed(*DetailsPageLocators.table_rows)))) and index <= last_row_index:
                cells_list = self.get_columns_by_row_index_from_table(table_titles, index, source, tab_index)
                self.scroll_horizontal(0, tab_index)
                if cells_list not in rows_list and len(cells_list) > 0:
                    rows_list.append(cells_list)
            else:
                index = index - 1
                last_row_index = self.get_index_of_last_visible_row(index, DetailsPageLocators.table_row_cells(index), "row-id")
                if max(list(map(lambda x: int(x.get_attribute("row-index")), self.wait_to_be_displayed(*DetailsPageLocators.table_rows)))) == index:
                    update_all_rows = True
        self.zoom(1)
        return table_titles, rows_list

    def get_column_by_name(self, current_index, coulmn_name):
        row_end = False
        current_index = str(current_index)
        cell = ''
        index = 0
        while not row_end:
            rows_index_and_id =  list(map(lambda elem:(elem.get_attribute('row-index'),elem.get_attribute('row-id')),self.wait_to_be_displayed(*DetailsPageLocators.table_rows)))
            rows_id = list(map(lambda row: row[1] if row[0] == current_index else '', rows_index_and_id))
            row_index = list(dict.fromkeys(rows_id))
            if '' in row_index:
                row_index.remove('')
            row_columns = self.wait_to_be_displayed(*DetailsPageLocators.columns_locator(row_index[0]))
            all_columns = list(map(lambda elem: (elem.get_attribute("col-id"), elem.size['width'], elem), row_columns))
            column = list(filter(None, map(lambda elem: f"found_{elem[2].text}" if elem[0] == coulmn_name and elem[1] > 0 else False, all_columns)))
            if len(column) > 0:
                cell = column[0].strip("found_")
                row_end = True
            else:
                index = index + reduce(lambda x, y: x + y, list(map(lambda elem: elem[1], all_columns[:(len(all_columns) - 1)])))
                self.scroll_horizontal(index)
        return cell

    def get_all_column_cells_by_column_name(self, coulmn_name):
        coulmn_name = coulmn_name.replace(' ', '')
        rows_list = []
        update_all_rows = False
        index = -1
        last_row = self.get_index_of_last_visible_row(index, None, "row-index")
        while not update_all_rows:
            index = index + 1
            if index <= last_row:
                rows_list.append(self.get_column_by_name(index,coulmn_name))
            else:
                index = index - 1
                last_row = self.get_index_of_last_visible_row(index, DetailsPageLocators.cell_by_column_name(index, coulmn_name), "row-index")
                if last_row == index:
                    update_all_rows = True
        return rows_list

    def search_filter_by_text(self,search_text):
        search_filter_input = self.wait_to_be_visible(*DetailsPageLocators.search_filter)
        search_filter_input[0].send_keys(search_text)

    def click_on_Export_button(self):
        self.wait_and_click_on_element(*DetailsPageLocators.Export_button)

    def click_to_sort_column(self, coulmn_name):
        self.zoom(0.25)
        self.web_driver.execute_script("arguments[0].click();", self.wait_to_be_visible(*DetailsPageLocators.column_to_sort(coulmn_name))[0])
        self.zoom(1)

    def read_ui_table(self, source, tab_index=0):
        """
        :return: A matrix with the data from the UI with the headers
        """
        titles, table_row_dicts = self.get_all_table_row(source, tab_index)
        ui_table = [titles]
        if source == "export":
            # Convert the table_row_dicts (dictionary) to list - using in validation with CSV file
            for table_row_dict in table_row_dicts:
                table_row_list = list(map(lambda title: table_row_dict[title.replace(' ', '')], titles))
                ui_table.append(table_row_list)
        else:
            ui_table.append(table_row_dicts)
        return ui_table

    def get_selected_tab_index(self):
        """
        :return: A Number representing the index of the selected tab, the first tab is 0,
        """
        all_product_tabs = self.wait_to_be_displayed(*DetailsPageLocators.all_product_tabs)
        all_product_tabs = list(map(lambda product_tab_element: product_tab_element.text, all_product_tabs))
        return all_product_tabs.index(self.selected_product_tab)

    def click_on_share_button(self):
        self.wait_and_click_on_element(*DetailsPageLocators.share_button)

    def table_rows_count(self):
        """
        :return: A Number of rows in the table
        """
        update_all_rows = False
        index = -1
        self.zoom(0.25)
        last_row_index = self.get_index_of_last_visible_row(index, None, "row-id")
        while not update_all_rows:
            index = last_row_index
            last_row_index = self.get_index_of_last_visible_row(index, DetailsPageLocators.table_row_cells(index), "row-id")
            if max(list(map(lambda x: int(x.get_attribute("row-index")),self.wait_to_be_displayed(*DetailsPageLocators.table_rows)))) == index:
                update_all_rows = True
        self.zoom(1)
        return last_row_index + 1

    def update_title_column_as_key(self,table_titles, col_id, source=None):
        """

        :param table_titles: list of table titles
        :param col_id: column id
        :param source:  source to validate: Export -  Match the title to what appears in the CSV file / else: Match the title to what appears in the Resource file
        :return: key = column title as matching string
        """
        if source:  #Resource
            key = col_id
        else:
            #CSV
            lower_titles = list(map(lambda item: ("".join(item.split())).lower(), table_titles))
            if col_id.lower() in lower_titles:
                key = table_titles[lower_titles.index(col_id.lower())]
        return key

    def get_too_much_data_error_message_content(self):
        error_message_elements = self.wait_to_be_displayed(*DetailsPageLocators.too_much_data_error)
        error_message_content = list(map(lambda err_msg_element:err_msg_element.text, filter(lambda err_msg_element: len(err_msg_element.text) > 0, error_message_elements)))[0]
        _RE_COMBINE_WHITESPACE = re.compile(r"\s+")
        error_message_content = _RE_COMBINE_WHITESPACE.sub(" ", error_message_content).strip()
        return error_message_content

    def get_rows_number(self, tab_number=0):
        table_titles = self.get_all_table_titles(tab_number)
        return len(self.get_all_column_cells_by_column_name(table_titles[0]))

    def get_product_tabs_names(self):
        """
        get all tabs names from UI
        :return:
        """
        all_product_tabs = self.wait_to_be_displayed(*DetailsPageLocators.all_product_tabs)
        all_product_tabs = [tab.get_attribute("textContent").strip() for tab in all_product_tabs]
        return [tab.upper() for tab in all_product_tabs]

    def update_product_tabs_by_api(self, context):
        """
        API call to get all tabs names and tabs ids
        tabs names -saved in self.product_tabs_names_by_api
        tabs ids - saved in self.product_tabs_id_by_api ( will be used for API call to get the table data)
        """
        token = context.common_page.get_token_from_swiss_login()
        api_call = TraceitApi(token, context.config.userdata['environment'])
        self.product_tabs_names_by_api, self.product_tabs_id_by_api  = api_call.get_all_category_tabs_by_API(context.product_selection.product_category)

    def get_tab_data_by_API(self, context, by, value):
        token = context.common_page.get_token_from_swiss_login()
        api_call = TraceitApi(token, context.config.userdata['environment'])
        if by == 'tab_index':
            tab_id = self.product_tabs_id_by_api[int(value)]
            res = api_call.get_table_by_tab_id(tab_id, self.product_id_label)
        else:
            res = api_call.get_table_for_catts_category(value, self.product_id_label, context.config.userdata['environment'])
        [dict.update({k: ""}) for dict in res for k, v in dict.items() if dict[k] == None]
        [dict.update({k: v.replace("    ", " ")}) for dict in res for k, v in dict.items()]
        [dict.update({k: v.replace("  ", " ")}) for dict in res for k, v in dict.items()]
        return res

    def get_last_update_from_UI(self):
        last_update = self.wait_to_be_displayed(*DetailsPageLocators.last_update_label)
        last_update = last_update[0].text.strip().split(', ')
        last_update[0] = last_update[0].strip('Last Update: ')
        return last_update

    def get_last_update_from_API(self, context):
        token = context.common_page.get_token_from_swiss_login()
        api_call = TraceitApi(token, context.config.userdata['environment'])
        res = api_call.get_last_update_by_API()
        date_str = res[0]['LastUpdate'].split('T')
        date_str[0] = datetime.datetime.strptime(date_str[0], '%Y-%m-%d').strftime('%m-%d-%Y')
        return date_str

    def get_current_date(self):
        today = datetime.date.today()
        return today.strftime('%m-%d-%Y')



