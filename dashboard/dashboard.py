import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Set page config
st.set_page_config(page_title="Bike Sharing Analysis Dashboard", page_icon="🚴", layout="wide")

# Load data
@st.cache_data
def load_data():
    df_day = pd.read_csv('main_data.csv')
    df_day['dteday'] = pd.to_datetime(df_day['dteday'])
    
    # Create mappings
    season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    weather_map = {1: 'Clear', 2: 'Mist', 3: 'Light Snow/Rain', 4: 'Heavy Rain'}
    weekday_map = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'}
    
    df_day['season_name'] = df_day['season'].map(season_map)
    df_day['weather_name'] = df_day['weathersit'].map(weather_map)
    df_day['weekday_name'] = df_day['weekday'].map(weekday_map)
    
    # Categorize demand
    percentile_90 = df_day['cnt'].quantile(0.90)
    percentile_10 = df_day['cnt'].quantile(0.10)
    df_day['demand_category'] = 'Normal'
    df_day.loc[df_day['cnt'] >= percentile_90, 'demand_category'] = 'Peak'
    df_day.loc[df_day['cnt'] <= percentile_10, 'demand_category'] = 'Low'
    
    return df_day

df_day = load_data()

# Styling
st.markdown("""
<style>
    .main { padding: 2rem; }
    .metric-card { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🚴 Bike Sharing Analysis Dashboard")
    st.markdown("Washington D.C. Bike Sharing System Analysis | 2011-2012")
with col2:
    st.image("https://img.icons8.com/color/96/000000/bicycle.png")

st.markdown("---")

# Key Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_users = df_day['cnt'].sum()
    st.metric("Total Users (2011-2012)", f"{int(total_users):,.0f}", "")

with col2:
    avg_daily_users = df_day['cnt'].mean()
    st.metric("Avg Daily Users", f"{int(avg_daily_users):,.0f}", "")

with col3:
    registered_pct = (df_day['registered'].sum() / df_day['cnt'].sum() * 100)
    st.metric("Registered Users %", f"{registered_pct:.1f}%", "")

with col4:
    casual_pct = (df_day['casual'].sum() / df_day['cnt'].sum() * 100)
    st.metric("Casual Users %", f"{casual_pct:.1f}%", "")

st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Seasonal Analysis", "📅 Daily Pattern", "🌡️ Weather Impact", "⏰ Demand Optimization"])

with tab1:
    st.subheader("Seasonal Pattern Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Season bar chart
        season_order = ['Spring', 'Summer', 'Fall', 'Winter']
        season_data = df_day.groupby('season_name')[['casual', 'registered']].mean().reindex(season_order)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        x = np.arange(len(season_order))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, season_data['casual'], width, label='Casual', color='#FF6B6B', alpha=0.8)
        bars2 = ax.bar(x + width/2, season_data['registered'], width, label='Registered', color='#4ECDC4', alpha=0.8)
        
        ax.set_title('Average Users per Season', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Users', fontsize=10)
        ax.set_xticks(x)
        ax.set_xticklabels(season_order)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}', ha='center', va='bottom', fontsize=9)
        
        st.pyplot(fig, use_container_width=True)
    
    with col2:
        # Season comparison metrics
        season_stats = df_day.groupby('season_name')['cnt'].agg(['mean', 'median', 'std', 'min', 'max']).reindex(season_order)
        st.dataframe(season_stats.round(0), use_container_width=True)
        
        # Insights
        max_season = season_stats['mean'].idxmax()
        min_season = season_stats['mean'].idxmin()
        st.info(f"""
        **Key Insights:**
        - **Peak Season:** {max_season} with {season_stats.loc[max_season, 'mean']:.0f} avg users/day
        - **Low Season:** {min_season} with {season_stats.loc[min_season, 'mean']:.0f} avg users/day
        - **Seasonal Variation:** {((season_stats.loc[max_season, 'mean'] / season_stats.loc[min_season, 'mean'] - 1) * 100):.1f}% difference
        """)

with tab2:
    st.subheader("Daily Pattern & Workday Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Workday comparison
        workday_data = df_day.groupby('workingday')[['casual', 'registered', 'cnt']].mean()
        workday_labels = ['Weekend/Holiday', 'Working Day']
        
        fig, ax = plt.subplots(figsize=(10, 6))
        x = np.arange(len(workday_labels))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, [workday_data.loc[0, 'casual'], workday_data.loc[1, 'casual']], width, label='Casual', color='#FF6B6B', alpha=0.8)
        bars2 = ax.bar(x + width/2, [workday_data.loc[0, 'registered'], workday_data.loc[1, 'registered']], width, label='Registered', color='#4ECDC4', alpha=0.8)
        
        ax.set_title('Working Day vs Weekend/Holiday', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Users', fontsize=10)
        ax.set_xticks(x)
        ax.set_xticklabels(workday_labels)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}', ha='center', va='bottom', fontsize=9)
        
        st.pyplot(fig, use_container_width=True)
    
    with col2:
        # Day of week pattern
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday_avg = df_day.groupby('weekday_name')['cnt'].mean().reindex(day_order)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#4ECDC4' if day not in ['Saturday', 'Sunday'] else '#FFD700' for day in day_order]
        bars = ax.bar(day_order, weekday_avg, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
        
        ax.set_title('Average Users by Day of Week', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Users', fontsize=10)
        plt.xticks(rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom', fontsize=9)
        
        st.pyplot(fig, use_container_width=True)

with tab3:
    st.subheader("Weather Impact on Bike Usage")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Weather analysis
        weather_order = ['Clear', 'Mist', 'Light Snow/Rain', 'Heavy Rain']
        weather_data = df_day.groupby('weather_name')[['casual', 'registered', 'cnt']].mean()
        weather_data = weather_data.reindex(weather_order)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#95E1D3', '#F38181', '#AA96DA', '#FCBAD3']
        bars = ax.bar(weather_order, weather_data['cnt'], color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
        
        ax.set_title('Average Users by Weather Condition', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Users', fontsize=10)
        plt.xticks(rotation=15, ha='right')
        ax.grid(axis='y', alpha=0.3)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom', fontsize=9)
        
        st.pyplot(fig, use_container_width=True)
    
    with col2:
        # Weather correlation
        weather_factors = ['temp', 'atemp', 'hum', 'windspeed', 'cnt']
        correlation = df_day[weather_factors].corr()['cnt'].drop('cnt').sort_values(ascending=True)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        colors_corr = ['#FF6B6B' if x < 0 else '#4ECDC4' for x in correlation.values]
        bars = ax.barh(range(len(correlation)), correlation.values, color=colors_corr, alpha=0.8, edgecolor='black', linewidth=1.5)
        
        ax.set_yticks(range(len(correlation)))
        ax.set_yticklabels(correlation.index)
        ax.set_title('Weather Factors Correlation with Users', fontsize=12, fontweight='bold')
        ax.set_xlabel('Pearson Correlation', fontsize=10)
        ax.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
        ax.grid(axis='x', alpha=0.3)
        
        for i, val in enumerate(correlation.values):
            ax.text(val + 0.02 if val > 0 else val - 0.02, i, f'{val:.3f}', va='center', fontweight='bold', fontsize=9)
        
        st.pyplot(fig, use_container_width=True)

with tab4:
    st.subheader("Demand Optimization Insights")
    
    # Peak vs Low demand
    col1, col2, col3 = st.columns(3)
    
    with col1:
        peak_count = len(df_day[df_day['demand_category'] == 'Peak'])
        st.metric("Peak Demand Days", peak_count, f"({peak_count/len(df_day)*100:.1f}%)")
    
    with col2:
        normal_count = len(df_day[df_day['demand_category'] == 'Normal'])
        st.metric("Normal Demand Days", normal_count, f"({normal_count/len(df_day)*100:.1f}%)")
    
    with col3:
        low_count = len(df_day[df_day['demand_category'] == 'Low'])
        st.metric("Low Demand Days", low_count, f"({low_count/len(df_day)*100:.1f}%)")
    
    st.markdown("---")
    
    # Demand characteristics
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Peak Demand Days Characteristics:**")
        peak_days = df_day[df_day['demand_category'] == 'Peak']
        peak_chars = {
            'Avg Users': f"{peak_days['cnt'].mean():.0f}",
            'Avg Temp': f"{peak_days['temp'].mean()*41:.1f}°C",  # Denormalized
            'Top Season': peak_days['season_name'].mode()[0],
            'Favorite Weather': peak_days['weather_name'].mode()[0],
            'Working Days %': f"{(peak_days['workingday'].mean()*100):.1f}%"
        }
        for key, val in peak_chars.items():
            st.write(f"• {key}: **{val}**")
    
    with col2:
        st.write("**Low Demand Days Characteristics:**")
        low_days = df_day[df_day['demand_category'] == 'Low']
        low_chars = {
            'Avg Users': f"{low_days['cnt'].mean():.0f}",
            'Avg Temp': f"{low_days['temp'].mean()*41:.1f}°C",  # Denormalized
            'Top Season': low_days['season_name'].mode()[0],
            'Favorite Weather': low_days['weather_name'].mode()[0],
            'Working Days %': f"{(low_days['workingday'].mean()*100):.1f}%"
        }
        for key, val in low_chars.items():
            st.write(f"• {key}: **{val}**")
    
    st.markdown("---")
    st.write("**📌 Recommended Actions:**")
    st.write("""
    1. **Dynamic Pricing**: Offer discounts during low demand periods to increase utilization
    2. **Maintenance Scheduling**: Schedule major maintenance during low demand seasons (Winter)
    3. **Fleet Adjustment**: Increase bike availability by 25-35% during peak seasons (Summer/Fall)
    4. **Marketing Focus**: Target casual users during weekends with special promotions
    5. **Commuter Benefits**: Develop subscription plans for registered users during peak commuting hours (7-9 AM, 5-7 PM)
    """)

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 12px;'>
    📊 Data Analysis | 2011-2012 Washington D.C. Bike Sharing Data<br>
    Generated with Streamlit | Last Updated: 2024
</div>
""", unsafe_allow_html=True)
