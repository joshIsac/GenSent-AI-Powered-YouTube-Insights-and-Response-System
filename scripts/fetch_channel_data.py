from googleapiclient.discovery import build
import matplotlib.pyplot as plt
import csv
from datetime import datetime
import os 
import time




#fetch live statistics
def fetch_channel_id(youtube, channel_name):
    """
    Fetch the Channel ID from the YouTube Data API by searching with a channel name.
    """
    try:
        search_response = youtube.search().list(
            q=channel_name, part="snippet", type="channel", maxResults=1
        ).execute()

        if not search_response["items"]:
            return {"error": "Channel not found!"}

        # Extract channel ID
        channel_id = search_response["items"][0]["id"]["channelId"]
        return {"channel_id": channel_id}
    
    except Exception as e:
        return {"error": f"Error fetching channel ID: {str(e)}"}
    



def fetch_channel_statistics(youtube, channel_name):
    """
    Fetch the channel statistics and related metadata for analytics.
    """
    try:
        # Fetch the Channel ID
        channel_id_response = fetch_channel_id(youtube, channel_name)
        if "error" in channel_id_response:
            return channel_id_response  # Propagate the error if fetching ID fails

        channel_id = channel_id_response["channel_id"]

        # Fetch channel statistics using the Channel ID
        channel_response = youtube.channels().list(
            part="snippet,statistics", id=channel_id
        ).execute()

        if not channel_response["items"]:
            return {"error": "Unable to retrieve channel statistics!"}

        # Extract statistics and snippet information
        stats = channel_response["items"][0]["statistics"]
        snippet = channel_response["items"][0]["snippet"]

        # Prepare the channel data dictionary
        channel_data = {
            "Channel ID": channel_id,
            "Channel Name": snippet["title"],
            "Channel Description": snippet.get("description", "N/A"),
            "Subscribers": stats.get("subscriberCount", "N/A"),
            "Total Views": stats.get("viewCount", "N/A"),
            "Video Count": stats.get("videoCount", "N/A"),
            "Created Date": snippet.get("publishedAt", "N/A"),
            "Country": snippet.get("country", "N/A"),
        }

        return channel_data
    
    
    
    
    

    except Exception as e:
        return {"error": f"Error fetching channel statistics: {str(e)}"}
