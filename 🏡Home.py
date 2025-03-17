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
        
        c.execute('SELECT count FROM visits')
        row = c.fetchone()
        if row is None:
            c.execute('INSERT INTO visits (count) VALUES (0)')
            conn.commit()
        
        c.execute('UPDATE visits SET count = count + 1')
        conn.commit()
        
        c.execute('SELECT count FROM visits')
        return c.fetchone()[0]

visitor_count = get_visitor_count()

# ============================ INLINE IMAGE ENCODING ============================ #
@st.cache_data
def get_image_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

image_path = "D:/BHEL Sentiment Social Analysis/Images/bhel.png"
image_base64 = get_image_base64(image_path)

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
    st.markdown(f"👥 **Visitors Count:** {visitor_count}")
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

# ============================ IMAGE SLIDER (CACHED) ============================ #
@st.cache_data
def load_valid_images(image_list):
    return [img for img in image_list if os.path.exists(img)]

image_list = [
    "./Images/BHEL_Cover.png",
    "./Images/BHEL_Cover1.png",
    "./Images/BHEL_Cover2.png",
    "./Images/BHEL_Cover3.png",
    "./Images/BHEL_Cover4.png",
    "./Images/BHEL_Cover5.png",
    "./Images/BHEL_Cover6.png"
]
valid_images = load_valid_images(image_list)

image_placeholder = st.empty()

# ============================ CONTAINER SECTION ============================ #
st.markdown("### Products & Services")
st.write("""
          BHEL is one of the largest engineering and manufacturing companies of its kind in India engaged in design, engineering,
          construction, testing, commissioning, and servicing of a wide range of products and services with over 180 product offerings 
          to meet the ever-growing needs of the core sectors of the economy.
         """)

# Define card data with image paths
card_data = [
    {"title": "Power Generation", "image": "D:/BHEL Sentiment Social Analysis/Images/power_gen.jpg", "description": "BHEL provides a range of power generation solutions, including thermal, nuclear, and renewable energy solutions."},
    {"title": "Transmission & Distribution", "image": "D:/BHEL Sentiment Social Analysis/Images/transmission.jpg", "description": "BHEL plays a crucial role in power transmission and distribution with cutting-edge technologies."},
    {"title": "Railway Electrification", "image": "D:/BHEL Sentiment Social Analysis/Images/railway.jpg", "description": "BHEL contributes to railway electrification, enhancing efficiency and sustainability."},
    {"title": "Defence Equipment", "image": "D:/BHEL Sentiment Social Analysis/Images/defence.jpg", "description": "Manufacturing and supplying critical defence equipment and components."},
    {"title": "Renewable Energy", "image": "D:/BHEL Sentiment Social Analysis/Images/renewable.jpg", "description": "BHEL is actively involved in wind, solar, and hydro power solutions."},
    {"title": "Oil & Gas", "image": "D:/BHEL Sentiment Social Analysis/Images/oilgas.jpg", "description": "BHEL provides high-performance equipment for oil and gas exploration and refining."},
    {"title": "Nuclear Energy", "image": "D:/BHEL Sentiment Social Analysis/Images/nuclearenergy.jpg", "description": "BHEL provides high-performance equipment for oil and gas exploration and refining."},
    {"title": "Hydro Power", "image": "D:/BHEL Sentiment Social Analysis/Images/hydropower.jpg", "description": "BHEL provides high-performance equipment for oil and gas exploration and refining."},
    {"title": "EV Charger", "image": "D:/BHEL Sentiment Social Analysis/Images/evcharger.jpg", "description": "BHEL provides high-performance equipment for oil and gas exploration and refining."}
]

placeholder_img = "D:/BHEL Sentiment Social Analysis/Images/power_gen.jpg"  # Default placeholder

# Define number of columns per row
num_cols = 3

# Loop through card data in chunks of 3 for proper spacing
for i in range(0, len(card_data), num_cols):
    with st.container():
        cols = st.columns(num_cols)
        for j in range(num_cols):
            if i + j < len(card_data):
                data = card_data[i + j]
                img_path = os.path.abspath(data["image"]) if os.path.exists(data["image"]) else placeholder_img
                with cols[j]:
                    st.image(img_path, caption=data["title"], use_container_width=True)  # Fixed parameter
                    st.subheader(data["title"])
                    st.write(data["description"])
        st.markdown("<br>", unsafe_allow_html=True)  # Adds spacing between rows

# ============================ FOOTER ============================ #
st.markdown("""
    <div style="background-color: black; color: white; text-align: center; padding: 10px;">
        <p>Copyright © 2020 - All Rights Reserved - Official Website of Bharat Heavy Electricals Limited</p>
        <p>BHEL House, Siri Fort, New Delhi - 110049, India</p>
        <p>CIN: L74899DL1964GOI004281</p>
        <p><b>Note: Content on this website is published and managed by Bharat Heavy Electricals Limited</b></p>
        <p><b>Maintained By : Sushant Joshi, Intern BHEL</b></p>
    </div>
""", unsafe_allow_html=True)

# ============================ IMAGE SLIDESHOW ============================ #
if valid_images:
    for _ in range(5):
        for img in valid_images:
            image_placeholder.image(img, caption="Sentiment Analyzer", use_container_width=True)
            time.sleep(5)
else:
    st.error("🚨 No valid images found!")
