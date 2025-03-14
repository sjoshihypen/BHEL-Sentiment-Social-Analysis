import streamlit as st
import os 
import time
import sqlite3
import mysql.connector
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
# ============================ IMAGE PATHS ============================ #
image_paths = {
    "bhel": "D:/BHEL/Images/bhel.jpg"
}

# ============================ UI LAYOUT ============================ #
# Title and Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("BHEL: Social Sentiment Analysis")
with col2:
    if os.path.exists(image_paths["bhel"]):
        st.image(image_paths["bhel"], caption="BHEL Vision", use_container_width=True)
    else:
        st.error("🚨 Image Not Found: BHEL logo")

# ============================ SIDEBAR MENU ============================ #
with st.sidebar:
     st.markdown(f"👥 **Visitors Count:** `{visitor_count}`")  

# Manage session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Sidebar Menu
with st.sidebar:
    selected = option_menu(
        menu_title="BHEL",
        options=["Home", "Contact", "Signup", "Login"],
        icons=["house", "envelope", "door-open", "key"],
        default_index=0,
        orientation="vertical",
        menu_icon="cast",
        styles={
            "icon": {"font-size": "17px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"3px", "--hover-color": "#262730"}
        }
    )

    # Contact Form
    if selected == "Contact":
        st.write("# Contact Us")
        with st.form("Contact"):
            CName = st.text_input('Name', placeholder='Enter Name')
            CPhone = st.text_input('Mobile', placeholder='Enter Mobile')
            CEmail = st.text_input('Email', placeholder='Enter Email')
            CMessage = st.text_area('Message', placeholder='Enter Your Message Here...')
            Contact_submit = st.form_submit_button('Submit')
            if Contact_submit:
                st.success("We will contact you soon...", icon="✅")
    
    # Signup Form
    elif selected == "Signup":
        st.write("# Hello 👋, Sign Up Here")
        with st.form("Registration"):
            def init_connection():
                return mysql.connector.connect(**st.secrets["mysql"])
            conn = init_connection()
            cursor = conn.cursor()

            RName = st.text_input('Name', placeholder='Enter Name')
            RPhone = st.text_input('Mobile', placeholder='Enter Mobile')
            REmail = st.text_input('Email', placeholder='Enter Email')
            RPassword = st.text_input('Password', placeholder='Enter Password', type="password")

            Signup = st.form_submit_button('Register Me')
            if Signup:
                try:
                    cursor.execute("INSERT INTO register (Fname, Phone, Email, Pass) VALUES (%s, %s, %s, %s)", 
                                   (RName, RPhone, REmail, RPassword))
                    conn.commit()
                    st.success("Congratulations! You are part of SENSI", icon="✅")
                except Exception as e:
                    st.error(f"Error: {e}")
                finally:
                    cursor.close()
                    conn.close()
    
    # Login Form
    elif selected == "Login":
        st.write("# Hello 👋, Login Here")
        with st.form("Login"):
            def init_connection():
                return mysql.connector.connect(**st.secrets["mysql"])
            conn = init_connection()
            cursor = conn.cursor()

            REmail = st.text_input('Email', placeholder='Enter Email')
            RPassword = st.text_input('Password', placeholder='Enter Password', type="password")

            Login = st.form_submit_button('Login')
            if Login:
                cursor.execute("SELECT * FROM register WHERE Email = %s AND Pass = %s", (REmail, RPassword))
                user = cursor.fetchone()
                if user:
                    st.session_state.logged_in = True
                    st.success("Welcome! Logged in Successfully", icon="✅")
                else:
                    st.error("OOPS!!! Invalid ID or Password", icon="🚨")
                cursor.close()
                conn.close()

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

st.markdown("""
    <div style="text-align: center;">
        <strong>© 2025 BHEL Social Sentiment Analysis. All rights reserved.</strong><br>
        <strong>Unauthorized use or duplication is strictly prohibited.</strong><br>
        <strong>Developed by : Sushant Joshi & Intern BHEL.</strong>
    </div>
""", unsafe_allow_html=True)
