# ═══════════════════════════════════════════════════════════════
# NutriVision — Streamlit Dashboard
# CC26-PRU442 | Coding Camp powered by DBS Foundation 2026
# ═══════════════════════════════════════════════════════════════

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page Config ────────────────────────────────────────────────
st.set_page_config(
    page_title="NutriVision Dashboard",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    [data-testid="stSidebar"] * { color: #e0e0e0 !important; }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 { color: #64ffda !important; }

    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #1e3a5f, #0d2137);
        border: 1px solid #2a5298;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .kpi-value { font-size: 2.2rem; font-weight: 700; color: #64ffda; }
    .kpi-label { font-size: 0.85rem; color: #a0b4c8; margin-top: 5px; }
    .kpi-delta-pos { font-size: 0.8rem; color: #4caf50; }
    .kpi-delta-neg { font-size: 0.8rem; color: #ef5350; }

    /* Insight Panel */
    .insight-box {
        background: linear-gradient(135deg, #0d2137, #1a3a5f);
        border-left: 4px solid #64ffda;
        border-radius: 8px;
        padding: 15px 20px;
        margin: 10px 0;
    }
    .insight-box p { color: #c8d8e8; font-size: 0.9rem; margin: 0; }

    /* Risk badges */
    .badge-safe { background:#1b5e20; color:#a5d6a7; padding:3px 10px; border-radius:20px; font-size:0.8rem; }
    .badge-low  { background:#f57f17; color:#fff9c4; padding:3px 10px; border-radius:20px; font-size:0.8rem; }
    .badge-mid  { background:#e65100; color:#ffe0b2; padding:3px 10px; border-radius:20px; font-size:0.8rem; }
    .badge-high { background:#b71c1c; color:#ffcdd2; padding:3px 10px; border-radius:20px; font-size:0.8rem; }

    /* Main background */
    .main { background-color: #0a0e1a; }
    h1, h2, h3 { color: #64ffda; }
</style>
""", unsafe_allow_html=True)

# ── Load Data ──────────────────────────────────────────────────
@st.cache_data
def load_data():
        df = pd.read_csv('nutrivision_final_v4.csv')

        return df

df = load_data()

# ── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("# 🥗 NutriVision")
    st.markdown("**CC26-PRU442 | DBS Foundation 2026**")
    st.markdown("---")

    st.markdown("### 🔍 Filter Data")

    # Filter Kategori
    all_cats = sorted(df['food_category'].dropna().unique())
    selected_cats = st.multiselect(
        "Kategori Makanan",
        options=all_cats,
        default=all_cats[:8] if len(all_cats) > 8 else all_cats,
        help="Pilih satu atau lebih kategori makanan"
    )

    # Filter Risk Level
    risk_options = ['Aman', 'Risiko Rendah', 'Risiko Sedang', 'Risiko Tinggi']
    selected_risk = st.multiselect(
        "Level Risiko",
        options=risk_options,
        default=risk_options,
        help="Filter berdasarkan tingkat risiko kesehatan"
    )

    # Filter Range Kalori
    cal_min, cal_max = int(df['calories'].min()), int(df['calories'].max())
    cal_range = st.slider(
        "Range Kalori (kcal/100g)",
        min_value=cal_min,
        max_value=cal_max,
        value=(0, 800),
        help="Filter makanan berdasarkan kalori"
    )

    # Filter Sumber Data
    sources = sorted(df['source'].unique())
    selected_sources = st.multiselect(
        "Sumber Dataset",
        options=sources,
        default=sources
    )

    st.markdown("---")
    st.markdown("### ℹ️ Tentang Dataset")
    st.info(f"Total makanan: **{len(df):,}**\nKolom: **{len(df.columns)}**")
    st.markdown("---")
    st.caption("NutriVision v4 | Data Science | CC26-PRU442")

# ── Apply Filters ──────────────────────────────────────────────
filtered = df[
    (df['food_category'].isin(selected_cats) if selected_cats else True) &
    (df['risk_level'].isin(selected_risk) if selected_risk else True) &
    (df['calories'].between(cal_range[0], cal_range[1])) &
    (df['source'].isin(selected_sources) if selected_sources else True)
].copy()

# ── Header ─────────────────────────────────────────────────────
st.markdown("# 🥗 NutriVision Analytics Dashboard")
st.markdown(f"*Analisis Gizi & Risiko Kesehatan — CC26-PRU442 | {len(filtered):,} makanan ditampilkan*")
st.markdown("---")

# ── KPI Cards ──────────────────────────────────────────────────
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{len(filtered):,}</div>
        <div class="kpi-label">Total Makanan</div>
    </div>""", unsafe_allow_html=True)

with col2:
    avg_cal = filtered['calories'].mean()
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{avg_cal:.0f}</div>
        <div class="kpi-label">Rata-rata Kalori (kcal)</div>
    </div>""", unsafe_allow_html=True)

with col3:
    avg_hs = filtered['health_score'].mean()
    delta_color = 'kpi-delta-pos' if avg_hs >= 50 else 'kpi-delta-neg'
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{avg_hs:.1f}</div>
        <div class="kpi-label">Rata-rata Health Score</div>
        <div class="{delta_color}">{'✅ Di atas rata-rata' if avg_hs >= 50 else '⚠️ Di bawah rata-rata'}</div>
    </div>""", unsafe_allow_html=True)

with col4:
    pct_high_risk = (filtered['risk_level'] == 'Risiko Tinggi').mean() * 100
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{pct_high_risk:.1f}%</div>
        <div class="kpi-label">Makanan Risiko Tinggi</div>
    </div>""", unsafe_allow_html=True)

with col5:
    n_cats = filtered['food_category'].nunique()
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{n_cats}</div>
        <div class="kpi-label">Kategori Aktif</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Row 1: Distribusi + Risk Pie ───────────────────────────────
st.markdown("## 📊 Analisis Distribusi & Risiko")
col_left, col_right = st.columns([3, 2])

with col_left:
    nutrisi_choice = st.selectbox(
        "Pilih nutrisi untuk histogram:",
        options=['calories', 'protein_g', 'carbs_g', 'fat_g', 'fiber_g', 'sugar_g', 'sodium_mg', 'health_score'],
        index=0
    )
    fig_hist = px.histogram(
        filtered, x=nutrisi_choice, nbins=50,
        color='risk_level',
        color_discrete_map={
            'Aman': '#27ae60', 'Risiko Rendah': '#f39c12',
            'Risiko Sedang': '#e67e22', 'Risiko Tinggi': '#e74c3c'
        },
        title=f'Distribusi {nutrisi_choice} (per 100g)',
        template='plotly_dark',
        labels={nutrisi_choice: nutrisi_choice, 'count': 'Jumlah Makanan'}
    )
    fig_hist.update_layout(height=350, margin=dict(t=40, b=20))
    st.plotly_chart(fig_hist, use_container_width=True)

with col_right:
    risk_counts = filtered['risk_level'].value_counts().reset_index()
    risk_counts.columns = ['risk_level', 'count']
    fig_pie = px.pie(
        risk_counts, values='count', names='risk_level',
        color='risk_level',
        color_discrete_map={
            'Aman': '#27ae60', 'Risiko Rendah': '#f39c12',
            'Risiko Sedang': '#e67e22', 'Risiko Tinggi': '#e74c3c'
        },
        title='Distribusi Risk Level',
        template='plotly_dark'
    )
    fig_pie.update_layout(height=350, margin=dict(t=40, b=20))
    st.plotly_chart(fig_pie, use_container_width=True)

# ── Row 2: Kalori per Kategori + Scatter ──────────────────────
st.markdown("## 🏷️ Profil Kategori & Korelasi Nutrisi")
col_a, col_b = st.columns(2)

with col_a:
    cat_avg = filtered.groupby('food_category').agg(
        avg_calories=('calories', 'mean'),
        count=('food_name', 'count')
    ).reset_index().sort_values('avg_calories', ascending=False).head(15)

    fig_bar = px.bar(
        cat_avg, x='avg_calories', y='food_category',
        orientation='h',
        color='avg_calories',
        color_continuous_scale='RdYlGn_r',
        title='Rata-rata Kalori per Kategori (Top 15)',
        template='plotly_dark',
        labels={'avg_calories': 'Kalori (kcal)', 'food_category': ''}
    )
    fig_bar.update_layout(height=420, margin=dict(t=40, b=20), coloraxis_showscale=False)
    st.plotly_chart(fig_bar, use_container_width=True)

with col_b:
    x_axis = st.selectbox("X-axis:", ['calories', 'protein_g', 'fat_g', 'carbs_g', 'sodium_mg'], index=0, key='x_scatter')
    y_axis = st.selectbox("Y-axis:", ['health_score', 'fiber_g', 'sugar_g', 'protein_g', 'calories'], index=0, key='y_scatter')

    sample_size = min(2000, len(filtered))
    scatter_df = filtered.sample(sample_size, random_state=42) if len(filtered) > sample_size else filtered

    fig_scatter = px.scatter(
        scatter_df, x=x_axis, y=y_axis,
        color='risk_level',
        color_discrete_map={
            'Aman': '#27ae60', 'Risiko Rendah': '#f39c12',
            'Risiko Sedang': '#e67e22', 'Risiko Tinggi': '#e74c3c'
        },
        hover_data=['food_name', 'food_category'],
        title=f'{y_axis} vs {x_axis}',
        template='plotly_dark',
        opacity=0.5
    )
    fig_scatter.update_layout(height=380, margin=dict(t=40, b=20))
    st.plotly_chart(fig_scatter, use_container_width=True)

# ── Row 3: Risiko per Penyakit ────────────────────────────────
st.markdown("## 🏥 Analisis Risiko Penyakit Kronis")
col_d1, col_d2, col_d3 = st.columns(3)

diseases = [
    ('risk_diabetes',     'Diabetes',     '#e74c3c', 'sugar_g',        'Gula'),
    ('risk_hypertension', 'Hipertensi',   '#9b59b6', 'sodium_mg',      'Sodium'),
    ('risk_obesity',      'Obesitas',     '#e67e22', 'saturated_fat_g','Lemak Jenuh'),
]

for col_widget, (risk_col, disease_name, color, nutrisi_col, nutrisi_label) in zip([col_d1, col_d2, col_d3], diseases):
    with col_widget:
        pct = filtered[risk_col].mean() * 100
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=pct,
            title={'text': f"Risiko {disease_name}", 'font': {'color': 'white'}},
            number={'suffix': '%', 'font': {'color': color}},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': 'white'},
                'bar': {'color': color},
                'bgcolor': '#1a2a3a',
                'steps': [
                    {'range': [0, 20],  'color': '#1b5e20'},
                    {'range': [20, 40], 'color': '#f57f17'},
                    {'range': [40, 100],'color': '#b71c1c'}
                ]
            }
        ))
        fig_gauge.update_layout(
            height=220, template='plotly_dark',
            margin=dict(t=50, b=10, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            font={'color': 'white'}
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

# ── Row 4: Tabel Interaktif ────────────────────────────────────
st.markdown("## 📋 Tabel Data Interaktif")

search_term = st.text_input("🔍 Cari nama makanan:", placeholder="Ketik nama makanan...")
display_cols = ['food_name', 'food_category', 'calories', 'protein_g',
                'carbs_g', 'fat_g', 'fiber_g', 'sugar_g', 'sodium_mg',
                'health_score', 'risk_level', 'source']

table_df = filtered[display_cols].copy()
if search_term:
    table_df = table_df[table_df['food_name'].str.contains(search_term, case=False, na=False)]

table_df = table_df.round(2)
st.dataframe(
    table_df.head(200),
    use_container_width=True,
    height=400,
    column_config={
        'health_score': st.column_config.ProgressColumn(
            'Health Score', min_value=0, max_value=100, format="%d"
        ),
        'calories': st.column_config.NumberColumn('Kalori', format="%.0f kcal"),
        'protein_g': st.column_config.NumberColumn('Protein', format="%.1f g"),
        'risk_level': st.column_config.TextColumn('Risk Level'),
    }
)
st.caption(f"Menampilkan {min(200, len(table_df))} dari {len(table_df):,} makanan yang sesuai filter")

# ── Row 5: Insight Panel ───────────────────────────────────────
st.markdown("## 💡 Panel Insight Otomatis")

top_risky = filtered.nlargest(1, 'risk_count')['food_name'].values[0] if len(filtered) > 0 else '-'
top_healthy = filtered.nlargest(1, 'health_score')['food_name'].values[0] if len(filtered) > 0 else '-'
pct_safe = (filtered['risk_level'] == 'Aman').mean() * 100
avg_fiber = filtered['fiber_g'].mean()

insights = [
    f"🥗 Makanan paling sehat dalam filter saat ini: **{top_healthy}** (berdasarkan health_score tertinggi)",
    f"⚠️ Makanan dengan risiko gabungan tertinggi: **{top_risky}** — perlu pembatasan konsumsi",
    f"✅ **{pct_safe:.1f}%** makanan dalam filter termasuk kategori 'Aman' dari ketiga risiko penyakit kronis",
    f"🌿 Rata-rata serat dalam filter: **{avg_fiber:.1f}g/100g** — {'cukup baik ✅' if avg_fiber >= 3 else 'rendah ⚠️ (ideal >3g/100g)'}",
]

for ins in insights:
    st.markdown(f"""
    <div class="insight-box">
        <p>{ins}</p>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#4a6fa5; font-size:0.85rem;'>"
    "NutriVision Analytics Dashboard | CC26-PRU442 | Coding Camp powered by DBS Foundation 2026"
    "</p>",
    unsafe_allow_html=True
)
