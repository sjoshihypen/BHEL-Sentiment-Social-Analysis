import streamlit as st
import re
import os
import numpy as np
import matplotlib.pyplot as plt

# Set Streamlit page configuration
st.set_page_config(page_title="Facebook Sentiment Analysis", layout="wide")

with st.sidebar:
        st.title(f"Key Features:")
        st.write(
            """
            ✅ **Secure Authentication (Stored in Streamlit Secrets).**\n
            ✅ **Scrape Facebooks Posts,Videos.**\n
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

# Path to the logo image
image_path = "D:/BHEL/Images/bhel.jpg"

# Title and Logo Display
st.markdown("<br>", unsafe_allow_html=True)  # Spacing
col1, col2 = st.columns([4, 1])
with col1:
    st.title("BHEL: Facebook Sentiment Analysis")
with col2:
    if os.path.exists(image_path):
        st.image(image_path, caption="BHEL Vision", use_container_width=True)
    else:
        st.error("🚨 Image Not Found: BHEL logo")

# Function to validate Facebook URL (Fix for public pages & profiles)
def is_valid_facebook_url(url):
    fb_pattern = r"^(https?:\/\/)?(www\.)?facebook\.com\/[a-zA-Z0-9._-]+(\/)?$"
    return bool(re.match(fb_pattern, url))

# Initialize Session State for user selections
if "analysis_duration" not in st.session_state:
    st.session_state.analysis_duration = "Weekly (7 Days)"

# URL Input Field with Proper Alignment
col1, col2 = st.columns([1, 2])  # Adjust column width for alignment
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
        st.warning("⚠️ Please enter a Facebook Profile URL.")
    elif not is_valid_facebook_url(url):
        st.error("❌ Invalid Facebook URL! Please enter a correct profile link.")
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
                st.markdown(f"**Neutral  Comments 😐 :** {neutral_comments}")
                st.markdown(f"**Negative Comments ❌ :** {negative_comments}")
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
