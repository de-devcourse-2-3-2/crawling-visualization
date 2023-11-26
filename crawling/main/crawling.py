from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import re
import postgres_write as pw
from common import *


class Crawling:
    def __init__(self, target_link):
        """
        Initialize the Crawling class with the target link.

        Args:
        - target_link (str): The target link for crawling.
        """
        self.target_link = target_link

    def main_page_crawling_scrapping(self):
        """
        Perform crawling and scraping on the main page of the specified target link.
        """
        postgres = pw.DB_Write()
        postgres.tables_create()

        op = Options()
        op.add_argument('headless')
        op.add_argument('window-size=1920X1080')
        op.add_argument('headless')
        with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=op) as driver:
            main_page_url = f"https://www.musinsa.com/app/{self.target_link}/lists"
            soup = set_driver_and_soup(crawling_page_url=main_page_url, driver=driver)
            total_paging_num = int(soup.find("span", "totalPagingNum").text)

            for i in range(1, total_paging_num + 1):
                codi_page_url = f"https://www.musinsa.com/app/{self.target_link}/lists?page={i}"
                soup = set_driver_and_soup(crawling_page_url=codi_page_url, driver=driver)
                codi_elements = soup.find_all("li", "style-list-item")

                for codi_element in codi_elements:
                    img_element = codi_element.select_one("div.style-list-item__thumbnail > a > div > img")
                    img_src = img_element.attrs["src"]

                    category_element = codi_element.select_one("div.style-list-information > a > span")
                    category = category_element.text if category_element.text else "아동복"

                    info_elements = codi_element.select_one("div.post-information").find_all("span")
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

                    codi_number_element = codi_element.select_one("div.style-list-item__thumbnail > a")
                    codi_number = re.sub(r'[^0-9]', '', str(codi_number_element.attrs["onclick"]))

                    subject = self.target_link + "-" + codi_number

                    tags, goods_detail_data = self.codi_page_crawling_scrapping(codi_number=codi_number, driver=driver)

                    style_data_list = [subject, when, category, season, views, img_src, tags]
                    logging.info("Style No.{} row- {}".format(codi_number, style_data_list))
                    style_id = postgres.insert_style_data(style_data_list)
                    goods_ids = postgres.insert_goods_data(goods_detail_data)
                    postgres.insert_style_goods(style_id, goods_ids)

    def codi_page_crawling_scrapping(self, codi_number, driver):
        """
        Perform crawling and scraping on the detailed page of the specified codi.

        Args:
        - codi_number (str): The codi number to be crawled.
        - driver: Selenium WebDriver instance.

        Returns:
        - tuple: Tags and goods detail data.
        """
        codi_page_url = f"https://www.musinsa.com/app/{self.target_link}/views/{codi_number}"
        soup = set_driver_and_soup(crawling_page_url=codi_page_url, driver=driver)

        tags = []
        tag_element_list = soup.find_all("a", "ui-tag-list__item")
        for tag_element in tag_element_list:
            tags.append(tag_element.text)
        tags = "".join(tags)

        brands = []
        brand_element_list = soup.find_all("a", "brand")
        for brand_element in brand_element_list:
            brands.append(brand_element.text)

        names = []
        name_element_list = soup.find_all("a", "brand_item")
        for name_element in name_element_list:
            names.append(name_element.text)

        prices = []
        del_prices = []
        price_element_list = soup.find_all("div", "price")
        for price_element in price_element_list:
            price_string = price_element.text
            price_string_list = price_string.split('원')
            price_string = price_string_list[0]
            price = int(re.sub(r'[^0-9]', '', price_string))
            prices.append(price)
            del_price = None
            if len(price_string_list) > 2:
                del_price_string = price_string_list[1]
                del_price = int(re.sub(r'[^0-9]', '', del_price_string))
            del_prices.append(del_price)

        goods_detail_data = [(a, b, c, d) for a, b, c, d in zip(brands, names, prices, del_prices)]
        return tags, goods_detail_data