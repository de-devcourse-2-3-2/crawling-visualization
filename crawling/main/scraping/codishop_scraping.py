from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
from datetime import date
import time, re, logging, psycopg2
from ..database import postgres_write as pw


def set_driver_and_soup(crawling_page_url):
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
    data_list.extend([date.today(), None, None])   #.strftime('%Y-%m-%d %H:%M:%S')



def main_page_scraping(soup):
    codies = soup.find_all("li", "style-list-item")  # 해당 페이지의 코디 리스트.

    for codi in codies:  # 현재 페이지의 모든 코디에 대해서 수행
        img_element = codi.select_one("div.style-list-item__thumbnail > a > div > img")
        img_src = img_element.attrs["src"]  # 이미지 url

        category_element = codi.select_one("div.style-list-information > a > span") # 스타일 카테고리
        # category를 분류할 때, 아동복 코디의 경우 text가 존재하지 않아 null값인 경우 '아동복'으로 저장
        category = category_element.text if category_element.text else "아동복"  # 예) 캐주얼, 아메카지, ..

        info_elements = codi.select_one("div.post-information").find_all("span")  # 코디 게시일, 조회수에 대한 정보를 포함하고 있는 element
        # 올린지 얼마 안 된 게시글에는 'N' 텍스트를 가진 <span> 태그가 하나 더 있음.
        # 일부 게시글에는 '댓글' 텍스트를 가진 <span> 태그가 하나 더 있음.
        # 구조 : (N) | 게시일 | 조회수 | (댓글)
        date_element, view_element = None, None
        if info_elements[0].text == 'N':
            date_element = info_elements[1]
            view_element = info_elements[2]
        else:
            date_element = info_elements[0]
            view_element = info_elements[1]
        dates = date_element.text.split('.')  # 코디 게시일 예) "23.11.07"
        # date = psycopg2.Date(int("20" + dates[0]), int(dates[1]), int(dates[2]))
        month = int(dates[1])
        when = date(int("20" + dates[0]), month, int(dates[2]))  # .strftime("%Y-%m-%d")  # formatting. "YYYY-MM-DD"
        if 3<=month<=5:
            season = "spring"
        elif 6<=month<=8:
            season = "summer"
        elif 9<=month<=11:
            season = "fall"
        else:
            season = "winter"
        views = int(re.sub(r'[^0-9]', '', view_element.text))  # 코디 게시물 조회수 예) "조회수 1,100" -> 1100 추출.

        codi_number_element = codi.select_one("div.style-list-item__thumbnail > a") # 코디 넘버링 값
        codi_number = re.sub(r'[^0-9]', '', str(codi_number_element.attrs["onclick"]))  # ex) "goView(37149)" -> 37149 추출.\
        subject = "shop" + "-" + codi_number  # 해당 코디의 제목 예) "shop-1511".
        return codi_number, [subject, when, category, season, views, img_src]


def scraping_goods_detail(soup):
    # 브랜드 목록 예시) "나이키"
    brands = return_list_data(soup, "a", "brand")  # class="brand"에 해당되는 브랜드 리스트
    # 상품명 목록 예시) "레더 크롭 숏 패딩 (브라운)"
    names = return_list_data(soup, "a", "brand_item")  # class="brand_item"에 해당되는 상품이름 리스트

    prices, del_prices = [], [] # 현재 가격 & 삭제된 가격 목록
    price_element_list = soup.find_all("div", "price")  # class="price"에 해당되는 상품 가격 리스트
    for price_element in price_element_list:
        price_string_list = price_element.text.split('원')  # 예시) 269,100원299,000원10% ==> {현재가격}{삭제가격}{할인율}
        price_string = price_string_list[0]  # 현재 가격에 대한 처리
        prices.append(int(re.sub(r'[^0-9]', '', price_string)))  # 예시) "26,900" => 26900

        del_price = None  # 삭제된 가격에 대한 처리.
        if len(price_string_list) > 2:  # 삭제된 가격이 존재하는 경우 값 입력, 아니면 None 그대로.
            del_price = int(re.sub(r'[^0-9]', '', price_string_list[1]))
        del_prices.append(del_price)

    goods_detail_data = [(a,b,c,d) for a,b,c,d in zip(brands, names, prices, del_prices)]
    logging.debug(goods_detail_data)
    return goods_detail_data


def main_page_crawling():
    ''' 추출한 정보들
        ** style table **
        1. subject: 제목. ex)"styles-1511"(string)
        2. date: 게시된 날짜. ex)"2023-11-07"(string)
        3. category: 스타일 카테고리. ex)"댄디"(string)
        4. views: 조회수. ex)1100(int)
        5. img_src: 이미지 URL. ex)"https://.*"(string)
        6. tags: 태그 목록. ex)["#겨울", "#깔끔한", ..](list)
        ** goods table **
        7. brands: 브랜드 목록. ex)["나이키", "아디다스", ..](list)
        8. names: 상품명 목록. ex)["레더 크롭 숏 패딩", "우먼스 스탠다드 코듀로이 오버롤", ..](list)
        9. prices: 현재 가격 목록. ex)[12000, 50000, ..](list). 취소선 없는 가격.
        10. del_prices: 삭제된 가격 목록. ex)[22000, 60000, ..](list). 취소선 있는 가격.
    '''
    postgres = pw.DB_Write()
    postgres.tables_create()

    global driver
    with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
        soup = set_driver_and_soup("https://www.musinsa.com/app/styles/lists")  # 코디샵 전체 페이지
        total_pages_number = int(soup.find("span", "totalPagingNum").text)

        # for i in range(1, total_pages_number + 1):
        for i in range(1, 5):
            soup = set_driver_and_soup(f"https://www.musinsa.com/app/codimap/lists?page={i}")
            codi_number, style_data_list = main_page_scraping(soup)  # db write 단위!

            # 상세 페이지 크롤링 시작을 위해 soup 재세팅
            soup = set_driver_and_soup(f"https://www.musinsa.com/app/styles/views/{codi_number}") # 해당 코디 상세 페이지
            tags = return_list_data(soup, "a", "ui-tag-list__item")  # 태그 목록 예시) "#겨울"
            style_data_list.append(" ".join(tags))
            # add_at_columns(style_data_list)
            logging.info("Style No.{} row- {}".format(codi_number, style_data_list))
            style_id = postgres.insert_style_data(style_data_list)

            goods_detail_data = scraping_goods_detail(soup)
            goods_ids = postgres.insert_goods_data(goods_detail_data)
            postgres.insert_style_goods(style_id, goods_ids)