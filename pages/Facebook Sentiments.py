import streamlit as st
import re
import os
import base64
import numpy as np
import matplotlib.pyplot as plt

# Set Streamlit page configuration
st.set_page_config(page_title="BHEL: Facebook Sentiment Analysis", layout="wide")

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
        <h1>BHEL: Facebook Sentiment Analysis</h1>
        {'<img src="data:image/png;base64,' + image_base64 + '" style="width: 200px; height: 120px;">' if image_base64 else ''}
    </div>
    """,
    unsafe_allow_html=True
)

st.write("  ")
st.write("  ")

# ============================ SIDEBAR FEATURES ============================ #
with st.sidebar:
    st.title("Key Features:")
    st.write(
        """
        ✅ **Secure Authentication (Stored in Streamlit Secrets).**\n
        ✅ **Scrape Facebook Posts, Videos.**\n
        ✅ **Extract Comments & Perform Sentiment Analysis.**\n
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

# Function to validate Facebook URL
def is_valid_facebook_url(url):
    fb_pattern = r"^(https?:\/\/)?(www\.)?facebook\.com\/[a-zA-Z0-9._-]+(\/)?$"
    return bool(re.match(fb_pattern, url))

# Initialize session state for analysis duration
if "analysis_duration" not in st.session_state:
    st.session_state.analysis_duration = "Weekly (7 Days)"

# URL Input Field
col1, col2 = st.columns([1, 2])  
with col1:
    st.markdown("<b>Enter / Paste Facebook Profile URL:</b>", unsafe_allow_html=True)
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
        st.warning("⚠️ Please enter a Facebook Profile URL.")
    elif not is_valid_facebook_url(url):
        st.error("❌ Invalid Facebook URL! Please enter a correct profile link.")
    else:
        st.success(f"✅ Analysis for {st.session_state.analysis_duration} has started!")

        # Simulating sentiment analysis
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
                st.markdown(f"**Neutral  Comments 😐 :** {neutral_comments}")
                st.markdown(f"**Negative Comments ❌ :** {negative_comments}")
                st.markdown("**Total Posts / Videos:** _Coming Soon_")

            with col2:
                labels = ["Positive", "Neutral", "Negative"]
                sizes = [positive_comments, neutral_comments, negative_comments]
                colors = ["green", "yellow", "red"]

                fig, ax = plt.subplots(figsize=(3.5, 3.5))
                wedges, texts, autotexts = ax.pie(
                    sizes,
                    labels=labels,
                    autopct="%1.1f%%",
                    startangle=90,
                    colors=colors,
                    wedgeprops={"edgecolor": "black", "linewidth": 1},
                    textprops={"fontsize": 10, "weight": "bold"}
                )

                center_circle = plt.Circle((0, 0), 0.70, fc="white")
                fig.gca().add_artist(center_circle)

                st.pyplot(fig)

st.markdown("""
    <div style="text-align: center;">
        <strong>© 2025 BHEL Social Sentiment Analysis. All rights reserved.</strong><br>
        <strong>Unauthorized use or duplication is strictly prohibited.</strong><br>
        <strong>Developed by: Sushant Joshi & Intern BHEL.</strong>
    </div>
""", unsafe_allow_html=True)
