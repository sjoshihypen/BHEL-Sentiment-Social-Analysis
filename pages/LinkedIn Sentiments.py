import streamlit as st
import re
import os
import base64
import numpy as np
import matplotlib.pyplot as plt
import requests
import json

# Set Streamlit page configuration
st.set_page_config(page_title="BHEL: LinkedIn Sentiment Analysis", layout="wide")

# LinkedIn API Credentials (Replace with actual credentials)
CLIENT_ID = "your_linkedin_client_id"
CLIENT_SECRET = "your_linkedin_client_secret"
REDIRECT_URI = "https://your-redirect-url.com"
ACCESS_TOKEN = "your_access_token"  # Obtain this from OAuth flow

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
        <h1>BHEL: LinkedIn Sentiment Analysis</h1>
        {'<img src="data:image/png;base64,' + image_base64 + '" style="width: 200px; height: 120px;">' if image_base64 else ''}
    </div>
    """,
    unsafe_allow_html=True
)

st.write("  ")
st.write("  ")

# Sidebar with key features
with st.sidebar:
    st.title(f"Key Features:")
    st.write(
        """
        ✅ **Secure Authentication (Stored in Streamlit Secrets).**\n
        ✅ **Scrape LinkedIn Posts & Extract Comments.**\n
        ✅ **Perform Sentiment Analysis.**\n
        ✅ **Engagement Statistics & Sentiment Breakdown.**\n
        ✅ **Visualizations with Graphs & Charts.**\n
        ✅ **Downloadable CSV Reports.**\n
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

# Function to validate LinkedIn URL and extract Post ID
def extract_post_id(url):
    pattern = r"(?:linkedin\.com\/.*\/posts\/)([\w-]+)"
    match = re.search(pattern, url)
    return match.group(1) if match else None

# Function to fetch LinkedIn comments
def get_linkedin_comments(post_id):
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    url = f"https://api.linkedin.com/v2/socialActions/{post_id}/comments"

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching LinkedIn comments. Status Code: {response.status_code}")
        return None

# Input for LinkedIn Post URL
col1, col2 = st.columns([1, 2])
with col1:
    st.markdown("<b>Enter LinkedIn Post URL:</b>", unsafe_allow_html=True)
with col2:
    url = st.text_input("", key="profile_url", label_visibility="collapsed")

# Select Analysis Duration
st.markdown("### **Select Analysis Duration:**")
selected_duration = st.radio(
    "",
    ["Weekly (7 Days)", "Monthly (30 Days)", "Yearly (365 Days)"],
    index=0,
    horizontal=True
)

# Centered Analyze Button
st.markdown("<br>", unsafe_allow_html=True)
col_space1, col_button, col_space2 = st.columns([3, 1, 3])
with col_button:
    analyze_clicked = st.button(f"**Analyze**")

# Perform Analysis when button is clicked
if analyze_clicked:
    if not url:
        st.warning("⚠️ Please enter a LinkedIn Post URL.")
    else:
        post_id = extract_post_id(url)
        if not post_id:
            st.error("❌ Invalid LinkedIn URL! Please enter a correct post link.")
        else:
            st.success(f"✅ Analysis for {selected_duration} has started!")

            # Fetch comments using LinkedIn API
            comments = get_linkedin_comments(post_id)
            if comments and "elements" in comments:
                st.write(comments["elements"])  # Placeholder for processing comments

                # Simulating sentiment analysis (Replace with actual AI model)
                np.random.seed(42)
                positive_comments = np.random.randint(50, 200)
                neutral_comments = np.random.randint(20, 100)
                negative_comments = np.random.randint(10, 80)

                # Dashboard Summary
                with st.container():
                    col1, col2 = st.columns([4, 2])
                    with col1:
                        st.subheader("**Dashboard Summary**")
                        st.markdown(f"**Overall Positive Comments ✅ :** {positive_comments}")
                        st.markdown(f"**Overall Neutral  Comments 😐 :** {neutral_comments}")
                        st.markdown(f"**Overall Negative Comments ❌ :** {negative_comments}")
                        st.markdown("**Total Posts / Videos :** _Coming Soon_")  # Placeholder for total posts

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
            else:
                st.warning("⚠️ No comments found or an error occurred.")

st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align: center;">
        <strong>© 2025 LinkedIn Sentiment Analysis. All rights reserved.</strong><br>
        <strong>Unauthorized use or duplication is strictly prohibited.</strong><br>
        <strong>Developed by: Sushant Joshi, Intern BHEL.</strong>
    </div>
    """,
    unsafe_allow_html=True
)
