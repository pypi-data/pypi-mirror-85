import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from testing.testcases import LiveTornadoTestCase
from testing.selenium_helper import SeleniumHelper


class CitationImportTest(LiveTornadoTestCase, SeleniumHelper):
    fixtures = [
        'initial_documenttemplates.json',
        'initial_styles.json'
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.base_url = cls.live_server_url
        driver_data = cls.get_drivers(1)
        cls.driver = driver_data["drivers"][0]
        cls.client = driver_data["clients"][0]
        cls.driver.implicitly_wait(driver_data["wait_time"])
        cls.wait_time = driver_data["wait_time"]

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        self.user = self.create_user(
            username='Yeti',
            email='yeti@snowman.com',
            passtext='otter1'
        )

    def test_import_on_bibliography_page(self):
        self.login_user(self.user, self.driver, self.client)
        self.driver.get(self.base_url + "/bibliography")
        self.driver.find_element_by_xpath(
            '//*[normalize-space()="Import from Database"]'
        ).click()
        self.driver.find_element(By.ID, "bibimport-enable-crossref").click()
        self.driver.find_element(By.ID, "bibimport-search-text").send_keys(
            "Money"
        )
        time.sleep(5)
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "button.api-import"
                )
            )
        ).click()
        self.assertEqual(
            len(self.driver.find_elements_by_css_selector(
                '.edit-bib.fw-link-text'
            )),
            1
        )

    def test_import_in_editor(self):
        self.login_user(self.user, self.driver, self.client)
        self.driver.get(self.base_url + "/")
        WebDriverWait(self.driver, self.wait_time).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    ".new_document button"
                )
            )
        ).click()
        WebDriverWait(self.driver, self.wait_time).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'editor-toolbar'))
        )
        self.driver.find_element(By.CSS_SELECTOR, ".article-body").click()
        self.driver.find_element_by_css_selector(
            'button[title="Cite"]'
        ).click()
        self.driver.find_element_by_xpath(
            '//*[normalize-space()="Import from database"]'
        ).click()
        self.driver.find_element(By.ID, "bibimport-enable-gesis").click()
        self.driver.find_element(By.ID, "bibimport-search-text").send_keys(
            "Fish"
        )
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "button.api-import"
                )
            )
        ).click()
        self.assertEqual(
            len(self.driver.find_elements_by_css_selector(
                'span.delete'
            )),
            1
        )
        self.driver.find_element_by_xpath(
            '//*[normalize-space()="Insert"]'
        ).click()
        self.assertEqual(
            len(self.driver.find_elements_by_css_selector(
                'span.citation'
            )),
            1
        )
        # Edit editor explicitly
        self.driver.get(self.base_url + "/")
        time.sleep(1)
