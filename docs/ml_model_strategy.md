# ML Model Strategy & Algorithm Analysis

## 1. Introduction & Objective
The objective of this project is to research, design, and plan a Machine Learning model approach for wait time prediction. Accurate wait time predictions are crucial for improving operational efficiency, resource allocation, and customer/patient satisfaction. This document outlines the algorithm comparisons, architectural strategy, and best practices for developing a robust time-series forecasting model.

## 2. Algorithm Comparison
We evaluate four primary algorithms for this predictive task, ranging from baseline statistical approaches to advanced deep learning.

### Linear Regression (Baseline)
*   **Description:** A simple approach that assumes a linear relationship between input features (e.g., number of people in queue, time of day) and the target variable (wait time).
*   **Pros:** Highly interpretable, extremely fast training and inference, minimal compute resources required, serves as a great baseline.
*   **Cons:** Unable to capture complex, non-linear relationships or sophisticated temporal patterns. Often underperforms on highly variable real-world data.

### Random Forest
*   **Description:** An ensemble learning method constructing a multitude of decision trees at training time and outputting the average prediction.
*   **Pros:** Handles non-linear data well, robust to outliers and missing values, requires minimal feature scaling.
*   **Cons:** Prone to larger model sizes, slower inference times compared to single trees or linear models, cannot extrapolate trends outside the training data range.

### XGBoost (Extreme Gradient Boosting)
*   **Description:** An optimized distributed gradient boosting library highly efficient, flexible, and portable. It builds trees sequentially, where each new tree corrects errors made by previously trained trees.
*   **Pros:** Frequently achieves state-of-the-art results on tabular data, handles missing values inherently, provides feature importance metrics, fast execution speed compared to other ensemble methods.
*   **Cons:** More complex to tune (many hyperparameters), higher risk of overfitting if not regularized properly.

### LSTM (Long Short-Term Memory)
*   **Description:** A type of Recurrent Neural Network (RNN) capable of learning order dependence in sequence prediction problems. 
*   **Pros:** Excellent at capturing long-term temporal dependencies and complex sequential patterns (pure time-series).
*   **Cons:** High computational complexity, slow training and inference, requires large volumes of data to perform well, "black box" nature limits interpretability.

## 3. Trade-off Analysis

| Algorithm | Accuracy | Interpretability | Inference Time | Training Complexity |
| :--- | :--- | :--- | :--- | :--- |
| **Linear Regression** | Low | Very High | Very Fast | Very Low |
| **Random Forest** | Medium-High | Medium | Moderate | Low-Medium |
| **XGBoost** | High | Medium | Fast | High (Tuning) |
| **LSTM** | High (for sequences)| Low | Slow | Very High |

**Conclusion:** For typical operational wait time predictions involving tabular features (historical averages, day of week, staff count), **XGBoost** presents the optimal balance of high accuracy and fast inference time, while remaining manageable regarding computational resources.

## 4. Proposed Architecture & Hyperparameter Strategy
### Model Architecture
We propose a phased approach:
1.  **Phase 1 (Baseline):** Implement Linear Regression and a naive moving average model to establish baseline metrics.
2.  **Phase 2 (Primary Model):** Develop an **XGBoost Regressor** as the primary predictive engine. It will consume a combination of engineered temporal features and real-time operational state features.

### Hyperparameter Strategy
We will employ **Bayesian Optimization** (via libraries like Optuna) rather than exhaustive Grid Search, as it converges on optimal hyperparameters much faster.
Key XGBoost parameters to tune:
*   `max_depth`: Control tree complexity (typically between 3 and 10).
*   `learning_rate` (eta): Step size shrinkage (typically 0.01 to 0.3).
*   `n_estimators`: Number of boosting rounds.
*   `subsample` & `colsample_bytree`: To prevent overfitting by adding randomness.

## 5. Time Series Best Practices
Wait time prediction is inherently a time-series problem. The following practices are critical:
*   **Feature Engineering:** 
    *   *Lag Features:* Historical wait times (e.g., $T-1$, $T-2$ hours).
    *   *Rolling Statistics:* Moving averages and standard deviations over the last $N$ hours.
    *   *Temporal Encoding:* Cyclical encoding (sine/cosine transformations) for hour of day, day of week, and month to preserve cyclical continuity.
*   **Data Splitting:** Avoid random K-fold cross-validation, which causes data leakage from the future into the past. We will use **Walk-Forward Validation** (Time Series Split) to ensure the model is always trained on past data and evaluated on future data.

## 6. Validation & Evaluation Metrics
To rigorously evaluate model performance, we will utilize the following metrics:
1.  **MAE (Mean Absolute Error):** Our primary metric. It provides a linear penalty for errors and is highly interpretable (e.g., "The model is off by 4.5 minutes on average").
2.  **RMSE (Root Mean Squared Error):** Useful for penalizing larger errors heavily. Important if severe underestimations/overestimations of wait times have a high operational cost.
3.  **MAPE (Mean Absolute Percentage Error):** Useful for communicating accuracy to non-technical stakeholders (e.g., "Predictions are within 10% of the actual wait time").
