import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from matplotlib import font_manager, rc
from pathlib import Path
import pandas as pd
from .utils import Utils
from datetime import datetime
import os
import matplotlib.font_manager

# font_manager._rebuild()


class Plot:  # init 메서드가 없는데 이걸 어케 써..? 여기에 () 이거 붙이면 스태틱으로만 쓸수있기라도 함?
    # Constants for managing files
    FILE_NAME_LINE = ''
    FILE_NAME_PIE = ''
    FILE_NAME_STACKED_BAR = ''
    SAVE_DESTINATION = str(Path.cwd()) + '\\plot\\static\\media\\'

    # font_manager._rebuild()
    
    def font_setting(self, plt):
        # font_path = os.path.join(os.path.dirname(__file__), 'static', 'resources', 'NanumGothic.ttf')
        font_path = 'plot/static/resources/NanumGothic.ttf'  # 여기서 경로를 .ttf 파일의 실제 경로로 바꿔주세요.
        
        # if os.path.exists(font_path):
        #     print(f"파일이 존재합니다: {font_path}")
        # else:
        #     print(f"파일이 존재하지 않습니다: {font_path}")

        # FontProperties 객체를 생성합니다.
        # font_prop = font_manager.FontProperties(fname=font_path)
        # font_list = matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
        # plt.rc('font', family='NanumGothic')
        # matplotlib.rcParams['axes.unicode_minus'] = False
        # 폰트 이름을 가져옵니다.
        # # matplotlib의 전역 폰트 설정을 업데이트합니다.
        # plt.rcParams['font.family'] = font_prop.get_name()
        # plt.rcParams['axes.unicode_minus'] = False

        # font_prop = font_manager.FontProperties(fname='plot/static/resources/NanumGothic.ttf')
        # plt.xticks(fontproperties=font_prop)
        plt.rcParams["font.family"] = "NanumGothic"

    def get_file_name_line(self):
        return self.FILE_NAME_LINE

    def get_file_name_pie(self):
        return self.FILE_NAME_PIE

    def get_file_name_stacked_bar(self):
        return self.FILE_NAME_STACKED_BAR

    def save_figure(self, figure, file_name):
        figure.savefig(self.SAVE_DESTINATION + file_name)

    def line(self, date_list, category_views_dict):
        date_objects = [datetime.strptime(date, "%Y-%m") for date in date_list]

        # 그래프 생성
        plt.figure(figsize=(15, 10))

        for category, views in category_views_dict.items():
            plt.plot(date_objects, views, marker='o', label=category)

        plt.title('Monthly Views by Category')
        plt.xlabel('Date')
        plt.ylabel('Views')
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
        plt.grid(True)
        # 지수 표기법이 아닌 일반 표기법 설정
        plt.ticklabel_format(axis='y', style='plain')

        # font
        self.font_setting(plt)

        # 그래프 저장
        self.save_figure(plt, self.FILE_NAME_LINE)

        return self.FILE_NAME_LINE

    def pie(self, data):
        brands, totals = data
        fig, ax = plt.subplots()
        ax.pie(totals, labels=brands)
        # font
        self.font_setting(plt)
        self.save_figure(fig, self.FILE_NAME_PIE)
        plt.close()
        return self.FILE_NAME_PIE

    def stacked_bar(self, data):
        # make it dataframe
        df = pd.DataFrame(data[0], index=data[1])
        # get style category names
        style_names = list(Utils.ALL_CATEGORIES)
        style_names.append('기타')
        # get the totals for each row
        totals = df.sum(axis=1)
        # calculate the percent for each row
        percent = df.div(totals, axis=0).mul(100).round(0)

        # create the plot
        ax = percent.plot(kind='barh', stacked=True, figsize=(12, 8), colormap='terrain', xticks=[], legend=False)
        # index label fontsize settings
        ax.set_yticklabels(ax.get_yticklabels(), fontsize=28)
        # remove ticks
        ax.tick_params(left=False, bottom=False)
        # remove all spines
        ax.spines[['top', 'bottom', 'left', 'right']].set_visible(False)

        # iterate through each container
        for s, c in zip(style_names, ax.containers):
            labels = []  # custom label
            for v in c:
                # get percentage
                p = int(v.get_width())
                # make text label with style name if it's in top 5
                text = s + '\n' + str(p) + '%' if p != 0 else ''
                # add to labels
                labels.append(text)
            # create labels
            ax.bar_label(c, labels=labels, label_type='center', fontsize=16, color='w',
                         path_effects=[path_effects.withStroke(linewidth=3, foreground='k')])
        # font
        self.font_setting(plt)
        # save it
        self.save_figure(ax.get_figure(), self.FILE_NAME_STACKED_BAR)
        plt.close()
        return self.FILE_NAME_STACKED_BAR
