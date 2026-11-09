# 📱 Social Media Content Engagement Analysis (Project ID: DA-020)

**Academic Program:** B.Tech — Intro to Data Analytics  
**Semester:** III | **Section:** E | **Project ID:** `DA-020`  
**Mentor Name:** Mr. Unwan Khan  

---

## 📌 1. Project Overview & Problem Statement

In digital marketing, content teams produce multiple media formats (Reels/Videos, Carousels, Static Images, Text Posts) and publish across varying hours and days. However, without quantitative analytics, publishing schedules and format selections are often based on guesswork.

### Project Objective:
Explore post-level impressions, reach, likes, comments, shares, saves, and publishing timestamps using an organic dataset to:
1. Formulate and compute standardized **Engagement Rates** ($ERR$ and $ER_{Imp}$).
2. Compare at least two key content attributes (**Content Formats** and **Publishing Timing Windows**).
3. Identify top-performing and underperforming content via performance rankings.
4. Produce **4 core analytical charts** visualizing distributions, efficiency, and peak activity.
5. Propose a structured set of **actionable content experiments** to support editorial planning and campaign reporting.
6. Strictly uphold data ethics: **no scraping of private account data**.

---

## 📐 2. Mathematical Metric Definitions & Formulations

### 1. Engagement Rate by Reach ($ERR$)
$$\text{ERR} (\%) = \left( \frac{\text{Likes} + \text{Comments} + \text{Shares} + \text{Saves}}{\text{Reach}} \right) \times 100$$
- **Numerator:** Total Interactions ($\text{Likes} + \text{Comments} + \text{Shares} + \text{Saves}$)
- **Denominator:** Unique Reach (Number of distinct accounts who viewed the post)

### 2. Engagement Rate by Impressions ($ER_{Imp}$)
$$\text{ER}_{\text{Imp}} (\%) = \left( \frac{\text{Total Interactions}}{\text{Impressions}} \right) \times 100$$
- **Denominator:** Gross Impressions (Total times post appeared on screen, including repeat views)

### 3. Community Discussion vs Virality Ratios:
- **Comment-to-Like Ratio:** $\frac{\text{Comments}}{\text{Likes}}$ (Measures depth of discussion versus casual scrolling)
- **Shares per 1,000 Reach:** $\left( \frac{\text{Shares}}{\text{Reach}} \right) \times 1000$ (Measures advocacy and virality)

---

## 📊 3. Core Analytical Charts (4 Required)

1. **Chart 1 — Mean Engagement Rate by Post Format (Bar Chart):** Compares average ERR % across Reels, Carousels, Images, and Text.
2. **Chart 2 — Engagement Spread & Outliers (Boxplot):** Visualizes the variance, median, and outlier performance within each format.
3. **Chart 3 — Publishing Heatmap (Day of Week vs. Hour of Day):** Highlights high-density engagement time slots for optimal scheduling.
4. **Chart 4 — Reach vs. Total Interactions (Scatter Plot with Hue):** Demonstrates interaction efficiency and virality per viewer.

---

## 🧪 4. Proposed Content Marketing Experiments

- **Experiment 1 (Carousel Save Optimization):** Test 6-slide educational carousels against single static infographics to measure bookmarking lift ($Saves/Reach$).
- **Experiment 2 (Mid-Week Evening Window):** Test scheduling major launches on Wednesday/Thursday 7:00 PM versus Tuesday 10:00 AM to capitalize on high-engagement slots.
- **Experiment 3 (Conversation Prompts):** Use Text/Quote posts on Tuesdays focused on industry hot takes to drive a high Comment-to-Like ratio ($>0.15$).

---

## 📁 5. Repository Directory Structure

```text
Social-Media-content-Engagement-analysis/
│
├── data/
│   ├── social_media_engagement_data.csv   # Raw dataset with post-level metrics
│   ├── cleaned_social_media_data.csv      # Preprocessed & imputed dataset
│   └── data_dictionary.md                 # Metric definitions & documentation
│
├── notebooks/
│   └── Social_Media_Content_Engagement_Analysis.ipynb  # Master Jupyter Notebook
│
├── outputs/
│   ├── charts/
│   │   ├── chart1_engagement_by_format.png
│   │   ├── chart2_engagement_distribution_boxplot.png
│   │   ├── chart3_timing_heatmap.png
│   │   └── chart4_reach_vs_interactions_virality.png
│   └── post_performance_rankings.csv
│
├── reports/
│   └── content_experiments_and_strategy.md   # Marketing experiments & recommendations
│
├── run_pipeline.py                        # Complete analytics pipeline runner
├── app.py                                 # Interactive Streamlit Web Analytics Dashboard
├── requirements.txt                       # Python dependencies
├── package.json                           # Workspace configuration
├── LICENSE                                # Project license
└── README.md                              # Main documentation
```

---

## 🚀 6. How to Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Ramandeepkaur-codes/Social-Media-content-Engagement-analysis.git
   cd Social-Media-content-Engagement-analysis
   ```

2. **Open in Jupyter Notebook or Google Colab:**
   - Launch Jupyter: `jupyter notebook`
   - Navigate to `notebooks/Social_Media_Content_Engagement_Analysis.ipynb`
   - Run all cells sequentially.

3. **Launch the Interactive Streamlit Web Dashboard:**
   ```bash
   streamlit run app.py
   ```
   Open your browser at `http://localhost:8501` to view the interactive executive dashboard, multi-format filter tools, publishing heatmaps, virality scatter plots, and the A/B scenario simulator.
