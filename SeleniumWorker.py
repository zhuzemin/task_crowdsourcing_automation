from selenium import webdriver
from PyQt5.QtCore import pyqtSignal, QThread
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
DEBUG = True

def debug(s):
    if DEBUG:
        print(s )

class SeleniumWorker(QThread):
    progress_update = pyqtSignal(int)  # 信号类型：int

    def __init__(self, parent=None):
        super().__init__(parent)
        KeywordList=None

    def run(self):
        self.DoWork()


    def DoWork(self):
        count=0
        options = webdriver.ChromeOptions()
        options.add_argument("user-data-dir=Chrome\\Application\\PortableProfile")  # Path to your chrome profile
        options.binary_location="Chrome\\Application\\chrome.exe"
        driver = webdriver.Chrome(options=options)
        #input=browser.find_element_by_css_selector("input.gLFyf.gsfi")
        for keyword in self.KeywordList:
            driver.get('https://www.google.com/search?q='+keyword)
            #main_window = driver.current_window_handle
            container=driver.find_elements_by_css_selector('div.bkWMgd')[-1]
            #driver.execute_script("arguments[0].setAttribute('class','vote-link up voted')", element)
            searchResultList=container.find_elements_by_css_selector('div.g')
            debug('len(searchResultList): '+str(len(searchResultList)))
            urlList=[]
            for searchResult in searchResultList:
                debug('searchResult.textContent: '+driver.execute_script("return arguments[0].textContent", searchResult))
                a=searchResult.find_element_by_css_selector('a')
                debug('a.href: '+driver.execute_script("return arguments[0].href", a))
                urlList.append(driver.execute_script("return arguments[0].href", a))
                #driver.switch_to.window(main_window)
            debug('urlList: '+','.join(urlList))

            #input.send_keys(keyword)
            self.progress_update.emit(count)
            count=count+1


    def Pause(self):
        self.pause



    def Terminate(self):
        self.terminate()