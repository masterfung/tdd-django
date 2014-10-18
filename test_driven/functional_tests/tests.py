__author__ = 'htm'
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_now_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Joe has heard about a cool new online to-do app. He goes
        # to check out its homepage
        self.browser.get(self.live_server_url)

        # He notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a To-Do item'
        )

        # He types "Buy peacock feathers" into a text box (Joe's hobby
        # is tying fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')

        # When he hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list table
        inputbox.send_keys(Keys.ENTER)
        joe_list_url = self.browser.current_url
        self.assertRegex(joe_list_url, '/lists/.+')
        self.check_for_now_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting him to add another item. He
        # enters "Peacock is the magic to all!" (Joe is very methodical)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Peacock is the magic to all!')
        inputbox.send_keys(Keys.ENTER)

        self.check_for_now_in_list_table('1: Buy peacock feathers')
        self.check_for_now_in_list_table('2: Peacock is the magic to all!')



        # The page updates again, and now shows both items on his list
        self.check_for_now_in_list_table('2: Peacock is the magic to all!')
        self.check_for_now_in_list_table('1: Buy peacock feathers')

        # All of a sudden, a new user, Jared appears on the site.

        ## We start a new browser session to make sure that no information from
        ## Joe's session is coming through via the cookies
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Jared visits the home page and did not see Joes's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('Peacock is the magic to all!', page_text)

        # Jared starts his own personal list by entering a new item.
        # He is an interesting man!
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Go to the gym!')
        inputbox.send_keys(Keys.ENTER)

        # Jared gets his own unique URL
        jared_list_url = self.browser.current_url
        self.assertRegex(jared_list_url, '/lists/.+')
        self.assertNotEqual(jared_list_url, joe_list_url)

        # Again, this only indicates that Joe's personal peacock
        # list does not exist!
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Go to the gym!', page_text)

    def test_layout_and_styling(self):
        # Joe arrives @ the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # He notices the input box is aligned centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )

        # He later starts a new list and sees the input is nicely
        # centered there as well
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )