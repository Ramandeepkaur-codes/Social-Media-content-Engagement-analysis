"""
Social Media Content Engagement Analysis Dashboard (DA-020)
Academic Program: B.Tech — Intro to Data Analytics | Semester III, Section E
Mentor: Mr. Unwan Khan
"""

import os
import pandas as pd
import numpy as np
import altair as alt
import streamlit as st

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Social Media Engagement Analytics",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# CUSTOM CSS STYLING
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Top Header Card */
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    .main-header h1 {
        color: #ffffff;
        font-weight: 700;
        margin: 0 0 8px 0;
        font-size: 28px;
    }
    .main-header p {
        color: #e0e7ff;
        font-size: 14px;
        margin: 0;
    }
    .badge-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 12px;
    }
    .badge {
        background: rgba(255, 255, 255, 0.2);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
        backdrop-filter: blur(4px);
    }
    
    /* Metric Cards */
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
        margin-bottom: 15px;
    }
    .metric-title {
        font-size: 13px;
        color: #6b7280;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 26px;
        font-weight: 700;
        color: #111827;
        margin: 4px 0;
    }
    .metric-sub {
        font-size: 12px;
        color: #10b981;
        font-weight: 500;
    }
    
    /* Insight Box */
    .insight-box {
        background: #f0fdf4;
        border-left: 4px solid #16a34a;
        padding: 16px 20px;
        border-radius: 0 8px 8px 0;
        margin: 15px 0;
        color: #166534;
        font-size: 14px;
    }
    
    .experiment-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 16px;
    }
    .experiment-title {
        font-size: 16px;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATA LOADING & CACHING
# -----------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
CHARTS_DIR = os.path.join(OUTPUTS_DIR, "charts")

CLEANED_CSV = os.path.join(DATA_DIR, "cleaned_social_media_data.csv")
RAW_CSV = os.path.join(DATA_DIR, "social_media_engagement_data.csv")
RANKINGS_CSV = os.path.join(OUTPUTS_DIR, "post_performance_rankings.csv")

@st.cache_data
def load_data():
    if not os.path.exists(CLEANED_CSV):
        # Fallback: run pipeline if cleaned data does not exist
        import subprocess
        subprocess.run(["python", os.path.join(BASE_DIR, "run_pipeline.py")], check=True)
    
    df = pd.read_csv(CLEANED_CSV)
    df['published_at'] = pd.to_datetime(df['published_at'])
    return df

@st.cache_data
def load_rankings():
    if os.path.exists(RANKINGS_CSV):
        return pd.read_csv(RANKINGS_CSV)
    return None

try:
    df_raw = load_data()
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# -----------------------------------------------------------------------------
# SIDEBAR FILTERS & CONTROLS
# -----------------------------------------------------------------------------
st.sidebar.image("https://img.icons8.com/clouds/200/000000/social-network.png", width=90)
st.sidebar.title("🎛️ Control Panel")
st.sidebar.markdown("Filter posts by content formats, time windows, and engagement thresholds.")

# Format Filter
all_formats = sorted(df_raw['post_type'].unique())
selected_formats = st.sidebar.multiselect(
    "Content Formats",
    options=all_formats,
    default=all_formats,
    help="Select one or more content formats to analyze."
)

# Day of Week Filter
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
all_days = [d for d in days_order if d in df_raw['day_of_week'].unique()]
selected_days = st.sidebar.multiselect(
    "Day of Week",
    options=all_days,
    default=all_days,
    help="Select publishing days."
)

# Time Slot Filter
slot_order = ['Morning (6AM-12PM)', 'Afternoon (12PM-5PM)', 'Evening (5PM-9PM)', 'Night (9PM-6AM)']
all_slots = [s for s in slot_order if s in df_raw['time_slot'].unique()]
selected_slots = st.sidebar.multiselect(
    "Publishing Time Slot",
    options=all_slots,
    default=all_slots,
    help="Select day time windows."
)

# Metric Sliders
min_reach = int(df_raw['reach'].min())
max_reach = int(df_raw['reach'].max())
reach_range = st.sidebar.slider(
    "Unique Reach Range",
    min_value=min_reach,
    max_value=max_reach,
    value=(min_reach, max_reach),
    step=200
)

min_err = float(df_raw['err_percent'].min())
max_err = float(df_raw['err_percent'].max())
err_range = st.sidebar.slider(
    "Engagement Rate by Reach (ERR %)",
    min_value=min_err,
    max_value=max_err,
    value=(min_err, max_err),
    step=0.2
)

# Apply Filters
filtered_df = df_raw[
    (df_raw['post_type'].isin(selected_formats)) &
    (df_raw['day_of_week'].isin(selected_days)) &
    (df_raw['time_slot'].isin(selected_slots)) &
    (df_raw['reach'] >= reach_range[0]) &
    (df_raw['reach'] <= reach_range[1]) &
    (df_raw['err_percent'] >= err_range[0]) &
    (df_raw['err_percent'] <= err_range[1])
].copy()

# Sidebar Reset / Data Refresh
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Showing:** `{len(filtered_df)}` of `{len(df_raw)}` posts")
if st.sidebar.button("🔄 Recompute / Refresh Pipeline"):
    st.cache_data.clear()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("""
**Project Details:**
- **ID:** `DA-020` | Section E
- **Program:** B.Tech Data Analytics
- **Mentor:** Mr. Unwan Khan
""")

# -----------------------------------------------------------------------------
# MAIN HEADER
# -----------------------------------------------------------------------------
st.markdown("""
<div class="main-header">
    <h1>📱 Social Media Content Engagement Analytics Dashboard</h1>
    <p>Executive Analytics & Quantitative Decision Support System for Multi-Format Digital Publishing</p>
    <div class="badge-container">
        <span class="badge">🎓 B.Tech Data Analytics</span>
        <span class="badge">🏷️ Project ID: DA-020</span>
        <span class="badge">👤 Lead: Ramandeep Kaur</span>
        <span class="badge">👨‍🏫 Mentor: Mr. Unwan Khan</span>
        <span class="badge">🔒 Ethical Organic Dataset (No PII)</span>
    </div>
</div>
""", unsafe_allow_html=True)

if filtered_df.empty:
    st.warning("⚠️ No posts match the current filter selection. Please adjust your sidebar filters.")
    st.stop()

# -----------------------------------------------------------------------------
# GLOBAL TOP KPI METRIC ROW
# -----------------------------------------------------------------------------
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Total Posts</div>
        <div class="metric-value">{}</div>
        <div class="metric-sub">Analyzed Content</div>
    </div>
    """.format(len(filtered_df)), unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Gross Impressions</div>
        <div class="metric-value">{:,.0f}</div>
        <div class="metric-sub">Total Screen Views</div>
    </div>
    """.format(filtered_df['impressions'].sum()), unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Unique Reach</div>
        <div class="metric-value">{:,.0f}</div>
        <div class="metric-sub">Distinct Accounts</div>
    </div>
    """.format(filtered_df['reach'].sum()), unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Total Interactions</div>
        <div class="metric-value">{:,.0f}</div>
        <div class="metric-sub">Likes+Comms+Shares+Saves</div>
    </div>
    """.format(filtered_df['total_interactions'].sum()), unsafe_allow_html=True)

with col5:
    avg_err = filtered_df['err_percent'].mean()
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Mean ERR (%)</div>
        <div class="metric-value">{:.2f}%</div>
        <div class="metric-sub">Per Audience Reach</div>
    </div>
    """.format(avg_err), unsafe_allow_html=True)

with col6:
    avg_eri = filtered_df['eri_percent'].mean()
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Mean ERI (%)</div>
        <div class="metric-value">{:.2f}%</div>
        <div class="metric-sub">Per Impression Feed</div>
    </div>
    """.format(avg_eri), unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DASHBOARD TABS
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📈 Executive Overview",
    "📊 Format Analysis (Chart 1 & 2)",
    "⏰ Timing & Heatmap (Chart 3)",
    "🚀 Virality & Reach (Chart 4)",
    "🏆 Post Performance Rankings",
    "🧪 Marketing Experiments & Simulator",
    "📚 Methodology & Formulas"
])

# =============================================================================
# TAB 1: EXECUTIVE OVERVIEW
# =============================================================================
with tab1:
    st.subheader("Executive Summary & Content Performance Overview")
    st.markdown(
        "Quantitative comparison of content format resonance, interaction compositions, and core marketing metrics."
    )
    
    c_left, c_right = st.columns([3, 2])
    
    with c_left:
        st.markdown("##### 📊 Engagement Rates by Content Format (ERR % vs. ERI %)")
        agg_summary = filtered_df.groupby('post_type').agg(
            mean_err=('err_percent', 'mean'),
            mean_eri=('eri_percent', 'mean'),
            total_posts=('post_id', 'count')
        ).reset_index()
        
        melted_agg = pd.melt(
            agg_summary, 
            id_vars=['post_type'], 
            value_vars=['mean_err', 'mean_eri'],
            var_name='Metric', 
            value_name='Rate'
        )
        melted_agg['Metric'] = melted_agg['Metric'].map({
            'mean_err': 'ERR % (By Reach)',
            'mean_eri': 'ERI % (By Impressions)'
        })
        
        chart_summary = alt.Chart(melted_agg).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6).encode(
            x=alt.X('post_type:N', title='Content Format', axis=alt.Axis(labelAngle=0)),
            y=alt.Y('Rate:Q', title='Average Rate (%)'),
            color=alt.Color('Metric:N', scale=alt.Scale(domain=['ERR % (By Reach)', 'ERI % (By Impressions)'], range=['#2563eb', '#10b981'])),
            xOffset='Metric:N',
            tooltip=[
                alt.Tooltip('post_type:N', title='Format'),
                alt.Tooltip('Metric:N', title='Metric Type'),
                alt.Tooltip('Rate:Q', format='.2f', title='Rate (%)')
            ]
        ).properties(height=340)
        
        st.altair_chart(chart_summary, use_container_width=True)
    
    with c_right:
        st.markdown("##### 🧩 Interaction Composition by Format")
        comp_df = filtered_df.groupby('post_type').agg({
            'likes': 'sum',
            'comments': 'sum',
            'shares': 'sum',
            'saves': 'sum'
        }).reset_index()
        
        comp_melted = pd.melt(
            comp_df,
            id_vars=['post_type'],
            value_vars=['likes', 'comments', 'shares', 'saves'],
            var_name='Interaction Type',
            value_name='Count'
        )
        
        comp_chart = alt.Chart(comp_melted).mark_bar().encode(
            x=alt.X('sum(Count):Q', stack='normalize', title='Share of Total Interactions', axis=alt.Axis(format='%')),
            y=alt.Y('post_type:N', title='Format'),
            color=alt.Color('Interaction Type:N', scale=alt.Scale(scheme='category10')),
            tooltip=[
                alt.Tooltip('post_type:N', title='Format'),
                alt.Tooltip('Interaction Type:N', title='Type'),
                alt.Tooltip('sum(Count):Q', format=',.0f', title='Total Count')
            ]
        ).properties(height=340)
        
        st.altair_chart(comp_chart, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
        💡 <b>Key Finding:</b> <b>Reels</b> deliver the highest reach efficiency and top overall ERR (<b>~12.2%</b>), while <b>Carousels</b> dominate high-intent engagement with the highest proportion of bookmarks/saves (<b>~2.4% save rate</b>). <b>Text Posts</b> generate disproportionately high comment-to-like ratios (<b>> 0.16</b>), acting as prime community conversation starters.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("##### 📋 Group Summary Aggregations")
    fmt_stats = filtered_df.groupby('post_type').agg(
        Posts=('post_id', 'count'),
        Avg_Reach=('reach', lambda x: f"{x.mean():,.0f}"),
        Avg_Impressions=('impressions', lambda x: f"{x.mean():,.0f}"),
        Avg_Interactions=('total_interactions', lambda x: f"{x.mean():,.0f}"),
        Mean_ERR=('err_percent', lambda x: f"{x.mean():.2f}%"),
        Median_ERR=('err_percent', lambda x: f"{x.median():.2f}%"),
        Mean_ERI=('eri_percent', lambda x: f"{x.mean():.2f}%"),
        Avg_Saves=('saves', lambda x: f"{x.mean():,.0f}"),
        Shares_per_1k=('shares_per_1k_reach', lambda x: f"{x.mean():.2f}")
    ).reset_index()
    st.dataframe(fmt_stats, use_container_width=True, hide_index=True)

# =============================================================================
# TAB 2: FORMAT ANALYSIS (CHART 1 & 2)
# =============================================================================
with tab2:
    st.subheader("Content Format Performance Analysis")
    st.markdown(
        "Investigating the variance, average engagement rate, and outlier boundaries across all 4 publishing formats."
    )
    
    f_col1, f_col2 = st.columns(2)
    
    with f_col1:
        st.markdown("#### 📊 Chart 1: Mean Engagement Rate (ERR %) by Content Format")
        fmt_agg = filtered_df.groupby('post_type')['err_percent'].mean().reset_index()
        fmt_agg.columns = ['post_type', 'mean_err']
        
        chart1_alt = alt.Chart(fmt_agg).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8).encode(
            x=alt.X('post_type:N', title='Content Format', sort=['Reel', 'Carousel', 'Static Image', 'Text Post'], axis=alt.Axis(labelAngle=0)),
            y=alt.Y('mean_err:Q', title='Mean ERR (%)', scale=alt.Scale(domain=[0, fmt_agg['mean_err'].max() * 1.25])),
            color=alt.Color('post_type:N', legend=None, scale=alt.Scale(range=['#1f77b4', '#2ca02c', '#ff7f0e', '#9467bd'])),
            tooltip=[
                alt.Tooltip('post_type:N', title='Format'),
                alt.Tooltip('mean_err:Q', format='.2f', title='Mean ERR (%)')
            ]
        )
        
        text1 = chart1_alt.mark_text(
            align='center',
            baseline='bottom',
            dy=-5,
            fontWeight='bold',
            fontSize=12
        ).encode(
            text=alt.Text('mean_err:Q', format='.2f')
        )
        
        st.altair_chart(chart1_alt + text1, use_container_width=True)
        st.caption("Standardized formula: Total Interactions (Likes + Comments + Shares + Saves) divided by Unique Reach.")
    
    with f_col2:
        st.markdown("#### 📦 Chart 2: Engagement Rate Distribution & Spread (Boxplot)")
        
        chart2_box = alt.Chart(filtered_df).mark_boxplot(extent='min-max', size=45).encode(
            x=alt.X('post_type:N', title='Content Format', sort=['Reel', 'Carousel', 'Static Image', 'Text Post'], axis=alt.Axis(labelAngle=0)),
            y=alt.Y('err_percent:Q', title='Engagement Rate by Reach (ERR %)'),
            color=alt.Color('post_type:N', legend=None, scale=alt.Scale(range=['#1f77b4', '#2ca02c', '#ff7f0e', '#9467bd']))
        )
        
        stripplot = alt.Chart(filtered_df).mark_circle(size=35, opacity=0.4, color='#1e293b').encode(
            x=alt.X('post_type:N', sort=['Reel', 'Carousel', 'Static Image', 'Text Post']),
            y=alt.Y('err_percent:Q'),
            tooltip=['post_id', 'post_type', 'err_percent', 'reach', 'total_interactions']
        )
        
        st.altair_chart(chart2_box + stripplot, use_container_width=True)
        st.caption("Box shows 25th, 50th (median), and 75th percentiles. Dots display individual post distributions.")

    with st.expander("🖼️ View Original Publication-Grade Matplotlib/Seaborn Charts"):
        c1_img = os.path.join(CHARTS_DIR, "chart1_engagement_by_format.png")
        c2_img = os.path.join(CHARTS_DIR, "chart2_engagement_distribution_boxplot.png")
        ic1, ic2 = st.columns(2)
        if os.path.exists(c1_img):
            ic1.image(c1_img, caption="Chart 1: Mean ERR % (High-Res Seaborn Render)")
        if os.path.exists(c2_img):
            ic2.image(c2_img, caption="Chart 2: Distribution Boxplot (High-Res Seaborn Render)")

# =============================================================================
# TAB 3: TIMING & HEATMAP (CHART 3)
# =============================================================================
with tab3:
    st.subheader("Publishing Timing & Day-Part Heatmap Analysis")
    st.markdown(
        "Identifying peak engagement density windows across days of the week and daytime slots for editorial scheduling."
    )
    
    t_col1, t_col2 = st.columns([3, 2])
    
    with t_col1:
        st.markdown("#### 🗓️ Chart 3: Publishing Heatmap (Day of Week vs. Time Slot)")
        
        # Prepare heatmap data
        heatmap_data = filtered_df.groupby(['day_of_week', 'time_slot'])['err_percent'].mean().reset_index()
        
        heatmap_chart = alt.Chart(heatmap_data).mark_rect().encode(
            x=alt.X('time_slot:N', title='Publishing Time Window', sort=slot_order),
            y=alt.Y('day_of_week:N', title='Day of Week', sort=days_order),
            color=alt.Color('err_percent:Q', title='Mean ERR (%)', scale=alt.Scale(scheme='yellowgreenblue')),
            tooltip=[
                alt.Tooltip('day_of_week:N', title='Day'),
                alt.Tooltip('time_slot:N', title='Time Window'),
                alt.Tooltip('err_percent:Q', format='.2f', title='Mean ERR (%)')
            ]
        ).properties(height=360)
        
        text_hm = heatmap_chart.mark_text(baseline='middle', fontWeight='bold').encode(
            text=alt.Text('err_percent:Q', format='.2f'),
            color=alt.condition(alt.datum.err_percent > 8, alt.value('white'), alt.value('black'))
        )
        
        st.altair_chart(heatmap_chart + text_hm, use_container_width=True)
    
    with t_col2:
        st.markdown("#### 📊 Weekend vs. Weekday Performance")
        weekend_agg = filtered_df.groupby('is_weekend').agg(
            posts=('post_id', 'count'),
            mean_err=('err_percent', 'mean'),
            mean_reach=('reach', 'mean')
        ).reset_index()
        weekend_agg['Type'] = weekend_agg['is_weekend'].map({0: 'Weekday (Mon-Fri)', 1: 'Weekend (Sat-Sun)'})
        
        we_chart = alt.Chart(weekend_agg).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6).encode(
            x=alt.X('Type:N', title='', axis=alt.Axis(labelAngle=0)),
            y=alt.Y('mean_err:Q', title='Mean ERR (%)'),
            color=alt.Color('Type:N', scale=alt.Scale(range=['#3b82f6', '#f59e0b']), legend=None),
            tooltip=[
                alt.Tooltip('Type:N', title='Period'),
                alt.Tooltip('mean_err:Q', format='.2f', title='Mean ERR (%)'),
                alt.Tooltip('posts:Q', title='Total Posts')
            ]
        ).properties(height=220)
        
        we_text = we_chart.mark_text(dy=-5, fontWeight='bold').encode(text=alt.Text('mean_err:Q', format='.2f'))
        st.altair_chart(we_chart + we_text, use_container_width=True)
        
        st.markdown("##### 🏆 Top 3 Publishing Time Slots:")
        top_slots = heatmap_data.sort_values(by='err_percent', ascending=False).head(3)
        for _, row in top_slots.iterrows():
            st.markdown(f"⭐ **{row['day_of_week']} - {row['time_slot']}**: `{row['err_percent']:.2f}%` Mean ERR")

    with st.expander("🖼️ View Original Publication Heatmap (Matplotlib/Seaborn)"):
        c3_img = os.path.join(CHARTS_DIR, "chart3_timing_heatmap.png")
        if os.path.exists(c3_img):
            st.image(c3_img, caption="Chart 3: Publishing Heatmap (High-Res Render)")

# =============================================================================
# TAB 4: VIRALITY & REACH (CHART 4)
# =============================================================================
with tab4:
    st.subheader("Audience Reach vs. Total Interactions & Virality Efficiency")
    st.markdown(
        "Evaluating interaction yields per unique audience reach and identifying advocacy ratios."
    )
    
    v_col1, v_col2 = st.columns([3, 2])
    
    with v_col1:
        st.markdown("#### 🎯 Chart 4: Reach vs. Total Interactions (Virality Slope)")
        
        scatter_chart = alt.Chart(filtered_df).mark_circle(size=90, opacity=0.85).encode(
            x=alt.X('reach:Q', title='Unique Audience Reach'),
            y=alt.Y('total_interactions:Q', title='Total Interactions (Likes+Comments+Shares+Saves)'),
            color=alt.Color('post_type:N', title='Content Format', scale=alt.Scale(range=['#1f77b4', '#2ca02c', '#ff7f0e', '#9467bd'])),
            tooltip=[
                alt.Tooltip('post_id:N', title='Post ID'),
                alt.Tooltip('post_type:N', title='Format'),
                alt.Tooltip('reach:Q', format=',.0f', title='Reach'),
                alt.Tooltip('total_interactions:Q', format=',.0f', title='Interactions'),
                alt.Tooltip('err_percent:Q', format='.2f', title='ERR (%)')
            ]
        ).properties(height=380)
        
        trend = scatter_chart.transform_regression(
            'reach', 'total_interactions'
        ).mark_line(color='#111827', strokeDash=[4, 4], size=2)
        
        st.altair_chart(scatter_chart + trend, use_container_width=True)
        st.caption("Dashed line represents linear virality efficiency trend. High outliers indicate virality breakthrough.")
    
    with v_col2:
        st.markdown("#### 💬 Community Discussion vs. Virality")
        ratio_chart = alt.Chart(filtered_df).mark_circle(size=80, opacity=0.8).encode(
            x=alt.X('shares_per_1k_reach:Q', title='Shares per 1,000 Reach (Virality)'),
            y=alt.Y('comment_to_like_ratio:Q', title='Comment-to-Like Ratio (Discussion)'),
            color=alt.Color('post_type:N', scale=alt.Scale(range=['#1f77b4', '#2ca02c', '#ff7f0e', '#9467bd']), legend=None),
            tooltip=['post_id', 'post_type', 'shares_per_1k_reach', 'comment_to_like_ratio']
        ).properties(height=380)
        
        st.altair_chart(ratio_chart, use_container_width=True)
        st.caption("Top-Left: Discussion Drivers (Text Posts). Bottom-Right: Virality Drivers (Reels/Carousels).")

    with st.expander("🖼️ View Original Chart 4 (Matplotlib/Seaborn)"):
        c4_img = os.path.join(CHARTS_DIR, "chart4_reach_vs_interactions_virality.png")
        if os.path.exists(c4_img):
            st.image(c4_img, caption="Chart 4: Reach vs Interactions (High-Res Render)")

# =============================================================================
# TAB 5: POST RANKINGS & DATA EXPLORER
# =============================================================================
with tab5:
    st.subheader("Post Performance Rankings & Complete Data Explorer")
    st.markdown("Top 10 high-performing posts and Bottom 5 underperformers based on ERR %.")
    
    rank_tab1, rank_tab2, rank_tab3 = st.tabs(["🥇 Top 10 High Performers", "🔻 Bottom 5 Underperformers", "📋 Complete Dataset Explorer"])
    
    with rank_tab1:
        top_10 = filtered_df.sort_values(by='err_percent', ascending=False).head(10).copy()
        top_10.insert(0, 'Rank', [f"#{i+1}" for i in range(len(top_10))])
        
        st.markdown("##### 🏆 Top 10 Ranked Posts by Engagement Rate by Reach (ERR %)")
        st.dataframe(
            top_10[['Rank', 'post_id', 'post_type', 'published_at', 'reach', 'impressions', 'total_interactions', 'likes', 'comments', 'shares', 'saves', 'err_percent', 'eri_percent']],
            use_container_width=True,
            hide_index=True
        )
    
    with rank_tab2:
        bottom_5 = filtered_df.sort_values(by='err_percent', ascending=True).head(5).copy()
        bottom_5.insert(0, 'Rank', [f"Underperformer #{i+1}" for i in range(len(bottom_5))])
        
        st.markdown("##### ⚠️ Bottom 5 Lowest Performing Posts")
        st.dataframe(
            bottom_5[['Rank', 'post_id', 'post_type', 'published_at', 'reach', 'impressions', 'total_interactions', 'likes', 'comments', 'shares', 'saves', 'err_percent', 'eri_percent']],
            use_container_width=True,
            hide_index=True
        )
        st.warning("Recommendation for underperformers: Avoid publishing static single images during off-peak morning hours without clear Call-To-Action (CTA) prompts.")

    with rank_tab3:
        st.markdown("##### 🔍 Full Interactive Post-Level Data Explorer")
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        
        # Download Filtered Data Button
        csv_download = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Dataset as CSV",
            data=csv_download,
            file_name="filtered_social_media_engagement.csv",
            mime="text/csv"
        )

# =============================================================================
# TAB 6: MARKETING EXPERIMENTS & SIMULATOR
# =============================================================================
with tab6:
    st.subheader("Structured Marketing Experiments & Interactive What-If Simulator")
    st.markdown(
        "Actionable A/B testing frameworks proposed for editorial teams and interactive scenario simulation."
    )
    
    e1, e2, e3 = st.columns(3)
    
    with e1:
        st.markdown("""
        <div class="experiment-card">
            <div class="experiment-title">🧪 Experiment 1: Carousel Save Lift</div>
            <p><b>Hypothesis:</b> Publishing 6-slide educational carousels with tactical frameworks will lift the Save-to-Reach ratio by >35% compared to static infographics.</p>
            <p><b>Primary Metric:</b> <code>Saves / Reach</code></p>
            <p><b>Target Window:</b> Tuesday & Thursday Midday</p>
        </div>
        """, unsafe_allow_html=True)
        
    with e2:
        st.markdown("""
        <div class="experiment-card">
            <div class="experiment-title">🧪 Experiment 2: Mid-Week Evening Window</div>
            <p><b>Hypothesis:</b> Shifting campaign launches from Tuesday 10:00 AM to Wednesday/Thursday 7:00 PM will increase first-24h ERR% by at least 2.5 percentage points.</p>
            <p><b>Primary Metric:</b> <code>ERR %</code></p>
            <p><b>Target Window:</b> Wednesday / Thursday 5PM-9PM</p>
        </div>
        """, unsafe_allow_html=True)
        
    with e3:
        st.markdown("""
        <div class="experiment-card">
            <div class="experiment-title">🧪 Experiment 3: Discussion Prompts</div>
            <p><b>Hypothesis:</b> Text Posts featuring polarizing industry debates and prompt questions will maintain Comment-to-Like ratio > 0.15.</p>
            <p><b>Primary Metric:</b> <code>Comments / Likes</code></p>
            <p><b>Target Window:</b> Monday & Tuesday Morning</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🧮 Interactive 'What-If' Post Engagement Simulator")
    st.markdown("Predict the expected engagement rates, total interactions, and benchmark comparison for an upcoming planned post.")
    
    sim_col1, sim_col2 = st.columns([1, 1])
    
    with sim_col1:
        sim_type = st.selectbox("Planned Content Format", options=['Reel', 'Carousel', 'Static Image', 'Text Post'])
        sim_impressions = st.number_input("Estimated Gross Impressions", min_value=1000, max_value=100000, value=20000, step=1000)
        
        # Benchmark defaults based on historical data
        hist_fmt = df_raw[df_raw['post_type'] == sim_type]
        default_reach_ratio = (hist_fmt['reach'] / hist_fmt['impressions']).median()
        default_like_rate = (hist_fmt['likes'] / hist_fmt['reach']).median() * 100
        
        sim_reach = int(sim_impressions * default_reach_ratio)
        st.info(f"Estimated Unique Reach: **{sim_reach:,.0f}** (based on historical {default_reach_ratio:.1%} reach ratio for {sim_type}s)")
        
        sim_likes = st.number_input("Expected Likes", min_value=10, max_value=10000, value=int(sim_reach * (default_like_rate / 100)), step=20)
        sim_comments = st.number_input("Expected Comments", min_value=0, max_value=2000, value=int(sim_likes * 0.08), step=5)
        sim_shares = st.number_input("Expected Shares", min_value=0, max_value=2000, value=int(sim_reach * 0.012), step=5)
        sim_saves = st.number_input("Expected Saves", min_value=0, max_value=2000, value=int(sim_reach * 0.022), step=5)
    
    with sim_col2:
        sim_total_interactions = sim_likes + sim_comments + sim_shares + sim_saves
        sim_err = (sim_total_interactions / sim_reach) * 100
        sim_eri = (sim_total_interactions / sim_impressions) * 100
        sim_c2l = sim_comments / sim_likes if sim_likes > 0 else 0
        sim_shares_1k = (sim_shares / sim_reach) * 1000
        
        historical_median_err = hist_fmt['err_percent'].median()
        historical_top_quartile_err = hist_fmt['err_percent'].quantile(0.75)
        
        st.markdown("#### 🎯 Simulation Results & Benchmark")
        
        res1, res2 = st.columns(2)
        res1.metric("Predicted ERR (%)", f"{sim_err:.2f}%", delta=f"{sim_err - historical_median_err:+.2f}% vs Format Median")
        res2.metric("Predicted Total Interactions", f"{sim_total_interactions:,.0f}")
        
        res3, res4 = st.columns(2)
        res3.metric("Predicted ERI (%)", f"{sim_eri:.2f}%")
        res4.metric("Shares per 1k Reach", f"{sim_shares_1k:.1f}")
        
        if sim_err >= historical_top_quartile_err:
            st.success("🌟 **Top Quartile Performer!** This simulated post beats 75% of historical posts in this category.")
        elif sim_err >= historical_median_err:
            st.info("👍 **Above Average Performer:** Meets standard content benchmark targets.")
        else:
            st.warning("⚠️ **Below Format Median:** Consider boosting save hooks or call-to-actions to elevate interactions.")

# =============================================================================
# TAB 7: METHODOLOGY & FORMULAS
# =============================================================================
with tab7:
    st.subheader("Academic Project Documentation, Mathematical Formulas & Ethics")
    
    doc_col1, doc_col2 = st.columns(2)
    
    with doc_col1:
        st.markdown("#### 📐 Mathematical Formulations & Standardized Metrics")
        st.latex(r"\text{ERR (\%)} = \left(\frac{\text{Likes} + \text{Comments} + \text{Shares} + \text{Saves}}{\text{Reach}}\right) \times 100")
        st.markdown("""
        - **Denominator:** Unique accounts reached. Standard metric for true resonance.
        """)
        
        st.latex(r"\text{ER}_{\text{Imp}} \text{ (\%)} = \left(\frac{\text{Total Interactions}}{\text{Impressions}}\right) \times 100")
        st.markdown("""
        - **Denominator:** Gross impressions (including duplicate feed impressions).
        """)
        
        st.latex(r"\text{Comment-to-Like Ratio} = \frac{\text{Comments}}{\text{Likes}}")
        st.markdown("""
        - **Significance:** Measures discussion depth vs. passive double-tap scrolling.
        """)
        
        st.latex(r"\text{Shares per 1,000 Reach} = \left(\frac{\text{Shares}}{\text{Reach}}\right) \times 1000")
        st.markdown("""
        - **Significance:** Measures viral word-of-mouth advocacy.
        """)
    
    with doc_col2:
        st.markdown("#### 🛡️ Data Ethics, Imputation & Compliance")
        st.markdown("""
        - **Data Privacy:** Synthetic/clean post-level metrics with **zero Personally Identifiable Information (PII)** and **no automated scraping of private user accounts**.
        - **Missing Values Handling:**
            - Missing `reach`: Imputed using format-specific median Reach-to-Impressions ratio:
              $$\\text{Reach}_{\\text{imputed}} = \\text{round}(\\text{Impressions} \\times \\text{Ratio}_{\\text{format}})$$
            - Missing `comments`, `shares`, `saves`: Filled with `0` (reflecting zero user activity rather than null).
        - **Academic Attribution:**
            - **Course:** B.Tech Intro to Data Analytics (Semester III, Section E)
            - **Project ID:** `DA-020`
            - **Mentor:** Mr. Unwan Khan
        """)
        
    st.markdown("---")
    st.markdown("##### 📖 Data Dictionary Quick Reference")
    st.table(pd.DataFrame({
        "Attribute": ["post_id", "post_type", "published_at", "impressions", "reach", "likes", "comments", "shares", "saves", "err_percent", "eri_percent"],
        "Type": ["String (ID)", "Categorical", "Datetime", "Integer", "Integer", "Integer", "Integer", "Integer", "Integer", "Float (%)", "Float (%)"],
        "Description": ["Unique post key", "Format (Reel, Carousel, Image, Text)", "Timestamp", "Screen views", "Unique viewer count", "Positive reactions", "User text comments", "Forward/reshares", "Saved/bookmarked", "Engagement rate by reach", "Engagement rate by impressions"]
    }))

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    "<center style='color:#6b7280; font-size:13px;'>Social Media Content Engagement Analysis Dashboard (DA-020) • Developed for B.Tech Data Analytics Project • 2026</center>",
    unsafe_allow_html=True
)
