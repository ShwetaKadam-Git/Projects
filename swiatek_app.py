import streamlit as st
import pandas as pd
import seaborn as sns
import io
import scipy.stats as stats

# Load dataset
df = pd.read_excel("C:/Users/DELL/PycharmProjects/PythonProject/Tennis/Iga_Cleaned.xlsx")

st.title("Iga Swiatek's Performance Analysis w.r.t W/UFEs ")
st.write(f"Sample data includes matches between - 2018 Prague Open to 2025 Indian Wells (Few match stats are missing in the data)")
# Sidebar for navigation
st.sidebar.header("Navigation")
section = st.sidebar.radio("Go to", ["Summary Statistics", "Data Visualizations"])

if section == "Summary Statistics":
    st.subheader("Dataset Overview")
    st.write(df.describe())

    # Performance Metrics
    st.subheader("Performance Metrics")

    total_matches = len(df)
    df['Outcome'] = df['Outcome'].str.strip()
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


    #Key stats
    st.subheader("Key statistics analyzed for the input data")
    # Strip whitespace and non-breaking spaces from both columns
    df['Outcome'] = df['Outcome'].str.strip()
    df['Opponent'] = df['Opponent'].str.strip()

    lost_against = df[df['Outcome'] == 'L']['Opponent'].unique()
    won_against = df[df['Outcome'] == 'W']['Opponent'].unique()

    never_lost_against = [opponent for opponent in won_against if opponent not in lost_against]

    st.write(f"Never Lost Against following players w.r.t the sample data : ")
    st.dataframe(never_lost_against)

    # forehand backhand comparison

    # Assuming 'df' is your DataFrame
    st.write("Forehand and Backhand comparison")
    # Calculate average winners per point
    avg_forehand_winners = df['FHWPerPtNoAceNoDFs'].mean()
    avg_backhand_winners = df['BHWPerPointNoAceNoDFs'].mean()

    # Compare averages
    st.write(f"Average Forehand Winners Per Point: {avg_forehand_winners:.4f}")
    st.write(f"Average Backhand Winners Per Point: {avg_backhand_winners:.4f}")

    if avg_forehand_winners > avg_backhand_winners:
        st.write("Forehand is stronger (higher average winners per point).")
    elif avg_backhand_winners > avg_forehand_winners:
        st.write("Backhand is stronger (higher average winners per point).")
    else:
        st.write("Forehand and backhand winners per point are equal.")

    # Statistical Test (Optional)
    t_stat, p_value = stats.ttest_ind(df['FHWPerPtNoAceNoDFs'], df['BHWPerPointNoAceNoDFs'],
                                      equal_var=False)  # Welch's t-test for unequal variances.
    st.write(f"T-statistic: {t_stat:.4f}")
    st.write(f"P-value: {p_value:.4f}")

    if p_value < 0.05:
        st.write("The difference in forehand and backhand winners per point is statistically significant.")
    else:
        st.write("The difference in forehand and backhand winners per point is not statistically significant.")

    # Best and Worst Opponents
    st.subheader("Best and Worst Opponents by Winners/UnforcedError Ratio")

    top_opponents = df.groupby("Opponent")["Ratio:W/UFEs"].mean().sort_values(ascending=False).head(10)
    worst_opponents = df.groupby("Opponent")["Ratio:W/UFEs"].mean().sort_values(ascending=True).head(10)

    st.write("Top 10 Opponents (Best Performance by W/UFEs Ratio)")
    st.dataframe(top_opponents)

    st.write("Bottom 10 Opponents (Worst Performance by W/UFEs Ratio)")
    st.dataframe(worst_opponents)

    st.write("Dataset Information: ")
    buffer = io.StringIO()  # Create a string buffer
    df.info(buf=buffer)  # Redirect df.info() output to the buffer
    s = buffer.getvalue()  # Get the string value from the buffer

    st.text(s)  # Display the string in Streamlit

    # st.subheader("Unique Values Per Column")
    # st.write(df.nunique())


elif section == "Data Visualizations":
    # User-selectable charts
    chart_type = st.selectbox(
        "Choose a chart to display",
        [
            "Feature Correlation Heatmap",
            "Wins & Losses vs Opponents",
            "Distribution of Winners (Histogram)",
            "Histogram of Winners",
            "Boxplot of UFEs",
            "Heatmap of Win/Loss per opponent",
        ],
    )

    if chart_type == "Feature Correlation Heatmap":
        st.subheader("Feature Correlation Heatmap")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(df.corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
        st.pyplot(fig)

    elif chart_type == "Wins & Losses vs Opponents":
        st.subheader("Wins & Losses vs Opponents")
        opponent_result = df.groupby("Opponent")["Outcome"].value_counts().unstack(fill_value=0)
        fig, ax = plt.subplots(figsize=(12, 6))
        opponent_result.plot(kind="bar", stacked=True, ax=ax)
        plt.title("Wins & Losses vs Opponents")
        st.pyplot(fig)

    elif chart_type == "Distribution of Winners (Histogram)":
        st.subheader("Distribution of Winners per Match")
        fig, ax = plt.subplots(figsize=(8, 5))
        if 'Match Number' not in df.columns:
            df['Match Number'] = range(1, len(df) + 1)  # add a Match number column if it does not exist.
        sns.lineplot(x="Match Number", y="Winners", data=df, marker='o', ax=ax)  # use lineplot or scatter plot
        plt.title("Winners per Match")
        plt.xlabel("Match Number")
        plt.ylabel("Number of Winners")
        st.pyplot(fig)

    elif chart_type == "Histogram of Winners":
        fig, ax = plt.subplots()
        sns.histplot(df["Winners"], bins=30, ax=ax)
        st.pyplot(fig)
        #st.write("Top Opponents by Avg Winner/Error Ratio")
        #top_opponents = df.groupby("Opponent")["Ratio:W/UFEs"].mean().sort_values(ascending=False).head(10)
        #st.dataframe(top_opponents)

    elif chart_type == "Boxplot of UFEs":
        fig, ax = plt.subplots()
        sns.boxplot(x=df["Unforced Errors"], ax=ax)
        st.pyplot(fig)
        #st.write("Top Opponents by Avg Winner/Error Ratio")
        #top_opponents = df.groupby("Opponent")["Ratio:W/UFEs"].mean().sort_values(ascending=False).head(10)
        #st.dataframe(top_opponents)

    elif chart_type == "Heatmap of Win/Loss per opponent":
        opponent_result = df.groupby("Opponent")["Outcome"].value_counts().unstack(fill_value=0)
        fig, ax = plt.subplots(figsize=(15, len(opponent_result) * 0.5))
        sns.heatmap(opponent_result, annot=True, cmap="YlGnBu", fmt="d", ax=ax)
        ax.set_title("Win/Loss Heatmap vs Opponents")
        ax.set_xlabel("Outcome")
        ax.set_ylabel("Opponent")
        plt.yticks(rotation=0)
        st.pyplot(fig)
