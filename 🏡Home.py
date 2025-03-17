import streamlit as st
import os
import time
import sqlite3
import base64
from streamlit_option_menu import option_menu

# ============================ PAGE CONFIGURATION ============================ #
st.set_page_config(layout="wide", page_title="BHEL | Social Sentiment Analysis")

# ============================ VISITOR COUNT (SQLite) ============================ #
def get_visitor_count():
    with sqlite3.connect('visitor_count.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS visits (count INTEGER)''')
        conn.commit()

        # Initialize visitor count if not present
        c.execute('SELECT count FROM visits')
        row = c.fetchone()
        if row is None:
            c.execute('INSERT INTO visits (count) VALUES (0)')
            conn.commit()

        # Increment visitor count
        c.execute('UPDATE visits SET count = count + 1')
        conn.commit()

        # Retrieve updated visitor count
        c.execute('SELECT count FROM visits')
        return c.fetchone()[0]

visitor_count = get_visitor_count()

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
        <h1>BHEL: Social Sentiment Analysis</h1>
        {'<img src="data:image/png;base64,' + image_base64 + '" style="width: 200px; height: 120px;">' if image_base64 else ''}
    </div>
    """,
    unsafe_allow_html=True
)

st.write("  ")
st.write("  ")

# ============================ SIDEBAR MENU ============================ #
with st.sidebar:
    st.markdown(f"👥 **Visitors Count:** `{visitor_count}`")

    selected = option_menu(
        menu_title="BHEL",
        options=["Home", "Contact", "Signup", "Login"],
        icons=["house", "envelope", "door-open", "key"],
        default_index=0,
        orientation="vertical",
        menu_icon="cast",
        styles={
            "icon": {"font-size": "17px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "3px", "--hover-color": "#262730"}
        }
    )

# ============================ IMAGE SLIDER ============================ #
image_list = [
    "./Images/BHEL_Cover.png",
    "./Images/BHEL_Cover1.png",
    "./Images/BHEL_Cover2.png",
    "./Images/BHEL_Cover3.png",
    "./Images/BHEL_Cover4.png",
    "./Images/BHEL_Cover5.png",
    "./Images/BHEL_Cover6.png"
]

image_placeholder = st.empty()
# ============================ FOOTER ============================ #
st.markdown("""
    <div style="text-align: center;">
        <strong>© 2025 BHEL Social Sentiment Analysis. All rights reserved.</strong><br>
        <strong>Unauthorized use or duplication is strictly prohibited.</strong><br>
        <strong>Developed by: Sushant Joshi & Intern BHEL.</strong>
    </div>
""", unsafe_allow_html=True)

# Initialize session state for slideshow control
if "slideshow_running" not in st.session_state:
    st.session_state.slideshow_running = True

# Image Slideshow (Loops 5 times with pause/resume control)
valid_images = [img for img in image_list if os.path.exists(img)]
if valid_images:
    for _ in range(5):  # Adjust number of loops
        for img in valid_images:
            if not st.session_state.slideshow_running:
                break  # Exit loop if paused
            image_placeholder.image(img, caption="Sentiment Analyzer", use_container_width=True)
            time.sleep(5)
else:
    st.error("🚨 No valid images found!")
