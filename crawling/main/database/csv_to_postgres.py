# csv file -> DB로 write하는 파일.
# Encoding 방식에 유의해서 테스트해 봐야할 것 같음.
# postgres_write.py 파일의 return_postgresql_conn 메서드에서 db_config에서 encoding방식 utf16으로 일단 적용.
import postgres_write as pw
import pandas as pd
import datetime

def main():
    pw.tables_create()

    codishop_dataset = pd.read_csv('codishop(2023-11-09_12h_2m).csv', encoding='utf-16')
    codimap_dataset = pd.read_csv('codimap(2023-11-10_10h_19m).csv', encoding='utf-16')
    dataset = pd.concat([codishop_dataset, codimap_dataset], ignore_index=True) # 전체 데이터셋

    for idx, row in dataset.iterrows():
        # style table 관련 정보들
        subject = row['subject'] # subject: 제목. ex)"codimap-1511"(string)
        date = row['date'] # date: 게시된 날짜. ex)"2023-11-07"(string)
        category = row['category'] # category: 스타일 카테고리. ex)"댄디"(string)
        views = row['views'] # views: 조회수. ex)1100(int)
        img_url = row['URL'] # URL: 이미지 URL. ex)"https://.*"(string)
        tags = row['tag'] # tags: 태그 목록. ex)["#겨울", "#깔끔한", ..](list)
        created_at = datetime.datetime.now() # 현재 시각
        style_dataset = [subject, date, category, views, img_url, tags, created_at, None, None]
        # 스타일 테이블 insert
        pw.insert_style_data(style_list=style_dataset) # subject, date, category, views, url, tag, created_at, updated_at, deleted_at

        # goods table 관련 정보들
        brands = row['brands'] # brands: 브랜드 목록. ex)["나이키", "아디다스", ..](list)
        names = row['names'] # names: 상품명 목록. ex)["레더 크롭 숏 패딩", "우먼스 스탠다드 코듀로이 오버롤", ..](list)
        prices = row['prices'] # prices: 현재 가격 목록. ex)[12000, 50000, ..](list). 취소선 없는 가격.
        del_prices = row['del_prices'] # del_prices: 삭제된 가격 목록. ex)[22000, 60000, ..](list). 취소선 있는 가격.
        for i in range(len(brands)):
            name = names[i]
            brand = brands[i]
            price = prices[i]
            del_price = del_prices[i]
            goods_dataset = [name, brand, price, del_price]

            # 상품 테이블 insert
            pw.insert_goods_data(goods_list=goods_dataset)

if __name__ == '__main__':
    main()