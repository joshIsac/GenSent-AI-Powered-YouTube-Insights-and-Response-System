import streamlit as st
import sys
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
import pandas as pd

# Add GitHub repository path for additional scripts
sys.path.append("D:/GitHub/GenSent-AI-Powered-YouTube-Insights-and-Response-System/scripts")

from scripts.fetch_channel_data import fetch_channel_statistics
from scripts.fetch_video_stats import fetch_video_metadata, trending_video_region
from scripts.visualisation import visualize_essential_metrics

# Load API Key from environment variables
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

# Initialize YouTube API client
def initialize_youtube_api():
    return build("youtube", "v3", developerKey=API_KEY)

# Function to fetch and display channel statistics
def fetch_and_display_channel_data(channel_name):
    if channel_name.strip():
        youtube = initialize_youtube_api()
        with st.spinner("Fetching channel analytics..."):
            channel_data = fetch_channel_statistics(youtube, channel_name)
        
        if "error" in channel_data:
            st.error(channel_data["error"])
        else:
            st.success(f"Fetched analytics for: {channel_data['Channel Name']}")
            st.write(f"**Subscribers**: {channel_data['Subscribers']}")
            st.write(f"**Total Views**: {channel_data['Total Views']}")
            st.write(f"**Video Count**: {channel_data['Video Count']}")
            st.write(f"**Description**: {channel_data['Channel Description']}")
            st.write(f"**Country**: {channel_data['Country']}")
            st.write(f"**Created On**: {channel_data['Created Date']}")

# Function to fetch and display video metadata
def fetch_and_display_video_data(channel_name, video_title=None):
    if channel_name.strip():
        youtube = initialize_youtube_api()
        with st.spinner("Fetching video metadata..."):
            video_data = fetch_video_metadata(youtube, channel_name, video_title)
        
        if "error" in video_data:
            st.error(video_data["error"])
        else:
            st.success("Fetched video data successfully!")
            video_data_df = pd.DataFrame(video_data)

            st.write("### Video Metadata")
            st.dataframe(video_data_df)

            st.write("### Visualizations")
            visualize_essential_metrics(video_data_df)

# Function to fetch and display trending videos
def fetch_and_display_trending_videos(region_code="US"):
    youtube = initialize_youtube_api()
    with st.spinner("Fetching trending videos..."):
        trending_data = trending_video_region(youtube, region_code=region_code)
    
    if "error" in trending_data:
        st.error(trending_data["error"])
    else:
        st.success(f"Trending videos in region: {trending_data['Region Codes'].get(region_code, 'Unknown')}")
        trending_videos_data = pd.DataFrame(trending_data["Trending Videos"])
        
        st.write("### Trending Videos")
        st.dataframe(trending_videos_data)

        st.write("### Visualizations")
        visualize_essential_metrics(trending_videos_data)

# Streamlit Multi-Page Navigation
def main():
    st.title("GenSent: AI-Powered YouTube Insights")
    
    page = st.sidebar.radio(
        "Navigate", 
        ["Home", "Channel Analytics", "Video Insights", "Trending Videos", "Sentiment Analysis"]
    )

    if page == "Home":
        st.write("""
        ### Welcome to GenSent
        Gain AI-powered insights into YouTube channels, video performance, and sentiment analysis on comments.
        Use the sidebar to navigate through different sections.
        """)

    elif page == "Channel Analytics":
        st.subheader("YouTube Channel Analytics")
        channel_name = st.text_input("Enter YouTube Channel Name:")
        if st.button("Fetch Channel Analytics"):
            fetch_and_display_channel_data(channel_name)

    elif page == "Video Insights":
        st.subheader("Video Metadata & Analysis")
        channel_name = st.text_input("Enter YouTube Channel Name:")
        video_title = st.text_input("Enter Video Title (optional):")
        if st.button("Fetch Video Metadata"):
            fetch_and_display_video_data(channel_name, video_title)

    elif page == "Trending Videos":
        st.subheader("Trending Videos Insights")
        region_code = st.selectbox("Select Region Code:", ["US", "IN", "GB", "CA", "AU", "JP", "KR"])
        if st.button("Fetch Trending Videos"):
            fetch_and_display_trending_videos(region_code)

    elif page == "Sentiment Analysis":
        st.subheader("YouTube Comment Sentiment Analysis (Coming Soon!)")
        st.write("This feature will analyze comments for sentiment using AI.")

if __name__ == "__main__":
    main()
