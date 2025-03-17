import streamlit as st
import re
import os
import base64
import tweepy
import numpy as np
import matplotlib.pyplot as plt

# Set Streamlit page configuration
st.set_page_config(page_title="BHEL: X Sentiment Analysis", layout="wide")

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
        <h1>BHEL: X Sentiment Analysis</h1>
        {'<img src="data:image/png;base64,' + image_base64 + '" style="width: 200px; height: 120px;">' if image_base64 else ''}
    </div>
    """,
    unsafe_allow_html=True
)

st.write("  ")
st.write("  ")

# API Credentials (Store in Streamlit Secrets for Security)
API_KEY = st.secrets["TWITTER"]["TWITTER_API_KEY"]
API_SECRET = st.secrets["TWITTER"]["TWITTER_API_SECRET"]
ACCESS_TOKEN = st.secrets["TWITTER"]["TWITTER_ACCESS_TOKEN"]
ACCESS_SECRET = st.secrets["TWITTER"]["TWITTER_ACCESS_SECRET"]

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

with st.sidebar:
        st.title(f"Key Features:")
        st.write(
            """
            ✅ **Secure Authentication (Stored in Streamlit Secrets).**\n
            ✅ **Scrape X Posts, Videos.**\n
            ✅ **Extract Comments & Perform Sentiment Analysis.**\n
            ✅ **Engagement Statistics & Sentiment Breakdown.**\n
            ✅ **Visualizations with Graphs & Charts.**\n
            ✅ **Downloadable CSV Reports.**\n
     """)
st.write("\n\n")

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

# Function to validate X URL
def is_valid_x_url(url):
    x_pattern = r"^(https?:\/\/)?(www\.)?x\.com\/[A-Za-z0-9_]+$"
    return bool(re.match(x_pattern, url))

# Fetch X Posts and Media
def fetch_x_posts(username, count=20):
    try:
        tweets = api.user_timeline(screen_name=username, count=count, tweet_mode="extended")
        posts = []
        for tweet in tweets:
            media_urls = []
            if 'media' in tweet.entities:
                media_urls = [media['media_url'] for media in tweet.entities['media']]
            posts.append({
                "text": tweet.full_text,
                "likes": tweet.favorite_count,
                "retweets": tweet.retweet_count,
                "media": media_urls
            })
        return posts
    except Exception as e:
        st.error(f"Error fetching posts: {e}")
        return []

# Initialize Session State for user selections
if "analysis_duration" not in st.session_state:
    st.session_state.analysis_duration = "Weekly (7 Days)"

# URL Input Field with Proper Alignment
col1, col2 = st.columns([1, 2])  # Adjust column width for alignment
with col1:
    st.markdown("<b>Enter / Paste X Profile URL:</b>", unsafe_allow_html=True)
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

# Perform Analysis when button is clicked
if analyze_clicked:
    if not url:
        st.warning("⚠️ Please enter a X Profile URL.")
    elif not is_valid_x_url(url):
        st.error("❌ Invalid X URL! Please enter a correct profile link.")
    else:
        st.success(f"✅ Analysis for {st.session_state.analysis_duration} has started!")

        # Simulating sentiment analysis (Replace with actual API or Model)
        np.random.seed(42)
        positive_comments = np.random.randint(50, 200)
        neutral_comments = np.random.randint(20, 100)
        negative_comments = np.random.randint(10, 80)

        # Dashboard Summary
        with st.container():
            col1, col2 = st.columns([4, 2])
            with col1:
                st.subheader("**Dashboard Summary**")
                st.markdown(f"**Positive Comments ✅ :** {positive_comments}")
                st.markdown(f"**Neutral  Comments 😐:** {neutral_comments}")
                st.markdown(f"**Negative Comments ❌:** {negative_comments}")
                st.markdown("**Total Posts / Videos:** _Coming Soon_")  # Placeholder for total posts

            with col2:
                # Doughnut Chart for Sentiment Distribution
                labels = ["Positive", "Neutral", "Negative"]
                sizes = [positive_comments, neutral_comments, negative_comments]
                colors = ["green", "yellow", "red"]

                fig, ax = plt.subplots(figsize=(3.5, 3.5))  # Adjust figure size
                wedges, texts, autotexts = ax.pie(
                    sizes,
                    labels=labels,
                    autopct="%1.1f%%",
                    startangle=90,
                    colors=colors,
                    wedgeprops={"edgecolor": "black", "linewidth": 1},
                    textprops={"fontsize": 10, "weight": "bold"}
                )

                # Draw a white circle in the center to create a doughnut chart
                center_circle = plt.Circle((0, 0), 0.70, fc="white")
                fig.gca().add_artist(center_circle)

                # Display the chart
                st.pyplot(fig)

st.markdown("""
    <div style="text-align: center;">
        <strong>© 2025 BHEL Social Sentiment Analysis. All rights reserved.</strong><br>
        <strong>Unauthorized use or duplication is strictly prohibited.</strong><br>
        <strong>Developed by : Sushant Joshi & Intern BHEL.</strong>
    </div>
""", unsafe_allow_html=True)
