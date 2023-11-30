# from django.test import TestCase
# from plot import Plot
# import os
# import unittest
# # Create your tests here.

# class Plot_test(unittest.TestCase):


#     def test_line(self) :
#         Plot.line(seasons,data)
#         is_file = os.path.isfile(Plot.SAVE_DESTINATION + '/' + FILE_NAME_LINE)
#         self.assertTrue(, "File does not exist.")

#     def test_line(self) :
#         Plot.line(dataframe)
#         is_file = os.path.isfile(Plot.SAVE_DESTINATION + '/' + FILE_NAME_STACKED_BAR)
#         self.assertTrue(is_file, "File does not exist.")

#     if __name__ == "__main__":
#         unittest.main()


# ########
# # SAMPLE
# ########

# # sample for line chart
# seasons = ['19-Mar','19-Jun','19-Sep','19-Dec','20-Mar','20-Jun','20-Sep','20-Dec','21-Mar','21-Jun','21-Sep','21-Dec','22-Mar','22-Jun','22-Sep','22-Dec','23-Mar','23-Jun','23-Sep','23-Dec']
# data = [
#         {'AMEKAJI': [1, 3, 4, 7, 11, 18, 39, 40, 30, 35, 32, 31, 20, 15, 11, 7, 7, 2, 13, 10]},
#         {'CASUAL': [39, 40, 30, 35, 32, 31, 20, 4, 18, 9, 4, 12, 16, 8, 16, 20, 16, 19, 15, 8]},
#         {'RETRO': [7, 5, 5, 16, 9, 4, 5, 8, 9, 14, 23, 28, 34, 39, 40, 30, 35, 32, 31, 20]},
#         {'SPORTY': [5, 7, 9, 7, 8, 8, 10, 11, 9, 8, 11, 12, 10, 10, 10, 9, 8, 7, 6, 8]},
#         {'ROMANCE': [6, 20, 4, 13, 6, 17, 5, 12, 1, 8, 1, 15, 5, 10, 20, 19, 10, 2, 10, 16]}
#     ]

# # sample for stacked bar chart
# dataframe = pd.DataFrame({  '레트로':   [103281, 75376, 66957, 73071],
#                             '캐주얼':   [0, 2323, 48567, 33587],
#                             '아메카지' :[54165, 75619, 48567, 33587],
#                             '스포티' :  [54165, 75619, 0, 33587],
#                             '로맨틱' :  [54165, 0, 48567, 33587],
#                             '골프' :    [54165, 75619, 48567, 0],
#                             '기타' :    [30000,25000,2999,1000]
#                         },
#                         index=['Spring', 'Summer', 'Autumn', 'Winter'])