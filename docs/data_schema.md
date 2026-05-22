# Data Schema & Feature Planning

## 1. Introduction

This document defines the data schema and feature engineering strategy for the SmartQueue AI system. The objective is to design a structured dataset that supports accurate and scalable machine learning models for predicting patient waiting time in healthcare facilities.

The schema is aligned with the ML strategy defined previously, ensuring compatibility with regression-based models such as XGBoost.

---

## 2. Data Schema Design

The dataset is designed to capture temporal, operational, and service-related factors that influence patient waiting time.

### Core Features:

* **doctor_id**: Unique identifier for the service provider (doctor)
* **date**: Full date of visit (YYYY-MM-DD)
* **day**: Day of the week (Monday–Sunday)
* **hour**: Hour of arrival (0–23)
* **number_of_patients**: Number of patients currently in queue
* **department**: Service unit (e.g., General, Dental, Pediatrics)
* **waiting_time (target)**: Actual waiting time in minutes

---

## 3. Feature Categorization

To improve model interpretability and performance, features are categorized as follows:

###  Provider Features
- doctor_id

This feature represents the individual service provider. Different doctors may have different service speeds, which significantly impacts patient waiting time.

###  Temporal Features

* hour
* day
* date

These features capture time-based patterns such as peak hours and weekly trends.

---

###  Queue Features

* number_of_patients

Represents real-time system load and directly impacts waiting time.

---

###  Service Features

* department

Different departments have varying service durations and queue behaviors.

---

## 4. Feature Engineering Strategy

To enhance predictive performance, additional derived features will be considered:

###  Lag Features

* Previous waiting time (t-1, t-2 hours)

###  Rolling Statistics

* Moving average of waiting time over last N hours

###  Cyclical Encoding

* Encode hour and day using sine/cosine transformation to preserve periodicity

Example:

* sin(hour), cos(hour)
* sin(day), cos(day)

Doctor-based patterns may also be analyzed to capture service variability between providers.

---

## 5. Data Types & Representation

| Feature            | Type        | Description                        |
| ------------------ | ----------- | ---------------------------------- |
| doctor_id          | Categorical | Encoded (One-Hot / Label Encoding) |
| hour               | Numerical   | Integer (0–23)                     |
| day                | Categorical | Encoded (One-Hot / Label Encoding) |
| number_of_patients | Numerical   | Integer                            |
| department         | Categorical | Encoded                            |
| waiting_time       | Numerical   | Continuous (minutes)               |

---

## 6. Data Preprocessing Pipeline

The preprocessing pipeline will include:

* Handling missing values (imputation or removal)
* Encoding categorical features (One-Hot Encoding)
* Feature scaling (if required for specific models)
* Outlier detection and removal
* Feature selection based on importance scores

---

## 7. Model Input & Output Schema

### Input Format:

Structured feature vector:

[hour, day_encoded, number_of_patients, department_encoded]

### Output:

* Predicted waiting time (in minutes)

---

## 8. Data Validation Rules

To ensure data quality:

* hour must be between 0–23
* number_of_patients must be ≥ 0
* waiting_time must be ≥ 0
* department must belong to predefined categories
* no null values in critical features

---

## 9. Data Pipeline Overview

1. Raw data collection (simulation / historical)
2. Data cleaning & preprocessing
3. Feature engineering
4. Model training dataset generation
5. Validation & testing split (time-based split)

---

## 10. Conclusion

The proposed data schema is designed to support robust and scalable machine learning models for wait time prediction. By incorporating temporal, queue, and service-related features, along with advanced feature engineering techniques, the system is expected to deliver accurate and reliable predictions in real-world healthcare scenarios.
