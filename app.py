import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# General Configuration
st.set_page_config(page_title="Data Visualization", layout="centered")
st.title("University Data Dashboard")
st.markdown("Integrants: Roberto Escobar, Andrés Moreno, Laura Sanchez, Isabella Vega")
st.markdown("Explore trends in student retention and satisfaction")

# Load dataset
df = pd.read_csv("university_student_data.csv")

# Sidebar filters
years = sorted(df["Year"].unique())
terms = sorted(df["Term"].unique())

col1, col2 = st.columns(2)
with col1:
    year_selected = st.selectbox("Select year", years, index=len(years)-1)
with col2:
    term_selected = st.selectbox("Select academic term", terms)

# Filter dataset
df_filtered = df[(df["Year"] == year_selected) & (df["Term"] == term_selected)]

# Visualization controls
col3, col4 = st.columns([2, 1])
with col3:
    mode = st.radio(
        "Visualization mode",
        ["Cumulative up to selected year", "Only the selected year"],
        index=0,
        help="Choose whether to display cumulative trends or only one specific year."
    )
with col4:
    show_grid = st.checkbox("Show grid", value=True)
    color = st.color_picker("Line color", value="#1f77b4")

# Prepare data for plot
if mode == "Cumulative up to selected year":
    df_plot = df[df["Year"] <= year_selected].copy()
    title = f"Retention trend up to {year_selected}"
else:
    df_plot = df[df["Year"] == year_selected].copy()
    title = f"Retention rate in {year_selected}"

# KPIs
avg_retention = round(df_filtered["Retention Rate (%)"].mean(), 2)
avg_satisfaction = round(df_filtered["Student Satisfaction (%)"].mean(), 2)
total_enrolled = int(df_filtered["Enrolled"].sum())

col_a, col_b, col_c = st.columns(3)
col_a.metric("Average Retention Rate", f"{avg_retention}%")
col_b.metric("Average Satisfaction", f"{avg_satisfaction}%")
col_c.metric("Total Enrolled Students", f"{total_enrolled}")

# Main chart
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df_plot["Year"], df_plot["Retention Rate (%)"], marker="o", linestyle="-", color=color)
ax.set_title(title)
ax.set_xlabel("Year")
ax.set_ylabel("Retention Rate (%)")
ax.grid(show_grid)
fig.tight_layout()
st.pyplot(fig)

# Comparison between Spring and Fall terms
st.subheader("Comparison between Spring and Fall terms")
st.markdown("This chart shows how the average retention rate differs between Spring and Fall terms over the years.")

df_comparison = df.groupby(["Year", "Term"])["Retention Rate (%)"].mean().reset_index()

fig3, ax3 = plt.subplots(figsize=(8,5))
sns.barplot(data=df_comparison, x="Year", y="Retention Rate (%)", hue="Term", palette="coolwarm", ax=ax3)
ax3.set_title("Comparison between Spring and Fall terms")
ax3.set_xlabel("Year")
ax3.set_ylabel("Average Retention Rate (%)")
ax3.legend(title="Term")
st.pyplot(fig3)


# Additional charts in tabs
tab1, tab2 = st.tabs(["Satisfaction by Year", "Full Dataset"])

with tab1:
    fig2, ax2 = plt.subplots(figsize=(8,5))
    sns.barplot(data=df, x="Year", y="Student Satisfaction (%)", palette="viridis", ax=ax2)
    ax2.set_title("Student Satisfaction by Year")
    plt.xticks(rotation=45)
    st.pyplot(fig2)

with tab2:
    st.dataframe(df, use_container_width=True)

st.caption("Use the controls to explore retention and satisfaction by year or academic term.")