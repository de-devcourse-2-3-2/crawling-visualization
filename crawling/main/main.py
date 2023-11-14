from crawling.main.crawling import Crawling

# 여기서 컴퓨팅 리소스를 더 쓰되, 두 크롤링을 동시에 수행하게 만든다면 더욱 재밌
if __name__ == '__main__':
    # DO create table
    Crawling.main_page_crawling("https://www.musinsa.com/app/styles/lists")
    Crawling.main_page_crawling("https://www.musinsa.com/app/codimap/lists")