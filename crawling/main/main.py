from crawling import Crawling

if __name__ == '__main__':
    """
    Main script to initiate Crawling for style and codimap lists on Musinsa website.
    
    Example:
    ```
    python main.py
    ```
    """

    # Crawling for Style Lists
    style_crawler = Crawling(top_url="https://www.musinsa.com/app/styles/lists")
    style_crawler.main_page_crawling()

    # Crawling for Codimap Lists
    codimap_crawler = Crawling(top_url="https://www.musinsa.com/app/codimap/lists")
    codimap_crawler.main_page_crawling()
