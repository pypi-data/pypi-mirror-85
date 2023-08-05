import unittest
import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# import Faker

default_hub_host = 'selenium-hub:4444'

def get_driver(browser, hub_host):
    if (browser == 'chrome'):
        options = webdriver.ChromeOptions()
        options.add_argument('window-size=1200x768')
        capabilities = DesiredCapabilities.CHROME.copy()
        driver = webdriver.Remote(
            command_executor="http://%s/wd/hub" % (hub_host),
            desired_capabilities=capabilities,
            options=options
        )

        return driver

    if (browser == 'firefox'):
        options = webdriver.FirefoxOptions()
        options.add_argument('-width=1920')
        options.add_argument('-height=1080')
        options.set_preference("geo.prompt.testing", True)
        options.set_preference("geo.prompt.testing.allow", False)
        capabilities = DesiredCapabilities.FIREFOX.copy()

        driver = webdriver.Remote(
            command_executor="http://%s/wd/hub" % (hub_host),
            desired_capabilities=capabilities,
            options=options
        )

        return driver

    raise ValueError('Browser not supported')


def get_hub_host(config):
    if 'hub_host' in config and config['hub_host'] is not None:
        return config['hub_host']

    return default_hub_host

class BaseTestCase(unittest.TestCase):
    def __init__(self, testname, config, environment, browser):
        super(BaseTestCase, self).__init__(testname)
        BaseTestCase.environment = environment
        BaseTestCase.config = config[environment]
        BaseTestCase.browser = browser

    @classmethod
    def setUpClass(cls):
        hub_host = get_hub_host(cls.config)
        cls.driver = get_driver(cls.browser, hub_host)
        cls.driver.get(cls.config['url'])

        # cls.faker = Faker(['es_MX', 'en_US'])

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def takeScreenshot(self, test_name):
        print(self.__class__.__name__)

    #     self.driver.get_screenshot_as_file();

    def generateExceptionReport(self, exception):
        driver = self.driver
        screenshot = driver.get_screenshot_as_base64()
        console_log = driver.get_log('browser')
        console_log_string = json.dumps(console_log)
        formatedException = '''
        <p class="lead">{0}</p>
        
        <h4>Browser Screenshot</h4>
        <img src="data:image/png;base64,{1}">
        
        <h5>Browser Console</h5>
        <code>{2}</code>
        '''.format(exception, screenshot, console_log_string)

        return formatedException
