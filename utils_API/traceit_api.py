from utils_API.api_handler import ApiHandler


class TraceitApi:

    def __init__(self,token, env):
        env = "-dev" if env== 'DEV' else ''
        self.base_api_url = f"https://traceitapi{env}.swiss.intel.com/v2/"
        self.api_call = ApiHandler(self.base_api_url, token)

    def get_all_category_tabs_by_API(self, category):
        """
        implementation API call to get all tabs by category
        :param category:- product category
        :return: 2 lists : 1- tabs names 2- tabs ids
        """
        url = f"categories/{category}/reports"
        tabs = self.api_call.get_api_response(url)
        return [tab['report_description'].upper() for tab in tabs],[tab['report_id'] for tab in tabs]

    def get_last_update_by_API(self):
        """
        implementation API call to get last update
        :return: last update
        """
        url = "last_update"
        return self.api_call.get_api_response(url)

    def get_table_by_tab_id(self, tab_id, product_id):
        """
        implementation API call to get table by tab id
        :param tab_id: product tab id
        :return: list of Dictionaries -represents the table data
        """
        url = f"reports/{tab_id}?id={product_id}"
        return self.api_call.get_api_response(url)

    def get_table_for_catts_category(self, category, product_id, env):
        """
        implementation API call to get table for catts_category by category
        :param category: catts category (Visual ID or lot)
        :return: list of Dictionaries -represents the table data
        """
        env = "-dev" if env == 'DEV' else ''
        self.api_call.set_base_api_url(f"https://traceit{env}.swiss.intel.com/api/v1/catts/")
        url = f"{category}?id={product_id}"
        res= self.api_call.get_api_response(url)
        return res["rows"]

