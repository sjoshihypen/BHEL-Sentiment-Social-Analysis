# BHEL | Social Sentiment Analysis
![BHEL Sentiment Analysis](./Images/BHEL_Cover.png)

## Overview
BHEL Social Sentiment Analysis is a Streamlit web application that analyzes social media posts about **Bharat Heavy Electricals Limited (BHEL)**. It assists users in comprehending public opinion by scraping and analyzing LinkedIn post comments. The application features secure authentication, a contact system, and a visitor counter to monitor engagement. With its user-friendly intuitive interface, interactive image sliders, and granular sentiment analysis, this tool simplifies tracking and visualizing what people say about BHEL on social media.

## 🏗 Features

**1. ✅ Secure Authentication (Stored in Streamlit Secrets)**

Enjoy a secure and seamless login experience with credentials stored in Streamlit Secrets. This ensures your authentication data remains safe, encrypted, and private from external breaches, making the platform highly secure for all users.

**2. 🔍 Scrape Different Social Media Platforms Posts & Videos**

Automatically collect Different Social Media Platforms posts related to BHEL and analyze public engagement. Stay updated on industry trends, user opinions, and brand sentiment, helping businesses make data-driven decisions in real time.

**3. 💬 Extract Comments & Perform Sentiment Analysis**

Our AI-powered tool scans post comments to determine sentiment—positive, neutral, or negative. This analysis helps identify public opinion and provides insights into the brand’s reputation and user engagement levels.

**4. 📊 Engagement Statistics & Sentiment Breakdown**

Track likes, shares, and comments on LinkedIn posts. Get a detailed sentiment breakdown to measure audience perception, making it easier to adjust marketing strategies and boost engagement.

**5. 📉 Visualizations with Graphs & Charts**

Gain deep insights with interactive visualizations! Our platform generates bar charts, pie charts, and trend graphs to showcase sentiment trends, engagement levels, and audience behavior in an easy-to-understand format.

**6. 📁 Downloadable CSV Reports**
Export sentiment analysis results and engagement metrics into CSV files. This feature allows businesses to maintain records, conduct in-depth studies, and use the data for future strategies and reporting.

## 🛠 Installation Guide
**1. Clone the Repository**
```bash
   git clone https://github.com/your-repo/BHEL-Sentiment-Analysis.git
   cd BHEL-Sentiment-Analysis
```

**2. Install Dependencies**
```bash
   pip install -r requirements.txt
```

**3. Run the Application**
```bash
   streamlit run app.py
```

## 🗄 Database Configuration
**1. SQLite for Visitor Count**
- The project uses SQLite to maintain a visitor count.
- The database file is created automatically if not present.

**2. MySQL for User Authentication**
- Update the `st.secrets` configuration with your MySQL database credentials.
- MySQL is used to manage user registration and login.

## Tech Stack
- **Python** 🐍
- **Streamlit** 🌐
- **SQLite** 🗃️ (Visitor Count)
- **MySQL** 🛢️ (User Authentication)

## 🤝 Contributing
We welcome contributions! If you’d like to contribute:
1. Fork the repository 📌
2. Create a new branch 🌿
3. Commit your changes 🔥
4. Open a pull request ✅

## 📄 License
This project is **open-source** and available under the **MIT License**.

---
### ⭐ **Show some love!**
If you like this project, don't forget to give it a ⭐ on GitHub!

🔗 Connect with us: [LinkedIn](https://linkedin.com) | [Twitter](https://twitter.com)

