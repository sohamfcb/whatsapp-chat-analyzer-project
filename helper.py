from urlextract import URLExtract
from  wordcloud import  WordCloud
import pandas as pd
from collections import Counter
extractor=URLExtract()

def fetch_stats(selected_user,df):

    if selected_user!='Overall':
        df=df[df['user'] == selected_user]

    num_messages=df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())

    num_media_messages=df[df['message']=='<Media omitted>\n'].shape[0]

    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messages,len(words),num_media_messages,len(links)

def most_active_users(df):
    x=df['user'].value_counts().head()
    df=round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x,df


def create_wordcloud(selected_user,df):

    if selected_user!='Overall':
        df=df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    words = []

    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc=wc.generate(temp['message'].str.cat(sep=' '))
    return df_wc

def most_common_words(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    stop_words = ['ha', 'haa', 'haan', 'na', 'naa', 'nhi', 'keno', 'kyano', 'kano', 'bhai', 'vai', 'ei', 'e', 'ki',
                  're', 'ami', 'tui', 'tumi', 'amay', 'amake', 'toke', 'amake', 'kor', 'korte', 'hobe', 'acha', 'accha',
                  'achha', 'achchha', 'khub', 'aage', 'aaj', 'aj', 'kal', 'kaal', 'kya', 'kyu', 'kyun', 'tu', 'tereko',
                  'ko', 'hi', 'se', 'to', 'toh', 'hoga', 'the', 'is', 'hai', 'of', 'you', 'hum', 'main', 'and', 'bhi','theke','bol','ja','ta','er','o','kore','ar','aar','eta','ota','tai','kichu','ohh','uff','sob','shob','son','shon','kichhu','abar','ebar','but','te','amar','amr','sathe','shathe','bole','hobe','hbe','tho','tor','nei','ekta','thik','hoy','hoye','jani','oi','tr','r','or','kono','tao','ache','de','ke','ache','message','deleted','bhalo','this','that','niye','de','noy','was','ekhon','akhon','gulo']

    # words = []
    # for message in temp['message']:
    #     words.extend(message.split())

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)



    most_common_df=pd.DataFrame(Counter(words).most_common(20),columns=['Word','Frequency'])
    return most_common_df


def monthly_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))

    timeline['time'] = time

    daily_timeline = df.groupby('date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def monthly_activity_map(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user'] == selected_user]

    return df['month'].value_counts()


def activity_heatmap(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user'] == selected_user]

    user_heatmap=df.pivot_table(index='day_name',columns='hour',values='message',aggfunc='count').fillna(0)

    return user_heatmap