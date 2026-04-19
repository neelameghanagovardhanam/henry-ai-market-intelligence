import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from dotenv import load_dotenv
import os
from openai import OpenAI
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"), override=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ai_call(system_msg, user_msg):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            max_tokens=700
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"
 
# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="HENRY Intelligence Platform",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "HENRY Market Intelligence - Built for Financial Advisors"
    }
)
 
# ---------------- ENHANCED STYLES ----------------
st.markdown("""
<style>
    /* Main theme colors - Enhanced with cooler tones */
    :root {
        --primary-color: #0891b2;
        --secondary-color: #06b6d4;
        --accent-color: #10b981;
        --danger-color: #ef4444;
        --background-light: #f0fdfa;
        --cool-gradient-1: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --cool-gradient-2: linear-gradient(135deg, #0891b2 0%, #06b6d4 100%);
        --cool-gradient-3: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Page background with subtle pattern */
    .main {
        background: linear-gradient(180deg, #f0fdfa 0%, #ffffff 100%);
    }
    
    /* Custom metric cards - Cooler design */
    .metric-card {
        background: linear-gradient(135deg, #0891b2 0%, #06b6d4 100%);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 8px 16px rgba(8, 145, 178, 0.2);
        color: white;
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .metric-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 24px rgba(8, 145, 178, 0.3);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 10px 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.95;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    /* Tooltip styling - Hover-based */
    .tooltip-container {
        position: relative;
        display: inline-block;
        cursor: help;
    }
    
    .tooltip-text {
        visibility: hidden;
        width: 320px;
        background-color: #1e293b;
        color: #fff;
        text-align: left;
        border-radius: 12px;
        padding: 15px;
        position: absolute;
        z-index: 1000;
        bottom: 125%;
        left: 50%;
        margin-left: -160px;
        opacity: 0;
        transition: opacity 0.3s, visibility 0.3s;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
        font-size: 0.85rem;
        line-height: 1.6;
    }
    
    .tooltip-text::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -8px;
        border-width: 8px;
        border-style: solid;
        border-color: #1e293b transparent transparent transparent;
    }
    
    .tooltip-container:hover .tooltip-text {
        visibility: visible;
        opacity: 1;
    }
    
    .tooltip-trigger {
        color: #0891b2;
        font-weight: 600;
        border-bottom: 2px dotted #0891b2;
        padding-bottom: 2px;
    }
    
    /* Data table styling */
    .dataframe {
        font-size: 0.9rem;
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Section headers - Cooler gradient */
    .section-header {
        background: linear-gradient(90deg, #0891b2 0%, #06b6d4 100%);
        color: white;
        padding: 12px 20px;
        border-radius: 10px;
        margin: 15px 0;
        font-size: 1.2rem;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(8, 145, 178, 0.15);
    }
    
    /* Sidebar styling - Cooler background */
    .css-1d391kg {
        background: linear-gradient(180deg, #ecfeff 0%, #f0fdfa 100%);
    }
    
    /* Tab styling - Enhanced cool design */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #e0f2fe 0%, #f0fdfa 100%);
        border-radius: 12px 12px 0 0;
        padding: 12px 24px;
        font-weight: 600;
        color: #0891b2;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, #bae6fd 0%, #ccfbf1 100%);
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0891b2 0%, #06b6d4 100%);
        color: white;
        border-color: #0891b2;
        box-shadow: 0 4px 8px rgba(8, 145, 178, 0.3);
    }
    
    /* Alert boxes - Cooler colors */
    .info-box {
        background: linear-gradient(135deg, #e0f2fe 0%, #f0fdfa 100%);
        border-left: 5px solid #0891b2;
        padding: 18px;
        border-radius: 10px;
        margin: 15px 0;
        box-shadow: 0 2px 8px rgba(8, 145, 178, 0.1);
    }
    
    .success-box {
        background: linear-gradient(135deg, #d1fae5 0%, #ecfdf5 100%);
        border-left: 5px solid #10b981;
        padding: 18px;
        border-radius: 10px;
        margin: 15px 0;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.1);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fef3c7 0%, #fef9e7 100%);
        border-left: 5px solid #f59e0b;
        padding: 18px;
        border-radius: 10px;
        margin: 15px 0;
        box-shadow: 0 2px 8px rgba(245, 158, 11, 0.1);
    }
    
    /* Button enhancements */
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Card-like containers */
    .cool-card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(8, 145, 178, 0.1);
        border: 1px solid #e0f2fe;
        margin: 15px 0;
    }
    
    /* Better metric styling */
    div[data-testid="metric-container"] {
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(8, 145, 178, 0.08);
    }
    
    /* Improve dataframe styling */
    .dataframe thead tr th {
        background-color: #0891b2 !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 12px !important;
    }
    
    .dataframe tbody tr:hover {
        background-color: #f0fdfa !important;
    }
    
    /* Better expander styling */
    .streamlit-expanderHeader {
        background-color: #e0f2fe;
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* Sidebar improvements */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ecfeff 0%, #f0fdfa 100%);
    }
    
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMultiSelect label,
    section[data-testid="stSidebar"] .stSlider label {
        color: #0f172a;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)
 
# ---------------- TOOLTIP DEFINITIONS ----------------
TOOLTIPS = {
    "henry_index": """
    <strong>HENRY Index</strong> measures the ratio of earned income to passive income (investments).<br><br>
    <strong>📊 Formula:</strong> AGI ÷ (Dividends + Interest Income + 1)<br><br>
    <strong>🎯 Why it matters:</strong><br>
    • Higher values = High earners who haven't diversified into investments yet<br>
    • These are your IDEAL clients: making money but need wealth management<br>
    • Sweet spot: HENRY Index > 50<br><br>
    <strong>💡 Example:</strong> Someone earning $150K with only $2K in investment income has a high HENRY Index
    """,
    
    "market_score": """
    <strong>Market Score</strong> is a composite metric ranking ZIP codes by opportunity.<br><br>
    <strong>🧮 Components:</strong><br>
    • 50% HENRY Index (earning vs. investing gap)<br>
    • 30% Market Size (number of tax returns)<br>
    • 20% Velocity (year-over-year growth)<br><br>
    <strong>🎯 Scoring:</strong><br>
    • 0.8+ = Excellent opportunity<br>
    • 0.6-0.8 = Good potential<br>
    • 0.4-0.6 = Moderate<br>
    • <0.4 = Low priority<br><br>
    <strong>💰 Use case:</strong> Prioritize your marketing budget to high-scoring markets
    """,
    
    "velocity": """
    <strong>Wealth Velocity</strong> tracks how fast a market is becoming "HENRY-fied."<br><br>
    <strong>📈 Calculation:</strong> Change in HENRY Index from 2021 to 2022<br><br>
    <strong>🔥 Positive velocity means:</strong><br>
    • Salaries growing faster than investments<br>
    • Emerging tech hubs or gentrifying areas<br>
    • Growing pool of clients who need your services<br><br>
    <strong>⚠️ Action:</strong> Target markets with velocity > 5 for early positioning
    """,
    
    "income_brackets": """
    <strong>Income Brackets</strong> filter the wealth tier you want to target.<br><br>
    <strong>💵 Tiers:</strong><br>
    • $75K-$100K: Early career professionals<br>
    • $100K-$200K: <strong>Prime HENRY zone</strong> - established but not wealthy<br>
    • $200K+: High earners transitioning to wealth<br><br>
    <strong>🎯 Strategy:</strong> Focus on $100K-$200K for highest conversion rates
    """,
    
    "population_filter": """
    <strong>Minimum Population</strong> ensures you're looking at viable markets.<br><br>
    <strong>📊 Why filter:</strong><br>
    • Small ZIP codes = unreliable data<br>
    • Need critical mass for cost-effective marketing<br>
    • Recommendation: Set to 100+ returns<br><br>
    <strong>💡 Sweet spot:</strong> 200-500 returns = large enough for campaigns, small enough to dominate
    """,
    
    "top_n": """
    <strong>Top N</strong> controls how many markets to display in rankings.<br><br>
    <strong>🎯 Recommended settings:</strong><br>
    • 10-20 = Focus on best opportunities<br>
    • 50-100 = Broader market research<br><br>
    <strong>💼 Pro tip:</strong> Start with top 20, expand as you scale operations
    """
}
 
# ---------------- HELPER FUNCTION FOR INLINE TOOLTIPS ----------------
def create_tooltip(text, tooltip_key):
    """Create an inline tooltip that shows on hover"""
    if tooltip_key in TOOLTIPS:
        return f"""
        <div class="tooltip-container">
            <span class="tooltip-trigger">{text}</span>
            <div class="tooltip-text">{TOOLTIPS[tooltip_key]}</div>
        </div>
        """
    return text
 
# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    try:
        df21 = pd.read_csv('21zpallagi.csv')
        df22 = pd.read_csv('22zpallagi.csv')
        
        df21['zipcode'] = df21['zipcode'].astype(str).str.zfill(5)
        df22['zipcode'] = df22['zipcode'].astype(str).str.zfill(5)
        
        return df21, df22
    except FileNotFoundError:
        st.error("⚠️ Data files not found. Please ensure '21zpallagi.csv' and '22zpallagi.csv' are in the app directory.")
        st.stop()
 
df21, df22 = load_data()
 
# ---------------- METRICS COMPUTATION ----------------
def compute_henry(df):
    """Calculate HENRY Index for each ZIP code"""
    df = df.copy()
    df['henry_index'] = df['A00200'] / (df['A00600'] + df['A01000'] + 1)
    df['henry_index'] = df['henry_index'].replace([np.inf, -np.inf], 0).fillna(0)
    return df
 
def normalize(x):
    """Min-max normalization"""
    return (x - x.min()) / (x.max() - x.min() + 1e-6)
 
def get_risk_level(henry_index, velocity):
    """Categorize market risk level"""
    if henry_index > 60 and velocity > 5:
        return "🔥 Hot Market", "#10b981"
    elif henry_index > 40 and velocity > 0:
        return "📈 Growing", "#0891b2"
    elif henry_index > 40:
        return "✅ Stable", "#6b7280"
    else:
        return "⚠️ Low Priority", "#ef4444"
 
# ---------------- SIDEBAR ----------------
st.sidebar.markdown("""
<div style="
    text-align: center;
    padding: 12px 10px;
    background: linear-gradient(135deg, #0891b2 0%, #06b6d4 100%);
    border-radius: 10px;
    margin-bottom: 15px;
    box-shadow: 0 4px 12px rgba(8, 145, 178, 0.2);
">
    <img src="https://img.icons8.com/fluency/96/financial-growth-analysis.png" width="40" style="margin-bottom: 6px;" />
    <h2 style="
        margin: 0;
        color: white;
        font-size: 1.1em;
        font-weight: 700;
        letter-spacing: 0.3px;
    ">🎯 Market Filters</h2>
</div>
""", unsafe_allow_html=True)
 
# First-time user guide
if 'first_visit' not in st.session_state:
    st.session_state.first_visit = True
 
if st.session_state.first_visit:
    with st.sidebar.expander("👋 First time here? Start here!", expanded=True):
        st.markdown("""
        **Welcome to HENRY Intelligence!**
        
        This platform helps you find high-earning professionals who need financial advisory services.
        
        **Quick Start:**
        1. Select a state (or keep ALL)
        2. Choose income brackets (default is optimal)
        3. Explore the tabs to find opportunities
        4. Use AI Advisor to generate outreach emails
        
        💡 Hover over highlighted terms for detailed explanations!
        """)
        if st.button("Got it! Don't show again"):
            st.session_state.first_visit = False
            st.rerun()
 
# Reset button
if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
    st.session_state.clear()
    st.rerun()
 
st.sidebar.markdown("""
<div style="
    background: linear-gradient(90deg, #0891b2 0%, #06b6d4 100%);
    color: white;
    padding: 10px 15px;
    border-radius: 10px;
    margin: 20px 0 15px 0;
    font-size: 1.1em;
    font-weight: 600;
    box-shadow: 0 2px 8px rgba(8, 145, 178, 0.2);
">
Geographic Filter
</div>
""", unsafe_allow_html=True)
 
state = st.sidebar.selectbox(
    "Select State",
    ["ALL"] + sorted(df22['STATE'].dropna().unique()),
    help="Filter markets by U.S. state"
)
 
st.sidebar.markdown("""
<div style="
    background: linear-gradient(90deg, #0891b2 0%, #06b6d4 100%);
    color: white;
    padding: 10px 15px;
    border-radius: 10px;
    margin: 20px 0 15px 0;
    font-size: 1.1em;
    font-weight: 600;
    box-shadow: 0 2px 8px rgba(8, 145, 178, 0.2);
">
Income Targeting
</div>
""", unsafe_allow_html=True)
 
# Income Brackets
stub_labels = {
    4: "$75k - $100k",
    5: "$100k - $200k",
    6: "$200k+"
}
 
selected_stubs = st.sidebar.multiselect(
    "Income Brackets",
    options=[4, 5, 6],
    default=[5, 6],
    format_func=lambda x: stub_labels[x],
    help="Focus on high-earning professionals"
)
 
st.sidebar.markdown("""
<div style="
    background: linear-gradient(90deg, #0891b2 0%, #06b6d4 100%);
    color: white;
    padding: 10px 15px;
    border-radius: 10px;
    margin: 20px 0 15px 0;
    font-size: 1.1em;
    font-weight: 600;
    box-shadow: 0 2px 8px rgba(8, 145, 178, 0.2);
">
Market Size
</div>
""", unsafe_allow_html=True)
 
# Population filter
min_returns = st.sidebar.slider(
    "Minimum Population (Tax Returns)",
    0, 2000, 100, 50,
    help="Exclude small ZIP codes"
)
 
# Top N
top_n = st.sidebar.slider(
    "Top N Markets to Display",
    10, 100, 20, 5,
    help="Number of markets to show in rankings"
)
 
st.sidebar.markdown("---")
st.sidebar.markdown(f"""
<div style="
    text-align: center;
    color: #64748b;
    font-size: 0.85em;
    padding: 15px 10px;
    background: #f0fdfa;
    border-radius: 10px;
    margin-top: 20px;
">
🕐 Last updated:<br>
<strong style="color: #0891b2;">{datetime.now().strftime('%Y-%m-%d %H:%M')}</strong>
</div>
""", unsafe_allow_html=True)
 
# ---------------- PROCESS DATA ----------------
df22 = compute_henry(df22)
df21 = compute_henry(df21)
 
df22 = df22[df22['zipcode'] != '00000']
df21 = df21[df21['zipcode'] != '00000']
 
# Apply filters
df22 = df22[df22['agi_stub'].isin(selected_stubs)]
df21 = df21[df21['agi_stub'].isin(selected_stubs)]
 
if state != "ALL":
    df22 = df22[df22['STATE'] == state]
    df21 = df21[df21['STATE'] == state]
 
df22 = df22[df22['N1'] >= min_returns]
df21 = df21[df21['N1'] >= min_returns]
 
# Aggregate
df_grouped = df22.groupby(['zipcode', 'STATE']).agg({
    'henry_index': 'mean',
    'N1': 'sum',
    'A00200': 'mean',
    'A00600': 'mean',
    'A01000': 'mean'
}).reset_index()
 
# ---------------- WEALTH VELOCITY ----------------
df21_agg = df21.groupby('zipcode').agg({
    'henry_index': 'mean',
    'A00600': 'mean',
    'A01000': 'mean'
}).reset_index()
 
df22_agg = df22.groupby('zipcode').agg({
    'henry_index': 'mean',
    'A00600': 'mean',
    'A01000': 'mean'
}).reset_index()
 
merged = df22_agg.merge(df21_agg, on='zipcode', suffixes=('_22', '_21'))
merged['velocity'] = merged['henry_index_22'] - merged['henry_index_21']
 
merged['investment_21'] = merged['A00600_21'] + merged['A01000_21']
merged['investment_22'] = merged['A00600_22'] + merged['A01000_22']
 
merged['investment_growth'] = (
    (merged['investment_22'] - merged['investment_21']) /
    (merged['investment_21'] + 1)
)
 
# Emerging HENRY hubs
emerging = merged[
    (merged['velocity'] > 0) &
    (merged['investment_growth'] < 0.05)
]
 
df_grouped = df_grouped.merge(emerging[['zipcode', 'velocity']], on='zipcode', how='left')
df_grouped['velocity'] = df_grouped['velocity'].fillna(0)
 
# ---------------- MARKET SCORE ----------------
df_grouped['henry_score'] = normalize(df_grouped['henry_index'])
df_grouped['size_score'] = normalize(df_grouped['N1'])
df_grouped['velocity_score'] = normalize(df_grouped['velocity'])
 
df_grouped['market_score'] = (
    0.5 * df_grouped['henry_score'] +
    0.3 * df_grouped['size_score'] +
    0.2 * df_grouped['velocity_score']
)
 
# Add risk categorization
df_grouped['risk_category'], df_grouped['risk_color'] = zip(*df_grouped.apply(
    lambda row: get_risk_level(row['henry_index'], row['velocity']), axis=1
))

# Create zip_display column with state in brackets
df_grouped['zip_display'] = df_grouped['zipcode'] + ' (' + df_grouped['STATE'] + ')'
 
# ---------------- HEADER ----------------
st.markdown("""
<div style="
    background: linear-gradient(135deg, #0891b2 0%, #06b6d4 100%);
    padding: 15px 25px;
    border-radius: 12px;
    margin-bottom: 15px;
    box-shadow: 0 4px 12px rgba(8, 145, 178, 0.2);
    display: flex;
    align-items: center;
    gap: 15px;
">
    <div style="
        background: white;
        border-radius: 10px;
        padding: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    ">
        <img src="https://img.icons8.com/fluency/96/financial-growth-analysis.png" width="40" />
    </div>
    <div style="flex: 1;">
        <h1 style="
            margin: 0;
            color: white;
            font-size: 1.5em;
            font-weight: 700;
            letter-spacing: -0.3px;
        ">
            HENRY Market Intelligence Platform
        </h1>
        <p style="
            margin: 3px 0 0 0;
            color: rgba(255, 255, 255, 0.9);
            font-size: 0.85em;
            font-weight: 400;
        ">
            AI-Powered Decision Support for Financial Advisors
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
 
# ---------------- FILTER SUMMARY ----------------
summary_col1, summary_col2, summary_col3 = st.columns([2.5, 2.5, 1.5])
 
with summary_col1:
    st.markdown(f"""
    <div class="info-box" style="padding: 12px; margin: 10px 0;">
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
        <strong style="color: #0891b2; font-size: 0.9em;">Geographic Scope:</strong>
        <span style="color: #0f172a; font-weight: 600; font-size: 0.9em;">{state}</span>
    </div>
    <div style="display: flex; align-items: center; gap: 8px;">
        <strong style="color: #0891b2; font-size: 0.9em;">Income Range:</strong>
        <span style="color: #0f172a; font-weight: 600; font-size: 0.9em;">{', '.join([stub_labels[s] for s in selected_stubs])}</span>
    </div>
    </div>
    """, unsafe_allow_html=True)
 
with summary_col2:
    st.markdown(f"""
    <div class="info-box" style="padding: 12px; margin: 10px 0;">
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
        <strong style="color: #0891b2; font-size: 0.9em;">Min Population:</strong>
        <span style="color: #0f172a; font-weight: 600; font-size: 0.9em;">{min_returns:,} returns</span>
    </div>
    <div style="display: flex; align-items: center; gap: 8px;">
        <strong style="color: #0891b2; font-size: 0.9em;">Showing Top:</strong>
        <span style="color: #0f172a; font-weight: 600; font-size: 0.9em;">{top_n} markets</span>
    </div>
    </div>
    """, unsafe_allow_html=True)
 
with summary_col3:
    # Prepare export data
    export_df = df_grouped.sort_values('market_score', ascending=False).head(top_n)
    csv = export_df.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="Export Data",
        data=csv,
        file_name=f"henry_markets_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True,
        type="primary",
        help=f"Download top {top_n} markets as CSV file"
    )
 
# ---------------- KPI METRICS ----------------
st.markdown("""
<div style="
    background: linear-gradient(90deg, #0891b2 0%, #06b6d4 100%);
    color: white;
    padding: 10px 20px;
    border-radius: 10px;
    margin: 15px 0 12px 0;
    font-size: 1.1em;
    font-weight: 600;
    box-shadow: 0 2px 8px rgba(8, 145, 178, 0.2);
">
Key Performance Indicators
</div>
""", unsafe_allow_html=True)
 
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
 
with kpi1:
    st.markdown(f"""
    <div class="metric-card" style="padding: 18px;">
        <div class="metric-label" style="font-size: 0.8rem;">Total Markets</div>
        <div class="metric-value" style="font-size: 2rem;">{len(df_grouped):,}</div>
    </div>
    """, unsafe_allow_html=True)
 
with kpi2:
    avg_henry = df_grouped['henry_index'].mean()
    tooltip_html = create_tooltip("HENRY Index", "henry_index")
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%); padding: 18px;">
        <div class="metric-label" style="font-size: 0.8rem;">AVG {tooltip_html}</div>
        <div class="metric-value" style="font-size: 2rem;">{avg_henry:.1f}</div>
    </div>
    """, unsafe_allow_html=True)
 
with kpi3:
    avg_score = df_grouped['market_score'].mean()
    tooltip_html = create_tooltip("Market Score", "market_score")
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%); padding: 18px;">
        <div class="metric-label" style="font-size: 0.8rem;">AVG {tooltip_html}</div>
        <div class="metric-value" style="font-size: 2rem;">{avg_score:.2f}</div>
    </div>
    """, unsafe_allow_html=True)
 
with kpi4:
    hot_markets = len(df_grouped[df_grouped['market_score'] > 0.7])
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #10b981 0%, #14b8a6 100%); padding: 18px;">
        <div class="metric-label" style="font-size: 0.8rem;">Hot Markets</div>
        <div class="metric-value" style="font-size: 2rem;">{hot_markets}</div>
    </div>
    """, unsafe_allow_html=True)
 
st.markdown("---")
 
# ---------------- TABS ----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🗺️ Market Explorer",
    "🏆 Top Opportunities",
    "📈 Growth Analysis",
    "🤖 AI Advisor",
    "📚 Insights Library"
])
 
# ---------------- TAB 1: MARKET EXPLORER ----------------
with tab1:
    st.markdown('<div class="section-header">Geographic Market Distribution</div>', unsafe_allow_html=True)
    
    col_map1, col_map2 = st.columns([2.5, 1])
    
    with col_map1:
        state_data = df_grouped.groupby('STATE').agg({
            'market_score': 'mean',
            'henry_index': 'mean',
            'N1': 'sum'
        }).reset_index()
        
        fig_map = px.choropleth(
            state_data,
            locations='STATE',
            locationmode="USA-states",
            color='market_score',
            color_continuous_scale='Teal',
            scope="usa",
            labels={'market_score': 'Market Score'},
            title="Market Score by State"
        )
        
        fig_map.update_layout(
            height=550,
            geo=dict(bgcolor='rgba(0,0,0,0)'),
            margin=dict(l=0, r=0, t=40, b=0),
            font=dict(size=12)
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
    
    with col_map2:
        st.markdown('<div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 12px rgba(8, 145, 178, 0.1);"><h3 style="margin-top: 0; color: #0891b2;">State Rankings</h3>', unsafe_allow_html=True)
        top_states = state_data.sort_values('market_score', ascending=False).head(10)
        
        # Create a more compact ranking display
        ranking_html = ""
        for rank, (idx, row) in enumerate(top_states.iterrows(), 1):
            medal = "1." if rank == 1 else "2." if rank == 2 else "3." if rank == 3 else f"{rank}."
            ranking_html += f"""
            <div style="padding: 8px 0; border-bottom: 1px solid #e0f2fe; display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 1.1em; min-width: 30px;">{medal}</span>
                    <span style="font-weight: 600; color: #0891b2;">{row['STATE']}</span>
                </div>
                <div style="text-align: right;">
                    <div style="font-weight: 700; color: #0f172a;">{row['market_score']:.3f}</div>
                    <div style="font-size: 0.75em; color: #64748b;">{row['henry_index']:.0f} HENRY</div>
                </div>
            </div>
            """
        
        st.markdown(ranking_html + "</div>", unsafe_allow_html=True)
    
    # Scatter plot
    st.markdown("---")
    st.markdown("### Market Segmentation: Size vs. Opportunity")
    st.caption("Hover over bubbles to see details. Bubble size represents market score, color shows growth velocity.")
    
    fig_scatter = px.scatter(
        df_grouped.sort_values('market_score', ascending=False).head(100),
        x='N1',
        y='henry_index',
        size='market_score',
        color='velocity',
        hover_data={
            'zip_display': True,
            'market_score': ':.3f',
            'N1': ':,',
            'henry_index': ':.1f',
            'velocity': ':+.2f'
        },
        color_continuous_scale='RdYlGn',
        labels={
            'N1': 'Market Size (Number of Returns)',
            'henry_index': 'HENRY Index',
            'velocity': 'Growth Velocity',
            'zip_display': 'ZIP Code'
        },
        size_max=30
    )
    
    fig_scatter.update_layout(
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12)
    )
    
    fig_scatter.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(8, 145, 178, 0.1)')
    fig_scatter.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(8, 145, 178, 0.1)')
    
    st.plotly_chart(fig_scatter, use_container_width=True)
 
# ---------------- TAB 2: TOP OPPORTUNITIES ----------------
with tab2:
    st.markdown('<div class="section-header">Top Investment Opportunities</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <p style="color: #64748b; margin-bottom: 15px;">Markets ranked by {create_tooltip("Market Score", "market_score")} - a composite metric of opportunity, size, and growth.</p>
    """, unsafe_allow_html=True)
    
    top_df = df_grouped.sort_values('market_score', ascending=False).head(top_n)
    
    # Bar chart with gradient - now showing ZIP with state
    fig_bar = go.Figure()
    
    fig_bar.add_trace(go.Bar(
        x=top_df['zip_display'],
        y=top_df['market_score'],
        marker=dict(
            color=top_df['henry_index'],
            colorscale='Teal',
            colorbar=dict(title="HENRY<br>Index"),
            line=dict(color='rgba(8, 145, 178, 0.4)', width=1.5)
        ),
        text=top_df['market_score'].round(3),
        textposition='outside',
        textfont=dict(size=10, color='#0f172a'),
        hovertemplate='<b>Market:</b> %{x}<br><b>Score:</b> %{y:.3f}<br><b>HENRY:</b> %{marker.color:.1f}<extra></extra>'
    ))
    
    fig_bar.update_layout(
        title="Market Score by ZIP Code (Top Markets)",
        xaxis_title="ZIP Code (State)",
        yaxis_title="Market Score",
        height=450,
        showlegend=False,
        xaxis_type='category',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12)
    )
    
    fig_bar.update_xaxes(showgrid=False, tickangle=-45)
    fig_bar.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(8, 145, 178, 0.1)')
    
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Enhanced data table
    st.markdown("---")
    st.markdown("### Detailed Market Analysis")
    
    display_df = top_df[['zip_display', 'market_score', 'henry_index', 'N1', 'velocity', 'risk_category']].copy()
    display_df.columns = ['ZIP Code (State)', 'Market Score', 'HENRY Index', 'Population', 'Velocity', 'Status']
    
    # Format numbers
    display_df['Market Score'] = display_df['Market Score'].round(3)
    display_df['HENRY Index'] = display_df['HENRY Index'].round(1)
    display_df['Velocity'] = display_df['Velocity'].round(2)
    display_df['Population'] = display_df['Population'].astype(int)
    
    st.dataframe(
        display_df,
        use_container_width=True,
        height=450,
        column_config={
            "ZIP Code (State)": st.column_config.TextColumn("ZIP Code (State)", width="medium"),
            "Market Score": st.column_config.ProgressColumn(
                "Market Score",
                format="%.3f",
                min_value=0,
                max_value=1,
            ),
            "HENRY Index": st.column_config.NumberColumn(
                "HENRY Index",
                format="%.1f",
            ),
            "Population": st.column_config.NumberColumn(
                "Population",
                format="%d",
            ),
            "Velocity": st.column_config.NumberColumn(
                "Velocity",
                format="%+.2f",
            ),
            "Status": st.column_config.TextColumn("Market Status", width="medium"),
        },
        hide_index=True
    )
 
# ---------------- TAB 3: GROWTH ANALYSIS ----------------
with tab3:
    st.markdown('<div class="section-header">Emerging HENRY Hubs</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <p style="color: #64748b; margin-bottom: 15px;">Markets with positive {create_tooltip("Wealth Velocity", "velocity")} indicate areas where incomes are growing faster than investments - prime opportunities!</p>
    """, unsafe_allow_html=True)
    
    # Only show the bar chart, full width
    growth_df = df_grouped[df_grouped['velocity'] > 0]
    growth_df = growth_df.sort_values('velocity', ascending=False).head(top_n)
    
    fig_growth = go.Figure()
    
    fig_growth.add_trace(go.Bar(
        x=growth_df['zip_display'],
        y=growth_df['velocity'],
        marker=dict(
            color=growth_df['velocity'],
            colorscale='Greens',
            showscale=False,
            line=dict(color='rgba(16, 185, 129, 0.4)', width=1.5)
        ),
        text=growth_df['velocity'].round(2),
        textposition='outside',
        textfont=dict(size=10, color='#0f172a', family='Arial'),
        hovertemplate='<b>Market:</b> %{x}<br><b>Velocity:</b> %{y:.2f}<br><extra></extra>'
    ))
    
    fig_growth.update_layout(
        title={
            'text': "Year-over-Year HENRY Index Growth",
            'font': {'size': 16, 'color': '#0f172a'}
        },
        xaxis_title="ZIP Code (State)",
        yaxis_title="Velocity (HENRY Index Change)",
        height=480,
        showlegend=False,
        xaxis_type='category',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        margin=dict(t=60, b=60, l=60, r=20)
    )
    
    fig_growth.update_xaxes(
        showgrid=False,
        tickangle=-45,
        tickfont=dict(size=10)
    )
    fig_growth.update_yaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='rgba(16, 185, 129, 0.1)'
    )
    
    st.plotly_chart(fig_growth, use_container_width=True)
 
# ---------------- TAB 4: AI ADVISOR ----------------
def generate_email(zip_code, state, income, investment, market_score, henry_index, velocity):
    
    system_msg = """
    You are a professional financial advisor marketing assistant.
    Write personalized, human-like outreach emails using data.
    """

    prompt = f"""
    Create a personalized outreach email.

    Market Data:
    - ZIP Code: {zip_code}, {state}
    - Average Income: ${income:,.0f}
    - Investment Level: ${investment:,.0f}
    - Market Score: {market_score:.2f}
    - HENRY Index: {henry_index:.1f}
    - Growth Velocity: {velocity:.2f}

    Requirements:
    - Include subject line
    - Explain wealth gap clearly
    - Professional tone (not robotic)
    - Add CTA for consultation
    - Keep under 250 words
    """

    return ai_call(system_msg, prompt)
 
def generate_newsletter(top_markets_df, state_filter):
    
    system_msg = """
    You are a financial analyst creating executive-level newsletters.
    """

    data_summary = top_markets_df.head(5)[['zip_display', 'market_score', 'henry_index', 'velocity']].to_string()

    prompt = f"""
    Create a monthly HENRY market newsletter.

    State Filter: {state_filter}

    Top Markets Data:
    {data_summary}

    Include:
    - Title
    - Top 5 markets summary
    - Key insights
    - Strategic recommendations
    - Professional tone
    """

    return ai_call(system_msg, prompt)
 
 
with tab4:
    st.markdown('<div class="section-header">AI-Powered Marketing Tools</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="cool-card">
    <h3>What Can AI Do For You?</h3>
    <p>Our AI tools help you:</p>
    <ul>
        <li><strong>📧 Personalize Outreach:</strong> Generate emails customized to each market's unique characteristics (income levels, growth trends, market maturity)</li>
        <li><strong>📰 Create Newsletters:</strong> Automatically compile monthly market intelligence reports</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Tool selector
    ai_tool = st.radio(
        "Select AI Tool:",
        ["📧 Email Generator", "📰 Newsletter Creator"],
        horizontal=True
    )
    
    st.markdown("---")
    
    if ai_tool == "📧 Email Generator":
        col_ai1, col_ai2 = st.columns([1, 2])
        
        with col_ai1:
            st.markdown("### Select Target Market")
            
            # Create options with state in brackets
            zip_options = df_grouped.sort_values('market_score', ascending=False).head(100)['zip_display'].tolist()
            
            selected_zip_display = st.selectbox(
                "Choose ZIP Code",
                zip_options,
                help="Top 100 markets by score"
            )
            
            # Extract just the ZIP code for data lookup
            selected_zip = selected_zip_display.split(' (')[0]
            
            zip_data = df_grouped[df_grouped['zipcode'] == selected_zip].iloc[0]
            
            # Market summary card
            st.markdown(f"""
            <div class="metric-card" style="text-align: left;">
                <h3>📍 {selected_zip_display}</h3>
                <hr style="border-color: rgba(255,255,255,0.3);">
                <p><strong>Market Score:</strong> {zip_data['market_score']:.3f}</p>
                <p><strong>HENRY Index:</strong> {zip_data['henry_index']:.1f}</p>
                <p><strong>Avg Income:</strong> ${zip_data['A00200']:,.0f}</p>
                <p><strong>Population:</strong> {zip_data['N1']:,.0f} returns</p>
                <p><strong>Growth:</strong> {zip_data['velocity']:+.2f}</p>
                <p><strong>Status:</strong> {zip_data['risk_category']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Generate button
            if st.button("✨ Generate Email", use_container_width=True, type="primary"):
                st.session_state.email_generated = True
        
        with col_ai2:
            st.markdown("### Generated Outreach Email")
            
            st.markdown("""
            <div class="info-box">
            <strong>🎨 How Personalization Works:</strong><br>
            • Income data determines the "wealth gap" messaging<br>
            • Growth velocity adds urgency and timing context<br>
            • Market score influences the tone (prime vs. emerging)<br>
            • HENRY Index shapes the value proposition<br>
            • All metrics come from real IRS tax data for this specific ZIP code
            </div>
            """, unsafe_allow_html=True)
            
            if 'email_generated' not in st.session_state:
                st.info("👈 Select a ZIP code and click 'Generate Email' to create personalized outreach content.")
            else:
                total_investment = zip_data['A00600'] + zip_data['A01000']
                
                with st.spinner("Generating personalized email..."):
                    email = generate_email(
                        selected_zip,
                        zip_data['STATE'],
                        zip_data['A00200'],
                        total_investment,
                        zip_data['market_score'],
                        zip_data['henry_index'],
                        zip_data['velocity']
                    )
                
                st.text_area(
                    "Email Content",
                    email,
                    height=600,
                    help="Copy this email and customize with your branding"
                )
                
                # Copy button
                st.download_button(
                    label="📥 Download Email Template",
                    data=email,
                    file_name=f"henry_outreach_{selected_zip}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                
                # Analytics
                st.markdown("---")
                st.markdown("### Email Insights")
                
                col_insight1, col_insight2, col_insight3 = st.columns(3)
                
                with col_insight1:
                    st.metric("Word Count", len(email.split()))
                
                with col_insight2:
                    st.metric("Estimated Read Time", f"{len(email.split()) // 200 + 1} min")
                
                with col_insight3:
                    personalization_score = min(100, int(zip_data['market_score'] * 100))
                    st.metric("Personalization Score", f"{personalization_score}%")
    
    else:  # Newsletter Creator
        st.markdown("### Monthly Market Intelligence Newsletter")
        
        st.markdown("""
        <div class="info-box">
        <strong>📧 What This Creates:</strong><br>
        A professionally formatted newsletter highlighting your top markets, complete with data insights and strategic recommendations. 
        Perfect for sharing with your team or sending to prospects.
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("✨ Generate Newsletter", use_container_width=True, type="primary"):
            with st.spinner("Generating newsletter..."):
                newsletter_content = generate_newsletter(
                    df_grouped.sort_values('market_score', ascending=False).head(top_n),
                    state
                )
            
            st.markdown(newsletter_content)
            
            st.download_button(
                label="📥 Download Newsletter (Markdown)",
                data=newsletter_content,
                file_name=f"henry_newsletter_{datetime.now().strftime('%Y%m')}.md",
                mime="text/markdown",
                use_container_width=True
            )
 
# ---------------- TAB 5: INSIGHTS LIBRARY ----------------
with tab5:
    st.markdown('<div class="section-header">Market Intelligence Insights</div>', unsafe_allow_html=True)
    
    st.markdown("""
    Deep dive into the data behind HENRY markets. Use these insights to inform your strategy.
    """)
    
    # Key insights
    insight_col1, insight_col2 = st.columns(2)
    
    with insight_col1:
        st.markdown("### What Makes a Good HENRY Market?")
        st.markdown(f"""
        <div class="info-box">
        <strong>Top 3 Characteristics:</strong>
        <ol>
            <li><strong>High {create_tooltip("HENRY Index", "henry_index")} (>50):</strong> Significant gap between earnings and investments</li>
            <li><strong>Critical Mass (>200 returns):</strong> Enough prospects for cost-effective marketing</li>
            <li><strong>Positive {create_tooltip("Velocity", "velocity")} (>0):</strong> Growing income without proportional investment growth</li>
        </ol>
        
        <strong>💡 Pro Tip:</strong> Markets with HENRY Index 50-100 convert better than 100+ (less competition from wealth managers).
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Investment Opportunity Tiers")
        st.markdown("""
        <div class="success-box">
        <strong>🔥 Tier 1: Hot Markets (Score 0.75+)</strong><br>
        Immediate action required. High conversion potential.<br><br>
        
        <strong>📈 Tier 2: Growing (Score 0.5-0.75)</strong><br>
        Strong potential. Position early for future growth.<br><br>
        
        <strong>✅ Tier 3: Stable (Score 0.3-0.5)</strong><br>
        Steady prospects. Good for sustained campaigns.<br><br>
        
        <strong>⚠️ Tier 4: Low Priority (<0.3)</strong><br>
        Limited opportunity. Focus elsewhere.
        </div>
        """, unsafe_allow_html=True)
    
    with insight_col2:
        st.markdown("### Understanding the Metrics")
        
        st.markdown(f"""
        <div class="cool-card">
        <h4>{create_tooltip("HENRY Index", "henry_index")}</h4>
        <p>Measures the gap between what people earn vs. what they invest. Higher = more opportunity.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="cool-card">
        <h4>{create_tooltip("Market Score", "market_score")}</h4>
        <p>Composite metric combining HENRY Index, market size, and growth velocity into one actionable number.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="cool-card">
        <h4>{create_tooltip("Wealth Velocity", "velocity")}</h4>
        <p>Year-over-year change showing if a market is becoming more "HENRY-fied" over time.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Case Study: Austin, TX")
        st.markdown("""
        <div class="warning-box">
        <strong>Market Profile:</strong> Tech hub with rapid income growth<br>
        <strong>HENRY Index:</strong> 78 (High)<br>
        <strong>Velocity:</strong> +12.5 (Very High)<br>
        <strong>Key Insight:</strong> Young professionals earning $150K+ but haven't started serious investing yet.<br><br>
        
        <strong>Recommended Strategy:</strong>
        <ul>
            <li>Target tech workers aged 28-35</li>
            <li>Focus on tax-advantaged retirement accounts</li>
            <li>Emphasize long-term wealth building</li>
            <li>Leverage digital marketing (high tech literacy)</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Data quality notes
    st.markdown("---")
    st.markdown("### Important Notes")
    st.info("""
    **Data Limitations:**
    - Based on IRS tax return data (2021-2022)
    - Aggregated at ZIP code level (individual variation exists)
    - Investment income includes dividends and interest (may not capture all wealth)
    - Does not include retirement accounts (401k, IRA) which are pre-tax
    
    **Best Practices:**
    - Combine with demographic data for fuller picture
    - Validate high-priority markets with local research
    - Test messaging with small campaigns before scaling
    - Monitor conversion rates to refine targeting
    """)

# ---------------- FOOTER ----------------
st.markdown("---")
footer_col1 = st.columns(1)[0]

with footer_col1:
    st.caption("📊 **Data Source:** IRS Statistics of Income (2021-2022)")