# dashboard/app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(
    page_title="Gentrifikasi DKI Jakarta - Dashboard Ekonomi",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #4B5563;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #F3F4F6;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
    }
</style>
""", unsafe_allow_html=True)

# Load data function
@st.cache_data
def load_data():
    # Load your Excel files
    df_yoy = pd.read_excel('../data/PDRB_Jakarta_YoY.xlsx')
    df_nilai = pd.read_excel('../data/PDRB_Jakarta_Nilai.xlsx')
    
    # Load complete datasets
    df_laju = pd.read_excel('../data/Laju Pertumbuhan (Y-ON-Y) PDRB Provinsi DKI Jakarta Atas Dasar Konstan 2010 Menurut Pengeluaran, 2025.xlsx')
    df_pdrb_full = pd.read_excel('../data/PDRB Triwulanan Provinsi DKI Jakarta Atas Dasar Harga Konstan Menurut Pengeluaran, 2025.xlsx')
    
    # Clean and transform data
    # Clean df_laju
    df_laju = df_laju.iloc[3:].reset_index(drop=True)
    df_laju.columns = ['Komponen', 'Triwulan I', 'Triwulan II', 'Triwulan III', 'Triwulan IV', 'Tahunan']
    df_laju = df_laju.melt(id_vars=['Komponen'], var_name='Triwulan', value_name='Pertumbuhan')
    df_laju = df_laju.dropna(subset=['Pertumbuhan'])
    
    # Clean df_pdrb_full
    df_pdrb_full = df_pdrb_full.iloc[3:].reset_index(drop=True)
    df_pdrb_full.columns = ['Komponen', 'Triwulan I', 'Triwulan II', 'Triwulan III', 'Triwulan IV', 'Tahunan']
    df_pdrb_full = df_pdrb_full.melt(id_vars=['Komponen'], var_name='Triwulan', value_name='Nilai')
    df_pdrb_full = df_pdrb_full.dropna(subset=['Nilai'])
    
    return df_yoy, df_nilai, df_laju, df_pdrb_full

# Main app
def main():
    # Header
    st.markdown('<h1 class="main-header">🏙️ DASHBOARD ANALISIS GENTRIFIKASI DKI JAKARTA</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Visualisasi Interaktif PDRB dan Indikator Ekonomi Makro 2025</p>', unsafe_allow_html=True)
    
    # Load data
    df_yoy, df_nilai, df_laju, df_pdrb_full = load_data()
    
    # Sidebar
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/0/0b/Logo_Provinsi_DKI_Jakarta.png", 
                width=100)
        st.title("Filter Dashboard")
        
        st.subheader("Tahun Analisis")
        tahun = st.selectbox("Pilih Tahun", [2025], index=0)
        
        st.subheader("Komponen Ekonomi")
        komponen_options = [
            'Pengeluaran Konsumsi Rumah Tangga',
            'Pengeluaran Konsumsi Pemerintah',
            'Pembentukan Modal Tetap Bruto',
            'PDRB'
        ]
        selected_components = st.multiselect(
            "Pilih Komponen",
            komponen_options,
            default=komponen_options
        )
        
        st.subheader("Jenis Visualisasi")
        chart_type = st.selectbox(
            "Tipe Chart",
            ["Line Chart", "Bar Chart", "Area Chart", "Scatter Plot"]
        )
        
        st.subheader("Metrik Tambahan")
        show_metrics = st.checkbox("Tampilkan Metrik KPI", value=True)
        show_forecast = st.checkbox("Tampilkan Proyeksi", value=False)
        
        st.divider()
        st.caption("Sumber Data: BPS Provinsi DKI Jakarta 2025")
    
    # Main content
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview", 
        "💰 Konsumsi", 
        "🏗️ Investasi", 
        "📈 Analisis", 
        "📥 Ekspor"
    ])
    
    with tab1:
        st.header("Overview Ekonomi DKI Jakarta 2025")
        
        # KPI Metrics
        if show_metrics:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                pdrb_q3 = df_pdrb_full[(df_pdrb_full['Komponen'] == 'PDRB') & 
                                      (df_pdrb_full['Triwulan'] == 'Triwulan III')]['Nilai'].values[0]
                st.metric(
                    label="PDRB Q3 2025",
                    value=f"Rp {pdrb_q3/1000:.1f}T",
                    delta="4.96% YoY"
                )
            
            with col2:
                konsumsi_rt = df_pdrb_full[(df_pdrb_full['Komponen'] == 'Pengeluaran Konsumsi Rumah Tangga') & 
                                         (df_pdrb_full['Triwulan'] == 'Triwulan III')]['Nilai'].values[0]
                st.metric(
                    label="Konsumsi Rumah Tangga",
                    value=f"Rp {konsumsi_rt/1000:.1f}T",
                    delta="5.01% YoY"
                )
            
            with col3:
                pmtb_q3 = df_pdrb_full[(df_pdrb_full['Komponen'] == 'Pembentukan Modal Tetap Bruto') & 
                                      (df_pdrb_full['Triwulan'] == 'Triwulan III')]['Nilai'].values[0]
                st.metric(
                    label="Investasi (PMTB)",
                    value=f"Rp {pmtb_q3/1000:.1f}T",
                    delta="3.67% YoY"
                )
            
            with col4:
                growth_avg = df_laju[df_laju['Komponen'] == 'PDRB']['Pertumbuhan'].mean()
                st.metric(
                    label="Rata-rata Pertumbuhan",
                    value=f"{growth_avg:.2f}%",
                    delta="0.23% dari Q2"
                )
        
        # Chart 1: PDRB Trend
        st.subheader("Tren PDRB Triwulanan 2025")
        col1, col2 = st.columns([3, 1])
        
        with col1:
            pdrb_data = df_pdrb_full[df_pdrb_full['Komponen'] == 'PDRB']
            
            if chart_type == "Line Chart":
                fig1 = px.line(pdrb_data, x='Triwulan', y='Nilai',
                              markers=True, line_shape='spline',
                              title='Perkembangan PDRB DKI Jakarta 2025')
            elif chart_type == "Bar Chart":
                fig1 = px.bar(pdrb_data, x='Triwulan', y='Nilai',
                             title='Perkembangan PDRB DKI Jakarta 2025',
                             color='Triwulan')
            elif chart_type == "Area Chart":
                fig1 = px.area(pdrb_data, x='Triwulan', y='Nilai',
                              title='Perkembangan PDRB DKI Jakarta 2025')
            else:
                fig1 = px.scatter(pdrb_data, x='Triwulan', y='Nilai',
                                 title='Perkembangan PDRB DKI Jakarta 2025',
                                 size=[20, 25, 30])
            
            fig1.update_layout(
                yaxis_title="Nilai (Miliar Rupiah)",
                xaxis_title="Triwulan",
                hovermode='x unified'
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            st.subheader("Data Points")
            st.dataframe(pdrb_data[['Triwulan', 'Nilai']].style.format({'Nilai': 'Rp {:,.0f}'}),
                        use_container_width=True)
        
        # Chart 2: Comparison Chart
        st.subheader("Perbandingan Komponen Utama")
        
        comparison_data = df_pdrb_full[df_pdrb_full['Komponen'].isin([
            'Pengeluaran Konsumsi Rumah Tangga',
            'Pembentukan Modal Tetap Bruto',
            'Pengeluaran Konsumsi Pemerintah'
        ])]
        
        fig2 = px.line(comparison_data, x='Triwulan', y='Nilai', color='Komponen',
                      markers=True, title='Perbandingan Komponen Ekonomi Utama')
        fig2.update_layout(
            yaxis_title="Nilai (Miliar Rupiah)",
            xaxis_title="Triwulan",
            legend_title="Komponen"
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        st.header("Analisis Konsumsi")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Konsumsi Rumah Tangga
            konsumsi_rt_data = df_pdrb_full[df_pdrb_full['Komponen'] == 'Pengeluaran Konsumsi Rumah Tangga']
            
            fig3 = go.Figure()
            fig3.add_trace(go.Bar(
                x=konsumsi_rt_data['Triwulan'],
                y=konsumsi_rt_data['Nilai'],
                name='Nilai',
                marker_color='#2E86C1'
            ))
            
            # Add growth line
            growth_rt = df_laju[df_laju['Komponen'] == 'Pengeluaran Konsumsi Rumah Tangga']
            fig3.add_trace(go.Scatter(
                x=growth_rt['Triwulan'],
                y=growth_rt['Pertumbuhan'] * 5000,  # Scale for visualization
                name='Pertumbuhan (%)',
                yaxis='y2',
                line=dict(color='#E74C3C', width=3),
                mode='lines+markers'
            ))
            
            fig3.update_layout(
                title='Konsumsi Rumah Tangga & Pertumbuhan',
                yaxis=dict(title='Nilai (Miliar Rupiah)'),
                yaxis2=dict(
                    title='Pertumbuhan (%)',
                    overlaying='y',
                    side='right',
                    range=[0, 30]
                ),
                hovermode='x unified'
            )
            st.plotly_chart(fig3, use_container_width=True)
        
        with col2:
            # Konsumsi Pemerintah
            konsumsi_gov_data = df_pdrb_full[df_pdrb_full['Komponen'] == 'Pengeluaran Konsumsi Pemerintah']
            
            fig4 = px.bar(konsumsi_gov_data, x='Triwulan', y='Nilai',
                         title='Konsumsi Pemerintah per Triwulan',
                         color='Nilai',
                         color_continuous_scale='Viridis')
            
            fig4.update_layout(
                yaxis_title="Nilai (Miliar Rupiah)",
                xaxis_title="Triwulan"
            )
            st.plotly_chart(fig4, use_container_width=True)
        
        # Growth Analysis
        st.subheader("Analisis Pertumbuhan Konsumsi")
        
        growth_comparison = df_laju[df_laju['Komponen'].isin([
            'Pengeluaran Konsumsi Rumah Tangga',
            'Pengeluaran Konsumsi Pemerintah'
        ])]
        
        fig5 = px.bar(growth_comparison, x='Triwulan', y='Pertumbuhan', color='Komponen',
                     barmode='group', title='Pertumbuhan YoY Konsumsi')
        fig5.update_layout(
            yaxis_title="Pertumbuhan (%)",
            xaxis_title="Triwulan"
        )
        st.plotly_chart(fig5, use_container_width=True)
    
    with tab3:
        st.header("Analisis Investasi (PMTB)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # PMTB Value
            pmtb_data = df_pdrb_full[df_pdrb_full['Komponen'] == 'Pembentukan Modal Tetap Bruto']
            
            fig6 = px.area(pmtb_data, x='Triwulan', y='Nilai',
                          title='Akumulasi Investasi (PMTB) 2025',
                          color_discrete_sequence=['#27AE60'])
            
            fig6.update_layout(
                yaxis_title="Nilai (Miliar Rupiah)",
                xaxis_title="Triwulan"
            )
            st.plotly_chart(fig6, use_container_width=True)
        
        with col2:
            # PMTB Growth
            pmtb_growth = df_laju[df_laju['Komponen'] == 'Pembentukan Modal Tetap Bruto']
            
            fig7 = go.Figure(data=[
                go.Indicator(
                    mode="gauge+number+delta",
                    value=pmtb_growth['Pertumbuhan'].mean(),
                    title={'text': "Rata-rata Pertumbuhan PMTB"},
                    delta={'reference': 3.0},
                    gauge={
                        'axis': {'range': [None, 10]},
                        'bar': {'color': "#2ECC71"},
                        'steps': [
                            {'range': [0, 3], 'color': "lightgray"},
                            {'range': [3, 6], 'color': "gray"},
                            {'range': [6, 10], 'color': "darkgray"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 6
                        }
                    }
                )
            ])
            
            fig7.update_layout(height=300)
            st.plotly_chart(fig7, use_container_width=True)
        
        # Investment Analysis
        st.subheader("Komparasi Investasi vs Konsumsi")
        
        comparison_df = df_pdrb_full[df_pdrb_full['Komponen'].isin([
            'Pembentukan Modal Tetap Bruto',
            'Pengeluaran Konsumsi Rumah Tangga'
        ])]
        
        fig8 = px.scatter(comparison_df, x='Triwulan', y='Nilai', color='Komponen',
                         size='Nilai', hover_name='Komponen',
                         title='Perbandingan Skala: Investasi vs Konsumsi RT')
        
        fig8.update_layout(
            yaxis_title="Nilai (Miliar Rupiah)",
            xaxis_title="Triwulan"
        )
        st.plotly_chart(fig8, use_container_width=True)
    
    with tab4:
        st.header("Analisis Lanjutan")
        
        # Correlation Analysis
        st.subheader("Analisis Korelasi")
        
        # Prepare data for correlation
        components_for_corr = [
            'Pengeluaran Konsumsi Rumah Tangga',
            'Pengeluaran Konsumsi Pemerintah',
            'Pembentukan Modal Tetap Bruto',
            'PDRB'
        ]
        
        corr_data = df_pdrb_full[df_pdrb_full['Komponen'].isin(components_for_corr)]
        corr_pivot = corr_data.pivot(index='Komponen', columns='Triwulan', values='Nilai')
        corr_matrix = corr_pivot.T.corr()
        
        # Shorten labels
        corr_matrix.index = [k.replace('Pengeluaran Konsumsi ', '').replace('Pembentukan ', '') 
                            for k in corr_matrix.index]
        corr_matrix.columns = corr_matrix.index
        
        fig9 = px.imshow(corr_matrix,
                        text_auto='.2f',
                        aspect="auto",
                        color_continuous_scale='RdBu',
                        title='Matriks Korelasi Antar Komponen Ekonomi')
        
        st.plotly_chart(fig9, use_container_width=True)
        
        # Forecast (simple)
        if show_forecast:
            st.subheader("Proyeksi Q4 2025")
            
            # Simple linear projection
            pdrb_values = df_pdrb_full[df_pdrb_full['Komponen'] == 'PDRB']['Nilai'].values
            quarters = np.array([1, 2, 3])
            
            # Linear regression for projection
            coeff = np.polyfit(quarters, pdrb_values, 1)
            projected_q4 = coeff[0] * 4 + coeff[1]
            
            fig10 = go.Figure()
            fig10.add_trace(go.Scatter(
                x=['Q1', 'Q2', 'Q3', 'Q4*'],
                y=list(pdrb_values) + [projected_q4],
                mode='lines+markers',
                name='PDRB Aktual & Proyeksi',
                line=dict(color='blue', width=3)
            ))
            
            fig