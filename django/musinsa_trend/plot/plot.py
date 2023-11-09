import matplotlib.pyplot as plt
from matplotlib import font_manager
from pathlib import Path
import pandas as pd

class Plot() :
    IMG_BASIC_LINE = 'image00.png'
    IMG_SEASONAL_TREND = 'image03.png'

    # font setting for 한글
    font_path = str(Path.cwd()) + '/resourse/applegothic.ttf'
    custom_font = font_manager.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = custom_font.get_name()

    def line(data) :
        title = '계절별 스타일 트렌드'

        # create plot
        for entry in data:
            dataset_name, values = entry.popitem()
            plt.plot(values, marker='o', label=dataset_name)

        # Style configurations
        plt.title(title)
        plt.xlabel('계절')
        plt.ylabel('등록된 코디 수')
        plt.legend()
        plt.grid(True)
        plt.savefig('/media/' + IMG_BASIC_LINE)

    def chart3(data) :
        df = pd.DataFrame({ '레트로': [103281, 75376, 66957, 73071],
                    '캐주얼': [0, 2323, 48567, 33587],
                    '아메카지' : [54165, 75619, 48567, 33587],
                    '스포티' : [54165, 75619, 0, 33587],
                    '로맨틱' : [54165, 0, 48567, 33587],
                    '골프' : [54165, 75619, 48567, 0],
                    '기타' : [30000,25000,2999,1000]
                  },
                        index=['Spring', 'Summer', 'Autumn', 'Winter'])

        # get columns name
        style_names = df.columns.tolist()
        # get the totals for each row
        totals = df.sum(axis=1)
        # calculate the percent for each row
        percent = df.div(totals, axis=0).mul(100).round(0)

        # create the plot
        ax = percent.plot(kind='barh', stacked=True, figsize=(16, 5), colormap='Paired', xticks=[], legend=False)

        # remove ticks
        ax.tick_params(left=False, bottom=False)
        # remove all spines
        ax.spines[['top', 'bottom', 'left', 'right']].set_visible(False)
        
        
        # iterate through each container
        for c in ax.containers:
            labels = [] # custom label

            for s,v in zip(style_names,c) :
                # get percentage
                p = int(v.get_width())
                # make text label with style name if it's in largest 5
                text = s+'\n'+str(p) + '%' if p != 0 else ''
                # add to labels
                labels.append(text)
            
            # create labels
            ax.bar_label(c, labels=labels, label_type='center', padding=0.3, color='w')

        # save it
        ax.get_figure().savefig('/media/' + IMG_SEASONAL_TREND)