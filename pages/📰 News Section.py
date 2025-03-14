import streamlit as st
import requests
from datetime import datetime
import pytz

# ============================ PAGE CONFIGURATION ============================ #
st.set_page_config(layout="wide", page_title="BHEL News")

# ============================ TITLE & SEARCH BAR LAYOUT ============================ #
col1, col2, col3 = st.columns([2, 1, 2])  # Layout for title, date picker, and search bar

with col1:
    st.write("## 📰 Latest BHEL News")  # Title

with col2:
    start_date = st.date_input("📅 **Start Date**", None)  # Start Date Picker

with col3:
    search_query = st.text_input("🔍 Search Headlines", placeholder="Enter keywords...")  # Search Bar

# Convert selected date to string format (YYYY-MM-DD) for API query
start_date_str = start_date.strftime("%Y-%m-%d") if start_date else None

# ============================ FETCH NEWS ============================ #
api_key = "3f1626f4d9f54e8b886196d34f444076"  # Replace with a valid API key

# Construct API URL based on user input
base_url = "https://newsapi.org/v2/everything"
query = search_query if search_query else "BHEL"
date_param = f"&from={start_date_str}" if start_date_str else ""

# Fetch up to 80 news articles using pagination
articles = []
page = 1
page_size = 40  # Fetch in batches to avoid API limits

while len(articles) < 80:
    news_url = f"{base_url}?q={query}{date_param}&sortBy=publishedAt&language=en&pageSize={page_size}&page={page}&apiKey={api_key}"
    response = requests.get(news_url)

    if response.status_code != 200:
        st.error(f"🚨 Failed to fetch news. API Error: {response.status_code}")
        break

    news_response = response.json()

    if news_response["status"] == "ok" and len(news_response["articles"]) > 0:
        articles.extend(news_response["articles"])
        if len(news_response["articles"]) < page_size:
            break  # Stop if there are no more articles
        page += 1  # Fetch next page
    else:
        break  # No more news available

# Limit articles to 80
articles = articles[:80]

if len(articles) == 0:
    st.warning("❌ No news found. Try another search keyword or date!")
else:
    # CSS for equal-sized cards with spacing
    st.markdown("""
        <style>
            .news-card {
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 15px;
                text-align: center;
                background-color: #f9f9f9;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                height: 350px;  /* Fixed Height */
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }
            .news-image {
                width: 100%;
                height: 150px;
                object-fit: cover;
                border-radius: 10px;
            }
            .news-title {
                font-size: 16px;
                font-weight: bold;
                margin: 10px 0;
                height: 50px; /* Fixed Height for Title */
                overflow: hidden;
            }
            .news-date {
                color: gray;
                font-size: 14px;
            }
            .news-link {
                color: blue;
                text-decoration: none;
                font-weight: bold;
            }
        </style>
    """, unsafe_allow_html=True)

    # Display news in a card layout (3 cards per row)
    for i in range(0, len(articles), 3):
        cols = st.columns(3)  # Ensures equal spacing between cards

        for j in range(3):
            if i + j < len(articles):
                article = articles[i + j]
                image_url = article.get("urlToImage", "https://via.placeholder.com/300")
                published_at = article.get("publishedAt", "")

                # Convert timestamp to IST
                if published_at:
                    utc_time = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
                    ist_time = utc_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone("Asia/Kolkata"))
                    formatted_time = ist_time.strftime("%d %B %Y, %I:%M %p IST")
                else:
                    formatted_time = "Date Unavailable"

                with cols[j]:
                    st.markdown(
                        f"""
                        <div class="news-card">
                            <img src="{image_url}" class="news-image">
                            <div class="news-title">{article['title']}</div>
                            <p class="news-date">🗓️ {formatted_time}</p>
                            <a href="{article['url']}" target="_blank" class="news-link">Read More</a>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

st.markdown("<br><br><br>", unsafe_allow_html=True)

# ============================ FOOTER ============================ #
st.markdown(""" 
    <div style="text-align: center;">
        <strong>© 2025 BHEL Social Sentiment Analysis. All rights reserved.</strong><br>
        <strong>Unauthorized use or duplication is strictly prohibited.</strong><br>
        <strong>Developed by : Sushant Joshi & Intern BHEL.</strong>
    </div>
""", unsafe_allow_html=True)
