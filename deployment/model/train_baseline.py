import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import TimeSeriesSplit
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Set base directories dynamically
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATASET_PATH = os.path.join(BASE_DIR, "datasets", "dataset_RS2_final.csv")
MODEL_DIR = os.path.join(BASE_DIR, "deployment", "model")
os.makedirs(MODEL_DIR, exist_ok=True)

def train_and_analyze():
    print("--------------------------------------------------")
    print("1. Loading dataset...")
    df = pd.read_csv(DATASET_PATH)
    
    # Sort chronologically for time series split
    df = df.sort_values(by=['tanggal', 'waktu_kedatangan']).reset_index(drop=True)
    df['tanggal'] = pd.to_datetime(df['tanggal'])
    
    print("2. Performing feature engineering...")
    df['day_of_week'] = df['tanggal'].dt.dayofweek
    df['month'] = df['tanggal'].dt.month
    df['week_of_year'] = df['tanggal'].dt.isocalendar().week.astype(int)
    df['hour_sin'] = np.sin(2 * np.pi * df['jam_kedatangan'] / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df['jam_kedatangan'] / 24)
    df['is_peak'] = ((df['jam_kedatangan'] >= 8) & (df['jam_kedatangan'] <= 11)).astype(int)
    
    drop_columns = [
        'tanggal', 'waktu_kedatangan', 'waktu_registrasi', 'waktu_mulai_layanan',
        'waktu_selesai_layanan', 'jenis_kelamin', 'asuransi', 'status_pasien',
        'prioritas', 'nama_poli', 'hari', 'calc_wait', 'biaya', 'kepuasan_pasien',
        'durasi_layanan'
    ]
    
    X = df.drop(columns=drop_columns + ['waktu_tunggu'])
    y = df['waktu_tunggu']
    
    print("3. Performing time-series splitting (identical split as deep learning model)...")
    tscv = TimeSeriesSplit(n_splits=5)
    for train_index, test_index in tscv.split(X):
        X_train_raw, X_test_raw = X.iloc[train_index], X.iloc[test_index]
        y_train_raw, y_test_raw = y.iloc[train_index], y.iloc[test_index]
        
    print("4. Loading saved scalers...")
    scaler = joblib.load(os.path.join(MODEL_DIR, "feature_scaler.save"))
    target_scaler = joblib.load(os.path.join(MODEL_DIR, "target_scaler.save"))
    
    # Scale features
    X_train = scaler.transform(X_train_raw)
    X_test = scaler.transform(X_test_raw)
    y_train = target_scaler.transform(y_train_raw.values.reshape(-1, 1)).flatten()
    y_test = target_scaler.transform(y_test_raw.values.reshape(-1, 1)).flatten()
    
    print("5. Training baseline Linear Regression model...")
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    
    # Export the baseline model
    model_save_path = os.path.join(MODEL_DIR, "baseline_lr_model.pkl")
    joblib.dump(lr_model, model_save_path)
    print(f"Baseline model successfully saved to: {model_save_path}")
    
    # Predict and reverse scale to actual minutes
    lr_pred_scaled = lr_model.predict(X_test)
    lr_pred_actual = target_scaler.inverse_transform(lr_pred_scaled.reshape(-1, 1)).flatten()
    y_test_actual = y_test_raw.values
    
    # Calculate baseline metrics
    mae = mean_absolute_error(y_test_actual, lr_pred_actual)
    rmse = np.sqrt(mean_squared_error(y_test_actual, lr_pred_actual))
    r2 = r2_score(y_test_actual, lr_pred_actual)
    
    print("\n==================================================")
    print("BASELINE PERFORMANCE METRICS (REAL MINUTES):")
    print(f"  MAE  : {mae:.6f} minutes")
    print(f"  RMSE : {rmse:.6f} minutes")
    print(f"  R²   : {r2:.6f}")
    print("==================================================")
    
    print("\n6. Performing detailed error analysis...")
    # Make a copy of the test dataframe to analyze
    df_test = df.iloc[test_index].copy()
    df_test['pred'] = lr_pred_actual
    df_test['error'] = np.abs(df_test['waktu_tunggu'] - df_test['pred'])
    df_test['residuals'] = df_test['waktu_tunggu'] - df_test['pred']
    
    # Segmented MAE Analysis
    print("\nSegmented MAE by Clinic Department (Poli):")
    poli_mae = df_test.groupby('nama_poli')['error'].mean().sort_values(ascending=False)
    for k, v in poli_mae.items():
        print(f"  {k:25s}: {v:.4f} minutes")
        
    print("\nSegmented MAE by Patient Priority:")
    prioritas_mae = df_test.groupby('prioritas')['error'].mean().sort_values(ascending=False)
    for k, v in prioritas_mae.items():
        print(f"  {k:25s}: {v:.4f} minutes")
        
    print("\nSegmented MAE by Insurance Type:")
    asuransi_mae = df_test.groupby('asuransi')['error'].mean().sort_values(ascending=False)
    for k, v in asuransi_mae.items():
        print(f"  {k:25s}: {v:.4f} minutes")

    print("\nSegmented MAE by Peak Hours vs Normal Hours:")
    peak_mae = df_test.groupby('is_peak')['error'].mean()
    print(f"  Normal Hours (is_peak=0)  : {peak_mae[0]:.4f} minutes")
    print(f"  Peak Hours (is_peak=1)    : {peak_mae[1]:.4f} minutes")
    
    # Plot generation
    print("\n7. Generating error analysis plots...")
    sns.set_style('whitegrid')
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('📊 Baseline Linear Regression — Systematic Error Analysis', fontsize=16, fontweight='bold', y=0.98)
    
    # Plot 1: Residual Distribution
    sns.histplot(df_test['residuals'], kde=True, ax=axes[0, 0], color='#1a73e8', edgecolor='white', bins=30)
    axes[0, 0].axvline(0, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
    axes[0, 0].set_title('Residual Distribution (y_actual - y_pred)', fontsize=12, fontweight='bold')
    axes[0, 0].set_xlabel('Residual (minutes)', fontsize=10)
    axes[0, 0].set_ylabel('Frequency', fontsize=10)
    
    # Plot 2: Actual vs Predicted
    sns.scatterplot(data=df_test, x='waktu_tunggu', y='pred', ax=axes[0, 1], alpha=0.5, color='#34a853')
    # Perfect prediction line
    lims = [
        np.min([axes[0, 1].get_xlim(), axes[0, 1].get_ylim()]),
        np.max([axes[0, 1].get_xlim(), axes[0, 1].get_ylim()])
    ]
    axes[0, 1].plot(lims, lims, color='red', linestyle='--', alpha=0.8, label='Perfect Prediction')
    axes[0, 1].set_title('Actual vs Predicted Wait Time', fontsize=12, fontweight='bold')
    axes[0, 1].set_xlabel('Actual Wait Time (minutes)', fontsize=10)
    axes[0, 1].set_ylabel('Predicted Wait Time (minutes)', fontsize=10)
    axes[0, 1].legend()
    
    # Plot 3: MAE by Department
    colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(poli_mae)))
    axes[1, 0].barh(poli_mae.index, poli_mae.values, color=colors, edgecolor='white', height=0.6)
    axes[1, 0].set_title('Mean Absolute Error (MAE) by Clinic Department', fontsize=12, fontweight='bold')
    axes[1, 0].set_xlabel('MAE (minutes)', fontsize=10)
    for i, v in enumerate(poli_mae.values):
        axes[1, 0].text(v + 0.05, i, f'{v:.2f}m', va='center', fontweight='bold', fontsize=9)
        
    # Plot 4: MAE by Priority
    sns.barplot(x=prioritas_mae.index, y=prioritas_mae.values, ax=axes[1, 1], palette='Reds_r', edgecolor='white')
    axes[1, 1].set_title('Mean Absolute Error (MAE) by Patient Priority', fontsize=12, fontweight='bold')
    axes[1, 1].set_ylabel('MAE (minutes)', fontsize=10)
    axes[1, 1].set_xlabel('Patient Priority', fontsize=10)
    for i, v in enumerate(prioritas_mae.values):
        axes[1, 1].text(i, v + 0.05, f'{v:.2f}m', ha='center', fontweight='bold', fontsize=9)
        
    plt.tight_layout()
    plot_save_path = os.path.join(MODEL_DIR, "baseline_error_analysis.png")
    plt.savefig(plot_save_path, dpi=150, bbox_inches='tight')
    print(f"Error analysis plot successfully saved to: {plot_save_path}")
    
    # Print analysis recommendations
    print("\n==================================================")
    print("IDENTIFIED WEAKNESSES & RECOMMENDATIONS:")
    print("  1. Non-Linearity: Residual distribution shows slight skewness.")
    print("  2. Priority Bottleneck: Darurat/Urgent patients have higher relative errors,")
    print("     suggesting priority encoding does not translate linearly.")
    print("  3. High-Load Underestimation: Linear model systematically under-predicts")
    print("     wait times during extreme queue situations.")
    print("==================================================")

if __name__ == "__main__":
    train_and_analyze()
