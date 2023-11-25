from bs4 import BeautifulSoup
import logging
import time
from datetime import date


def set_driver_and_soup(crawling_page_url, driver):
    """
    Set up the web driver and create a BeautifulSoup object for the given URL.

    Args:
    - crawling_page_url (str): The URL to be crawled.
    - driver: Selenium WebDriver instance.

    Returns:
    - BeautifulSoup: The BeautifulSoup object for the page.
    """
    driver.get(crawling_page_url)
    driver.implicitly_wait(60)
    time.sleep(0.5)
    logging.info("Main page crawling start. {}".format(crawling_page_url))
    return BeautifulSoup(driver.page_source, "html.parser")


def return_list_data(soup, tag_type, selector_path):
    """
    Extract text data from HTML elements matching the given tag type and selector path.

    Args:
    - soup: BeautifulSoup object for parsing HTML.
    - tag_type (str): The type of HTML tag to be searched.
    - selector_path (str): CSS selector path for the desired elements.

    Returns:
    - list: A list containing text data from matching elements.
    """
    try:
        tag_element_list = soup.find_all(tag_type, selector_path)
        return [tag_element.text for tag_element in tag_element_list]
    except Exception as e:
        logging.error("An error occurred while extracting data: {}".format(e))


def add_at_columns(data_list):
    """
    Add date-related columns to the given data list.

    Args:
    - data_list (list): The list to which date-related columns will be added.
    """
    data_list.extend([date.today(), None, None])