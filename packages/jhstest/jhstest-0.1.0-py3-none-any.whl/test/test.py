import pandas as pd

import os

import jhstest

DOC_PATH = '../data'       # 파일 위치

df= pd.read_excel(os.path.join(DOC_PATH, 'test.xlsx'))

jhstest.get_cloud(df, conditional_column='변수_NEW',conditional_value='업무만족도', target_column='voice')
print(df)