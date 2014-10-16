from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    def setup(self):
        self.browser = webdriver.Firefox()

    def tear_down(self):
        browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')

        self.assertIn('Awesome World!', self.browser.title)
        self.fail('Finished the test!')

if __name__ == '__main__':
    unittest.main(warnings='ignore')
