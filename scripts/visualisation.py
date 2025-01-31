import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


# Function to create visualization of top videos by views
def top_videos_by_views(data):
    """
    Bar chart for the Top 10 Videos based on Views
    """
    required_columns = ["Views", "Video Title"]
    if not all(col in data.columns for col in required_columns):
        st.warning("Missing columns for 'Top Videos by Views': 'Views', 'Video Title'")
        return

    data_sorted = data.sort_values(by="Views", ascending=False).head(10)  # Top 10 videos by views
    plt.figure(figsize=(10, 6))
    sns.barplot(data=data_sorted, x="Views", y="Video Title", palette="viridis")
    plt.title("Top 10 Videos by Views")
    plt.xlabel("Total Views")
    plt.ylabel("Video Title")
    st.pyplot(plt)
    plt.clf()  # Clear the figure to avoid overlapping


# Function to compare Views vs Likes vs Comments
def views_likes_comments(data):
    """
    Stacked bar chart for Views, Likes, and Comments comparison.
    """
    required_columns = ["Views", "Likes", "Comments", "Video Title"]
    if not all(col in data.columns for col in required_columns):
        st.warning("Missing columns for 'Views vs Likes vs Comments': 'Views', 'Likes', 'Comments', 'Video Title'")
        return

    data_sorted = data.sort_values(by="Views", ascending=False).head(10)  # Top 10 videos by views
    plt.figure(figsize=(12, 6))
    stacked_data = data_sorted[["Views", "Likes", "Comments"]].T
    stacked_data.columns = data_sorted["Video Title"]
    stacked_data.plot(kind="bar", stacked=True, figsize=(12, 6), colormap="coolwarm")
    plt.title("Views, Likes, and Comments Comparison (Top 10 Videos)")
    plt.xlabel("Metrics")
    plt.ylabel("Counts")
    st.pyplot(plt)
    plt.clf()  # Clear the figure


# Function to create Engagement Rate vs Views scatter plot
def engagement_rate_vs_views(data):
    """
    Scatter plot for Engagement Rate (%) vs. Views
    """
    required_columns = ["Views", "Engagement Rate (%)", "Video Title"]
    if not all(col in data.columns for col in required_columns):
        st.warning("Missing columns for 'Engagement Rate vs Views': 'Views', 'Engagement Rate (%)', 'Video Title'")
        return

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=data, x="Views", y="Engagement Rate (%)", hue="Video Title", palette="Set1", s=100)
    plt.title("Engagement Rate vs Views")
    plt.xlabel("Views")
    plt.ylabel("Engagement Rate (%)")
    plt.grid()
    st.pyplot(plt)
    plt.clf()  # Clear the figure


def trend_line_plot(data):
    """
    Line plot for visualizing trends in Views, Likes, and Comments.
    """
    required_columns = ["Views", "Likes", "Comments", "Video Title"]
    if not all(col in data.columns for col in required_columns):
        st.warning("Missing columns for 'Trend Line Plot': 'Views', 'Likes', 'Comments', 'Video Title'")
        return

    # Ensure 'Video Title' is available as an index for order
    data = data.sort_values(by="Views", ascending=False)  # Sort by Views or an index
    data = data.head(10)  # Focus on the top 10 videos

    plt.figure(figsize=(10, 6))
    plt.plot(data["Video Title"], data["Views"], label="Views", marker="o")
    plt.plot(data["Video Title"], data["Likes"], label="Likes", marker="o")
    plt.plot(data["Video Title"], data["Comments"], label="Comments", marker="o")
    plt.xticks(rotation=45, ha="right")
    plt.title("Trends in Video Performance (Top 10 Videos)")
    plt.xlabel("Video Title")
    plt.ylabel("Counts")
    plt.legend()
    plt.grid()
    st.pyplot(plt)
    plt.clf()


def metric_correlation_heatmap(data):
    """
    Heatmap showing the correlation between various metrics.
    """
    required_columns = ["Views", "Likes", "Comments", "Engagement Rate (%)"]
    if not all(col in data.columns for col in required_columns):
        st.warning("Missing columns for 'Metric Correlation Heatmap'.")
        return

    plt.figure(figsize=(8, 6))
    corr = data[required_columns].corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Between Metrics")
    st.pyplot(plt)
    plt.clf()  # Clear the figure


def metrics_distribution_boxplot(data):
    """
    Boxplot to visualize the distribution of Views, Likes, and Comments.
    """
    required_columns = ["Views", "Likes", "Comments"]
    if not all(col in data.columns for col in required_columns):
        st.warning("Missing columns for 'Metrics Distribution Boxplot'.")
        return

    plt.figure(figsize=(8, 6))
    sns.boxplot(data=data[required_columns], palette="muted")
    plt.title("Distribution of Metrics (Views, Likes, Comments)")
    plt.ylabel("Counts")
    st.pyplot(plt)
    plt.clf() 




def engagement_breakdown_pie_chart(data):
    """
    Pie chart showing the breakdown of engagement (Views, Likes, and Comments).
    """
    required_columns = ["Views", "Likes", "Comments"]
    if not all(col in data.columns for col in required_columns):
        st.warning("Missing columns for 'Engagement Breakdown Pie Chart'.")
        return

    engagement_totals = data[["Views", "Likes", "Comments"]].sum()
    plt.figure(figsize=(8, 6))
    plt.pie(
        engagement_totals,
        labels=engagement_totals.index,
        autopct="%1.1f%%",
        startangle=140,
        colors=sns.color_palette("pastel")
    )
    plt.title("Engagement Breakdown (Views, Likes, Comments)")
    st.pyplot(plt)
    plt.clf() 

# def regional_trends_bar_chart(data):
#     """
#     Bar chart for total views of trending videos by region.
#     """
#     required_columns = ["Region", "Views"]
#     if not all(col in data.columns for col in required_columns):
#         st.warning("Missing columns for 'Regional Trends Bar Chart'.")
#         return

#     regional_data = data.groupby("Region")["Views"].sum().reset_index()
#     regional_data = regional_data.sort_values(by="Views", ascending=False)

#     plt.figure(figsize=(8, 6))
#     sns.barplot(data=regional_data, x="Views", y="Region", palette="rocket")
#     plt.title("Total Views of Trending Videos by Region")
#     plt.xlabel("Total Views")
#     plt.ylabel("Region")
#     st.pyplot(plt)
#     plt.clf()



# Function to show all essential visualizations
def visualize_essential_metrics(data):
    """
    Display only the necessary visualizations for video performance.
    """
    st.write("### Key Video Metrics Visualizations")

    top_videos_by_views(data)  # Essential Visualization 1
    views_likes_comments(data)  # Essential Visualization 2
    engagement_rate_vs_views(data)  # Essential Visualization 3
    trend_line_plot(data)
    metric_correlation_heatmap(data)
    metrics_distribution_boxplot(data)
    engagement_breakdown_pie_chart(data)