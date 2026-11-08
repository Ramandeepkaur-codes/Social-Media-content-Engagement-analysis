"""
Complete End-to-End Pipeline for Social Media Content Engagement Analysis (DA-020)
Group: BT_DA_32 | Section: E | Mentor: Mr. Unwan Khan
Project ID: DA-020

This script:
1. Generates the raw dataset with realistic social media post metrics and intentional NaNs.
2. Cleans and imputes missing metrics according to course requirements.
3. Computes standardized engagement rates (ERR % and ERI %) and interaction ratios.
4. Performs comparative group analysis across Formats and Timing.
5. Produces post performance rankings (Top 10 & Bottom 5).
6. Generates all 4 required analytical charts using Matplotlib and Seaborn.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    outputs_dir = os.path.join(base_dir, "outputs")
    charts_dir = os.path.join(outputs_dir, "charts")

    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(outputs_dir, exist_ok=True)
    os.makedirs(charts_dir, exist_ok=True)

    print("=" * 70)
    print("RUNNING SOCIAL MEDIA CONTENT ENGAGEMENT ANALYSIS PIPELINE (DA-020)")
    print("=" * 70)

    # -------------------------------------------------------------
    # 1. GENERATE RAW DATASET (100 Realistic Posts)
    # -------------------------------------------------------------
    print("\n[1/6] Generating Raw Post-Level Dataset...")
    np.random.seed(42)

    post_types = ['Reel', 'Carousel', 'Static Image', 'Text Post']
    dates = pd.date_range(start="2024-01-01", periods=100, freq='28h')

    records = []
    for i in range(100):
        pid = f"POST_{i+1:03d}"
        ptype = post_types[i % 4]
        pub_time = dates[i]

        if ptype == 'Reel':
            impressions = int(np.random.normal(25000, 4000))
            reach = int(impressions * np.random.uniform(0.75, 0.82))
            likes = int(reach * np.random.uniform(0.07, 0.09))
            comments = int(likes * np.random.uniform(0.06, 0.09))
            shares = int(reach * np.random.uniform(0.012, 0.020))
            saves = int(reach * np.random.uniform(0.018, 0.025))
        elif ptype == 'Carousel':
            impressions = int(np.random.normal(16000, 2500))
            reach = int(impressions * np.random.uniform(0.70, 0.76))
            likes = int(reach * np.random.uniform(0.055, 0.075))
            comments = int(likes * np.random.uniform(0.06, 0.09))
            shares = int(reach * np.random.uniform(0.005, 0.009))
            saves = int(reach * np.random.uniform(0.020, 0.028))
        elif ptype == 'Static Image':
            impressions = int(np.random.normal(6500, 800))
            reach = int(impressions * np.random.uniform(0.68, 0.73))
            likes = int(reach * np.random.uniform(0.035, 0.048))
            comments = int(likes * np.random.uniform(0.04, 0.07))
            shares = int(reach * np.random.uniform(0.001, 0.003))
            saves = int(reach * np.random.uniform(0.003, 0.006))
        else: # Text Post
            impressions = int(np.random.normal(4200, 500))
            reach = int(impressions * np.random.uniform(0.68, 0.75))
            likes = int(reach * np.random.uniform(0.030, 0.042))
            comments = int(likes * np.random.uniform(0.14, 0.22))
            shares = int(reach * np.random.uniform(0.002, 0.005))
            saves = int(reach * np.random.uniform(0.001, 0.003))

        records.append({
            'post_id': pid,
            'post_type': ptype,
            'published_at': pub_time.strftime("%Y-%m-%d %H:%M:%S"),
            'impressions': max(impressions, 1000),
            'reach': max(reach, 800),
            'likes': max(likes, 10),
            'comments': max(comments, 0),
            'shares': max(shares, 0),
            'saves': max(saves, 0)
        })

    raw_df = pd.DataFrame(records)

    # Introduce intentional NaNs to test missing metric handling (Requirement)
    raw_df.loc[[6, 28, 58, 88], 'reach'] = np.nan
    raw_df.loc[[8, 17, 77], 'comments'] = np.nan

    raw_csv_path = os.path.join(data_dir, "social_media_engagement_data.csv")
    raw_df.to_csv(raw_csv_path, index=False)
    print(f"   -> Raw dataset saved: {raw_csv_path} ({len(raw_df)} rows)")

    # -------------------------------------------------------------
    # 2. CLEAN & ENGINEER DATASET (Step 2)
    # -------------------------------------------------------------
    print("\n[2/6] Cleaning Data & Imputing Missing Values...")
    df = pd.read_csv(raw_csv_path)

    # Impute missing comments with 0
    for col in ['likes', 'comments', 'shares', 'saves']:
        df[col] = df[col].fillna(0).astype(int)

    # Impute missing reach using median reach-to-impressions ratio per format
    known_mask = df['reach'].notnull()
    ratio_per_type = (df.loc[known_mask, 'reach'] / df.loc[known_mask, 'impressions']).groupby(df['post_type']).median()

    def impute_reach(row):
        if pd.isnull(row['reach']):
            return int(round(row['impressions'] * ratio_per_type.get(row['post_type'], 0.72)))
        return int(row['reach'])

    df['reach'] = df.apply(impute_reach, axis=1)

    # Datetime features
    df['published_at'] = pd.to_datetime(df['published_at'])
    df['day_of_week'] = df['published_at'].dt.day_name()
    df['hour_of_day'] = df['published_at'].dt.hour
    df['is_weekend'] = df['published_at'].dt.dayofweek.apply(lambda x: 1 if x >= 5 else 0)

    def get_time_slot(hour):
        if 6 <= hour < 12:
            return "Morning (6AM-12PM)"
        elif 12 <= hour < 17:
            return "Afternoon (12PM-5PM)"
        elif 17 <= hour < 21:
            return "Evening (5PM-9PM)"
        else:
            return "Night (9PM-6AM)"

    df['time_slot'] = df['hour_of_day'].apply(get_time_slot)

    # Documented KPI Calculations
    df['total_interactions'] = df['likes'] + df['comments'] + df['shares'] + df['saves']
    df['err_percent'] = ((df['total_interactions'] / df['reach']) * 100).round(2)
    df['eri_percent'] = ((df['total_interactions'] / df['impressions']) * 100).round(2)
    df['comment_to_like_ratio'] = np.where(df['likes'] > 0, (df['comments'] / df['likes']).round(4), 0)
    df['shares_per_1k_reach'] = ((df['shares'] / df['reach']) * 1000).round(2)

    cleaned_csv_path = os.path.join(data_dir, "cleaned_social_media_data.csv")
    df.to_csv(cleaned_csv_path, index=False)
    print(f"   -> Cleaned dataset saved: {cleaned_csv_path}")

    # -------------------------------------------------------------
    # 3. GROUP COMPARISONS (Step 3)
    # -------------------------------------------------------------
    print("\n[3/6] Computing Format & Timing Group Aggregations...")
    format_agg = df.groupby('post_type').agg(
        posts=('post_id', 'count'),
        avg_reach=('reach', 'mean'),
        avg_interactions=('total_interactions', 'mean'),
        mean_err=('err_percent', 'mean'),
        median_err=('err_percent', 'median'),
        mean_eri=('eri_percent', 'mean'),
        avg_saves=('saves', 'mean')
    ).round(2).sort_values(by='mean_err', ascending=False)
    print(format_agg)

    # -------------------------------------------------------------
    # 4. PERFORMANCE RANKINGS (Step 4)
    # -------------------------------------------------------------
    print("\n[4/6] Generating Top 10 and Bottom 5 Post Performance Rankings...")
    top_10 = df.sort_values(by='err_percent', ascending=False).head(10).copy()
    top_10['rank_category'] = 'Top 10 High Performer'
    top_10['rank'] = range(1, 11)

    bottom_5 = df.sort_values(by='err_percent', ascending=True).head(5).copy()
    bottom_5['rank_category'] = 'Bottom 5 Underperformer'
    bottom_5['rank'] = range(1, 6)

    rankings_df = pd.concat([top_10, bottom_5], ignore_index=True)
    rankings_csv = os.path.join(outputs_dir, "post_performance_rankings.csv")
    rankings_df.to_csv(rankings_csv, index=False)
    print(f"   -> Post performance rankings saved: {rankings_csv}")

    # -------------------------------------------------------------
    print('\n[4/6] Standardized metrics and post performance rankings generated.')
    print('=' * 70)

if __name__ == '__main__':
    main()