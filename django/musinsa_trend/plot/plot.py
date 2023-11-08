import json
import matplotlib.pyplot as plt
from matplotlib import font_manager
from pathlib import Path

class Plot() :
    # 폰트 경로 지정 (실제 폰트 파일 경로로 수정)
    font_path = str(Path.cwd()) + '/resourse/applegothic.ttf'
    custom_font = font_manager.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = custom_font.get_name()

    def chart1(data) :
        TITLE = '계절별 스타일 트렌드'

        # JSON 데이터 파싱
        data = json.loads(data)
        fig, ax = plt.subplots(figsize=(15, 6))

        # 그래프 그리기
        for entry in data:
            dataset_name, values = entry.popitem()
            plt.plot(values, marker='o', label=dataset_name)

        # 그래프 스타일 설정
        plt.title(TITLE)
        plt.xlabel('계절')
        plt.ylabel('등록된 코디 수')
        plt.legend()  # 범례 추가
        plt.grid(True)
    
    def save(plt) :
        plt.savefig('line_chart.png')