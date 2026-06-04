import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# 1. Load data yang sudah bersih
def run_ab_test():
    df = pd.read_csv('dataset_RS_clean.csv')

    # 2. Menyiapkan grup
    group_a = df[df['asuransi'] == 'BPJS']['waktu_tunggu']
    group_b = df[df['asuransi'] == 'Umum']['waktu_tunggu']

    # 3. Statistik Deskriptif
    print(f"Rata-rata Waktu Tunggu BPJS: {group_a.mean():.2f} menit")
    print(f"Rata-rata Waktu Tunggu Umum: {group_b.mean():.2f} menit")

    # 4. Inferensi Statistik (T-Test)
    t_stat, p_value = stats.ttest_ind(group_a, group_b)
    
    print(f"\nT-Statistic: {t_stat:.4f}")
    print(f"P-Value: {p_value:.4f}")

    if p_value < 0.05:
        print("\nHasil: Terdapat perbedaan signifikan secara statistik.")
    else:
        print("\nHasil: Tidak ada perbedaan signifikan secara statistik.")

    # 5. Visualisasi
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=df, x='asuransi', y='waktu_tunggu')
    plt.title('A/B Test: Waktu Tunggu Berdasarkan Asuransi')
    plt.savefig('hasil_ab_test.png')
    print("\nGrafik telah disimpan sebagai 'hasil_ab_test.png'")

if __name__ == '__main__':
    run_ab_test()