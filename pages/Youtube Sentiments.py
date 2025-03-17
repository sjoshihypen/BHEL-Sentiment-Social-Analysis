import streamlit as st
import re
import os 
import base64
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from googleapiclient.discovery import build
from textblob import TextBlob
from datetime import datetime, timedelta
from googleapiclient.errors import HttpError

# Set API Key for YouTube Data API v3
YOUTUBE_API_KEY = "AIzaSyDRJnYZ920R2Xr71GLoaWCbZ14u3xF0arg"
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# Streamlit Configuration
st.set_page_config(page_title="BHEL: YouTube Sentiment Analysis", layout="wide")

# ============================ INLINE IMAGE ENCODING ============================ #
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Path to the uploaded image
image_path = "D:/BHEL Sentiment Social Analysis/Images/bhel.png"  # Ensure correct path
image_base64 = get_image_base64(image_path) if os.path.exists(image_path) else None

# ============================ HEADER SECTION ============================ #
st.markdown(
    f"""
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <h1>BHEL: YouTube Sentiment Analysis</h1>
        {'<img src="data:image/png;base64,' + image_base64 + '" style="width: 200px; height: 120px;">' if image_base64 else ''}
    </div>
    """,
    unsafe_allow_html=True
)

st.write("  ")
st.write("  ")


# Sidebar Features
with st.sidebar:
    st.title("Key Features:")
    st.write(
        """
        ✅ **Secure Authentication.**\n
        ✅ **Scrape YouTube Videos & Comments.**\n
        ✅ **Perform Sentiment Analysis.**\n
        ✅ **Engagement Statistics & Sentiment Breakdown.**\n
        ✅ **Downloadable CSV Reports.**\n
        ✅ **Visualizations with Graphs & Charts.**\n
        """
    )

# Custom CSS for styling
st.markdown(
    """
    <style>
    .stRadio [role=radiogroup] {
        display: flex;
        justify-content: space-between;  
        gap: 20px;  
        width: 100%;  
    }
    .stTextInput>div>div {
        width: 100% !important;
    }
    .centered-button {
        display: flex;
        justify-content: center;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to validate YouTube URL
def is_valid_youtube_url(url):
    pattern = r"(https?:\/\/)?(www\.)?(youtube\.com\/(channel\/[\w-]+|@[\w-]+|user\/[\w-]+|c\/[\w-]+|watch\?v=[\w-]+))"
    return bool(re.match(pattern, url))

# Function to extract Channel ID from URL using API
def get_channel_id(youtube_url):
    try:
        if "channel/" in youtube_url:
            return youtube_url.split("channel/")[1].split("?")[0]
        elif "@" in youtube_url:
            username = youtube_url.split("@")[1].split("/")[0]
            request = youtube.search().list(part="id", q=username, type="channel", maxResults=1)
            response = request.execute()
            if response["items"]:
                return response["items"][0]["id"]["channelId"]
        else:
            return None
    except HttpError as e:
        st.error(f"❌ API Error: {e}")
        return None

# Function to fetch videos within the selected time frame
def fetch_videos(channel_id, duration):
    try:
        end_date = datetime.utcnow()
        if duration == "Weekly (7 Days)":
            start_date = end_date - timedelta(days=7)
        elif duration == "Monthly (30 Days)":
            start_date = end_date - timedelta(days=30)
        else:  # Yearly (365 Days)
            start_date = end_date - timedelta(days=365)

        start_date = start_date.isoformat("T") + "Z"
        video_data = []
        next_page_token = None

        while True:
            request = youtube.search().list(
                part="id,snippet",
                channelId=channel_id,
                order="date",
                maxResults=50,  
                publishedAfter=start_date,
                pageToken=next_page_token
            )
            response = request.execute()

            for item in response.get("items", []):
                video_id = item["id"].get("videoId")
                if video_id:
                    title = item["snippet"]["title"]
                    published_at = item["snippet"]["publishedAt"]

                    # Fetch video statistics (including views)
                    stats_request = youtube.videos().list(part="statistics", id=video_id)
                    stats_response = stats_request.execute()
                    view_count = stats_response["items"][0]["statistics"].get("viewCount", "0")

                    video_data.append((video_id, title, published_at, int(view_count)))

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break  

        return video_data
    except HttpError as e:
        st.error(f"❌ API Error: {e}")
        return []

# Function to fetch comments from a video
def fetch_comments(video_id):
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
            maxResults=100
        )
        response = request.execute()

        comments = []
        for item in response.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)

        return comments
    except HttpError:
        return []

# Function to perform sentiment analysis
def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# Function to process videos and extract sentiments
def process_videos(video_data):
    results = []
    total_positive, total_neutral, total_negative = 0, 0, 0

    for i, (video_id, title, published_at, views) in enumerate(video_data):
        comments = fetch_comments(video_id)
        positive, neutral, negative = 0, 0, 0

        for comment in comments:
            sentiment = analyze_sentiment(comment)
            if sentiment == "Positive":
                positive += 1
            elif sentiment == "Neutral":
                neutral += 1
            else:
                negative += 1

        results.append([i + 1, title, published_at, len(comments), views, positive, neutral, negative])
        total_positive += positive
        total_neutral += neutral
        total_negative += negative

    df = pd.DataFrame(results, columns=["S.No", "Title", "Uploaded Date", "Total Comments", "Views", "Positive", "Neutral", "Negative"])
    return df, total_positive, total_neutral, total_negative

# Initialize Session State for user selections
if "analysis_duration" not in st.session_state:
    st.session_state.analysis_duration = "Weekly (7 Days)"

# URL Input Field with Proper Alignment
col1, col2 = st.columns([1, 2])  # Adjust column width for alignment
with col1:
    st.markdown("<b>Enter / Paste YouTube Profile URL:</b>", unsafe_allow_html=True)
with col2:
    url = st.text_input("", key="profile_url", label_visibility="collapsed")

# Select Analysis Duration
st.markdown("### **Select Analysis Duration:**")
selected_duration = st.radio(
    "",
    ["Weekly (7 Days)", "Monthly (30 Days)", "Yearly (365 Days)"],
    index=["Weekly (7 Days)", "Monthly (30 Days)", "Yearly (365 Days)"].index(st.session_state.analysis_duration),
    horizontal=True
)

# Update session state when duration changes
if selected_duration != st.session_state.analysis_duration:
    st.session_state.analysis_duration = selected_duration

# Centered Analyze Button
st.markdown("<br>", unsafe_allow_html=True)
col_space1, col_button, col_space2 = st.columns([3, 1, 3])
with col_button:
    analyze_clicked = st.button(f"**Analyze**")

if analyze_clicked:
    if not url:
        st.warning("⚠️ Please enter a YouTube Profile URL.")
    elif not is_valid_youtube_url(url):
        st.error("❌ Invalid YouTube URL! Please enter a correct profile link.")
    else:
        st.success(f"✅ Analysis for {selected_duration} has started!")
        
        channel_id = get_channel_id(url)
        if channel_id:
            video_data = fetch_videos(channel_id, selected_duration)
            if video_data:
                df, pos, neu, neg = process_videos(video_data)

                # Display Dashboard Summary & Sentiment Breakdown
                with st.container():
                    col1, col2 = st.columns([4, 2])

                    with col1:
                        st.subheader("**Dashboard Summary**")
                        st.markdown(f"**Positive Comments ✅:** {pos}")
                        st.markdown(f"**Neutral  Comments 😐:** {neu}")
                        st.markdown(f"**Negative Comments ❌:** {neg}")
                        st.markdown(f"**Total Posts / Videos:** {len(df)}")  

                    with col2:
                        # Doughnut Chart for Sentiment Distribution
                        labels = ["Positive", "Neutral", "Negative"]
                        sizes = [pos, neu, neg]
                        colors = ["blue", "yellow", "red"]

                        fig, ax = plt.subplots(figsize=(3.5, 3.5))  
                        ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors, 
                               wedgeprops={"edgecolor": "black", "linewidth": 1})

                        center_circle = plt.Circle((0, 0), 0.70, fc="white")
                        fig.gca().add_artist(center_circle)
                        st.pyplot(fig)

                # Display Extracted Data
                st.subheader("Extracted Data")
                st.dataframe(df)

                # Centered Analyze Button
                st.markdown("<br>", unsafe_allow_html=True)
                col_space1, col_button, col_space2 = st.columns([4, 3, 4])
                with col_button:
                    download_clicked = st.download_button(label="**📥 Download CSV**", data=df.to_csv(index=False), file_name="Youtube_Sentiments_Analysis.csv", mime="text/csv")
                # Download Button
                # st.download_button(label="📥 Download CSV", data=df.to_csv(index=False), file_name="Youtube Sentiments Analysis.csv", mime="text/csv")

            else:
                st.warning("⚠️ No videos found in the selected time frame!")
        else:
            st.error("❌ Could not extract Channel ID! Please check your URL.")

st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center;">
        <strong>© 2025 BHEL Social Sentiment Analysis. All rights reserved.</strong><br>
        <strong>Unauthorized use or duplication is strictly prohibited.</strong><br>
        <strong>Developed by : Sushant Joshi, Intern BHEL.</strong>
    </div>
""", unsafe_allow_html=True)
