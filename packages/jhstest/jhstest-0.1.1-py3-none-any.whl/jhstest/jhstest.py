import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import HTML
import plotly.express as px


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


def sentance_inspect(_column):
    maxval=0
    list = _column.tolist()
    tokenized_list = [r.split() for r in list]
    sentence_len_by_token = [len(t) for t in tokenized_list]
    sentence_len_by_eumjeol = [len(s.replace(' ', '')) for s in list]
    # for s in list:
    #     if len(s.replace(' ', '')) >15000:
    #         if maxval <len(s):
    #             maxval = len(s)


    for t  in tokenized_list:
        if len(t)  == 0:
            print()
    print('maxval : ',maxval)
    plt.figure(figsize = (12,5))
    plt.hist(sentence_len_by_token, bins = 50, alpha=0.5, color="r", label="word")
    plt.hist(sentence_len_by_eumjeol, bins = 50, alpha=0.5, color="b", label="aplt.yscallphabet")
    plt.yscale('log', nonposy = 'clip')
    plt.title(_column.name)
    plt.xlabel('red:token / blue:eumjeol length')
    plt.ylabel('number of sentences')


    print('\n', )
    print('칼럼명 : {}'.format(_column.name))
    print('토큰 최대 길이 : {}'.format(np.max(sentence_len_by_token)))
    print('토큰 최소 길이 : {}'.format(np.min(sentence_len_by_token)))
    print('토큰 평균 길이 : {:.2f}'.format(np.mean(sentence_len_by_token)))
    print('토큰 길이 표준편차 : {:.2f}'.format(np.std(sentence_len_by_token)))
    print('토큰 중간 길이 : {}'.format(np.median(sentence_len_by_token)))
    print('제 1사분위 길이 : {}'.format(np.percentile(sentence_len_by_token, 25)))
    print('제 3사분위 길이 : {}'.format(np.percentile(sentence_len_by_token, 75)))


def correlation_matrix(df):
    fig, ax = plt.subplots()
    fig.set_size_inches(30,10)

    corrMatt = df.corr()
    mask = np.array(corrMatt)
    mask[np.tril_indices_from(mask)] = False
    sns.heatmap(df.corr(), mask=mask,vmax=.9, square=True,annot=True)





def draw_pie_graph(df, condition_column):
    res = df[condition_column].value_counts() \
        .to_frame('count').rename_axis(condition_column) \
        .reset_index()
    fig = px.pie(res, values='count', names=condition_column, title = condition_column)
    #HTML(fig.to_html())
    fig.update_traces(textinfo='percent+label')
    fig.show()


def draw_rank_graph(df, condition_column, top_count=20, title=''):
    plt.figure(figsize=(16,8))
    ax = sns.countplot(y=condition_column, data=df, order = df[condition_column].value_counts()[:top_count].index)
    ax.set_title(title, fontsize=20)