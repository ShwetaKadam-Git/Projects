import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import scipy.stats as stats

# Load dataset
df = pd.read_excel("Iga_Cleaned.xlsx")

# Set page title and description
st.title("Iga Swiatek's Performance Analysis w.r.t Winners/Unforced Errors")
st.write("Analyzing matches from 2018 Prague Open to 2025 Indian Wells (Some match stats are missing)")

# Sidebar navigation
st.sidebar.header("Navigation")
section = st.sidebar.radio("Go to", ["Summary Statistics", "Data Visualizations"])

# Section for Summary Statistics
if section == "Summary Statistics":
    st.subheader("Dataset Overview")
    st.write(df.describe())

    st.subheader("Performance Metrics")
    total_matches = len(df)
    wins = df[df["Outcome"] == "W"].shape[0]
    losses = df[df["Outcome"] == "L"].shape[0]
    win_percentage = round((wins / total_matches) * 100, 2)

    avg_winners = round(df["Winners"].mean(), 2)
    avg_ufes = round(df["Unforced Errors"].mean(), 2)

    st.write(f"Total Matches: {total_matches}")
    st.write(f"Total Wins: {wins} ({win_percentage}%)")
    st.write(f"Total Losses: {losses}")
    st.write(f"Average Winners per Match: {avg_winners}")
    st.write(f"Average Unforced Errors per Match: {avg_ufes}")

    st.subheader("Key Statistics")
    df['Outcome'] = df['Outcome'].str.strip()
    df['Opponent'] = df['Opponent'].str.strip()

    lost_against = df[df['Outcome'] == 'L']['Opponent'].unique()
    won_against = df[df['Outcome'] == 'W']['Opponent'].unique()
    never_lost_against = [opponent for opponent in won_against if opponent not in lost_against]

    st.write("Never Lost Against:")
    st.dataframe(never_lost_against)

    st.subheader("Forehand and Backhand Comparison")
    avg_forehand_winners = df['FHWPerPtNoAceNoDFs'].mean()
    avg_backhand_winners = df['BHWPerPointNoAceNoDFs'].mean()

    st.write(f"Average Forehand Winners Per Point: {avg_forehand_winners:.4f}")
    st.write(f"Average Backhand Winners Per Point: {avg_backhand_winners:.4f}")

    if avg_forehand_winners > avg_backhand_winners:
        st.write("Forehand is stronger.")
    elif avg_backhand_winners > avg_forehand_winners:
        st.write("Backhand is stronger.")
    else:
        st.write("Forehand and backhand are equally strong.")

    t_stat, p_value = stats.ttest_ind(df['FHWPerPtNoAceNoDFs'], df['BHWPerPointNoAceNoDFs'], equal_var=False)
    st.write(f"T-statistic: {t_stat:.4f}")
    st.write(f"P-value: {p_value:.4f}")

    if p_value < 0.05:
        st.write("Difference in forehand and backhand winners is significant.")
    else:
        st.write("Difference in forehand and backhand winners is not significant.")

    st.subheader("Best and Worst Opponents by W/UFEs Ratio")
    top_opponents = df.groupby("Opponent")["Ratio:W/UFEs"].mean().sort_values(ascending=False).head(10)
    worst_opponents = df.groupby("Opponent")["Ratio:W/UFEs"].mean().sort_values(ascending=True).head(10)

    st.write("Top Opponents:")
    st.dataframe(top_opponents)

    st.write("Bottom Opponents:")
    st.dataframe(worst_opponents)

    st.subheader("Dataset Information")
    buffer = io.StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()
    st.text(info_str)

# Section for Data Visualizations
elif section == "Data Visualizations":
    st.subheader("Choose a Chart to Display")
    chart_type = st.selectbox("", [
        "Feature Correlation Heatmap",
        "Wins & Losses vs Opponents",
        "Distribution of Winners",
        "Boxplot of Unforced Errors",
        "Win/Loss Heatmap vs Opponents"
    ])

    if chart_type == "Feature Correlation Heatmap":
        st.subheader("Feature Correlation Heatmap")
        fig, ax = plt.subplots(figsize=(10, 6))   
        df_numeric = df.select_dtypes(include=['number']) 
        df_numeric = df_numeric.dropna()
        sns.heatmap(df_numeric.corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
        st.pyplot(fig)

    elif chart_type == "Wins & Losses vs Opponents":
        st.subheader("Wins & Losses vs Opponents")
        opponent_result = df.groupby("Opponent")["Outcome"].value_counts().unstack(fill_value=0)
        fig, ax = plt.subplots(figsize=(12, 6))
        opponent_result.plot(kind="bar", stacked=True, ax=ax)
        plt.title("Wins & Losses vs Opponents")
        plt.xlabel("Opponent")
        plt.ylabel("Count")
        st.pyplot(fig)

    elif chart_type == "Distribution of Winners":
        st.subheader("Distribution of Winners per Match")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(x=df.index, y="Winners", data=df, marker='o', ax=ax)
        plt.title("Distribution of Winners")
        plt.xlabel("Match Number")
        plt.ylabel("Winners")
        st.pyplot(fig)

    elif chart_type == "Boxplot of Unforced Errors":
        st.subheader("Boxplot of Unforced Errors")
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.boxplot(x=df["Unforced Errors"], ax=ax)
        plt.title("Boxplot of Unforced Errors")
        plt.xlabel("Unforced Errors")
        st.pyplot(fig)

    elif chart_type == "Win/Loss Heatmap vs Opponents":
        st.subheader("Win/Loss Heatmap vs Opponents")
        opponent_result = df.groupby("Opponent")["Outcome"].value_counts().unstack(fill_value=0)
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(opponent_result, annot=True, cmap="YlGnBu", fmt="d", ax=ax)
        plt.title("Win/Loss Heatmap vs Opponents")
        plt.xlabel("Outcome")
        plt.ylabel("Opponent")
        st.pyplot(fig)
