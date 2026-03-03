import pandas as pd
import re

def enrich_chat_dataframe(df):
    df = df.copy()

    date_series = df['date'].astype(str).str.replace('-', '/', regex=False).str.strip()
    time_series = (
        df['time']
        .astype(str)
        .str.replace('\u202f', ' ', regex=False)
        .str.replace('\xa0', ' ', regex=False)
        .str.strip()
    )

    datetime_text = date_series + ' ' + time_series

    parsed_dt = pd.to_datetime(datetime_text, dayfirst=True, errors='coerce')
    unresolved = parsed_dt.isna()

    if unresolved.any():
        parsed_dt.loc[unresolved] = pd.to_datetime(
            datetime_text[unresolved],
            dayfirst=False,
            errors='coerce'
        )

    df['datetime'] = parsed_dt

    df = df.dropna(subset=['datetime'])

    # Date-time features
    df['year'] = df['datetime'].dt.year
    df['month'] = df['datetime'].dt.month
    df['month_name'] = df['datetime'].dt.month_name()
    df['day'] = df['datetime'].dt.day
    df['day_name'] = df['datetime'].dt.day_name()
    df['hour'] = df['datetime'].dt.hour
    df['minute'] = df['datetime'].dt.minute

    # Media messages
    df['is_media'] = df['message'].str.contains('<Media omitted>', na=False)

    # Word count
    df['word_count'] = df['message'].apply(
        lambda x: 0 if x == '<Media omitted>' else len(str(x).split())
    )

    # Link count
    url_pattern = r'(https?://\S+|www\.\S+)'
    df['link_count'] = df['message'].apply(
        lambda x: len(re.findall(url_pattern, str(x)))
    )

    return df


def monthly_timeline(df):
    return (
        df
        .groupby(['year', 'month', 'month_name'])
        .size()
        .reset_index(name='message_count')
        .sort_values(['year', 'month'])
    )


def daily_timeline(df):
    timeline = (
        df
        .groupby(df['datetime'].dt.date)
        .size()
        .reset_index(name='message_count')
    )
    timeline.columns = ['date', 'message_count']
    return timeline


def weekly_activity(df):
    return (
        df['day_name']
        .value_counts()
        .reset_index(name='message_count')
    )


def activity_heatmap_data(df):
    return (
        df
        .groupby(['day_name', 'hour'])
        .size()
        .reset_index(name='message_count')
    )


def fetch_basic_stats(df):
    return {
        'total_messages': df.shape[0],
        'total_words': df['word_count'].sum(),
        'media_messages': df['is_media'].sum(),
        'total_links': df['link_count'].sum()
    }


def most_active_users(df, top_n=10):
    return (
        df[df['user'] != 'group_notification']['user']
        .value_counts()
        .head(top_n)
        .reset_index(name='message_count')
    )