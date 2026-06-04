import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dashboard Insight RS", layout="wide")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('dataset_RS_clean.csv')
    df['waktu_kedatangan'] = pd.to_datetime(df['waktu_kedatangan'])
    df['jam'] = df['waktu_kedatangan'].dt.hour
    return df

df = load_data()

st.title("🏥 Dashboard Analisis Operasional Rumah Sakit")
st.markdown("--- ")

# Sidebar untuk Filter
st.sidebar.header("Filter Data")
selected_poli = st.sidebar.multiselect("Pilih Poliklinik", options=df['nama_poli'].unique(), default=df['nama_poli'].unique())
data_filtered = df[df['nama_poli'].isin(selected_poli)]

# Row 1: Key Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Kunjungan", f"{len(data_filtered):,}")
with col2:
    st.metric("Rata-rata Waktu Tunggu", f"{data_filtered['waktu_tunggu'].mean():.1f} Menit")
with col3:
    st.metric("Total Pendapatan", f"IDR {data_filtered['biaya'].sum():,}")

# Row 2: Charts
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📈 Kepadatan Kedatangan per Jam")
    hourly_counts = data_filtered['jam'].value_counts().sort_index().reset_index(name='count')
    fig_hour = px.line(hourly_counts, x='jam', y='count', title='Tren Kedatangan Pasien', markers=True)
    st.plotly_chart(fig_hour, use_container_width=True)

with col_right:
    st.subheader("💰 Efisiensi per Poliklinik")
    data_filtered['biaya_per_menit'] = data_filtered['biaya'] / data_filtered['durasi_layanan']
    efisiensi = data_filtered.groupby('nama_poli')['biaya_per_menit'].mean().sort_values().reset_index()
    fig_efisiensi = px.bar(efisiensi, x='biaya_per_menit', y='nama_poli', orientation='h', color='biaya_per_menit')
    st.plotly_chart(fig_efisiensi, use_container_width=True)

# Row 3: Predictive Interaction
st.markdown("--- ")
st.subheader("🔮 Simulator Prediksi Waktu Tunggu")
antrean_input = st.number_input("Masukkan Jumlah Antrean Saat Ini:", min_value=0, value=10)
# Menggunakan koefisien dari model yang sudah kita buat sebelumnya
estimasi = 4.43 + (1.71 * antrean_input)
st.success(f"Estimasi waktu tunggu pasien tersebut adalah: **{estimasi:.2f} Menit**")