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

# --- FUNGSI PENGIRAAN KEWANGAN DINAMIK METRIK ---
def kira_metrik_lengkap(aliran_untung_tahunan, jumlah_modal_terikat, tempoh_tahun):
    jum_untung = sum(aliran_untung_tahunan)
    kadar_pulangan_modal = (jum_untung / jumlah_modal_terikat * 100) if jumlah_modal_terikat > 0 else 0
    
    # Kira NPV & IRR
    aliran_tunai = [-jumlah_modal_terikat / tempoh_tahun] + aliran_untung_tahunan
    npv = sum([cf / (1.10**t) for t, cf in enumerate(aliran_tunai)])
    
    # Anggaran IRR & ROI
    purata_untung = jum_untung / tempoh_tahun if tempoh_tahun > 0 else 0
    irr = (purata_untung / (jumlah_modal_terikat / tempoh_tahun) * 100) if jumlah_modal_terikat > 0 else 0
    roi = irr * tempoh_tahun
    
    return jum_untung, kadar_pulangan_modal, npv, irr, roi

# --- STRUKTUR 3 TAB UTAMA ---
tab1, tab2, tab3 = st.tabs([
    "🛠️ Tab 1: Simulator Estet Dinamik (Bebas Hektar)", 
    "🌳 Tab 2: Anjakan Wawasan (Pakej Getah 5,787 Ha)", 
    "🌟 Tab 3: Anjakan Wawasan (Sawit & Konsolidasi 5,787 Ha)"
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
        
        aliran_untung_sim = [untung_tahunan_sim] * tempoh_sim
        jum_modal_sim = jum_opex_sim + jum_sewa_sim
        
        jum_untung_sim, kadar_untung_modal_sim, npv_sim, irr_sim, roi_sim = kira_metrik_lengkap(
            aliran_untung_sim, jum_modal_sim, tempoh_sim
        )

    with col_eff:
        st.subheader("💼 Penunjuk Prestasi Kewangan (KPI Rundingan)")
        
        r1_1, r1_2 = st.columns(2)
        if jum_untung_sim < 0:
            r1_1.error(f"Rugi Bersih ({tempoh_sim} Thn): -RM {abs(jum_untung_sim):,.0f}")
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
# TAB 2: ANJAKAN WAWASAN (PAKEJ GETAH SAHAJA)
# ==========================================
with tab2:
    st.header("🌳 Ladang Anjakan Wawasan - Portfolio Getah")
    st.info("📌 Khas Analisis Getah: Pilih Pakej 1 (2,300 Ha), Pakej 2 (3,487 Ha) atau Gabungan Getah (5,787 Ha). Mengandungi tangga sewa bertingkat (3+3+3).")
    
    pakej_choice = st.radio("Pilih Pakej Getah:", [
        "Pakej 1: Getah Matang Tua (2,300 Ha)",
        "Pakej 2: Getah Muda / Pra-Matang (3,487 Ha)",
        "Gabungan Pakej 1 + Pakej 2 (5,787 Ha Keseluruhan Getah)"
    ], horizontal=True)
    
    col_in_p, col_eff_p = st.columns([1, 2])
    
    with col_in_p:
        st.subheader("📋 Tetapan Kadar Sewa Bertingkat")
        tempoh_p = st.slider("Tempoh Unjuran (Tahun)", 1, 25, 9, key="p_t")
        
        # Slider Kadar Sewa mengikut Pakej
        if "Pakej 1" in pakej_choice and "Gabungan" not in pakej_choice:
            st.caption("📌 Status P1: Matang Tua. Hasil stabil 1,450 - 1,500 kg/Ha.")
            sewa_p1_val = st.slider("Kadar Sewa Pakej 1 (RM/Ha/Tahun)", 1200, 3500, 2300, key="p1_only_s")
            sewa_p2_f1_val, sewa_p2_f2_val = 1200, 2300
        elif "Pakej 2" in pakej_choice and "Gabungan" not in pakej_choice:
            st.caption("📌 Status P2: Muda. Sewa bertingkat Fasa 1 (Tahun 1-3) vs Fasa 2 (Tahun 4+).")
            sewa_p2_f1_val = st.slider("Sewa Diskaun Fasa 1 - Thn 1-3 (RM/Ha)", 500, 2000, 1200, key="p2_s1")
            sewa_p2_f2_val = st.slider("Sewa Penuh Fasa 2 - Thn 4+ (RM/Ha)", 1500, 3500, 2300, key="p2_s2")
            sewa_p1_val = 2300
        else: # Gabungan
            st.caption("📌 Gabungan P1 + P2 (5,787 Ha Getah Keseluruhan).")
            sewa_p1_val = st.slider("Kadar Sewa Pakej 1 (RM/Ha)", 1200, 3500, 2300, key="p_gab_s1")
            sewa_p2_f1_val = st.slider("Sewa Pakej 2 (Thn 1-3) RM/Ha", 500, 2000, 1200, key="p_gab_s2_f1")
            sewa_p2_f2_val = st.slider("Sewa Pakej 2 (Thn 4+) RM/Ha", 1500, 3500, 2300, key="p_gab_s2_f2")

        # LOGIK PENGIRAAN GELUNG TAHUN DEMI TAHUN GETAH
        aliran_untung_p = []
        total_sewa_p = 0
        total_opex_capex_p = 0
        
        for t in range(1, tempoh_p + 1):
            untung_t = 0
            sewa_t = 0
            opex_capex_t = 0
            
            # --- PAKEJ 1 (2,300 Ha) ---
            if "Pakej 1" in pakej_choice or "Gabungan" in pakej_choice:
                ha_1 = 2300
                if t <= 10:
                    prod_1 = 1450
                    sewa_1 = sewa_p1_val * ha_1
                    opex_1 = kos_opex_gc * ha_1
                    rev_1 = prod_1 * harga_clean_rm * ha_1
                elif 11 <= t <= 15: # Tanam Semula P1
                    sewa_1 = 500 * ha_1
                    opex_1 = 17480000 # Capex + Opex Tanam Semula
                    rev_1 = 0
                else: # Pulih Tanam Semula
                    prod_1 = 835 if t == 16 else (974 if t == 17 else 1450)
                    sewa_1 = 1200 * ha_1 if t <= 18 else sewa_p1_val * ha_1
                    opex_1 = kos_opex_gc * ha_1
                    rev_1 = prod_1 * harga_clean_rm * ha_1
                    
                untung_t += (rev_1 - (opex_1 + sewa_1))
                sewa_t += sewa_1
                opex_capex_t += opex_1

            # --- PAKEJ 2 (3,487 Ha) ---
            if "Pakej 2" in pakej_choice or "Gabungan" in pakej_choice:
                ha_2 = 3487
                if t <= 3: # Fasa Diskaun
                    prod_2 = 835 if t == 1 else (974 if t == 2 else 1105)
                    sewa_2 = sewa_p2_f1_val * ha_2
                    opex_2 = kos_opex_gc * ha_2
                    rev_2 = prod_2 * harga_clean_rm * ha_2
                elif 4 <= t <= 18: # Fasa Matang Penuh
                    prod_2 = 1450
                    sewa_2 = sewa_p2_f2_val * ha_2
                    opex_2 = kos_opex_gc * ha_2
                    rev_2 = prod_2 * harga_clean_rm * ha_2
                else: # Fasa Tanam Semula P2 (Thn 19+)
                    sewa_2 = 500 * ha_2
                    opex_2 = 19860000 # Capex + Opex
                    rev_2 = 0
                    
                untung_t += (rev_2 - (opex_2 + sewa_2))
                sewa_t += sewa_2
                opex_capex_t += opex_2

            aliran_untung_p.append(untung_t)
            total_sewa_p += sewa_t
            total_opex_capex_p += opex_capex_t

        # Panggilan Fungsi Metrik
        total_modal_p = total_opex_capex_p + total_sewa_p
        jum_untung_p, kadar_untung_modal_p, npv_p, irr_p, roi_p = kira_metrik_lengkap(
            aliran_untung_p, total_modal_p, tempoh_p
        )

    with col_eff_p:
        st.subheader("💼 Penunjuk Prestasi Kewangan Getah (KPI)")
        
        p1, p2 = st.columns(2)
        if jum_untung_p < 0:
            p1.error(f"Rugi Bersih ({tempoh_p} Thn): -RM {abs(jum_untung_p):,.0f}")
        else:
            p1.metric(f"Untung Bersih ({tempoh_p} Thn)", f"RM {jum_untung_p:,.0f}")
            
        p2.metric("Pulangan Atas Kos/Modal (%)", f"{kadar_untung_modal_p:.2f}%")
        
        st.markdown("---")
        p3, p4 = st.columns(2)
        p3.metric(f"Kos Operasi + Capex ({tempoh_p} Thn)", f"RM {total_opex_capex_p:,.0f}")
        p4.metric(f"Jumlah Komitmen Sewa ({tempoh_p} Thn)", f"RM {total_sewa_p:,.0f}")
        
        st.markdown("---")
        p5, p6, p7 = st.columns(3)
        p5.metric("NPV (@10%)", f"RM {npv_p:,.0f}")
        p6.metric("IRR (%)", f"{irr_p:.2f}%")
        p7.metric("ROI (%)", f"{roi_p:.2f}%")

# ==========================================
# TAB 3: ANJAKAN WAWASAN (SAWIT & KONSOLIDASI 5,787 HA)
# ==========================================
with tab3:
    st.header("🌟 Anjakan Wawasan - Integrasi Sawit & Konsolidasi Penuh")
    st.info("💡 Tab ini menggabungkan Pakej 3 (Sawit 1,550 Ha) bersama Pakej Getah untuk menunjukkan Aliran Tunai Penuh dan Strategi Subsidi Silang kepada KP.")
    
    fasa_view = st.selectbox("Pilih Perspektif Masa Rundingan:", [
        "Tahun 1-3: Fasa Awalan & Defisit Capex Sawit",
        "Tahun 1-9: Fasa RoU Pertengahan (3+3+3) - ZON KEEMASAN",
        "Tahun 1-25: Kitaran Hayat Penuh 25 Tahun"
    ])
    
    # Data Konsolidasi Dokumen
    if "Tahun 1-3" in fasa_view:
        untung_lantai = -11800000
        untung_siling = -19090000
        alert_msg = "🚨 FASA DEFISIT TUNAI: Penumpuan CAPEX Sawit RM11J/Thn. KP perlu pastikan sewa Pakej 3 kekal RM500/Ha!"
        alert_type = "error"
    elif "Tahun 1-9" in fasa_view:
        untung_lantai = 12230000
        untung_siling = 7880000
        alert_msg = "💰 ZON KEEMASAN (3+3+3): Unjuran Pukal 9 Tahun untung RM12.23J (Lantai). Fasa terbaik untuk dimuktamadkan!"
        alert_type = "success"
    else:
        untung_lantai = 68760000
        untung_siling = 8900000
        alert_msg = "📈 KITARAN PENUH 25 TAHUN: Projek sangat berdaya saing dengan Untung Pukal RM68.76 Juta (Kadar Lantai)."
        alert_type = "info"

    col_k1, col_k2 = st.columns(2)
    with col_k1:
        st.subheader("📊 Prestasi Kadar LANTAI (Floor)")
        if untung_lantai < 0:
            st.error(f"Untung/Rugi Bersih Pukal: -RM {abs(untung_lantai):,.0f}")
        else:
            st.metric("Untung Bersih Pukal Fasa", f"RM {untung_lantai:,.0f}")
        st.metric("NPV (@10% Diskaun)", "RM 3.92 Juta" if untung_lantai > 0 else "-RM 4.12 Juta")
        st.metric("ROI Keseluruhan", "17.01%" if untung_lantai > 0 else "-5.20%")
        
    with col_k2:
        st.subheader("📊 Prestasi Kadar SILING (Ceiling)")
        if untung_siling < 0:
            st.error(f"Untung/Rugi Bersih Pukal: -RM {abs(untung_siling):,.0f}")
        else:
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
    * **Strategi Pakej 3 (Sawit - 1,550 Ha):** Pertahankan sewa **RM500 – RM800/Ha**. Jika syarikat swasta minta RM1,500/Ha, tunjukkan bahawa aliran tunai Tahun 1–3 akan defisit melebihi RM20 Juta.
    * **Strategi Pakej 2 (Getah Muda - 3,487 Ha):** Guna formula sewa bertingkat ($3+3+3$). Tahun 1–3 minta diskaun **RM1,200/Ha**, dan naik ke **RM2,300/Ha** pada Tahun 4 selepas hasil pokok melepasi $1,200\text{ kg/Ha}$.
    * **Subsidi Silang:** Keuntungan Pakej 1 (Getah Matang - 2,300 Ha) sekitar **RM3.79J setahun** adalah 'perisai' untuk menampung kos pembangunan awal Pakej 3 Sawit.
    """)
