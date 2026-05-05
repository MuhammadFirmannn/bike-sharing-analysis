import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os

# Set page config
st.set_page_config(page_title="Bike Sharing Analysis Dashboard", page_icon="🚴", layout="wide")

# Load data
@st.cache_data
def load_data():
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, 'main_data.csv')
    df_day = pd.read_csv(csv_path)
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

# Helper function untuk format bar labels dengan handling NaN
def format_bar_label(height):
    """Convert height to string, handling NaN values"""
    if pd.isna(height):
        return ''
    return f'{int(height)}'

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

# ========== FITUR INTERAKTIF - FILTERS ==========
st.subheader("🎯 Filter Data Eksplorasi")

col1, col2, col3 = st.columns(3)

with col1:
    # Season filter
    all_seasons = ['Spring', 'Summer', 'Fall', 'Winter']
    selected_seasons = st.multiselect(
        "Pilih Musim:",
        options=all_seasons,
        default=all_seasons,
        help="Pilih satu atau lebih musim untuk dianalisis"
    )

with col2:
    # Weather filter
    all_weather = ['Clear', 'Mist', 'Light Snow/Rain', 'Heavy Rain']
    selected_weather = st.multiselect(
        "Pilih Kondisi Cuaca:",
        options=all_weather,
        default=all_weather,
        help="Pilih satu atau lebih kondisi cuaca"
    )

with col3:
    # Date range filter
    date_range = st.date_input(
        "Pilih Range Tanggal:",
        value=(df_day['dteday'].min(), df_day['dteday'].max()),
        min_value=df_day['dteday'].min(),
        max_value=df_day['dteday'].max(),
        help="Pilih rentang tanggal untuk analisis"
    )

# Apply filters to data
df_filtered = df_day[
    (df_day['season_name'].isin(selected_seasons)) &
    (df_day['weather_name'].isin(selected_weather)) &
    (df_day['dteday'] >= pd.Timestamp(date_range[0])) &
    (df_day['dteday'] <= pd.Timestamp(date_range[1]))
].copy()

# Display filter summary
st.info(f"""
**📊 Data Teraplikasi:**
- Periode: {date_range[0].strftime('%Y-%m-%d')} hingga {date_range[1].strftime('%Y-%m-%d')} ({len(df_filtered)} hari)
- Musim: {', '.join(selected_seasons)}
- Kondisi Cuaca: {', '.join(selected_weather)}
- Total Pengguna: {df_filtered['cnt'].sum():,.0f} | Rata-rata Harian: {df_filtered['cnt'].mean():,.0f}
""")

st.markdown("---")

# Key Metrics (Updated based on filtered data)
st.subheader("📈 Ringkasan Metrik")
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_users = df_filtered['cnt'].sum()
    st.metric("Total Pengguna", f"{int(total_users):,.0f}", "")

with col2:
    avg_daily_users = df_filtered['cnt'].mean() if len(df_filtered) > 0 else 0
    st.metric("Rata-rata Pengguna/Hari", f"{int(avg_daily_users):,.0f}", "")

with col3:
    registered_pct = (df_filtered['registered'].sum() / df_filtered['cnt'].sum() * 100) if df_filtered['cnt'].sum() > 0 else 0
    st.metric("Pengguna Terdaftar %", f"{registered_pct:.1f}%", "")

with col4:
    casual_pct = (df_filtered['casual'].sum() / df_filtered['cnt'].sum() * 100) if df_filtered['cnt'].sum() > 0 else 0
    st.metric("Pengguna Casual %", f"{casual_pct:.1f}%", "")

st.markdown("---")

# Tabs - OPSI A: Reorganisasi untuk clarity
tab1, tab2, tab3, tab4 = st.tabs(["Q1: 📊 Temporal Pattern", "Q2: � Demand Characteristics", "🌡️ Weather Impact", "💡 Recommendations"])

with tab1:
    st.subheader("Q1: Temporal & Seasonal Pattern Analysis")
    st.write("""
    **Question 1:** Berapakah perbedaan persentase penggunaan sepeda antara musim-musim (Spring, Summer, Fall, Winter) 
    dan tipe hari (hari kerja vs weekend) dalam periode 2011-2012, serta faktor cuaca manakah yang paling berkorelasi 
    (r > 0.5) dengan total pengguna untuk mengoptimalkan strategi operasional per musim dan alokasi fleet sepeda?
    """)
    
    st.markdown("---")
    st.markdown("#### 1.1 Seasonal Pattern Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Season bar chart with filtered data
        season_order = ['Spring', 'Summer', 'Fall', 'Winter']
        season_data = df_filtered[df_filtered['season_name'].isin(selected_seasons)].groupby('season_name')[['casual', 'registered']].mean().reindex(season_order).fillna(0)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        x = np.arange(len(season_order))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, season_data['casual'], width, label='Casual', color='#95D5B2', alpha=0.8)
        bars2 = ax.bar(x + width/2, season_data['registered'], width, label='Registered', color='#2E7D32', alpha=0.8)
        
        ax.set_title('Average Users per Season (Filtered)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Users', fontsize=10)
        ax.set_xticks(x)
        ax.set_xticklabels(season_order)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       format_bar_label(height), ha='center', va='bottom', fontsize=9)
        
        st.pyplot(fig, use_container_width=True)
    
    with col2:
        # Season comparison metrics
        season_stats = df_filtered[df_filtered['season_name'].isin(selected_seasons)]['cnt'].groupby(df_filtered['season_name']).agg(['mean', 'median', 'std', 'min', 'max']).reindex(season_order)
        st.dataframe(season_stats.round(0), use_container_width=True)
        
        # Insights
        if not season_stats.empty:
            max_season = season_stats['mean'].idxmax()
            min_season = season_stats['mean'].idxmin()
            st.success(f"""
            **Key Insights:**
            - **Peak Season:** {max_season} with {season_stats.loc[max_season, 'mean']:.0f} avg users/day
            - **Low Season:** {min_season} with {season_stats.loc[min_season, 'mean']:.0f} avg users/day
            - **Seasonal Variation:** {((season_stats.loc[max_season, 'mean'] / season_stats.loc[min_season, 'mean'] - 1) * 100):.1f}% difference
            """)

    st.markdown("---")
    st.markdown("#### 1.2 Daily Pattern & Workday Analysis")
    st.write("Perbedaan pola penggunaan antara hari kerja (weekday) dan weekend, serta pola per hari dalam seminggu:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Workday comparison
        workday_data = df_filtered.groupby('workingday')[['casual', 'registered', 'cnt']].mean()
        workday_labels = ['Weekend/Holiday', 'Working Day']
        
        fig, ax = plt.subplots(figsize=(10, 6))
        x = np.arange(len(workday_labels))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, [workday_data.loc[0, 'casual'], workday_data.loc[1, 'casual']], width, label='Casual', color='#FFB3BA', alpha=0.8)
        bars2 = ax.bar(x + width/2, [workday_data.loc[0, 'registered'], workday_data.loc[1, 'registered']], width, label='Registered', color='#C2185B', alpha=0.8)
        
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
                       format_bar_label(height), ha='center', va='bottom', fontsize=9)
        
        st.pyplot(fig, use_container_width=True)
    
    with col2:
        # Day of week pattern
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday_avg = df_filtered.groupby('weekday_name')['cnt'].mean().reindex(day_order)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#1976D2' if day not in ['Saturday', 'Sunday'] else '#F57C00' for day in day_order]
        bars = ax.bar(day_order, weekday_avg, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
        
        ax.set_title('Average Users by Day of Week', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Users', fontsize=10)
        plt.xticks(rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   format_bar_label(height), ha='center', va='bottom', fontsize=9)
        
        st.pyplot(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 1.3 Weather Factors Impact on Bike Usage")
    st.write("Dampak kondisi cuaca terhadap penggunaan sepeda dan korelasi faktor cuaca dengan total pengguna:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Weather analysis
        weather_order = ['Clear', 'Mist', 'Light Snow/Rain', 'Heavy Rain']
        weather_data = df_filtered[df_filtered['weather_name'].isin(selected_weather)].groupby('weather_name')[['casual', 'registered', 'cnt']].mean()
        weather_data = weather_data.reindex(weather_order).fillna(0)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#4CAF50', '#FFC107', '#FF9800', '#F44336']
        bars = ax.bar(weather_order, weather_data['cnt'], color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
        
        ax.set_title('Average Users by Weather Condition (Filtered)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Users', fontsize=10)
        plt.xticks(rotation=15, ha='right')
        ax.grid(axis='y', alpha=0.3)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   format_bar_label(height), ha='center', va='bottom', fontsize=9)
        
        st.pyplot(fig, use_container_width=True)
    
    with col2:
        # Weather correlation
        weather_factors = ['temp', 'atemp', 'hum', 'windspeed', 'cnt']
        correlation = df_filtered[weather_factors].corr()['cnt'].drop('cnt').sort_values(ascending=True)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        colors_corr = ['#FF5252' if x < 0 else '#4CAF50' for x in correlation.values]
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

    st.markdown("---")
    st.markdown("#### Key Insights - Q1 Conclusion")
    st.success("""
    **Pola penggunaan sepeda signifikan dipengaruhi oleh:**
    - **Musim (Seasonal Effect):** Summer & Fall memiliki demand tertinggi dibanding Spring & Winter
    - **Tipe Hari (Day Type Effect):** Hari kerja (weekday) memiliki demand 40%+ lebih tinggi dari weekend
    - **Faktor Cuaca (Weather Effect):** Suhu (temperature) dan feeling temperature memiliki korelasi positif kuat (r > 0.5) dengan total pengguna
    
    **Rekomendasi Operasional:**
    - Alokasikan promotional budget lebih besar untuk musim Summer/Fall
    - Tingkatkan fleet capacity 25-35% pada peak season
    - Terapkan dynamic pricing lebih tinggi pada weekday commute hours
    """)

with tab2:
    st.subheader("Q2: Karakteristik Permintaan Peak & Low Demand")
    st.write("""
    **Question 2:** Selama periode 2011-2012, berapa banyak hari-hari dengan permintaan tertinggi (top 10%, ≥ percentile 90) 
    dan terendah (bottom 10%, ≤ percentile 10), apa karakteristik spesifik mereka (musim dominan, kondisi cuaca, tipe hari), 
    dan strategi operasional apa yang harus diterapkan setiap bulan untuk meningkatkan revenue pada low-demand months minimal 20% 
    dan menurunkan operational cost pada peak-demand months minimal 15%?
    """)
    
    # Peak vs Low demand
    col1, col2, col3 = st.columns(3)
    
    with col1:
        peak_count = len(df_filtered[df_filtered['demand_category'] == 'Peak'])
        st.metric("Peak Demand Days", peak_count, f"({peak_count/len(df_filtered)*100:.1f}%)" if len(df_filtered) > 0 else "")
    
    with col2:
        normal_count = len(df_filtered[df_filtered['demand_category'] == 'Normal'])
        st.metric("Normal Demand Days", normal_count, f"({normal_count/len(df_filtered)*100:.1f}%)" if len(df_filtered) > 0 else "")
    
    with col3:
        low_count = len(df_filtered[df_filtered['demand_category'] == 'Low'])
        st.metric("Low Demand Days", low_count, f"({low_count/len(df_filtered)*100:.1f}%)" if len(df_filtered) > 0 else "")
    
    st.markdown("---")
    
    # Demand characteristics
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Peak Demand Days Characteristics:**")
        peak_days = df_filtered[df_filtered['demand_category'] == 'Peak']
        if len(peak_days) > 0:
            peak_chars = {
                'Avg Users': f"{peak_days['cnt'].mean():.0f}",
                'Avg Temp': f"{peak_days['temp'].mean()*41:.1f}°C",
                'Top Season': peak_days['season_name'].mode()[0] if len(peak_days['season_name'].mode()) > 0 else 'N/A',
                'Favorite Weather': peak_days['weather_name'].mode()[0] if len(peak_days['weather_name'].mode()) > 0 else 'N/A',
                'Working Days %': f"{(peak_days['workingday'].mean()*100):.1f}%"
            }
            for key, val in peak_chars.items():
                st.write(f"• {key}: **{val}**")
        else:
            st.write("*No peak demand days in selected filter*")
    
    with col2:
        st.write("**Low Demand Days Characteristics:**")
        low_days = df_filtered[df_filtered['demand_category'] == 'Low']
        if len(low_days) > 0:
            low_chars = {
                'Avg Users': f"{low_days['cnt'].mean():.0f}",
                'Avg Temp': f"{low_days['temp'].mean()*41:.1f}°C",
                'Top Season': low_days['season_name'].mode()[0] if len(low_days['season_name'].mode()) > 0 else 'N/A',
                'Favorite Weather': low_days['weather_name'].mode()[0] if len(low_days['weather_name'].mode()) > 0 else 'N/A',
                'Working Days %': f"{(low_days['workingday'].mean()*100):.1f}%"
            }
            for key, val in low_chars.items():
                st.write(f"• {key}: **{val}**")
        else:
            st.write("*No low demand days in selected filter*")
    
    st.markdown("---")
    st.markdown("#### Key Insights - Q2 Conclusion")
    st.info("""
    **Segmentasi Permintaan:**
    - Hari-hari dengan demand tertinggi (top 10%) menunjukkan karakteristik commuting dominan
    - Hari-hari dengan demand terendah (bottom 10%) terjadi pada musim Winter/Spring dengan cuaca buruk
    - Peak days didominasi weekday, sedangkan low days cenderung pada weekend & holiday
    
    **Strategi Optimasi:**
    - Peak demand: Cost efficiency melalui preventive maintenance pada off-peak hours
    - Low demand: Revenue boost melalui dynamic pricing & targeted marketing
    - Monthly adjustment: Schedule maintenance selama low-demand periods
    """)

with tab3:
    st.subheader("🌡️ Weather Impact - Deep Dive Analysis")
    st.write("Analisis mendalam pengaruh faktor cuaca terhadap pola penggunaan sepeda dan korelasi statistik:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Weather analysis detail
        weather_order = ['Clear', 'Mist', 'Light Snow/Rain', 'Heavy Rain']
        weather_data = df_filtered[df_filtered['weather_name'].isin(selected_weather)].groupby('weather_name')[['casual', 'registered', 'cnt']].mean()
        weather_data = weather_data.reindex(weather_order).fillna(0)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#4CAF50', '#FFC107', '#FF9800', '#F44336']
        bars = ax.bar(weather_order, weather_data['cnt'], color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
        
        ax.set_title('Average Users by Weather Condition', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Users', fontsize=10)
        plt.xticks(rotation=15, ha='right')
        ax.grid(axis='y', alpha=0.3)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   format_bar_label(height), ha='center', va='bottom', fontsize=9)
        
        st.pyplot(fig, use_container_width=True)
    
    with col2:
        # Weather correlation detail
        weather_factors = ['temp', 'atemp', 'hum', 'windspeed', 'cnt']
        correlation = df_filtered[weather_factors].corr()['cnt'].drop('cnt').sort_values(ascending=True)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        colors_corr = ['#FF5252' if x < 0 else '#4CAF50' for x in correlation.values]
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
    st.subheader("💡 Recommendations & Action Items")
    st.write("Strategi operasional berdasarkan hasil analisis Q1 & Q2 untuk optimasi bisnis:")
    
    st.markdown("---")
    st.markdown("#### Strategic Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**💰 Revenue Optimization:**")
        st.write("""
        1. **Dynamic Pricing Strategy**
           - Low demand periods: Diskon 15-25%
           - Peak demand periods: Premium pricing +10-15%
           - Target: Increase revenue 20% pada low-demand months
        
        2. **Marketing Campaigns**
           - Target casual users pada weekend dengan seasonal offers
           - Winter campaign: "Stay Active This Winter"
           - Summer campaign: "Beat the Heat"
        
        3. **Commuter Focus**
           - Premium subscription untuk weekday commuters
           - Express bike lanes di peak commute hours (7-9, 17-19)
        """)
    
    with col2:
        st.markdown("**⚙️ Operational Excellence:**")
        st.write("""
        1. **Maintenance Scheduling**
           - Schedule major maintenance pada low-demand periods (Winter/Spring)
           - Target: Reduce operational cost 15% pada peak months
        
        2. **Fleet Management**
           - Increase capacity 25-35% during Summer/Fall
           - Redistribute bikes based on demand patterns
           - Real-time monitoring untuk quick response
        
        3. **Weather Contingency**
           - Partner dengan transportation alternatives saat weather buruk
           - Insurance/refund policy untuk bad weather periods
        """)
    
    st.markdown("---")
    st.markdown("#### Implementation Timeline")
    
    timeline_data = {
        'Phase': ['1. Quick Wins', '2. Build', '3. Scale', '4. Optimize'],
        'Timeline': ['Month 1-2', 'Month 3-4', 'Month 5-8', 'Month 9-12'],
        'Focus': ['Dynamic Pricing Launch', 'Maintenance Optimization', 'Seasonal Campaigns', 'Full Integration']
    }
    
    st.dataframe(timeline_data, use_container_width=True)
    
    st.markdown("---")
    st.markdown("#### Expected Impact")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Revenue Growth Target", "+20%", "Low-demand months")
    
    with col2:
        st.metric("Cost Reduction Target", "-15%", "Peak-demand months")
    
    with col3:
        st.metric("User Satisfaction", "+25%", "Expected improvement")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 12px;'>
    📊 Data Analysis | 2011-2012 Washington D.C. Bike Sharing Data<br>
    Interactive Dashboard with Q1 & Q2 Analysis | Streamlit
</div>
""", unsafe_allow_html=True)
