from .scraping import codishop_scraping, codimap_scraping

# 여기서 컴퓨팅 리소스를 더 쓰되, 두 크롤링을 동시에 수행하게 만든다면 더욱 재밌
if __name__ == '__main__':
    # DO create table
    codishop_scraping.codishop()
    codimap_scraping.codimap()