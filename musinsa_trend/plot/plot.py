import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from matplotlib import font_manager
from pathlib import Path
import pandas as pd
from .utils import Utils 

class Plot() :
    # Constants for managing files
    FILE_NAME_LINE = 'image01.png'
    FILE_NAME_PIE = 'image02.png'
    FILE_NAME_STACKED_BAR = 'image03.png'
    SAVE_DESTINATION = str(Path.cwd()) + '/plot/static/media/'

    # font setting for 한글
    font_path = str(Path.cwd()) + '/plot/static/resources/NanumGothic.ttf'
    custom_font = font_manager.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = custom_font.get_name()

    def get_file_name_line(self):
        return self.FILE_NAME_LINE

    def get_file_name_pie(self):
        return self.FILE_NAME_PIE

    def get_file_name_stacked_bar(self):
        return self.FILE_NAME_STACKED_BAR

    def save_figure(self,figure, file_name) :
        figure.savefig(self.SAVE_DESTINATION + file_name)

    def line(self,index_season, data) :
        title = '계절별 스타일 트렌드'

        # create plot
        for entry in data:
            dataset_name, values = entry.popitem()
            plt.plot(values, marker='o', label=dataset_name)

        # Style configurations
        plt.title(title)
        plt.xlabel('계절')
        plt.ylabel('등록된 코디 수')
        plt.xticks(index_seasons)
        plt.legend()
        plt.grid(True)
        
        #save it
        self.save_figure(plt,self.FILE_NAME_LINE)
        return True

    def pie(self,data) :
        brands,totals = data
        fig, ax = plt.subplots()
        ax.pie(totals, labels=brands)
        self.save_figure(fig, self.FILE_NAME_PIE)
        return True

    def stacked_bar(self,data) :
        # make it dataframe
        df = pd.DataFrame(data[0],index = data[1])
        # get style category names
        style_names = list(Utils.ALL_CATEGORIES)
        style_names.append('기타')
        # get the totals for each row
        totals = df.sum(axis=1)
        # calculate the percent for each row
        percent = df.div(totals, axis=0).mul(100).round(0)

        # create the plot
        ax = percent.plot(kind='barh', stacked=True, figsize=(12,8), colormap='terrain', xticks=[], legend=False)
        # index label fontsize settings
        ax.set_yticklabels(ax.get_yticklabels(), fontsize=28)
        # remove ticks
        ax.tick_params(left=False, bottom=False)
        # remove all spines
        ax.spines[['top', 'bottom', 'left', 'right']].set_visible(False)
        
        # iterate through each container
        for s, c in zip(style_names,ax.containers):
            labels = [] # custom label
            for v in c :
                # get percentage
                p = int(v.get_width())
                # make text label with style name if it's in top 5
                text = s+'\n'+str(p) + '%' if p != 0 else ''
                # add to labels
                labels.append(text)
            # create labels
            ax.bar_label(c, labels=labels, label_type='center', fontsize=16,color='w', path_effects=[path_effects.withStroke(linewidth=3, foreground='k')])

        # save it
        self.save_figure(ax.get_figure(),self.FILE_NAME_STACKED_BAR)
        return True