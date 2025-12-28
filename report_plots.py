# report_plots_final_6graphs.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import os
import warnings
warnings.filterwarnings('ignore')

# Setup style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Fungsi format Rupiah
def format_rupiah(x, pos):
    if x >= 1e12:
        return f'Rp{x/1e12:.1f}T'
    elif x >= 1e9:
        return f'Rp{x/1e9:.1f}M'
    elif x >= 1e6:
        return f'Rp{x/1e6:.1f}M'
    else:
        return f'Rp{x:,.0f}'

# Buat folder plots jika belum ada
os.makedirs('plots', exist_ok=True)

def load_clean_data():
    """Load hanya data yang sudah clean (3 triwulan)"""
    print("📂 Loading clean data...")
    
    try:
        # Data YoY Growth
        df_yoy = pd.read_excel('data/PDRB_Jakarta_YoY.xlsx')
        df_yoy.columns = ['Komponen', 'Triwulan', 'Pertumbuhan']
        print(f"  ✅ YoY Data: {len(df_yoy)} rows, {df_yoy['Komponen'].unique()}")
        
        # Data Nilai
        df_nilai = pd.read_excel('data/PDRB_Jakarta_Nilai.xlsx')
        df_nilai.columns = ['Komponen', 'Triwulan', 'Nilai']
        print(f"  ✅ Nilai Data: {len(df_nilai)} rows")
        
        # Validasi data
        print(f"  📊 Triwulan tersedia: {df_nilai['Triwulan'].unique()}")
        print(f"  📊 Komponen tersedia: {df_nilai['Komponen'].unique()}")
        
        return df_yoy, df_nilai
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None, None

def create_6_complete_graphs():
    """Buat 6 grafik lengkap untuk laporan"""
    print("\n" + "="*60)
    print("🎨 MEMBUAT 6 GRAFIK LENGKAP UNTUK LAPORAN")
    print("="*60)
    
    # Load data
    df_yoy, df_nilai = load_clean_data()
    
    if df_nilai is None:
        print("❌ Tidak dapat melanjutkan, data tidak valid")
        return
    
    # ===============================
    # GRAFIK 1: TREN PDRB 2025
    # ===============================
    print("\n1. 📈 GRAFIK 1: Tren PDRB 2025")
    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Filter data PDRB
        pdrb_data = df_nilai[df_nilai['Komponen'] == 'PDRB'].copy()
        
        # Urutkan triwulan
        triwulan_order = {'Q1': 1, 'Q2': 2, 'Q3': 3}
        pdrb_data['Order'] = pdrb_data['Triwulan'].map(triwulan_order)
        pdrb_data = pdrb_data.sort_values('Order')
        
        # Bar chart dengan warna berbeda
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
        bars = ax.bar(range(len(pdrb_data)), pdrb_data['Nilai'], 
                     color=colors, alpha=0.8, width=0.6)
        
        # Tambahkan nilai di atas bar
        for i, (bar, row) in enumerate(zip(bars, pdrb_data.iterrows())):
            nilai = row[1]['Nilai']
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 5000,
                   f'Rp{nilai/1000:.1f}T', ha='center', va='bottom', fontsize=10)
            
            # Tambahkan pertumbuhan YoY jika ada
            growth_data = df_yoy[(df_yoy['Komponen'] == 'PDRB') & 
                                (df_yoy['Triwulan'] == row[1]['Triwulan'])]
            if not growth_data.empty:
                growth = growth_data.iloc[0]['Pertumbuhan']
                ax.text(bar.get_x() + bar.get_width()/2., height/2,
                       f'{growth}%', ha='center', va='center', 
                       fontsize=11, fontweight='bold', color='white')
        
        ax.set_title('PERKEMBANGAN PDRB DKI JAKARTA TAHUN 2025', 
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_ylabel('Nilai (Miliar Rupiah)', fontsize=12)
        ax.set_xlabel('Triwulan', fontsize=12)
        ax.set_xticks(range(len(pdrb_data)))
        ax.set_xticklabels(['Triwulan I', 'Triwulan II', 'Triwulan III'])
        ax.yaxis.set_major_formatter(FuncFormatter(format_rupiah))
        ax.grid(True, alpha=0.3, axis='y')
        
        # Tambahkan footer
        plt.figtext(0.5, 0.01, 'Sumber: BPS Provinsi DKI Jakarta 2025', 
                   ha='center', fontsize=9, style='italic')
        
        plt.tight_layout()
        plt.savefig('plots/GRAFIK_1_PDRB_TREND.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✅ Grafik 1: Tren PDRB berhasil dibuat")
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # ===============================
    # GRAFIK 2: KONSUMSI RUMAH TANGGA
    # ===============================
    print("\n2. 🏠 GRAFIK 2: Konsumsi Rumah Tangga")
    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Filter data Konsumsi RT
        konsumsi_data = df_nilai[df_nilai['Komponen'] == 'Konsumsi RT'].copy()
        konsumsi_data['Order'] = konsumsi_data['Triwulan'].map(triwulan_order)
        konsumsi_data = konsumsi_data.sort_values('Order')
        
        # Line chart dengan area
        ax.plot(konsumsi_data['Triwulan'], konsumsi_data['Nilai'], 
               marker='o', linewidth=3, markersize=10, color='#2ca02c', 
               markerfacecolor='white', markeredgewidth=2)
        
        # Isi area di bawah garis
        ax.fill_between(konsumsi_data['Triwulan'], konsumsi_data['Nilai'], 
                       alpha=0.2, color='#2ca02c')
        
        # Anotasi nilai
        for _, row in konsumsi_data.iterrows():
            ax.text(row['Triwulan'], row['Nilai'] + 1000, 
                   f'Rp{row["Nilai"]/1000:.1f}T', 
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
            
            # Tambahkan pertumbuhan
            growth = df_yoy[(df_yoy['Komponen'] == 'Konsumsi RT') & 
                           (df_yoy['Triwulan'] == row['Triwulan'])]
            if not growth.empty:
                ax.text(row['Triwulan'], row['Nilai'] * 0.9, 
                       f'{growth.iloc[0]["Pertumbuhan"]}% YoY', 
                       ha='center', va='top', fontsize=9, style='italic')
        
        ax.set_title('PERTUMBUHAN KONSUMSI RUMAH TANGGA DKI JAKARTA 2025', 
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_ylabel('Nilai (Miliar Rupiah)', fontsize=12)
        ax.set_xlabel('Triwulan', fontsize=12)
        ax.yaxis.set_major_formatter(FuncFormatter(format_rupiah))
        ax.grid(True, alpha=0.3)
        
        plt.figtext(0.5, 0.01, 'Sumber: BPS Provinsi DKI Jakarta 2025', 
                   ha='center', fontsize=9, style='italic')
        
        plt.tight_layout()
        plt.savefig('plots/GRAFIK_2_KONSUMSI_RT.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✅ Grafik 2: Konsumsi RT berhasil dibuat")
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # ===============================
    # GRAFIK 3: PMTB (INVESTASI)
    # ===============================
    print("\n3. 🏗️ GRAFIK 3: PMTB (Investasi Fisik)")
    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Filter data PMTB
        pmtb_data = df_nilai[df_nilai['Komponen'] == 'PMTB'].copy()
        pmtb_data['Order'] = pmtb_data['Triwulan'].map(triwulan_order)
        pmtb_data = pmtb_data.sort_values('Order')
        
        # Bar chart dengan gradient warna
        colors = ['#d62728', '#9467bd', '#8c564b']
        bars = ax.bar(range(len(pmtb_data)), pmtb_data['Nilai'], 
                     color=colors, alpha=0.8, width=0.6)
        
        # Anotasi
        for i, (bar, row) in enumerate(zip(bars, pmtb_data.iterrows())):
            nilai = row[1]['Nilai']
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 5000,
                   f'Rp{nilai/1000:.1f}T', ha='center', va='bottom', fontsize=10)
            
            # Growth annotation
            growth = df_yoy[(df_yoy['Komponen'] == 'PMTB') & 
                           (df_yoy['Triwulan'] == row[1]['Triwulan'])]
            if not growth.empty:
                growth_val = growth.iloc[0]['Pertumbuhan']
                color = 'green' if growth_val > 0 else 'red'
                ax.text(bar.get_x() + bar.get_width()/2., height/2,
                       f'↑ {growth_val}%' if growth_val > 0 else f'↓ {abs(growth_val)}%',
                       ha='center', va='center', fontsize=11, 
                       fontweight='bold', color=color)
        
        ax.set_title('TREN PEMBENTUKAN MODAL TETAP BRUTO (PMTB) DKI JAKARTA 2025', 
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_ylabel('Nilai (Miliar Rupiah)', fontsize=12)
        ax.set_xlabel('Triwulan', fontsize=12)
        ax.set_xticks(range(len(pmtb_data)))
        ax.set_xticklabels(['Triwulan I', 'Triwulan II', 'Triwulan III'])
        ax.yaxis.set_major_formatter(FuncFormatter(format_rupiah))
        ax.grid(True, alpha=0.3, axis='y')
        
        # Trend line
        x_numeric = range(len(pmtb_data))
        if len(pmtb_data) >= 2:
            z = np.polyfit(x_numeric, pmtb_data['Nilai'], 1)
            p = np.poly1d(z)
            ax.plot(x_numeric, p(x_numeric), "r--", alpha=0.8, linewidth=2, 
                   label='Trend Line')
            ax.legend()
        
        plt.figtext(0.5, 0.01, 'Sumber: BPS Provinsi DKI Jakarta 2025', 
                   ha='center', fontsize=9, style='italic')
        
        plt.tight_layout()
        plt.savefig('plots/GRAFIK_3_PMTB_TREND.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✅ Grafik 3: PMTB berhasil dibuat")
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # ===============================
    # GRAFIK 4: PERBANDINGAN YOY
    # ===============================
    print("\n4. 📊 GRAFIK 4: Perbandingan Pertumbuhan YoY")
    try:
        fig, ax = plt.subplots(figsize=(12, 7))
        
        # Komponen untuk ditampilkan
        components = ['Konsumsi RT', 'Konsumsi Pemerintah', 'PMTB', 'PDRB']
        filtered_yoy = df_yoy[df_yoy['Komponen'].isin(components)].copy()
        
        # Pivot untuk grouped bar
        pivot_data = filtered_yoy.pivot(index='Komponen', columns='Triwulan', values='Pertumbuhan')
        
        # Pastikan urutan kolom
        pivot_data = pivot_data[['Q1', 'Q2', 'Q3']]
        
        # Plot grouped bar
        x = np.arange(len(pivot_data.columns))
        width = 0.18
        
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        for i, komponen in enumerate(pivot_data.index):
            offset = width * i
            values = pivot_data.loc[komponen].values
            
            bars = ax.bar(x + offset, values, width, label=komponen, 
                         alpha=0.8, color=colors[i])
            
            # Anotasi nilai
            for j, v in enumerate(values):
                if not np.isnan(v):
                    ax.text(x[j] + offset, v + 0.3, f'{v:.1f}%', 
                           ha='center', va='bottom', fontsize=9)
        
        ax.set_title('LAJU PERTUMBUHAN EKONOMI DKI JAKARTA (YoY) 2025', 
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_ylabel('Pertumbuhan (%)', fontsize=12)
        ax.set_xlabel('Triwulan', fontsize=12)
        ax.set_xticks(x + width * (len(components) - 1) / 2)
        ax.set_xticklabels(['Triwulan I', 'Triwulan II', 'Triwulan III'])
        ax.legend(title='Komponen Ekonomi', bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, alpha=0.3, axis='y')
        ax.axhline(y=0, color='black', linewidth=0.5)
        
        # Highlight pertumbuhan tertinggi
        max_growth = pivot_data.max().max()
        if max_growth > 0:
            ax.axhline(y=max_growth, color='red', linestyle=':', alpha=0.5, 
                      label=f'Max: {max_growth:.1f}%')
        
        plt.figtext(0.5, 0.01, 'Sumber: BPS Provinsi DKI Jakarta 2025 | Year-on-Year Growth', 
                   ha='center', fontsize=9, style='italic')
        
        plt.tight_layout()
        plt.savefig('plots/GRAFIK_4_YOY_COMPARISON.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✅ Grafik 4: Perbandingan YoY berhasil dibuat")
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # ===============================
    # GRAFIK 5: KOMPOSISI PDRB
    # ===============================
    print("\n5. 🥧 GRAFIK 5: Komposisi PDRB Triwulan III")
    try:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Data untuk Triwulan III (asumsi Q3 adalah triwulan terakhir)
        q3_data = df_nilai[df_nilai['Triwulan'] == 'Q3'].copy()
        
        if len(q3_data) > 0:
            # 1. PIE CHART: Komposisi utama
            main_comps = ['Konsumsi RT', 'PMTB']
            pie_data = q3_data[q3_data['Komponen'].isin(main_comps)]
            
            if len(pie_data) > 0:
                # Hitung persentase
                total = pie_data['Nilai'].sum()
                percentages = (pie_data['Nilai'] / total * 100).round(1)
                
                # Plot pie chart
                wedges, texts, autotexts = ax1.pie(
                    pie_data['Nilai'], 
                    labels=[f'{k}\n({p}%)' for k, p in zip(pie_data['Komponen'], percentages)],
                    autopct='',  # Manual label di atas
                    startangle=90,
                    colors=['#ff9999', '#66b3ff'],
                    explode=(0.05, 0.05),
                    shadow=True
                )
                
                # Style teks
                for text in texts:
                    text.set_fontsize(10)
                    text.set_fontweight('bold')
                
                ax1.set_title('KOMPOSISI PDRB DKI JAKARTA\nTRIWULAN III 2025', 
                             fontsize=14, fontweight='bold', pad=20)
                ax1.axis('equal')  # Equal aspect ratio untuk circular pie
            
            # 2. BAR CHART: Perbandingan semua triwulan
            comps_to_compare = ['Konsumsi RT', 'PMTB']
            bar_data = df_nilai[df_nilai['Komponen'].isin(comps_to_compare)].copy()
            
            if len(bar_data) > 0:
                # Urutkan
                bar_data['Order'] = bar_data['Triwulan'].map(triwulan_order)
                bar_data = bar_data.sort_values(['Komponen', 'Order'])
                
                # Pivot untuk grouped bar
                pivot_bar = bar_data.pivot(index='Triwulan', columns='Komponen', values='Nilai')
                pivot_bar = pivot_bar.reindex(['Q1', 'Q2', 'Q3'])
                
                x = np.arange(len(pivot_bar))
                width = 0.35
                
                # Plot grouped bars
                rects1 = ax2.bar(x - width/2, pivot_bar['Konsumsi RT'], 
                                width, label='Konsumsi RT', color='#ff9999', alpha=0.8)
                rects2 = ax2.bar(x + width/2, pivot_bar['PMTB'], 
                                width, label='PMTB', color='#66b3ff', alpha=0.8)
                
                # Anotasi
                def autolabel(rects):
                    for rect in rects:
                        height = rect.get_height()
                        ax2.text(rect.get_x() + rect.get_width()/2., height + 0.02*max(pivot_bar.max()),
                                f'Rp{height/1000:.1f}T', ha='center', va='bottom', fontsize=9)
                
                autolabel(rects1)
                autolabel(rects2)
                
                ax2.set_title('PERBANDINGAN KOMPONEN UTAMA\nPER TRIWULAN', 
                             fontsize=14, fontweight='bold', pad=20)
                ax2.set_ylabel('Nilai (Miliar Rupiah)', fontsize=11)
                ax2.set_xlabel('Triwulan', fontsize=11)
                ax2.set_xticks(x)
                ax2.set_xticklabels(['Triwulan I', 'Triwulan II', 'Triwulan III'])
                ax2.legend()
                ax2.yaxis.set_major_formatter(FuncFormatter(format_rupiah))
                ax2.grid(True, alpha=0.3, axis='y')
        
        plt.figtext(0.5, 0.01, 'Sumber: BPS Provinsi DKI Jakarta 2025', 
                   ha='center', fontsize=9, style='italic')
        
        plt.tight_layout()
        plt.savefig('plots/GRAFIK_5_KOMPOSISI_PDRB.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✅ Grafik 5: Komposisi PDRB berhasil dibuat")
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # ===============================
    # GRAFIK 6: KONSUMSI PEMERINTAH
    # ===============================
    print("\n6. 🏛️ GRAFIK 6: Konsumsi Pemerintah")
    try:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # 1. Bar Chart: Nilai Konsumsi Pemerintah
        gov_data = df_nilai[df_nilai['Komponen'] == 'Konsumsi Pemerintah']
        if len(gov_data) == 0:
            # Coba cari di data YoY
            gov_growth = df_yoy[df_yoy['Komponen'] == 'Konsumsi Pemerintah']
            if len(gov_growth) > 0:
                # Buat bar chart dari growth data
                bars1 = ax1.bar(gov_growth['Triwulan'], gov_growth['Pertumbuhan'],
                              color=['#3498db', '#9b59b6', '#e74c3c'], alpha=0.8)
                
                for bar, growth in zip(bars1, gov_growth['Pertumbuhan']):
                    height = bar.get_height()
                    ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                            f'{growth:.1f}%', ha='center', va='bottom', 
                            fontsize=11, fontweight='bold')
                
                ax1.set_title('PERTUMBUHAN KONSUMSI PEMERINTAH (YoY)', 
                             fontsize=13, fontweight='bold')
                ax1.set_ylabel('Pertumbuhan (%)', fontsize=11)
                ax1.set_xlabel('Triwulan', fontsize=11)
                ax1.grid(True, alpha=0.3, axis='y')
        
        # 2. Perbandingan dengan komponen lain
        comps_for_radar = ['Konsumsi RT', 'Konsumsi Pemerintah', 'PMTB']
        q3_comparison = df_nilai[(df_nilai['Triwulan'] == 'Q3') & 
                                (df_nilai['Komponen'].isin(comps_for_radar))]
        
        if len(q3_comparison) > 0:
            # Normalisasi untuk radar chart (0-100)
            max_val = q3_comparison['Nilai'].max()
            normalized = (q3_comparison['Nilai'] / max_val * 100).round(1)
            
            # Bar chart comparison
            bars2 = ax2.bar(q3_comparison['Komponen'], normalized, 
                           color=['#2ca02c', '#3498db', '#d62728'], alpha=0.8)
            
            for bar, norm_val, actual_val in zip(bars2, normalized, q3_comparison['Nilai']):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height + 2,
                        f'Rp{actual_val/1000:.1f}T\n({norm_val:.0f}%)', 
                        ha='center', va='bottom', fontsize=9)
            
            ax2.set_title('PERBANDINGAN NILAI TRIWULAN III\n(Indexed to Max Value)', 
                         fontsize=13, fontweight='bold')
            ax2.set_ylabel('Index (%, max=100)', fontsize=11)
            ax2.set_xlabel('Komponen', fontsize=11)
            ax2.grid(True, alpha=0.3, axis='y')
            ax2.set_ylim(0, 110)
        
        plt.figtext(0.5, 0.01, 'Sumber: BPS Provinsi DKI Jakarta 2025 | Triwulan III 2025', 
                   ha='center', fontsize=9, style='italic')
        
        plt.suptitle('ANALISIS KONSUMSI PEMERINTAH DKI JAKARTA', 
                    fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig('plots/GRAFIK_6_KONSUMSI_PEMERINTAH.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✅ Grafik 6: Konsumsi Pemerintah berhasil dibuat")
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    print("\n" + "="*60)
    print("🎉 SELESAI! 6 GRAFIK TELAH DIBUAT:")
    print("="*60)
    print("1. 📈 GRAFIK_1_PDRB_TREND.png")
    print("2. 🏠 GRAFIK_2_KONSUMSI_RT.png")
    print("3. 🏗️ GRAFIK_3_PMTB_TREND.png")
    print("4. 📊 GRAFIK_4_YOY_COMPARISON.png")
    print("5. 🥧 GRAFIK_5_KOMPOSISI_PDRB.png")
    print("6. 🏛️ GRAFIK_6_KONSUMSI_PEMERINTAH.png")
    print("\n✅ Semua grafik tersimpan di folder 'plots/'")
    print("✅ Siap untuk dimasukkan ke dalam laporan!")

if __name__ == "__main__":
    print("🚀 MEMULAI GENERASI 6 GRAFIK LENGKAP")
    print("="*60)
    create_6_complete_graphs()