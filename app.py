import streamlit as st

from parser import parse_whatsapp_chat
from helper import (
    enrich_chat_dataframe,
    monthly_timeline,
    daily_timeline,
    weekly_activity,
    activity_heatmap_data,
    fetch_basic_stats,
    most_active_users
)
from visualizer import (
    plot_monthly_timeline,
    plot_daily_timeline,
    plot_weekly_activity,
    plot_activity_heatmap,
    plot_most_active_users
)

st.set_page_config(page_title="WhatsApp Chat Analyzer", layout="wide")
st.title("📊 WhatsApp Chat Analyzer")

# Sidebar
st.sidebar.header("Upload & Filters")
uploaded_file = st.sidebar.file_uploader("Upload WhatsApp Chat (.txt)", type="txt")

if uploaded_file:
    # ---- PIPELINE ----
    df = parse_whatsapp_chat(uploaded_file)
    df = enrich_chat_dataframe(df)

    if df.empty:
        st.warning("No valid WhatsApp messages could be parsed from this file. Please upload a standard exported chat .txt file.")
        st.stop()

    # User selection
    users = df['user'].unique().tolist()
    users = [u for u in users if u != 'group_notification']
    users.sort()
    users.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Select User", users)

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    # ---- METRICS ----
    stats = fetch_basic_stats(df)

    st.subheader("📌 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Messages", stats['total_messages'])
    col2.metric("Total Words", stats['total_words'])
    col3.metric("Media Messages", stats['media_messages'])
    col4.metric("Links Shared", stats['total_links'])

    st.divider()

    # ---- TIMELINES ----
    st.subheader("🕒 Message Timelines")

    col1, col2 = st.columns(2)

    with col1:
        monthly_df = monthly_timeline(df)
        fig = plot_monthly_timeline(monthly_df)
        st.pyplot(fig)

    with col2:
        daily_df = daily_timeline(df)
        fig = plot_daily_timeline(daily_df)
        st.pyplot(fig)

    st.divider()

    # ---- ACTIVITY ----
    st.subheader("📅 Activity Patterns")

    col1, col2 = st.columns(2)

    with col1:
        weekly_df = weekly_activity(df)
        fig = plot_weekly_activity(weekly_df)
        st.pyplot(fig)

    with col2:
        heatmap_df = activity_heatmap_data(df)
        fig = plot_activity_heatmap(heatmap_df)
        st.pyplot(fig)

    st.divider()

    # ---- MOST ACTIVE USERS (Overall only) ----
    if selected_user == "Overall":
        st.subheader("🏆 Most Active Users")
        active_users_df = most_active_users(df)
        fig = plot_most_active_users(active_users_df)
        st.pyplot(fig)

else:
    st.info("👈 Upload a WhatsApp chat export file to begin analysis.")