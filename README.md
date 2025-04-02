# Project Details
This project analyzes Iga Swiatek's match performance using a dataset containing 320 matches. It provides various insights, including summary statistics, opponent-based trends, match duration trends, and visualization of key performance metrics. The analysis is presented in an interactive Streamlit dashboard.

**Streamlit application link** - https://tennisanalysis.streamlit.app/

Features of the Project - 

**1. Summary Statistics**
This section provides a detailed overview of the dataset with key insights, including:
 - General Overview: Summary statistics, unique values, missing values
 - Performance Metrics: Win percentage, average winners, and unforced errors
 - Opponent-Based Insights: Best and worst opponents based on Winners/UFEs Ratio
 - Surface-Wise Performance: Analyzing performance across different court surfaces
 - Match Duration Trends: Average, longest, and shortest match durations

**2️. Data Visualizations**
The Data Visualizations section enables users to explore different match trends interactively. Available visualizations include:
 - Feature Correlation Heatmap – Identifies relationships between key features
 - Wins & Losses vs Opponents – Stacked bar chart showing performance against different players
 - Distribution of Winners (Histogram) – Visualizes how often winners are played
 - Boxplot of Unforced Errors – Helps analyze Iga's consistency in avoiding errors
 - Win/Loss Heatmap vs Opponents – Shows win/loss distribution across different players

**3. Technologies Used**
 - Python – Data analysis & visualization
 - Pandas – Data manipulation
 - Streamlit – Interactive web app
 - Matplotlib & Seaborn – Data visualization
 - OpenPyXL – Excel file handling

**4. File Structure**
- Tennis_Analysis/
-  📄 swiatek_app.py            # Streamlit Dashboard
-  📄 EDAForIga.py              # Exploratory Data Analysis
-  📄 Iga_Cleaned.xlsx          # Cleaned dataset (320 matches) Sample data extracted from TennisAbstract website https://www.tennisabstract.com/
-  📄 README.md                 # Project documentation

**5. Key Takeaways from the Analysis**
 - Iga Swiatek has a high win percentage, with consistent performance across surfaces.
 - Opponent analysis reveals players against whom she performs best and worst.

**6. Future Improvements**
 - Consider varied sample data in order to analyse the performance better and understand key performance indicators
 - Add predictive modeling for match outcome prediction with much more detailed dataset and parameters
 - Perform deeper time-series analysis to track performance trends over seasons with respect to different surfaces

