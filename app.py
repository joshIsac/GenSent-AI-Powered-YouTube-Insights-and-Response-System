import streamlit as st
import sys
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Add GitHub repository path for additional scripts
sys.path.append("D:/GitHub/GenSent-AI-Powered-YouTube-Insights-and-Response-System/scripts")

from scripts.fetch_channel_data import fetch_channel_statistics,fetch_channel_id
from scripts.fetch_video_stats import fetch_video_metadata,trending_video_region
from scripts.visualisation import visualize_essential_metrics
from scripts.sentiment_analysis import get_video_comments, preprocess_text, fetch_and_preprocess_comments


# Load API Key from environment variables
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

# Initialize YouTube API client
def initialize_youtube_api():
    youtube = build("youtube", "v3", developerKey=API_KEY)
    return youtube


# Function to fetch and display channel statistics
def fetch_and_display_channel_data(youtube,channel_name):
    if channel_name.strip():
        with st.spinner("Fetching channel analytics..."):
            channel_data = fetch_channel_statistics(youtube, channel_name)
        
        if "error" in channel_data:
            st.error(channel_data["error"])
        else:
            st.session_state.channel_data=channel_data
            st.success(f"Fetched analytics for: {channel_data['Channel Name']}")
            st.write(f"**Channel Name**: {channel_data['Channel Name']}")
            st.write(f"**Subscribers**: {channel_data['Subscribers']}")
            st.write(f"**Total Views**: {channel_data['Total Views']}")
            st.write(f"**Video Count**: {channel_data['Video Count']}")
            st.write(f"**Description**: {channel_data['Channel Description']}")
            st.write(f"**Country**: {channel_data['Country']}")
            st.write(f"**Created On**: {channel_data['Created Date']}")




# Function to fetch and display video metadata
def fetch_and_display_video_data(youtube,channel_name, video_title=None):
    if channel_name.strip():
        
        with st.spinner("Fetching video metadata..."):
            video_data = fetch_video_metadata(youtube, channel_name, video_title)
        
        if "error" in video_data:
            st.error(video_data["error"])
        else:
            st.success("Fetched video data successfully!")
            video_data_df = pd.DataFrame(video_data)  # Convert list of video data to DataFrame

            # Display video data in a table
            st.write("### Video Metadata")
            st.dataframe(video_data_df)

            # Visualize essential metrics
            st.write("### Visualizations")
            visualize_essential_metrics(video_data_df)

        

def fetch_and_display_trending_videos(youtube,region_code="US"):
    with st.spinner("Fetching trending videos..."):
        trending_data = trending_video_region(youtube, region_code=region_code)
    
    if "error" in trending_data:
        st.error(trending_data["error"])
    else:
        st.success(f"Trending videos in region: {trending_data['Region Codes'].get(region_code, 'Unknown')}")
        trending_videos_data = pd.DataFrame(trending_data["Trending Videos"])

        # Display trending videos in a table
        st.write("### Trending Videos")
        st.dataframe(trending_videos_data)


        # Visualize essential metrics
        st.write("### Visualizations for Trending Videos")
        visualize_essential_metrics(trending_videos_data)


# Function to fetch and preprocess video comments
def fetch_and_display_video_comments(youtube, channel_name, video_title):
    if not channel_name or not video_title:
        st.error("Please enter both a channel name and a video title.")
        return

    with st.spinner("Fetching and preprocessing comments..."):
        comments = get_video_comments(youtube, channel_name, video_title)

        if not comments:
            st.warning("No comments found for this video.")
            return

        # Convert comments to DataFrame
        comments_df = pd.DataFrame(comments, columns=["Original Comments"])

        # Preprocess the comments
        comments_df["Processed Comments"] = comments_df["Original Comments"].apply(preprocess_text)

        # Display comments in Streamlit
        st.write("### Original Comments")
        st.dataframe(comments_df[["Original Comments"]])

        st.write("### Processed Comments")
        st.dataframe(comments_df[["Processed Comments"]])

        # Save processed comments as CSV
        comments_df.to_csv("processed_comments.csv", index=False)
        st.success("Processed comments saved as 'processed_comments.csv'.")



# Main Streamlit App
def main():
    st.title("GenSent: YouTube Channel and Video Insights")
    st.write(
        """Welcome to GenSent, a cutting-edge AI-powered system designed to provide you with in-depth YouTube channel insights 
        and automated comment analysis. Just enter the name of a YouTube channel, 
        and explore real-time analytics!"""
    )


    # Initialize YouTube API only once
    youtube = initialize_youtube_api()

    # Sidebar: Select features
    st.sidebar.title("GenSent")
    st.sidebar.header("Input Channel Details")
    channel_name = st.sidebar.text_input("Enter YouTube Channel Name:")

    if st.sidebar.button("Fetch Channel Analytics"):
        fetch_and_display_channel_data(channel_name)

    st.sidebar.header("Input Video Details")
    video_title = st.sidebar.text_input("Enter Video Title (optional):")

    if st.sidebar.button("Fetch Video Metadata"):
        fetch_and_display_video_data(channel_name, video_title)

    st.sidebar.header("Trending Videos")
    region_code = st.sidebar.selectbox("Select Region Code:", ["US", "IN", "GB", "CA", "AU", "JP", "KR"])

    if st.sidebar.button("Fetch Trending Videos"):
        fetch_and_display_trending_videos(region_code)


    st.sidebar.header("Fetch & Preprocess Video Comments")
    st.sidebar.write("Enter a YouTube channel and video title to extract comments.")
    
    comment_channel_name = st.sidebar.text_input("Channel Name for Comments:")
    comment_video_title = st.sidebar.text_input("Video Title for Comments:")

    if st.sidebar.button("Fetch and Preprocess Comments"):
        fetch_and_display_video_comments(youtube, comment_channel_name, comment_video_title)

if __name__ == "__main__":
    main()
