import matplotlib.pyplot as plt
import pandas as pd

def plot_monthly_timeline(timeline_df):
    fig, ax = plt.subplots(figsize=(12, 5))

    if timeline_df.empty:
        ax.text(0.5, 0.5, "No timeline data available", ha='center', va='center')
        ax.axis('off')
        return fig

    period = timeline_df['month_name'] + ' ' + timeline_df['year'].astype(str)

    ax.plot(period, timeline_df['message_count'], marker='o')

    ax.set_title('Monthly Message Timeline')
    ax.set_xlabel('Month')
    ax.set_ylabel('Number of messages')
    plt.xticks(rotation=45)

    return fig


def plot_daily_timeline(daily_df):
    fig, ax = plt.subplots(figsize=(14, 5))

    if daily_df.empty:
        ax.text(0.5, 0.5, "No timeline data available", ha='center', va='center')
        ax.axis('off')
        return fig

    ax.plot(daily_df['date'], daily_df['message_count'])

    ax.set_title('Daily Message Timeline')
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of messages')

    return fig


def plot_weekly_activity(weekly_df):
    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    fig, ax = plt.subplots(figsize=(8, 5))

    if weekly_df.empty:
        ax.text(0.5, 0.5, "No weekly activity data available", ha='center', va='center')
        ax.axis('off')
        return fig

    weekly_df['day_name'] = pd.Categorical(
        weekly_df['day_name'],
        categories=days,
        ordered=True
    )
    weekly_df = weekly_df.sort_values('day_name')

    ax.bar(weekly_df['day_name'], weekly_df['message_count'])

    ax.set_title('Weekly Activity')
    ax.set_xlabel('Day')
    ax.set_ylabel('Number of messages')

    return fig


def plot_activity_heatmap(heatmap_df):
    if heatmap_df.empty:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "No activity data available",
                ha='center', va='center')
        ax.axis('off')
        return fig

    pivot = heatmap_df.pivot(
        index='day_name',
        columns='hour',
        values='message_count'
    ).fillna(0)

    if pivot.values.sum() == 0:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "No activity data available",
                ha='center', va='center')
        ax.axis('off')
        return fig

    day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    pivot = pivot.reindex(day_order).fillna(0)
    pivot = pivot.reindex(columns=sorted(pivot.columns), fill_value=0)

    fig, ax = plt.subplots(figsize=(12, 6))
    image = ax.imshow(pivot.values, aspect='auto', cmap='YlGnBu')
    fig.colorbar(image, ax=ax)

    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index)
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels([str(col) for col in pivot.columns], rotation=45)

    ax.set_title('Activity Heatmap (Day vs Hour)')
    ax.set_xlabel('Hour')
    ax.set_ylabel('Day')

    return fig


def plot_most_active_users(user_df):
    fig, ax = plt.subplots(figsize=(8, 5))

    if user_df.empty:
        ax.text(0.5, 0.5, "No user activity data available", ha='center', va='center')
        ax.axis('off')
        return fig

    ax.bar(user_df['user'], user_df['message_count'])

    ax.set_title('Most Active Users')
    ax.set_xlabel('User')
    ax.set_ylabel('Messages')
    plt.xticks(rotation=45)

    return fig