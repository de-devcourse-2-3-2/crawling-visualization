from unittest import TestCase
from ..main.scraping import codishop_scraping as cs


class CodiShopTest(TestCase):
    # def setUp(self):
    #     cs.set_driver_and_soup(crawling_page_url, driver)
    def test_codishop_main(self):
        cs.main_page_crawling()
        # self.fail()