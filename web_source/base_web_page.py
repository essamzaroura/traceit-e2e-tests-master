from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from utils.allure_utils import attach_text

class BaseWebPage(object):
    TIMEOUT_Web_Driver = 10
    TIMEOUT_Web_Element = 6   

    def __init__(self, web_driver, base_url):
        self.web_driver_wait = WebDriverWait(web_driver, BaseWebPage.TIMEOUT_Web_Driver)
        self.web_driver = web_driver
        self.base_url = base_url

    def open(self, url=None):
        if url is None:
            url = self.base_url
        self.web_driver.implicitly_wait(5)
        self.web_driver.maximize_window()
        self.web_driver.get(url)

    def open_ext(self,url):
        url = self.base_url + url
        attach_text("%s" % url, 'url')
        self.web_driver.get(url)

    def close(self):
        self.web_driver.close()
        # print("Tests completed - Close browsre ")

    def quit(self):
        self.web_driver.quit()
        print("Tests completed - Quit browsre ")

    #// All function in base page web
    def go_back(self):
        self.web_driver.back()
        time.sleep(0.25)

    def get_title(self):
        return self.web_driver.title

    def get_url(self):
        return self.web_driver.current_url

    def hover(self, *locator):
        element = self. wait_to_be_displayed(*locator)
        hover = ActionChains(self.web_driver).move_to_element(element[0])
        hover.perform()

    def switch_to_new_window(self):
        self.web_driver.switch_to.window(self.web_driver.window_handles[1])

    def refresh(self):
        self.web_driver.refresh()

    def find_element(self, *locator):
        try:
            return self.web_driver.find_element(*locator)
        except:
            raise NoSuchElementException("%s- Element not found, Locator: %s" % (self.__class__.__name__, locator[1])) from Exception

    def find_elements(self, *locator):
        try:
            return self.web_driver.find_elements(*locator)
        except:
            raise NoSuchElementException("%s- Element not found, Locator: %s" % (self.__class__.__name__, locator[1])) from Exception

    def find_elements_by_xpath(self, xpath):
        return self.find_elements(By.XPATH, xpath)

    def wait_and_click_on_alert_accept(self):
        try:
            # wait until alert is present
            element = WebDriverWait(self.web_driver, BaseWebPage.TIMEOUT_Web_Element).until(EC.alert_is_present())
            return True
        finally:
            return False

    def wait_and_click_on_element(self,*locator):
        try:
           element = WebDriverWait(self.web_driver, BaseWebPage.TIMEOUT_Web_Element).until(EC.element_to_be_clickable((locator)))
           try:
            element.click()
           except:
               raise TimeoutException(
                   "%s- failed to click on Element, Locator: %s " % (self.__class__.__name__, locator[1])) from Exception
        except:
            raise TimeoutException("%s- Element not found, Locator: %s " % (self.__class__.__name__, locator[1])) from Exception

    def wait_to_be_visible(self, *locator):
        try:
            element = WebDriverWait(self.web_driver, BaseWebPage.TIMEOUT_Web_Element).until(EC.visibility_of_all_elements_located(locator))
            return element
        except:
            raise TimeoutException("%s- Element not found, Locator: %s " % (self.__class__.__name__, locator[1])) from Exception

    def wait_to_be_displayed(self, *locator):
        try:
            element = WebDriverWait(self.web_driver, BaseWebPage.TIMEOUT_Web_Element).until(EC.presence_of_all_elements_located(locator))
            return element
        except:
            raise TimeoutException(
                "%s- Element not found, Locator: %s " % (self.__class__.__name__, locator[1])) from Exception

    def wait_for_element_be_invisible(self, *locator):
        try:
            element = WebDriverWait(self.web_driver, BaseWebPage.TIMEOUT_Web_Element).until(EC.invisibility_of_element_located(locator))
            return element
        except:
            return False

    def click_on_scrollbar_until_element_seen(self,scrollBar_locator,element_locator):
        if (len(self.web_driver.find_elements(*element_locator))<1):
            self.click_on_scrollbar_right_Base(scrollBar_locator)

    def click_on_scrollbar_right_Base(self, scrollBar_locator):
        self.web_driver.find_element(*scrollBar_locator).click()

    def scroll_horizontal(self, index, scroll_index=0):
        res = f"document.getElementsByClassName('ag-body-horizontal-scroll-viewport')[{scroll_index}].scrollTo({index},0)"
        self.web_driver.execute_script(res)
        time.sleep(0.15)

    def scroll_to_element(self, *locator):
        element = self.wait_to_be_displayed(*locator)
        self.web_driver.execute_script("arguments[0].scrollIntoView();", element[0])

    def open_new_web_tab(self):
        self.web_driver.execute_script("window.open('');")

    def switch_to_main_window(self):
        self.web_driver.switch_to.window(self.web_driver.window_handles[0])

    def zoom(self,percent):
        self.open_new_web_tab()
        self.switch_to_new_window()
        self.open(url="chrome://settings/")
        self.web_driver.execute_script(f"chrome.settingsPrivate.setDefaultZoom({percent})")
        self.close()
        self.switch_to_main_window()
        time.sleep(0.15)

    def is_element_found(self, *locator):
        try:
            time.sleep(0.15)
            self.web_driver.find_element(*locator)
            return True
        except:
            return False

    def find_element_by_xpath(self, xpath):
        return self.find_element(By.XPATH, xpath)
    
    def scroll_until_element_seen(self,All_locators,element):
        find_elem = None
        list_len = 0
        while not find_elem:
            try:
                find_elem = WebDriverWait(self.web_driver, BaseWebPage.TIMEOUT_Web_Element).until(EC.presence_of_element_located(element))
                return True
            except TimeoutException:
                self.web_driver.execute_script("arguments[0].scrollIntoView(true)",self.find_elements(*All_locators)[len(self.find_elements(*All_locators)) - 1])
                if len(self.find_elements(*All_locators)) != list_len:
                    list_len = len(self.find_elements(*All_locators))
                else:
                    return False

    def scroll_right_until_element_seen(self, row_width, element_locator):
        location = 0
        while location < row_width:
            try:
                return self.wait_to_be_displayed(*element_locator)
            except TimeoutException:
                location = location + 300
                self.scroll_horizontal(location)
        return self.wait_to_be_displayed(*element_locator)
        
    def is_element_visible(self, *locator):
        try:
            self.wait_to_be_visible(*locator)
            return True
        except TimeoutException:
            return False
