from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import postgres_write as pw
from common import *


class Crawling:
    def __init__(self, top_url):
        """
        Initialize the Crawling class with the top URL.

        Args:
        - top_url (str): The top URL for crawling.
        """
        self.top_url = top_url

    def main_page_scraping(self, soup):
        """
        Extract information from the main page soup.

        Args:
        - soup: BeautifulSoup object for the main page.

        Returns:
        - Tuple: A tuple containing codi_number and style data list.
        """
        codies = soup.find_all("li", "style-list-item")

        for codi in codies:
            img_element = codi.select_one("div.style-list-item__thumbnail > a > div > img")
            img_src = img_element.attrs["src"]

            category_element = codi.select_one("div.style-list-information > a > span")
            category = category_element.text if category_element.text else "아동복"

            info_elements = codi.select_one("div.post-information").find_all("span")
            date_element, view_element = None, None

            if info_elements[0].text == 'N':
                date_element = info_elements[1]
                view_element = info_elements[2]
            else:
                date_element = info_elements[0]
                view_element = info_elements[1]

            dates = date_element.text.split('.')
            month = int(dates[1])
            when = date(int("20" + dates[0]), month, int(dates[2]))

            if 2 <= month <= 4:
                season = "spring"
            elif 5 <= month <= 8:
                season = "summer"
            elif 9 <= month <= 10:
                season = "fall"
            else:
                season = "winter"

            views = int(re.sub(r'[^0-9]', '', view_element.text))

            codi_number_element = codi.select_one("div.style-list-item__thumbnail > a")
            codi_number = re.sub(r'[^0-9]', '', str(codi_number_element.attrs["onclick"]))

            subject = "shop" + "-" + codi_number
            
            return codi_number, [subject, when, category, season, views, img_src]

    def scraping_goods_detail(self, soup):
        """
        Scrape details of goods from the soup of the detailed page.

        Args:
        - soup: BeautifulSoup object for the detailed page.

        Returns:
        - List: A list containing details of goods.
        """
        brands = return_list_data(soup, "a", "brand")
        names = return_list_data(soup, "a", "brand_item")

        prices, del_prices = [], []

        price_element_list = soup.find_all("div", "price")
        for price_element in price_element_list:
            price_string_list = price_element.text.split('원')  
            price_string = price_string_list[0]
            prices.append(int(re.sub(r'[^0-9]', '', price_string)))  

            del_price = None  
            if len(price_string_list) > 2:  
                del_price = int(re.sub(r'[^0-9]', '', price_string_list[1]))
            del_prices.append(del_price)

        goods_detail_data = [(a, b, c, d) for a, b, c, d in zip(brands, names, prices, del_prices)]
        logging.debug(goods_detail_data)
        return goods_detail_data

    def main_page_crawling(self):
        """
        Perform crawling on the main page.

        - Extracts information from each page and stores it in the database.
        """
        postgres = pw.DB_Write()
        postgres.tables_create()

        with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
            soup = set_driver_and_soup(crawling_page_url=self.top_url, driver=driver)
            total_pages_number = int(soup.find("span", "totalPagingNum").text)

            for i in range(1, total_pages_number + 1):
                soup = set_driver_and_soup(crawling_page_url=f"https://www.musinsa.com/app/codimap/lists?page={i}", driver=driver)
                codi_number, style_data_list = self.main_page_scraping(soup)

                soup = set_driver_and_soup(crawling_page_url=f"https://www.musinsa.com/app/styles/views/{codi_number}", driver=driver)
                tags = return_list_data(soup, "a", "ui-tag-list__item")
                style_data_list.append(" ".join(tags))
                logging.info("Style No.{} row- {}".format(codi_number, style_data_list))
                style_id = postgres.insert_style_data(style_data_list)

                goods_detail_data = self.scraping_goods_detail(soup)
                goods_ids = postgres.insert_goods_data(goods_detail_data)
                postgres.insert_style_goods(style_id, goods_ids)
