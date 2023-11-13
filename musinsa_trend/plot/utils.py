class Plot_util:

    ALL_CATEGORIES = ("아메카지", "캐주얼", "시크", "댄디", "비즈니스캐주얼", "걸리시", "골프", "레트로", "로맨틱", "스포티", "스트릿", "고프코어")

    def get(self):
        return self.SAMPLE_DATA
    
    def get_data_for_pie(category, raw_data) :
        for category_data in raw_data['category_brand_counts']:
            if category_data['category'] == category:                    
                # Sort brands by total
                sorted_brand_counts = sorted(brand_counts, key=lambda x: x['total'], reverse=True)

                # Get only top 5 brands and their totals
                brands = [brand_count['brand'] for brand_count in sorted_brand_counts[:5]]
                totals = [brand_count['total'] for brand_count in sorted_brand_counts[:5]]

                # sum the total of the remaining brands
                others_total = sum(brand_count['total'] for brand_count in sorted_brand_counts[5:])

                # Append others
                brands.append("Others")
                totals.append(others_total)
                return (brands, totals)
        # EXPECTED RAW DATA AS INPUT FROM category_brand_count()
        # {
        #     'category_brand_counts': [
        #         {
        #             'category': '스포티',
        #             'brand_counts': [
        #                 {'brand': '나이키', 'total': 10},
        #                 {'brand': '아디다스', 'total': 5},
        #                 ...
        #             ]
        #         },
        #         {
        #             'category': '캐주얼',
        #             'brand_counts': [
        #                 {'brand': '에잇세컨즈', 'total': 8},
        #                 {'brand': '유니클로', 'total': 12},
        #                 ...
        #             ]
        #         },
        #         ...
        #     ]
        # }

    def get_data_for_stacked_bar(raw_data) :
        categories_count = {k : [0,0,0,0] for k in ALL_CATEGORIES}
        categories_count["기타"] = [0,0,0,0]

        for i, season in enumerate(raw_data.values()):
            for top_cat in season["top_categories"] :
                categories_count[top_cat["category"]][i] = top_cat["count"]
            categories_count["기타"][i] = season["other_count"]
        
        return (categories_count, ['봄', '여름', '가을', '겨울'])

        # EXPECTED RAW DATA FROM season_style_trend()
        # {
        #     "Spring": {
        #         "top_categories": [
        #             {"category": "캐주얼", "count": 150},
        #             {"category": "댄디", "count": 120},
        #             {"category": "아메카지", "count": 90},
        #             {"category": "레트로", "count": 80},
        #             {"category": "골프", "count": 70}
        #         ],
        #         "other_count": 260
        #     },
        #     "summer": {
        #         "top_categories": [
        #             {"category": "골프", "count": 150},
        #             {"category": "레트로", "count": 120},
        #             {"category": "고프코어", "count": 90},
        #             {"category": "시크", "count": 80},
        #             {"category": "아메카지", "count": 70}
        #         ],
        #         "other_count": 260
        #     },
        #     "autumn": {
        #         "top_categories": [
        #             {"category": "스트릿", "count": 150},
        #             {"category": "걸리시", "count": 120},
        #             {"category": "캐주얼", "count": 90},
        #             {"category": "로맨틱", "count": 80},
        #             {"category": "스포티", "count": 70}
        #         ],
        #         "other_count": 260
        #     },
        #     "winter": {
        #         "top_categories": [
        #             {"category": "고프코어", "count": 150},
        #             {"category": "캐주얼", "count": 120},
        #             {"category": "시크", "count": 90},
        #             {"category": "댄디", "count": 80},
        #             {"category": "로맨틱", "count": 70}
        #         ],
        #         "other_count": 260
        #     }
        # }