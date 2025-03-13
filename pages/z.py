import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import re
import nltk
import matplotlib.pyplot as plt
from datetime import datetime
from nltk.sentiment import SentimentIntensityAnalyzer

# Initialize NLTK sentiment analyzer
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

# Set Streamlit page configuration
st.set_page_config(page_title="LinkedIn Sentiment Analysis", layout="wide")

# Sidebar Features
with st.sidebar:
    st.title("Key Features:")
    st.write(
        """
        ✅ **Extract LinkedIn Posts & Videos**\n
        ✅ **Analyze Comments & Perform Sentiment Analysis**\n
        ✅ **View Total Comments & Engagement Statistics**\n
        ✅ **Download CSV Reports**\n
        ✅ **Interactive Graphs & Charts**\n
        """
    )

# Title
st.title("LinkedIn Sentiment Analysis")

# LinkedIn API Configuration
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"  # Replace with your LinkedIn API Access Token
BASE_URL = "https://api.linkedin.com/v2"

# Validate LinkedIn URL (supporting company and user posts)
def is_valid_linkedin_url(url):
    linkedin_pattern = r"(https?:\/\/)?(www\.)?linkedin\.com\/(company|in)\/([\w-]+)\/?"
    return bool(re.match(linkedin_pattern, url, re.IGNORECASE))

# Extract LinkedIn ID
def extract_linkedin_id(url):
    match = re.search(r"linkedin\.com\/(company|in)\/([\w-]+)", url)
    if match:
        return match.group(2)  # Extracts the ID after 'company/' or 'in/'
    return None

# Fetch LinkedIn Posts
def get_linkedin_posts(profile_id):
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    endpoint = f"{BASE_URL}/ugcPosts?q=authors&authors=urn:li:organization:{profile_id}&count=10"
    
    response = requests.get(endpoint, headers=headers)
    
    if response.status_code == 200:
        posts = response.json().get("elements", [])
        if not posts:
            st.error("❌ No posts found for this profile. The profile may be private or has no recent activity.")
        return posts
    else:
        st.error(f"❌ Failed to fetch posts. API Response: {response.text}")
        return []

# Fetch LinkedIn Comments for a Post
def get_linkedin_comments(post_id):
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    endpoint = f"{BASE_URL}/socialActions/{post_id}/comments"
    
    response = requests.get(endpoint, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("elements", [])
    else:
        st.error(f"❌ Failed to fetch comments for post {post_id}. API Response: {response.text}")
        return []

# Perform Sentiment Analysis
def analyze_sentiment(comment):
    sentiment_score = sia.polarity_scores(comment)
    if sentiment_score["compound"] >= 0.05:
        return "Positive"
    elif sentiment_score["compound"] <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# Input field for LinkedIn profile URL
url = st.text_input("Enter LinkedIn Profile URL:", key="linkedin_url")

# Analyze Button
if st.button("Analyze"):
    if not url:
        st.warning("⚠️ Please enter a LinkedIn Profile URL.")
    elif not is_valid_linkedin_url(url):
        st.error("❌ Invalid LinkedIn URL! Please enter a correct profile link.")
    else:
        profile_id = extract_linkedin_id(url)
        if not profile_id:
            st.error("❌ Unable to extract LinkedIn ID from URL.")
        else:
            st.success(f"✅ Fetching posts for {profile_id}...")
            posts = get_linkedin_posts(profile_id)
            
            if posts:
                # Process Posts
                post_data = []
                for post in posts:
                    post_id = post["id"]
                    text = post.get("specificContent", {}).get("com.linkedin.ugc.ShareContent", {}).get("shareCommentary", {}).get("text", "No caption")
                    timestamp = datetime.fromtimestamp(post["created"]["time"] / 1000).strftime('%Y-%m-%d')
                    
                    # Fetch comments
                    comments = get_linkedin_comments(post_id)
                    total_comments = len(comments)
                    sentiment_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
                    
                    for comment in comments:
                        comment_text = comment.get("message", {}).get("text", "")
                        sentiment = analyze_sentiment(comment_text)
                        sentiment_counts[sentiment] += 1
                    
                    post_data.append({
                        "S.No": len(post_data) + 1,
                        "Post ID": post_id,
                        "Caption": text,
                        "Uploaded Date": timestamp,
                        "Total Comments": total_comments,
                        "Positive Comments": sentiment_counts["Positive"],
                        "Neutral Comments": sentiment_counts["Neutral"],
                        "Negative Comments": sentiment_counts["Negative"]
                    })

                # Convert to DataFrame
                df = pd.DataFrame(post_data)

                # Save to CSV
                csv_file = "linkedin_analysis.csv"
                df.to_csv(csv_file, index=False)

                # Display Table
                st.markdown("### 📋 **Extracted LinkedIn Posts**")
                st.dataframe(df, use_container_width=True)

                # Sentiment Distribution Chart
                st.markdown("### 📊 **Sentiment Breakdown**")
                fig, ax = plt.subplots(figsize=(4, 4))
                labels = ["Positive", "Neutral", "Negative"]
                sizes = [
                    df["Positive Comments"].sum(),
                    df["Neutral Comments"].sum(),
                    df["Negative Comments"].sum()
                ]
                colors = ["green", "yellow", "red"]

                wedges, texts, autotexts = ax.pie(
                    sizes,
                    labels=labels,
                    autopct="%1.1f%%",
                    startangle=90,
                    colors=colors,
                    wedgeprops={"edgecolor": "black", "linewidth": 1},
                    textprops={"fontsize": 10, "weight": "bold"},
                )

                center_circle = plt.Circle((0, 0), 0.70, fc="white")
                fig.gca().add_artist(center_circle)
                st.pyplot(fig)

                # Download CSV Button
                st.markdown("### 📥 **Download Report**")
                st.download_button(
                    label="Download CSV 📄",
                    data=df.to_csv(index=False).encode("utf-8"),
                    file_name="LinkedIn_Sentiment_Analysis.csv",
                    mime="text/csv"
                )
