# 📖 Data Dictionary — Social Media Content Engagement Analysis (DA-020)

**Project Title:** Social Media Content Engagement Analysis  
**Project ID:** DA-020 | **Section:** E  
**Mentor:** Mr. Unwan Khan  

---

## 📌 Dataset Overview
The dataset contains post-level organic social media metrics tracking user engagement across different content formats, timestamps, and interaction types.

- **File Name:** `social_media_engagement_data.csv`
- **Total Records:** 100 posts
- **Privacy & Compliance:** Public/synthetic post-level metrics. No Personally Identifiable Information (PII) or private account data.

---

## 📊 Column Definitions

| Column Name | Data Type | Description | Unit / Example Values | Missing Values Handling |
|:---|:---:|:---|:---|:---:|
| `post_id` | String | Unique identifier for each social media post | `POST_001`, `POST_042` | No (Primary Key) |
| `post_type` | Categorical | Format of the published content | `Reel`, `Carousel`, `Static Image`, `Text Post` | None |
| `published_at` | Datetime | ISO 8601 timestamp when the post went live | `2024-02-14 19:30:00` | None |
| `impressions` | Integer | Total count of times the post was displayed on screen | Counts (e.g. `24500`, `6800`) | None (Denominator for $ER_{Imp}$) |
| `reach` | Integer | Total number of unique individual accounts who saw the post | Counts (e.g. `19200`, `4900`) | Imputed via format median Reach-to-Impression ratio |
| `likes` | Integer | Total positive feedback clicks | Counts (e.g. `1450`, `210`) | None |
| `comments` | Integer | Total text remarks or replies left by users | Counts (e.g. `112`, `12`) | Filled with `0` (indicates 0 comments) |
| `shares` | Integer | Total forwards or reshared actions | Counts (e.g. `280`, `14`) | Filled with `0` |
| `saves` | Integer | Bookmarks for future reference | Counts (e.g. `340`, `25`) | Filled with `0` |

---

## 📐 Documented Formulas & Denominators

1. **Total Interactions:**
   $$\text{Total Interactions} = \text{Likes} + \text{Comments} + \text{Shares} + \text{Saves}$$

2. **Engagement Rate by Reach (ERR %):**
   $$\text{ERR} (\%) = \left(\frac{\text{Total Interactions}}{\text{Reach}}\right) \times 100$$
   - *Denominator:* Unique accounts reached (best metric for post resonance).

3. **Engagement Rate by Impressions (ERI %):**
   $$\text{ERI} (\%) = \left(\frac{\text{Total Interactions}}{\text{Impressions}}\right) \times 100$$
   - *Denominator:* Total screen views (feed efficiency).

4. **Community Discussion & Virality Ratios:**
   - $\text{Comment-to-Like Ratio} = \frac{\text{Comments}}{\text{Likes}}$
   - $\text{Shares per 1,000 Reach} = \left(\frac{\text{Shares}}{\text{Reach}}\right) \times 1000$

