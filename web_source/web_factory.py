from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os.path
from web_source.base_web_page import BaseWebPage

def get_web(browser,url):
    if browser == "chrome":
        options = Options()
        options.binary_location = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--start-maximized")
        # options.add_argument("user-data-dir=C:\\Users\\sys_pearl3writer\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 2")
        # options.add_argument("--headless"from os) # Runs Chrome in headless mode.
        driver = webdriver.Chrome(chrome_options=options, executable_path=os.path.join(os.getcwd(), "bin", "chromedriver.exe"))
        driver.implicitly_wait(5)
        driver.maximize_window()
        return BaseWebPage(web_driver=driver, base_url=url)
        # return Web(webdriver.Chrome(executable_path=r'C:\\Projects-VSCode\\APT2\\checklist-e2e-tests\\bin\\chromedriver.exe',chrome_options=options))
