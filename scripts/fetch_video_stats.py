from googleapiclient.errors import HttpError
from scripts.engagement_rate import calculate_engagement_rate
import os
import pandas as pd

# save the video data 
def save_to_csv(video_data, file_name="video_insights.csv"):
    """
    Save video data to a CSV file.
    :param video_data: List of video dictionaries to save.
    :param file_name: Name of the output CSV file.
    """
    df = pd.DataFrame(video_data)
    df.to_csv(file_name, index=False)
    if not os.path.exists(file_name):
        raise FileNotFoundError(f"{file_name} was not created successfully.")
    if df.empty:
        raise ValueError("The CSV file is empty after saving.")
    print(f"Video data saved to {file_name}")



def fetch_video_metadata(youtube, channel_name, video_title=None, max_videos=15):
    try:
        # Search for the channel ID by channel name
        search_response = youtube.search().list(q=channel_name, part="snippet", type="channel", maxResults=1).execute()
        if not search_response["items"]:
            return {"error": "Channel not found!"}

        channel_id = search_response["items"][0]["id"]["channelId"]

        # Search for videos in the channel
        video_search_response = youtube.search().list(
            q=video_title if video_title else "",
            part="snippet",
            type="video",
            channelId=channel_id,
            maxResults=max_videos
        ).execute()

        if not video_search_response["items"]:
            return {"error": f"No videos found in channel '{channel_name}'!"}

        video_data_list = []
        for video_item in video_search_response["items"]:
            video_id = video_item["id"]["videoId"]

            # Fetch video details (views, likes, comments, etc.)
            video_details = youtube.videos().list(
                part="snippet,statistics",
                id=video_id
            ).execute()

            if not video_details["items"]:
                continue  # Skip if no details are found

            video_info = video_details["items"][0]
            snippet = video_info["snippet"]
            statistics = video_info["statistics"]

            # Get video metrics safely, with fallback to 0 if missing
            views = int(statistics.get("viewCount", 0))
            likes = int(statistics.get("likeCount", 0))
            comments = int(statistics.get("commentCount", 0))

            # Calculate engagement rate (using default value 0 for potential missing data)
            engagement_rate = calculate_engagement_rate(0, views, comments, likes)

            # Prepare video metadata
            video_data = {
                "Video Title": snippet["title"],
                "Video ID": video_id,
                "Published Date": snippet.get("publishedAt", "N/A"),
                "Views": views,
                "Likes": likes,
                "Comments": comments,
                "Engagement Rate (%)": round(engagement_rate, 2)
            }
            video_data_list.append(video_data)

        if not video_data_list:
            return {"error": f"No valid videos found for channel '{channel_name}'!"}

        # Save all video data to CSV
        save_to_csv(video_data_list, "video_insights.csv")
        return video_data_list

    except Exception as e:
        return {"error": f"Error fetching video metadata: {str(e)}"}
    


    

def trending_video_region(youtube,region_code="US",max_results=25):
    #List of region codes and their respective countries
    region_codes = {
        "US": "United States",
        "IN": "India",
        "GB": "United Kingdom",
        "CA": "Canada",
        "AU": "Australia",
        "DE": "Germany",
        "FR": "France",
        "JP": "Japan",
        "KR": "South Korea",
        "BR": "Brazil",
        "ZA": "South Africa",
    }

    try:
        # Fetch trending videos using the YouTube API
        trending_response = youtube.videos().list(
            part="snippet,statistics",
            chart="mostPopular",
            regionCode=region_code,
            maxResults=max_results
        ).execute()

        if not trending_response["items"]:
            return {"error": f"No trending videos found for region code '{region_code}'!"}
        
        trending_videos = []

        # Iterate through each trending video and collect statistics
        for video in trending_response["items"]:
            video_id = video["id"]
            snippet = video["snippet"]
            statistics = video["statistics"]

            # Fetch details and calculate engagement rate
            views = int(statistics.get("viewCount", 0))
            likes = int(statistics.get("likeCount", 0))
            comments = int(statistics.get("commentCount", 0))
            engagement_rate = calculate_engagement_rate(0, views, comments, likes)

            # Store video data
            video_data = {
                "Video Title": snippet["title"],
                "Video ID": video_id,
                "Published Date": snippet.get("publishedAt", "N/A"),
                "Views": views,
                "Likes": likes,
                "Comments": comments,
                "Engagement Rate (%)": round(engagement_rate, 2)
            }
            trending_videos.append(video_data)

        # Save the trending videos data to CSV
        save_to_csv(trending_videos, f"trending_videos_{region_code}.csv")

        # Add the dropdown list for region codes
        return {
            "Region Codes": region_codes,
            "Selected Region": region_code,
            "Trending Videos": trending_videos,
        }

    except HttpError as e:
        return {"error": f"API error: {e}"}
    except Exception as e:
        return {"error": f"Error fetching trending videos: {str(e)}"}
