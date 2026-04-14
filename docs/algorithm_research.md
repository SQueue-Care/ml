# Algorithm Research & Design

## 1. Introduction & Objective

The objective of this document is to research, analyze, and recommend patient distribution algorithms for the SQueue Care system. Intelligent algorithm selection is critical for minimizing wait times, balancing queue loads, and optimizing resource allocation in real-time. This document evaluates rule-based and machine learning approaches, provides complexity analysis, and proposes a phased implementation strategy.

---

## 2. Problem Definition

### 2.1 Input Parameters
- **Patient Characteristics:** Age, medical condition, insurance type, preferred doctor
- **Queue State:** Current queue lengths, active patients, estimated completion times
- **Resource Availability:** Doctor schedules, department capacity, current load
- **Historical Data:** Service times, peak hours, doctor efficiency metrics

### 2.2 Output Requirements
- **Optimal Assignment:** Department and doctor recommendation
- **Wait Time Prediction:** Estimated wait in minutes
- **Alternative Options:** Secondary recommendations for load-balanced assignment

### 2.3 Key Constraints
- **Real-time Performance:** < 500ms assignment latency (target: < 50ms)
- **Capacity Management:** Queue length must not exceed doctor capacity
- **Availability:** Respect doctor working hours and availability
- **Specialty Match:** Route to correct department for patient condition
- **Scalability:** Support 100+ concurrent patients per second

---

## 3. Algorithm Comparison

### 3.1 Rule-Based Approaches

#### Least Queue Length (LQL)
**Concept:** Assign to doctor with shortest current queue.

| Aspect | Rating | Notes |
|--------|--------|-------|
| **Accuracy** | Low | Reactive only, ignores service time |
| **Speed** | ⭐⭐⭐⭐⭐ | O(n), < 5ms |
| **Simplicity** | ⭐⭐⭐⭐⭐ | Trivial to implement |
| **Data Needs** | None | Real-time only |
| **Scalability** | Excellent | 100,000+ patients/sec possible |

**Pros:**
- Extremely fast (sub-5ms)
- Simple to implement and understand
- Prevents queue length extremes
- No historical data required

**Cons:**
- Ignores service time variability
- Doesn't account for doctor efficiency
- Can create "long tail" queues (few patients, long service times)
- Purely reactive, not predictive

**Recommendation:** **Best for MVP launch** (Week 1-4). Establishes baseline and gathers data.

---

#### Weighted Load Balancing (WLB)
**Concept:** Assign based on normalized queue length × estimated service time.

| Aspect | Rating | Notes |
|--------|--------|-------|
| **Accuracy** | Medium | Considers service time |
| **Speed** | ⭐⭐⭐⭐⭐ | O(n), < 20ms |
| **Simplicity** | ⭐⭐⭐⭐ | Minimal complexity |
| **Data Needs** | Historical service times | 1-2 weeks data |
| **Scalability** | Excellent | 50,000+ patients/sec possible |

**Formula:**
```
load_score = (queue_length / capacity) × avg_service_time
assignment = argmin(load_score)
```

**Pros:**
- Considers both queue length and service time
- Better load balancing than LQL
- Still very fast
- Uses accumulated historical data

**Cons:**
- Still reactive (doesn't predict)
- Equal weight for all patients
- No personalization

**Recommendation:** **Phase 2 upgrade** (Week 5-8) after collecting 4+ weeks of data.

---

#### Priority-Based Routing
**Concept:** Route based on urgency + load balancing.

| Aspect | Rating | Notes |
|--------|--------|-------|
| **Accuracy** | Medium-High | Respects medical priority |
| **Speed** | ⭐⭐⭐⭐ | O(n log n), < 20ms |
| **Simplicity** | ⭐⭐⭐ | Requires priority rules |
| **Data Needs** | Priority classification | Rule-based |
| **Scalability** | Excellent | 50,000+ patients/sec possible |

**Pros:**
- Handles medical emergencies appropriately
- Compatible with LQL/WLB
- Flexible priority rules

**Cons:**
- Requires priority classification
- Risk of starving routine patients
- Still doesn't predict future load

**Recommendation:** Optional enhancement for Phase 1-2 if emergency routing needed.

---

### 3.2 Machine Learning Approaches

#### Gradient Boosting (XGBoost/LightGBM)
**Concept:** Predict wait time for each possible assignment, select minimum.

| Aspect | Rating | Notes |
|--------|--------|-------|
| **Accuracy** | ⭐⭐⭐⭐⭐ | 65-80% prediction accuracy |
| **Speed** | ⭐⭐⭐⭐ | 30-50ms inference |
| **Simplicity** | ⭐⭐⭐ | Requires feature engineering |
| **Data Needs** | 1-3 months history | Significant training data |
| **Scalability** | Excellent | 12,500+ patients/sec possible |

**Features:**
- Historical service times (doctor + patient type)
- Temporal features (hour, day, day-of-week)
- Current queue state (length, load ratio)
- Doctor efficiency metrics
- Peak hour indicators

**Pros:**
- Highly accurate predictions
- Fast inference (production-ready)
- Explainable feature importance
- Handles non-linear patterns

**Cons:**
- Requires significant historical data (1-3 months)
- Feature engineering critical
- Model drift over time (requires retraining)
- Cold start problem for new doctors

**Recommendation:** **Phase 3** (Week 9-12) once sufficient data accumulated. Strong candidate for long-term deployment.

---

#### Reinforcement Learning (Q-Learning/Policy Gradient)
**Concept:** Train agent to learn optimal assignment policy via reward signals.

| Aspect | Rating | Notes |
|--------|--------|-------|
| **Accuracy** | ⭐⭐⭐⭐⭐ | Optimal if converged |
| **Speed** | ⭐⭐ | 100-500ms inference |
| **Simplicity** | ⭐ | Complex to implement |
| **Data Needs** | 2-3 months | Extensive historical data |
| **Scalability** | Poor | 1,000-2,500 patients/sec |

**Pros:**
- Learns complex patterns
- Adapts over time
- Optimizes multiple objectives
- Continuous improvement

**Cons:**
- Not real-time friendly (500ms+)
- Complex to implement and debug
- Requires extensive infrastructure
- "Black box" decisions
- Cold start problem severe

**Recommendation:** **Post-MVP enhancement** (after 6 months+ production data). Too complex for MVP.

---

#### Constraint Satisfaction Problem (CSP)
**Concept:** Model as optimization problem with hard/soft constraints.

| Aspect | Rating | Notes |
|--------|--------|-------|
| **Accuracy** | Optimal | Provably optimal |
| **Speed** | ⭐ | Seconds to minutes |
| **Simplicity** | ⭐ | Very complex |
| **Data Needs** | None | Rule-based |
| **Scalability** | ⭐ | < 100 patients/sec |

**Pros:**
- Mathematically rigorous
- Guarantees constraint satisfaction
- Explainable decisions

**Cons:**
- NP-hard (exponential complexity)
- Not suitable for real-time
- Requires solver libraries
- Complex to implement

**Recommendation:** **Future enhancement** for batch optimization (overnight scheduling), not real-time assignment.

---

### 3.3 Hybrid Approach: Two-Stage Routing

**Concept:**
- **Stage 1:** Use WLB to narrow to top 3 candidates (< 10ms)
- **Stage 2:** Use ML model to predict wait times (30-50ms)
- **Total:** < 100ms, balances speed and accuracy

| Aspect | Rating | Notes |
|--------|--------|-------|
| **Accuracy** | ⭐⭐⭐⭐ | 70-75% via ML |
| **Speed** | ⭐⭐⭐⭐ | < 100ms (good SLA) |
| **Simplicity** | ⭐⭐⭐ | Moderate complexity |
| **Data Needs** | 1-2 months | Practical amount |
| **Scalability** | Excellent | 10,000+ patients/sec |

**Advantages:**
- Combines speed of rule-based with ML accuracy
- Reasonable latency (meets 500ms target comfortably)
- Explainable: "Department X has Y minute wait"
- Production-ready architecture
- Practical for realistic timelines

**Disadvantages:**
- Requires ML model training
- More complex than pure rule-based
- Still needs historical data accumulation

**Recommendation:** **Excellent MVP+ candidate** if ML training completes early (Week 6-8). Strong fallback for Phase 3.

---

## 4. Algorithm Selection Strategy

### 4.1 Recommended Implementations

#### Stage 1: Least Queue Length
**Algorithm:** LQL - Least Queue Length  
**Complexity:** O(n) where n = total doctors  
**Latency Target:** < 5ms  
**Data Requirements:** None (real-time only)

**Implementation:**
```python
def assign_patient_lql(patient, available_doctors):
    # Filter by hard constraints
    candidates = [d for d in available_doctors
                  if d.in_working_hours()
                  and d.has_capacity()
                  and d.matches_specialty(patient)]
    
    if not candidates:
        return WAITLIST_OR_ALTERNATIVE
    
    # Select doctor with minimum queue length
    return min(candidates, key=lambda d: len(d.queue))
```

**Performance Characteristics:**
- Average wait time: 15-20 minutes
- Assignment latency: < 5ms
- Queue balance: Fair
- Scalability: 100,000+ patients/sec

**Strengths:**
- Trivial to implement and understand
- No historical data required
- Guarantees no extreme queue imbalances
- Establishes baseline metrics

**Limitations:**
- Ignores service time variability
- Reactive, not predictive
- Doesn't account for doctor efficiency differences
- Can create "long tail" queues

---

#### Stage 2: Weighted Load Balancing
**Algorithm:** WLB - Weighted Load Balancing  
**Complexity:** O(n) where n = total doctors  
**Latency Target:** < 20ms  
**Data Requirements:** Historical service times (1-2 weeks data)

**Implementation:**
```python
def assign_patient_wlb(patient, available_doctors):
    best_score = float('inf')
    best_doctor = None
    
    for doctor in available_doctors:
        # Queue length normalized by capacity
        queue_ratio = len(doctor.queue) / doctor.max_capacity
        
        # Service time with temporal adjustment
        service_time = doctor.get_avg_service_time(
            patient_type=patient.type,
            hour=current_hour
        )
        
        # Peak hour adjustment (1.0 normal, 1.2+ peak)
        peak_factor = get_peak_factor(current_hour, current_day)
        
        # Composite load score
        score = queue_ratio * (service_time * peak_factor)
        
        if score < best_score:
            best_score = score
            best_doctor = doctor
    
    return best_doctor
```

**Performance Characteristics:**
- Average wait time: 12-16 minutes (20% improvement over LQL)
- Assignment latency: < 20ms
- Queue balance: Good
- Scalability: 50,000+ patients/sec

**Strengths:**
- Considers both queue length and service time
- Better load balancing than LQL
- Still very fast
- Uses accumulated historical patterns

**Limitations:**
- Still reactive (doesn't predict future load)
- Requires service time baseline data
- Equal weight for all patient types
- No personalization

---

#### Stage 3: Two-Stage Routing with ML
**Algorithm:** TSR - Two-Stage Routing  
**Complexity:** O(n) for stage 1 + O(m) for stage 2, where m ≈ 3  
**Latency Target:** < 100ms  
**Data Requirements:** ML model (trained on 1-3 months history)

**Implementation:**

Stage 1 - Filter candidates using WLB:
```python
def filter_candidates(patient, available_doctors, k=3):
    scores = []
    
    for doctor in available_doctors:
        load = calculate_wlb_score(doctor, patient)
        scores.append((doctor, load))
    
    # Return top k candidates by load score
    scores.sort(key=lambda x: x[1])
    return [doc for doc, score in scores[:k]]
```

Stage 2 - Select best using ML prediction:
```python
def select_best_candidate(patient, candidates, ml_model):
    best_doctor = None
    best_wait = float('inf')
    best_confidence = 0
    
    for doctor in candidates:
        # Extract features for ML model
        features = extract_features(patient, doctor)
        
        # Predict wait time using trained model
        wait_pred, confidence = ml_model.predict(features)
        
        # Department load penalty (discourage high-load depts)
        dept_load = get_department_load(doctor.department)
        if dept_load > 0.8:
            wait_pred += 5  # Add 5 min penalty
        
        # Select assignment with minimum predicted wait
        if wait_pred < best_wait:
            best_wait = wait_pred
            best_doctor = doctor
            best_confidence = confidence
    
    return {
        'doctor': best_doctor,
        'predicted_wait': best_wait,
        'confidence': best_confidence
    }
```

**ML Feature Set:**
```python
features = {
    # Patient features
    'patient_age': patient.age,
    'patient_type': patient.patient_type,  # new/returning
    'severity': patient.severity,  # 1-5 scale
    
    # Doctor features
    'doctor_id': doctor.id,
    'doctor_efficiency': doctor.efficiency_rating,
    'doctor_experience': doctor.years_experience,
    
    # Queue state
    'current_queue_length': doctor.queue_length,
    'queue_ratio': doctor.queue_length / doctor.max_capacity,
    
    # Temporal features
    'hour_of_day': current_time.hour,
    'day_of_week': current_time.day_of_week,
    'is_peak_hour': is_peak_hour(current_time),
    'is_holiday': is_holiday(current_date),
    
    # Historical features
    'avg_service_time_for_type': historical_avg(doctor, patient.type),
    'peak_hour_multiplier': get_peak_factor(current_time),
    'recent_avg_wait_time': recent_avg(doctor),
    
    # Department features
    'dept_current_load': department.current_load / department.capacity,
    'dept_avg_service_time': department.avg_service_time,
}
```

**Performance Characteristics:**
- Average wait time: 10-14 minutes (30-35% improvement over LQL)
- Assignment latency: 50-100ms
- Prediction accuracy: 75%+ (MAE ≤ 15 minutes)
- Scalability: 10,000+ patients/sec

**Strengths:**
- Combines speed of rule-based with ML accuracy
- Reasonable latency for production use
- Explainable decisions: "Department X, wait time Y"
- Production-ready architecture

**Limitations:**
- Requires ML model training
- More complex implementation
- Needs 1-3 months of historical data

---

## 5. Complexity & Performance Analysis

### 5.1 Computational Complexity

| Algorithm | Time | Space | Latency | Peak Throughput |
|-----------|------|-------|---------|-----------------|
| **LQL** | O(n) | O(1) | < 5ms | 100,000/sec |
| **WLB** | O(n) | O(1) | < 20ms | 50,000/sec |
| **Priority** | O(n log n) | O(1) | < 20ms | 50,000/sec |
| **XGBoost** | O(model) | O(model) | 30-50ms | 12,500/sec |
| **RL** | O(state) | O(state) | 100-500ms | 1,000-2,500/sec |
| **CSP** | NP-hard | O(n²) | seconds | < 100/sec |

### 5.2 Real-Time Feasibility

**Peak Load Scenario:** 10 patients/second, 20 departments, 100 doctors

- **LQL** - Excellent (0.5ms per patient, 99.5% headroom)
- **WLB** - Excellent (2ms per patient, 99% headroom)
- **XGBoost** - Good (40ms per patient, 92% headroom)
- **RL** - Marginal (200ms per patient, 60% headroom)
- **CSP** - Not feasible (1000+ms per patient)

---

## 6. Feature Engineering

### 6.1 Scoring Function (MVP)

```
score = 0.7 × normalized_queue_length + 
        0.2 × load_balance_factor + 
        0.1 × patient_preference_match

Select: argmin(score)
```

### 6.2 Features for ML Model (Phase 3)

**Patient Features:** Age, patient type (new/returning), severity (1-5)
**Doctor Features:** Efficiency rating, years of experience
**Queue State:** Current queue length, queue ratio (length/capacity)
**Temporal Features:** Hour of day, day of week, peak hour flag, holiday flag
**Historical Features:** Average service time for patient type, peak hour multiplier, recent average wait

---

## 7. Data Requirements

| Phase | Algorithm | Data Needs |
|-------|-----------|-----------|
| **1** | LQL | None - real-time only |
| **2** | WLB | 4+ weeks of historical service times |
| **3** | ML | 1-3 months of complete queue history |

---

### Design Rationale

**LQL** provides immediate deployment capability without requiring historical data. It's sufficient for MVP validation.

**WLB** adds service time awareness once baseline data accumulates, improving queue balance and wait time prediction by 20%.

**Two-Stage Routing** combines fast rule-based filtering with ML predictions, achieving high accuracy while maintaining production latency targets. The two-stage approach prevents ML inference bottleneck by limiting predictions to top 3 candidates.

**Future methods** (RL, CSP) offer optimization beyond real-time constraints, suitable for batch processing and system-wide learning after sufficient operational data exists.

---
