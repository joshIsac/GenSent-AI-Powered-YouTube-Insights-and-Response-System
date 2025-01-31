import os
import re
import string
import nltk
import pandas as pd
from googleapiclient.discovery import build
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download NLTK resources
nltk.download("stopwords")
nltk.download("wordnet")

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()


def get_video_comments(youtube, channel_name, video_title):
    comments = []

    #  Get Channel ID from Channel Name
    search_response = youtube.search().list(
        part="snippet",
        q=channel_name,
        type="channel",
        maxResults=1
    ).execute()

    if not search_response["items"]:
        return "Channel not found."

    channel_id = search_response["items"][0]["id"]["channelId"]

    #  Get Video ID from Video Title
    video_search = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        q=video_title,
        type="video",
        maxResults=1
    ).execute()

    if not video_search["items"]:
        return "Video not found."

    video_id = video_search["items"][0]["id"]["videoId"]

    #  Fetch Comments
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText",
        maxResults=50
    )
    
    response = request.execute()

    for item in response.get("items", []):
        comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comments.append(comment)

    return comments


#Preprocess Text

def preprocess_text(text):
    # Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    # Convert text to lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    # Remove numbers
    text = re.sub(r"\d+", "", text)
    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    words = text.split()
    text = " ".join([word for word in words if word not in stop_words])
    # Lemmatize text
    text = " ".join([lemmatizer.lemmatize(word) for word in text.split()])
    # Remove symbols
    text = re.sub(r"[^\w\s]", "", text)
    return text


def fetch_and_preprocess_comments(youtube, channel_name, video_title):
    comments = get_video_comments(youtube, channel_name, video_title)

    if isinstance(comments, str):
        return comments  # Return error message if no video/channel found

    # Preprocess comments
    processed_comments = [preprocess_text(comment) for comment in comments]

    # Save to CSV
    df = pd.DataFrame({"Original Comment": comments, "Processed Comment": processed_comments})
    file_path = "processed_comments.csv"
    df.to_csv(file_path, index=False)

    return file_path, df
