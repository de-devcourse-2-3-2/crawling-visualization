import matplotlib.pyplot as plt
from matplotlib import font_manager
from pathlib import Path
import pandas as pd

class Plot() :
    # Constants for managing files
    FILE_NAME_LINE = 'image00.png'
    FILE_NAME_PIE = 'image01'
    FILE_NAME_STACKED_BAR = 'image02.png'
    SAVE_DESTINATION = '/static/media/'

    # font setting for 한글
    font_path = str(Path.cwd()) + '/plot/static/resources/NanumGothic.ttf'
    custom_font = font_manager.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = custom_font.get_name()

    def save_figure(figure, file_name) :
        figure.savefig(SAVE_DESTINATION + filename)

    def pie(data) :
        brands,totals = data
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels)
        save_figure(fig,FILE_NAME_PIE)

    def line(index_season, data) :
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
        save_figure(plt,FILE_NAME_LINE)

    def stacked_bar(data) :
        # make it dataframe
        df = pd.DataFrame(data[0],index = data[1])
        # get style category names
        style_names = ALL_CATEGORIES
        # get the totals for each row
        totals = df.sum(axis=1)
        # calculate the percent for each row
        percent = df.div(totals, axis=0).mul(100).round(0)

        # create the plot
        ax = percent.plot(kind='barh', stacked=True, figsize=(16, 5), colormap='terrain', xticks=[], legend=False)

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
            ax.bar_label(c, labels=labels, label_type='center', padding=0.3, color='k')

        # save it
        save_figure(ax.get_figure(),FILE_NAME_STACKED_bAR)