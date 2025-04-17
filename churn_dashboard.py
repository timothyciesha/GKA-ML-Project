import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Custom CSS for styling
st.markdown("""
    <style>
    .main {background-color: #f5f7fa;}
    .stButton>button {background-color: #4CAF50; color: white; border-radius: 8px; padding: 10px 20px;}
    .stButton>button:hover {background-color: #45a049;}
    .stSelectbox, .stSlider {background-color: #ffffff; border-radius: 5px; padding: 5px;}
    .css-1d391kg {background-color: #ffffff; border-radius: 10px; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);}
    h1 {color: #2c3e50; font-family: 'Arial', sans-serif; text-align: center;}
    h2 {color: #34495e; font-family: 'Arial', sans-serif; margin-top: 20px;}
    h3 {color: #34495e; font-family: 'Arial', sans-serif;}
    .metric-box {background-color: #ffffff; border-radius: 10px; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); text-align: center; margin: 10px 0;}
    .metric-box h3 {color: #2c3e50; margin: 0; font-size: 18px;}
    .metric-box p {color: #7f8c8d; margin: 5px 0 0; font-size: 24px; font-weight: bold;}
    .info-box {background-color: #e6f0fa; border-radius: 10px; padding: 15px; margin: 10px 0; border-left: 5px solid #4CAF50; color: #2c3e50;}
    .info-box h3 {color: #2c3e50;}
    .info-box p, .info-box li {color: #2c3e50;}
    </style>
""", unsafe_allow_html=True)

# Title and Welcome Section
st.title("🏬 Customer Churn Dashboard")
st.markdown("""
    <div class='info-box'>
    <h3>Welcome to the Customer Churn Dashboard!</h3>
    <p>This app helps you analyze customer churn for your building materials business using data from 2023-2025. It provides insights into which customers are at risk of churning, allowing your sales team to take targeted actions to retain them. With interactive filters, sorting, and visualizations, you can prioritize high-value customers, identify churn patterns, and download data for follow-up.</p>
    </div>
""", unsafe_allow_html=True)

# How to Use Section
st.markdown("""
    <div class='info-box'>
    <h3>How to Use This App</h3>
    <ul>
        <li><b>Overview Tab:</b> Get a quick snapshot of churn stats, like total churned customers and their financial impact, plus a chart of churn score distribution.</li>
        <li><b>Customer Data Tab:</b> Filter customers by churn score and probability, sort by key metrics (e.g., total value), and download filtered data for outreach.</li>
        <li><b>Visualizations Tab:</b> Explore churn patterns with scatter and box plots, showing relationships like total value vs. recency by churn score.</li>
    </ul>
    </div>
""", unsafe_allow_html=True)

# Quick Tips Section
st.markdown("""
    <div class='info-box'>
    <h3>Quick Tips</h3>
    <ul>
        <li>Use the sidebar filters to focus on specific churn risk levels (e.g., score=1 for moderate-risk shops).</li>
        <li>Sort by 'total_value' in the Customer Data tab to prioritize high-value customers for re-engagement.</li>
        <li>Check the scatter plot in Visualizations to spot high-value customers with high recency for urgent action.</li>
        <li>Download filtered data as a CSV to share with your team or import into your CRM.</li>
    </ul>
    </div>
""", unsafe_allow_html=True)

# Load the data
@st.cache_data
def load_data():
    df = pd.read_excel("customer_predictions_updated_2023-2025.xlsx")
    return df

df = load_data()

# Tabs for different views
tab1, tab2, tab3 = st.tabs(["📊 Overview", "🔍 Customer Data", "📈 Visualizations"])

# Tab 1: Overview
with tab1:
    st.header("Overview of Churn Predictions")
    st.markdown("Get a quick snapshot of your customer base and churn risks.")

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='metric-box'><h3>Total Customers</h3><p>{len(df)}</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-box'><h3>Churned (Score ≥ 1)</h3><p>{len(df[df['churn_score'] >= 1])}</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-box'><h3>Moderate Risk (Score = 1)</h3><p>{len(df[df['churn_score'] == 1])}</p></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='metric-box'><h3>Total Value (Churned)</h3><p>{int(df[df['churn_score'] >= 1]['total_value'].sum()):,}</p></div>", unsafe_allow_html=True)

    # Churn Score Distribution
    st.header("Churn Score Distribution")
    churn_dist = df['churn_score'].value_counts().sort_index()
    fig_dist = px.bar(
        x=churn_dist.index, y=churn_dist.values,
        labels={'x': 'Churn Score', 'y': 'Number of Customers'},
        color=churn_dist.index, color_continuous_scale='Blues',
        title="Distribution of Churn Scores"
    )
    fig_dist.update_layout(showlegend=False, title_x=0.5)
    st.plotly_chart(fig_dist, use_container_width=True)

# Tab 2: Customer Data
with tab2:
    st.header("Explore Customer Data")
    st.markdown("Filter, sort, and download customer data for targeted sales actions.")

    # Sidebar for filtering with added explanations
    with st.sidebar:
        st.header("🔧 Filter Options")
        st.markdown("**Select Churn Risk Levels**")
        st.markdown("Choose which churn risk categories to display (0 = not churned, 1 = moderate risk, 2 = higher risk, 3 = churned).")
        churn_score_filter = st.multiselect(
            "Select Churn Score", options=sorted(df['churn_score'].unique()), default=sorted(df['churn_score'].unique())
        )
        
        st.markdown("**Filter by Churn Probability**")
        st.markdown("Set the range of churn probability (0.0 to 1.0) to focus on customers with a specific likelihood of churning.")
        churn_prob_min = st.slider(
            "Minimum Churn Probability (Lower Bound)", 
            0.0, 1.0, 0.0, 0.05,
            help="Show customers with a churn probability at or above this value. Higher values focus on customers more likely to churn."
        )
        churn_prob_max = st.slider(
            "Maximum Churn Probability (Upper Bound)", 
            0.0, 1.0, 1.0, 0.05,
            help="Show customers with a churn probability at or below this value. Lower values focus on customers less certain to churn."
        )

    # Filter the dataframe
    filtered_df = df[
        (df['churn_score'].isin(churn_score_filter)) &
        (df['churn_prob'] >= churn_prob_min) &
        (df['churn_prob'] <= churn_prob_max)
    ]

    # Display filtered data
    st.markdown(f"**Showing {len(filtered_df)} customers**")
    st.dataframe(filtered_df.style.format({
        'total_value': '{:,.0f}', 'avg_value': '{:,.0f}', 'avg_price': '{:,.0f}',
        'churn_prob': '{:.2f}', 'purchase_std': '{:.2f}'
    }).set_table_styles([
        {'selector': 'th', 'props': [('background-color', '#34495e'), ('color', 'white')]},
        {'selector': 'td', 'props': [('border', '1px solid #ddd')]}
    ]), use_container_width=True)

    # Sorting options
    st.header("Sort Data")
    col_sort1, col_sort2 = st.columns(2)
    with col_sort1:
        sort_by = st.selectbox("Sort by", ["total_value", "recency", "frequency", "churn_prob"], index=0)
    with col_sort2:
        sort_order = st.radio("Sort Order", ["Descending", "Ascending"], index=0)
    ascending = (sort_order == "Ascending")
    sorted_df = filtered_df.sort_values(by=sort_by, ascending=ascending)
    st.dataframe(sorted_df.style.format({
        'total_value': '{:,.0f}', 'avg_value': '{:,.0f}', 'avg_price': '{:,.0f}',
        'churn_prob': '{:.2f}', 'purchase_std': '{:.2f}'
    }), use_container_width=True)

    # Download filtered data
    st.header("Download Filtered Data")
    csv = sorted_df.to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name="filtered_churn_data.csv",
        mime="text/csv"
    )

# Tab 3: Visualizations
with tab3:
    st.header("Visualize Churn Patterns")
    st.markdown("Explore relationships between key metrics to identify trends.")

    # Scatter plot: Total Value vs. Recency
    st.subheader("Total Value vs. Recency by Churn Score")
    fig_scatter = px.scatter(
        sorted_df,
        x="recency",
        y="total_value",
        color="churn_score",
        size="frequency",
        hover_data=["cstName", "churn_prob", "total_value", "frequency"],
        log_y=True,
        color_continuous_scale='Viridis',
        title="Total Value vs. Recency (Color by Churn Score, Size by Frequency)",
        labels={"recency": "Recency (Days)", "total_value": "Total Value (Log Scale)"}
    )
    fig_scatter.update_layout(title_x=0.5)
    st.plotly_chart(fig_scatter, use_container_width=True)

    # Box plot: Total Value by Churn Score
    st.subheader("Total Value Distribution by Churn Score")
    fig_box = px.box(
        sorted_df,
        x="churn_score",
        y="total_value",
        color="churn_score",
        log_y=True,
        color_discrete_sequence=px.colors.sequential.Blues,
        title="Total Value Distribution by Churn Score",
        labels={"churn_score": "Churn Score", "total_value": "Total Value (Log Scale)"}
    )
    fig_box.update_layout(showlegend=False, title_x=0.5)
    st.plotly_chart(fig_box, use_container_width=True)