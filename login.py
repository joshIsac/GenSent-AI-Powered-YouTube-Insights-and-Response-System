import streamlit as st
import os
import pandas as pd
from googleapiclient.discovery import build
from dotenv import load_dotenv
from scripts.fetch_channel_data import fetch_channel_statistics
from scripts.fetch_video_stats import fetch_video_metadata
from scripts.visualisation import visualize_essential_metrics
from scripts.sentiment_analysis import get_video_comments

# Load API Key
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

# Initialize YouTube API
def initialize_youtube_api():
    youtube = build("youtube", "v3", developerKey=API_KEY)
    return youtube

# Login function
def login():
    if st.button("Log in"):
        st.session_state.logged_in = True
        st.rerun()

# Logout function
def logout():
    if st.sidebar.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()

# Initialize session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Main App
def main():
    st.title("GenSent: AI-Powered YouTube Insights")

    if st.session_state.logged_in:
        # Navigation Sidebar
        st.sidebar.title("Navigation")
        app_page = st.sidebar.radio(
            "Choose a page",
            ["Dashboard", "Bug Reports", "System Alerts", "Search", "History"]
        )

        # Logout Button
        logout()

        # Initialize YouTube API
        youtube = initialize_youtube_api()

        if app_page == "Dashboard":
            st.title("Dashboard")
            st.sidebar.header("Input Channel Details")
            channel_name = st.sidebar.text_input("Enter YouTube Channel Name:")

            if st.sidebar.button("Fetch Channel Analytics"):
                with st.spinner("Fetching channel analytics..."):
                    channel_data = fetch_channel_statistics(youtube, channel_name)

                if "error" in channel_data:
                    st.error(channel_data["error"])
                else:
                    st.session_state.channel_data = channel_data
                    st.success(f"Fetched analytics for: {channel_data['Channel Name']}")
                    st.write(channel_data)

            st.sidebar.header("Input Video Details")
            video_title = st.sidebar.text_input("Enter Video Title (optional):")

            if st.sidebar.button("Fetch Video Metadata"):
                with st.spinner("Fetching video metadata..."):
                    video_data = fetch_video_metadata(youtube, channel_name, video_title)

                if "error" in video_data:
                    st.error(video_data["error"])
                else:
                    st.success("Fetched video data successfully!")
                    video_data_df = pd.DataFrame(video_data)
                    st.write("### Video Metadata")
                    st.dataframe(video_data_df)
                    visualize_essential_metrics(video_data_df)

        elif app_page == "Bug Reports":
            st.title("Bug Reports")
            st.write("Report or view system bugs here.")

        elif app_page == "System Alerts":
            st.title("System Alerts")
            st.write("View system alerts and notifications.")

        elif app_page == "Search":
            st.title("Search for YouTube Insights")
            st.sidebar.header("Fetch Comments")
            channel_name = st.sidebar.text_input("Enter YouTube Channel Name:")
            video_title = st.sidebar.text_input("Enter Video Title:")

            if st.sidebar.button("Fetch and Save Comments"):
                with st.spinner("Fetching comments..."):
                    result = get_video_comments(youtube, channel_name, video_title)

                if "saved" in result:
                    st.success(result)
                    df = pd.read_csv("comments.csv")
                    st.write("### Sample Comments")
                    st.dataframe(df.head(10))
                else:
                    st.error(result)

        elif app_page == "History":
            st.title("History")
            st.write("View your past searches and analytics.")

    else:
        st.title("Login Page")
        login()

if __name__ == "__main__":
    main()
