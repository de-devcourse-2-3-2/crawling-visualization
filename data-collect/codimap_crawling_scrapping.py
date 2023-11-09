# 코디맵 전체 페이지에서 진행하는 크롤링 및 스크래핑
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import time
import datetime
import re
import logger

def codimap():
    with webdriver.Chrome(service = Service(ChromeDriverManager().install())) as driver:
        codimap_lists_url = "https://www.musinsa.com/app/codimap/lists" # 코디맵 메인 페이지.
        driver.get(codimap_lists_url)
        driver.implicitly_wait(60)
        time.sleep(0.5) # delay time 설정.
        soup = BeautifulSoup(driver.page_source, "html.parser")
        total_pages_number = int(soup.find("span", "totalPagingNum").text) # 전체 페이지 수.

        # 모든 페이지에 대해서 수행
        for i in range(1, total_pages_number + 1):
            page_url = f"https://www.musinsa.com/app/codimap/lists?page={i}" # 코디맵의 {i}번 페이지.
            driver.get(page_url)
            driver.implicitly_wait(60)
            time.sleep(0.5) # delay time 설정.
            soup = BeautifulSoup(driver.page_source, "html.parser")
            codies = soup.find_all("li", "style-list-item") # 해당 페이지의 코디 리스트.
                
            # 현재 페이지의 모든 코디에 대해서 수행
            for codi in codies:
                    
                # 이미지 url.
                img_element = codi.select_one("div.style-list-item__thumbnail > a > div > img")
                img_src = img_element.attrs["src"]
        
                # 스타일 카테고리.
                category_element = codi.select_one("div.style-list-information > a > span")
                # category를 분류할 때, 아동복 코디의 경우 text가 존재하지 않음. 따라서, null값인 경우 '아동복'으로 저장.
                category = category_element.text if category_element.text else "아동복" # 예) 캐주얼, 아메카지, ..

                # 코디 게시일, 조회수 등에 대한 처리.
                info_elements = codi.select_one("div.post-information").find_all("span") # 정보를 포함하고 있는 element
                # 올린지 얼마 안 된 게시글에는 'N' 텍스트를 가진 <span> 태그가 하나 더 있음.
                # 일부 게시글에는 '댓글' 텍스트를 가진 <span> 태그가 하나 더 있음.
                # 구조 : (N) | 게시일 | 조회수 | (댓글)
                date_element = None
                view_element = None
                if info_elements[0].text == 'N':
                    date_element = info_elements[1]
                    view_element = info_elements[2]
                else:
                    date_element = info_elements[0]
                    view_element = info_elements[1]
                # 코디 게시일 처리.
                date_string = date_element.text # 예) "23.11.07"
                dates = date_string.split('.')
                year = int("20" + dates[0])
                month = int(dates[1])
                day = int(dates[2])
                date = datetime.date(year, month, day).strftime("%Y-%m-%d") # formatting. "YYYY-MM-DD"
                # 코디 조회수 처리.
                views = int(re.sub(r'[^0-9]', '', view_element.text)) # 예) "조회수 1,100" -> 1100 추출.
        
                # 코디 넘버링 값.
                codi_number_element = codi.select_one("div.style-list-item__thumbnail > a")
                codi_number = re.sub(r'[^0-9]', '', str(codi_number_element.attrs["onclick"])) # ex) "goView(37149)" -> 37149 추출.\
        
                # 해당 코디의 제목.
                subject = "codimap" + "-" + codi_number # 예) "codimap-1511".

                # --------------------------------------------------------------------------------     
                # 코디 상세 페이지에서의 수행.
                
                detail_url = f"https://www.musinsa.com/app/codimap/views/{codi_number}" # 해당 코디 상세 페이지
                driver.get(detail_url)
                driver.implicitly_wait(60)
                time.sleep(0.5) # delay time 설정.
                soup = BeautifulSoup(driver.page_source, "html.parser")
                    
                # 태그 목록.
                tags = []
                tag_element_list = soup.find_all("a", "ui-tag-list__item") # class="ui-tag-list__item"에 해당되는 태그 리스트
                for tag_element in tag_element_list:
                    tags.append(tag_element.text) # 예시) "#겨울"
                    
                # 브랜드 목록.
                brands = [] 
                brand_element_list = soup.find_all("a", "brand") # class="brand"에 해당되는 브랜드 리스트
                for brand_element in brand_element_list:
                    brands.append(brand_element.text) # 예시) "나이키"
        
                # 상품이름 목록.
                names = []
                name_element_list = soup.find_all("a", "brand_item") # class="brand_item"에 해당되는 상품이름 리스트
                for name_element in name_element_list:
                    names.append(name_element.text) # 예시) "레더 크롭 숏 패딩 (브라운)"
        
                # 현재 가격 목록.
                prices = []
                # del 가격 목록.
                del_prices = []
                price_element_list = soup.find_all("div", "price") # class="price"에 해당되는 상품 가격 리스트
                for price_element in price_element_list:
                    price_string = price_element.text # 예시) 269,100원299,000원10% ==> {현재가격}{삭제가격}{할인율}
                    price_string_list = price_string.split('원')
                    
                    # 현재 가격에 대한 처리.
                    price_string = price_string_list[0]
                    price = int(re.sub(r'[^0-9]', '', price_string))
                    prices.append(price) # 예시) "26,900" => 26900
            
                    # 삭제된 가격에 대한 처리.
                    del_price = None
                    # 삭제된 가격이 존재하는 경우 값 입력, 아니면 None 그대로.
                    if len(price_string_list) > 2: 
                        del_price_string = price_string_list[1]
                        del_price = int(re.sub(r'[^0-9]', '', del_price_string))
                    del_prices.append(del_price)
                
                ''' 추출된 정보들
                ** style table **
                1. subject: 제목. ex)"codimap-1511"(string)
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
                codimap_dataset = [subject, date, category, views, img_src, tags, brands, names, prices, del_prices] # 데이터 리스트.

                # 로그 파일 기록
                # 아직 log 파일명에 대한 인자 전달하는 방법을 모름.
                # logger.DEBUG(codimap_dataset)

                # DB Write
                '''
                작성
                '''

    return True

def main():
    if codimap():
        return "successed"
    else:
        return "error"

if __name__ == "__main__":
    main()