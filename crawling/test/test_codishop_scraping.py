from unittest import TestCase
from ..main.scraping import codishop_scraping as codishop


class Test(TestCase):
    def test_codishop_main(self):
        codishop.main_page_crawling()
        # self.fail()