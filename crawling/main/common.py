from bs4 import BeautifulSoup
import logging, time
from datetime import date


def set_driver_and_soup(crawling_page_url, driver):
    driver.get(crawling_page_url)
    driver.implicitly_wait(60)
    time.sleep(0.5)  # delay time 설정
    logging.info("Main page crawling start. {}".format(crawling_page_url))
    return BeautifulSoup(driver.page_source, "html.parser")


def return_list_data(soup, tag_type, selector_path):
    try:
        tag_element_list = soup.find_all(tag_type, selector_path)
        return [tag_element.text for tag_element in tag_element_list]
    except:
        logging.error("oops, there's sth wrong within bs4 object, tag type or css selector path")


def add_at_columns(data_list):
    data_list.extend([date.today(), None, None])  #.strftime('%Y-%m-%d %H:%M:%S')
