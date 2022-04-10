from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Wait2Load:
    def __init__(self, url):
        self.url = url

    def page_source(self, class_name, ext):
        """A function to wait for the website to load until the class_name taken as an argument.

        This function includes selenium headless mode. To use this you should have a web driver which is fit with
        exist selenium.

        :param class_name: Class_name for waiting until it downloads to website
        :param ext: Extension for website which will be process
        :return: page_source
        """
        headless_options = Options()
        headless_options.add_argument('--headless')

        driver = webdriver.Chrome(options=headless_options)
        driver.get(self.url + ext)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))

        return driver.page_source
