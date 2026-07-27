import streamlit as st

# Tetapan halaman dan reka bentuk lebar penuh
st.set_page_config(page_title="RISDA RoU Financial Dashboard", layout="wide")

# --- CUSTOM CSS UNTUK PAPARAN KORPORAT KP ---
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    h1 {
        color: #064e3b !important;
        font-weight: 800 !important;
        font-size: 2.3rem !important;
    }
    div[data-testid="metric-container"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        padding: 16px 20px !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
        border-left: 5px solid #047857 !important;
        transition: transform 0.2s ease-in-out;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        color: #1e293b !important;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        color: #64748b !important;
        text-transform: uppercase;
    }
    .negatif-box {
        background-color: #fef2f2 !important;
        border-left: 5px solid #ef4444 !important;
    }
    hr {
        margin-top: 1.2rem !important;
        margin-bottom: 1.2rem !important;
        border-top: 1px solid #cbd5e1 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Tajuk Utama
st.title("📊 Dashboard Analisis & Rundingan RoU RISDA")
st.caption("Alat Simulasi Dinamik Strategi Rundingan Kadar Sewaan Estet & Penilaian Impak Kewangan KP")
st.markdown("---")

# --- SIDEBAR: PARAMETER PASARAN GLOBAL ---
st.sidebar.header("⚙️ Parameter Pasaran Global")

harga_smr20 = st.sidebar.slider("Harga SMR 20 (sen/kg)", 500, 1200, 790)
insentif_risda = st.sidebar.slider("Insentif RISDA (sen/kg)", 0, 200, 100)
diskaun_kilang = st.sidebar.slider("Kos Pemprosesan/Diskaun (sen/kg)", 50, 200, 130)
kos_opex_gc = st.sidebar.slider("Kos Operasi + GC (RM/Ha/Tahun)", 5000, 12000, 7000)

# Pengiraan Harga Bersih SMR 20 (RM/kg)
harga_clean_rm = (harga_smr20 + insentif_risda - diskaun_kilang) / 100

st.sidebar.markdown("---")
st.sidebar.subheader("💰 Unjuran Pasaran")
st.sidebar.metric(label="Harga Bersih SMR 20", value=f"RM {harga_clean_rm:.2f}/kg")

if harga_clean_rm < 6.00:
    st.sidebar.error("⚠️ KLAUSA PENURUNAN SEWA: Harga bersih bawah RM6.00/kg. Disyorkan potongan sewa 20%.")

# --- FUNGSI PENGIRAAN KEWANGAN DINAMIK ---
def kira_metrik_kewangan(untung_tahunan, kadar_sewa, keluasan, tempoh_tahun):
    modal_terikat = kadar_sewa * keluasan
    if modal_terikat <= 0 or untung_tahunan <= 0:
        return modal_terikat, 0.0, 0.0, 0.0
    irr = (untung_tahunan / modal_terikat) * 100
    roi = irr * tempoh_tahun
    aliran_tunai = [-modal_terikat] + [untung_tahunan] * tempoh_tahun
    npv = sum([cf / (1.10**t) for t, cf in enumerate(aliran_tunai)])
    return modal_terikat, npv, irr, roi

# --- STRUKTUR 3 TAB UTAMA ---
tab1, tab2, tab3 = st.tabs([
    "🛠️ Tab 1: Simulator Estet Dinamik (Bebas Hektar)", 
    "🌳 Tab 2: Anjakan Wawasan (Analisis Pakej 1, 2 & 3)", 
    "🌟 Tab 3: Anjakan Wawasan (Konsolidasi 5,787 Ha & Rundingan KP)"
])

# ==========================================
# TAB 1: SIMULATOR ESTET DINAMIK (BEBAS HEKTAR)
# ==========================================
with tab1:
    st.header("🛠️ Simulator Estet Dinamik (Alat Rundingan Generik)")
    st.info("💡 Gunakan simulator ini untuk mana-mana estet swasta. Pilih preset atau laraskan luas hektar dan kadar sewa secara live semasa berunding.")
    
    col_preset, col_space = st.columns([1, 2])
    with col_preset:
        preset_choice = st.selectbox("📌 Pilih Preset Estet / Custom:", [
            "Custom (Simulasi Bebas)",
            "Tropika Sanjung (257 Ha)",
            "Sri Pelita Bumi (344 Ha)"
        ])
    
    # Preset Values
    if preset_choice == "Tropika Sanjung (257 Ha)":
        default_ha, default_prod, default_sewa = 257, 700, 1200
    elif preset_choice == "Sri Pelita Bumi (344 Ha)":
        default_ha, default_prod, default_sewa = 344, 1113, 1800
    else:
        default_ha, default_prod, default_sewa = 1000, 1500, 2000

    col_in, col_eff = st.columns([1, 2])
    
    with col_in:
        st.subheader("📋 Input Parametrik Rundingan")
        hektar_sim = st.slider("Keluasan Estet (Hektar)", 10, 10000, default_ha, key="sim_h")
        tempoh_sim = st.slider("Tempoh Pajakan RoU (Tahun)", 1, 20, 6, key="sim_t")
        prod_sim = st.slider("Produktiviti Hasil (kg/Ha/Tahun)", 400, 2500, default_prod, key="sim_p")
        sewa_sim = st.slider("Kadar Sewaan Rundingan (RM/Ha/Tahun)", 500, 4000, default_sewa, key="sim_s")
        
        jum_sewa_sim = sewa_sim * hektar_sim * tempoh_sim
        jum_opex_sim = kos_opex_gc * hektar_sim * tempoh_sim
        
        pendapatan_tahunan_sim = prod_sim * harga_clean_rm * hektar_sim
        kos_tahunan_sim = (kos_opex_gc + sewa_sim) * hektar_sim
        untung_tahunan_sim = pendapatan_tahunan_sim - kos_tahunan_sim
        
        jum_untung_sim = untung_tahunan_sim * tempoh_sim
        jum_modal_sim = jum_opex_sim + jum_sewa_sim
        kadar_untung_modal_sim = (jum_untung_sim / jum_modal_sim * 100) if jum_modal_sim > 0 else 0
        
        modal_sim, npv_sim, irr_sim, roi_sim = kira_metrik_kewangan(untung_tahunan_sim, sewa_sim, hektar_sim, tempoh_sim)

    with col_eff:
        st.subheader("💼 Penunjuk Prestasi Kewangan (KPI Rundingan)")
        
        r1_1, r1_2 = st.columns(2)
        if jum_untung_sim < 0:
            r1_1.error(f"Untung Bersih ({tempoh_sim} Thn): RM {jum_untung_sim:,.0f}")
        else:
            r1_1.metric(f"Untung Bersih ({tempoh_sim} Thn)", f"RM {jum_untung_sim:,.0f}")
            
        r1_2.metric("Pulangan Atas Kos/Modal (%)", f"{kadar_untung_modal_sim:.2f}%")
        
        st.markdown("---")
        r2_1, r2_2 = st.columns(2)
        r2_1.metric(f"Jumlah Kos Operasi+GC ({tempoh_sim} Thn)", f"RM {jum_opex_sim:,.0f}")
        r2_2.metric(f"Jumlah Komitmen Sewa ({tempoh_sim} Thn)", f"RM {jum_sewa_sim:,.0f}")
        
        st.markdown("---")
        r3_1, r3_2, r3_3 = st.columns(3)
        r3_1.metric("NPV (@10%)", f"RM {npv_sim:,.0f}")
        r3_2.metric("IRR (%)", f"{irr_sim:.2f}%")
        r3_3.metric("ROI (%)", f"{roi_sim:.2f}%")
        
        st.markdown("---")
        if untung_tahunan_sim < 0:
            st.error("🚨 ZON MERAH (PROJEK RUGI): Kadar sewa terlalu tinggi atau produktiviti rendah! KP disyorkan minta penurunan kadar sewa.")
        elif sewa_sim > 2400:
            st.warning("⚠️ AMARAN SILING SEWA: Kadar sewa melebihi RM2,400/Ha. Margin risiko agensi tinggi jika harga komoditi jatuh.")
        else:
            st.success("✅ ZON HIJAU (VIABLE): Cadangan kadar sewa berada dalam julat selamat untuk dipersetujui.")

# ==========================================
# TAB 2: ANJAKAN WAWASAN (PAKEJ INDIVIDU)
# ==========================================
with tab2:
    st.header("🌳 Ladang Anjakan Wawasan - Analisis Mengikut Pakej")
    
    pakej_choice = st.radio("Pilih Pakej Unjuran:", [
        "Pakej 1: Getah Matang Tua (2,300 Ha)",
        "Pakej 2: Getah Muda (2,337 Ha)",
        "Pakej 3: Semula Sawit (1,550 Ha)"
    ], horizontal=True)
    
    col_in_p, col_eff_p = st.columns([1, 2])
    
    with col_in_p:
        st.subheader("📋 Tetapan Kadar Sewa Rundingan")
        tempoh_p = st.slider("Tempoh Analisis (Tahun)", 1, 25, 9, key="p_t")
        
        if "Pakej 1" in pakej_choice:
            st.caption("📌 Status: Matang Tua (1,500 kg/Ha). Keuntungan stabil pada dekad pertama.")
            sewa_p = st.slider("Kadar Sewa P1 (RM/Ha/Tahun)", 1200, 3500, 2300, key="p1_s")
            prod_p = 1500
            ha_p = 2300
            capex_p = 0
        elif "Pakej 2" in pakej_choice:
            st.caption("📌 Status: Getah Muda. Rundingan sewa diskaun 3 tahun pertama (RM1,200).")
            sewa_p = st.slider("Kadar Sewa P2 (RM/Ha/Tahun)", 1000, 3000, 1200 if tempoh_p <= 3 else 2300, key="p2_s")
            prod_p = 974 if tempoh_p <= 3 else 1450
            ha_p = 2337
            capex_p = 0
        else:
            st.caption("📌 Status: Tanam Semula Sawit (GUHA). Capex RM11J setahun pada 3 tahun pertama.")
            sewa_p = st.slider("Kadar Sewa P3 (RM/Ha/Tahun)", 300, 1500, 500, key="p3_s")
            prod_p = 0
            ha_p = 1550
            capex_p = 11000000 if tempoh_p <= 3 else 0
            
        rev_p = (prod_p * harga_clean_rm * ha_p) if "Pakej 3" not in pakej_choice else (ha_p * 10 * 200 if tempoh_p > 3 else 0)
        cost_p = ((kos_opex_gc + sewa_p) * ha_p) + capex_p
        profit_p = rev_p - cost_p
        
        jum_untung_p = profit_p * tempoh_p
        jum_sewa_p = sewa_p * ha_p * tempoh_p
        jum_opex_p = (kos_opex_gc * ha_p * tempoh_p) + (capex_p * min(tempoh_p, 3))
        jum_modal_p = jum_opex_p + jum_sewa_p
        kadar_untung_modal_p = (jum_untung_p / jum_modal_p * 100) if jum_modal_p > 0 else 0

    with col_eff_p:
        st.subheader("💼 Penunjuk Prestasi Kewangan Pakej")
        p1, p2 = st.columns(2)
        if jum_untung_p < 0:
            p1.error(f"Untung/Rugi ({tempoh_p} Thn): RM {jum_untung_p:,.0f}")
        else:
            p1.metric(f"Untung Bersih ({tempoh_p} Thn)", f"RM {jum_untung_p:,.0f}")
            
        p2.metric("Pulangan Atas Kos/Modal (%)", f"{kadar_untung_modal_p:.2f}%")
        
        st.markdown("---")
        p3, p4 = st.columns(2)
        p3.metric(f"Kos Operasi + Capex ({tempoh_p} Thn)", f"RM {jum_opex_p:,.0f}")
        p4.metric(f"Jumlah Komitmen Sewa ({tempoh_p} Thn)", f"RM {jum_sewa_p:,.0f}")

# ==========================================
# TAB 3: ANJAKAN WAWASAN (KONSOLIDASI 5,787 HA)
# ==========================================
with tab3:
    st.header("🌟 Anjakan Wawasan - Konsolidasi Keseluruhan 5,787 Ha")
    st.info("💡 Pandangan Portfolio Keseluruhan. Gunakan ini untuk menunjukkan kepada syarikat swasta bagaimana Pakej 1 menyerap defisit Pakej 3 (Subsidi Silang).")
    
    fasa_view = st.selectbox("Pilih Perspektif Masa Rundingan:", [
        "Tahun 1-3: Fasa Awalan & Defisit Capex Sawit",
        "Tahun 1-9: Fasa RoU Pertengahan (3+3+3) - ZON KEEMASAN",
        "Tahun 1-25: Kitaran Hayat Penuh 25 Tahun"
    ])
    
    # Data Konsolidasi Berdasarkan Slaid Dokumen
    if "Tahun 1-3" in fasa_view:
        untung_lantai = -11800000
        untung_siling = -19090000
        rev_tot = 188730000
        cost_tot = 200530000
        alert_msg = "🚨 FASA DEFISIT TUNAI: Penumpuan CAPEX Sawit RM11J/Thn. KP perlu pastikan sewa Pakej 3 kekal RM500/Ha!"
        alert_type = "error"
    elif "Tahun 1-9" in fasa_view:
        untung_lantai = 12230000
        untung_siling = 7880000
        rev_tot = 580000000
        cost_tot = 567770000
        alert_msg = "💰 ZON KEEMASAN (3+3+3): Unjuran Pukal 9 Tahun untung RM12.23J (Lantai). Fasa terbaik untuk dimuktamadkan!"
        alert_type = "success"
    else:
        untung_lantai = 68760000
        untung_siling = 8900000
        rev_tot = 1249070000
        cost_tot = 1180310000
        alert_msg = "📈 KITARAN PENUH 25 TAHUN: Projek sangat berdaya saing dengan Untung Pukal RM68.76 Juta (Kadar Lantai)."
        alert_type = "info"

    col_k1, col_k2 = st.columns(2)
    with col_k1:
        st.subheader("📊 Prestasi Kadar LANTAI (Floor)")
        st.metric("Untung Bersih Pukal Fasa", f"RM {untung_lantai:,.0f}")
        st.metric("NPV (@10% Diskaun)", "RM 3.92 Juta" if untung_lantai > 0 else "-RM 4.12 Juta")
        st.metric("ROI Keseluruhan", "17.01%" if untung_lantai > 0 else "-5.20%")
        
    with col_k2:
        st.subheader("📊 Prestasi Kadar SILING (Ceiling)")
        st.metric("Untung Bersih Pukal Fasa", f"RM {untung_siling:,.0f}")
        st.metric("NPV (@10% Diskaun)", "RM 1.25 Juta" if untung_siling > 0 else "-RM 8.40 Juta")
        st.metric("ROI Keseluruhan", "10.34%" if untung_siling > 0 else "-9.10%")

    st.markdown("---")
    
    if alert_type == "error":
        st.error(alert_msg)
    elif alert_type == "success":
        st.success(alert_msg)
    else:
        st.info(alert_msg)
        
    st.subheader("💡 Nota Strategi Rundingan KP (Batu Penanda / Trade-off):")
    st.markdown("""
    * **Strategi Pakej 3 (Sawit):** Pertahankan sewa **RM500 – RM800/Ha**. Jika syarikat swasta minta RM1,500/Ha, tunjukkan bahawa aliran tunai Tahun 1–3 akan defisit melebihi RM20 Juta.
    * **Strategi Pakej 2 (Getah Muda):** Guna formula sewa bertingkat ($3+3+3$). Tahun 1–3 minta diskaun **RM1,200/Ha**, dan naik ke **RM2,300/Ha** pada Tahun 4 selepas hasil pokok melepasi $1,200\text{ kg/Ha}$.
    * **Subsidi Silang:** Keuntungan Pakej 1 (Getah Matang) sekitar **RM3.79J setahun** adalah 'perisai' untuk menampung kos pembangunan awal Pakej 3.
    """)
