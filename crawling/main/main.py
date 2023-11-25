from crawling import Crawling

if __name__ == '__main__':
    """
    Main script to initiate Crawling for style and codimap lists on Musinsa website.
    
    Example:
    ```
    python main.py
    ```
    """

    # Crawling for Codimap Lists
    codimap_crawler = Crawling(target_link = "codimap")
    codimap_crawler.main_page_crawling_scrapping()

    # Crawling for Style Lists
    style_crawler = Crawling(target_link = "styles")
    style_crawler.main_page_crawling_scrapping()