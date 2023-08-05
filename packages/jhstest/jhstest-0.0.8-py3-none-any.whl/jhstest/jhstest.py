import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt


def get_cloud(df, target_column, conditional_value='', conditional_column='all'):

    if conditional_column=='all':
        text = df[target_column].to_list()
    else:
        text = df[df[conditional_column]==conditional_value][target_column].to_list()

    count = Counter(text)
    words = dict(count.most_common())

    plt.figure(figsize=(16,14)) #이미지 사이즈 지정

    wordcloud = WordCloud(font_path='font/NanumGothic.ttf', background_color='white').generate_from_frequencies(words)
    plt.imshow(wordcloud,interpolation='lanczos')
    plt.axis('off')
    #plt.set_title(str(target_column), fontsize=20)
    plt.show()