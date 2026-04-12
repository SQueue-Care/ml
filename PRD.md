# Product Requirements Document (PRD)
## Intelligent Hospital Queue Management System

**Project ID:** CC26-PSU413  
**Theme:** Healthy Lives & Well-being  
**Program:** Coding Camp 2026 powered by DBS Foundation

---

## 1. Executive Summary

Hospital administration and queue management systems in Indonesia face significant challenges: long wait times, inefficient registration processes, and lack of patient transparency. The absence of predictive systems leads to uneven patient distribution and overload in specific departments, degrading service quality and patient experience.

This project develops a **Smart Healthcare Queue System** — a web-based platform that manages queue numbers, predicts wait times, and optimizes real-time patient distribution. It addresses root causes of operational inefficiency comprehensively, serving as a problem-solver rather than a superficial improvement.

### Key Research Questions
1. How can we build a queue system that visualizes wait time estimates accurately and in real-time?
2. How can we optimize patient distribution to reduce overload on specific services?
3. How can we improve patient information transparency to enhance their healthcare experience?

---

## 2. Problem Statement

### Current Pain Points
- **Long Wait Times:** Patients experience extended wait periods without accurate information
- **Inefficient Registration:** Manual and non-optimized booking processes
- **Lack of Transparency:** Patients cannot track queue status or estimated wait times
- **Poor Distribution:** No predictive system leads to uneven workload across departments
- **Limited Decision Support:** Staff lack real-time data for operational decisions

### Impact
- Reduced service quality and patient satisfaction
- Operational inefficiency and resource underutilization
- Poor patient experience during treatment

---

## 3. Product Vision & Objectives

### Vision
Create a data-driven, real-time hospital queue management system that improves operational efficiency and patient experience through intelligent queue distribution and transparent communication.

### Primary Objectives
1. **Reduce Wait Times:** Implement predictive models to accurately estimate and minimize patient wait times
2. **Optimize Operations:** Distribute patients intelligently to prevent department overload
3. **Enhance Transparency:** Provide patients with real-time queue status and wait time estimates
4. **Improve Decision-Making:** Equip hospital staff with actionable, real-time operational data

---

## 4. Product Scope

### In-Scope Features

#### 4.1 Queue Management
- Patient booking and registration via web interface
- Queue number assignment and management
- Real-time queue monitoring and visualization
- Department-based queue distribution

#### 4.2 Wait Time Prediction
- ML-based wait time estimation based on historical data
- Prediction model trained on patient visit patterns, service times, and doctor schedules
- Real-time prediction updates as patients move through the queue

#### 4.3 Patient Distribution Optimization
- Intelligent algorithm to distribute incoming patients across available services
- Load balancing to prevent department overload
- Recommendation system for optimal department routing

#### 4.4 User Interfaces
**Patient Portal:**
- Browse available departments and doctors
- Book appointment and obtain queue number
- Track queue status and wait time in real-time
- View estimated service completion time

**Admin Dashboard:**
- Monitor all active queues across departments
- View wait time metrics and performance analytics
- Manage doctor schedules and department capacity
- Generate operational insights and reports

#### 4.5 Backend Infrastructure
- RESTful API for queue management (CRUD operations)
- User authentication and authorization
- Database management for patients, doctors, schedules, and queue logs
- Integration layer for third-party services (mock BPJS API)

#### 4.6 Integration & Deployment
- Frontend deployment to Vercel
- Backend deployment to Render/Railway
- Database hosting on Supabase/Neon
- ML Model API integration with FastAPI/Flask

### Out-of-Scope Features

- Full BPJS integration (mock API only)
- Real-time AI model retraining in production
- Advanced features beyond MVP (SMS notifications, mobile app, etc.)
- Integration with existing hospital management systems
- Multi-language support beyond Indonesian/English
- Integration with hospital EMR systems

---

## 5. Key Features & Requirements

### 5.1 User Stories

#### Patient User Stories
**US1:** As a patient, I want to book an appointment and receive a queue number quickly so I can plan my visit efficiently.

**US2:** As a patient, I want to see my current queue position and estimated wait time so I can manage my time effectively.

**US3:** As a patient, I want to receive information about which department has shorter wait times so I can make informed decisions.

#### Admin User Stories
**US4:** As a hospital admin, I want to monitor all queues in real-time so I can identify bottlenecks and respond quickly.

**US5:** As a hospital admin, I want to see analytics on wait times and service metrics so I can make data-driven operational decisions.

**US6:** As a hospital admin, I want to manage doctor schedules and department capacities so I can optimize resource allocation.

### 5.2 Functional Requirements

| ID | Requirement | Priority | Component |
|----|-------------|----------|-----------|
| FR1 | System shall authenticate users (patients/admins) via secure login | High | Backend, Frontend |
| FR2 | System shall allow patients to book appointments with date/time selection | High | Frontend, Backend |
| FR3 | System shall assign unique queue numbers automatically | High | Backend |
| FR4 | System shall predict wait times using ML model with 80%+ accuracy | High | ML Model, Backend |
| FR5 | System shall display real-time queue status to all users | High | Frontend, Backend |
| FR6 | System shall recommend optimal department distribution based on current load | High | ML Model, Backend |
| FR7 | System shall maintain queue history for analytics | Medium | Database, Backend |
| FR8 | System shall support concurrent users without performance degradation | Medium | Backend, Infrastructure |
| FR9 | System shall integrate with mock BPJS API for insurance verification | Medium | Backend |
| FR10 | System shall provide admin dashboard with key performance metrics | High | Frontend, Backend |

### 5.3 Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR1 | Response Time | < 500ms for API calls |
| NFR2 | Availability | 99% uptime during business hours |
| NFR3 | Concurrent Users | Support 100+ simultaneous users |
| NFR4 | Database Query Time | < 1s for analytics queries |
| NFR5 | Security | HTTPS, password hashing (bcrypt), JWT authentication |
| NFR6 | Scalability | Auto-scaling backend to handle peak loads |
| NFR7 | Data Retention | 2 years of queue history |

---

## 6. Data Requirements

### Data Collection
- **Historical patient visit data:** arrival time, service duration, department, doctor
- **Doctor schedule data:** working hours, availability, service time per patient
- **Queue logs:** patient ID, department, queue position, wait time, service time

### Data Quality
- Data cleaning and preprocessing to handle missing values and outliers
- Exploratory data analysis (EDA) to identify patterns (peak hours, seasonal trends)
- Data validation and consistency checks

### Dummy Dataset Specifications
- Simulate 3-6 months of realistic hospital data
- Include various time patterns (weekdays, weekends, peak hours)
- Generate doctor availability and service time variations
- Create patient profiles with different characteristics

---

## 7. ML Model Requirements

### Wait Time Prediction Model
- **Input:** Patient characteristics, current queue state, doctor availability, historical patterns
- **Output:** Estimated wait time in minutes
- **Algorithm:** Regression-based (Linear Regression, Random Forest, or similar)
- **Target Accuracy:** MAE ≤ 15 minutes, RMSE acceptable within 20 minutes
- **Evaluation Metrics:** MAE (Mean Absolute Error), RMSE (Root Mean Squared Error), R² Score
- **Deployment:** Wrapped in FastAPI/Flask REST API

### Patient Distribution Model
- **Objective:** Minimize overall wait time and prevent service overload
- **Approach:** Rule-based or simple ML-based optimization
- **Output:** Recommendation for optimal department/doctor assignment

---

## 8. Technology Stack

### Frontend
- **Framework:** Next.js / React.js
- **Language:** JavaScript / TypeScript
- **UI Library:** Tailwind CSS, shadcn/ui (or similar)
- **State Management:** Redux / Zustand
- **Deployment:** Vercel

### Backend
- **Runtime:** Node.js
- **Framework:** Express.js / NestJS
- **Language:** JavaScript / TypeScript
- **Database:** PostgreSQL
- **Deployment:** Render / Railway
- **Database Hosting:** Supabase / Neon

### Machine Learning
- **Language:** Python
- **Data Processing:** Pandas, NumPy
- **ML Library:** Scikit-Learn
- **Model Serving:** FastAPI / Flask
- **Deployment:** Render / Railway

### Infrastructure
- **Authentication:** JWT (JSON Web Tokens)
- **API Protocol:** RESTful API
- **Version Control:** Git / GitHub
- **Containerization:** Docker (optional but recommended)

---

## 9. User Interface Requirements

### Patient Portal
- **Pages:** Landing, Login/Register, Dashboard, Booking, Queue Tracker
- **Key Features:**
  - Department selection with wait time preview
  - Appointment booking form
  - Real-time queue position display
  - Wait time countdown timer
  - Patient profile and history

### Admin Dashboard
- **Pages:** Login, Dashboard, Queue Monitor, Analytics, Settings
- **Key Features:**
  - Real-time queue status across all departments
  - Performance metrics (avg wait time, service rate, patient satisfaction)
  - Department workload visualization
  - Doctor schedule management
  - Historical data analytics and reports

---

## 10. Integration Points

### External APIs
- **BPJS Insurance API** (Mock): Patient insurance verification
- **Email Service** (Optional): Appointment confirmation and notifications
- **Cloud Services:** Vercel (frontend), Render (backend), Supabase (database)

### Internal Integration
- **Frontend ↔ Backend:** RESTful API calls
- **Backend ↔ ML Model:** API endpoint calls for predictions
- **Backend ↔ Database:** ORM queries (e.g., Prisma, TypeORM)

---

## 11. Success Metrics & KPIs

| Metric | Target | Measurement |
|--------|--------|-------------|
| Wait Time Prediction Accuracy | MAE ≤ 15 minutes | Model evaluation metrics |
| System Uptime | ≥ 99% | Monitoring tools (Sentry, etc.) |
| Page Load Time | < 2s | Frontend monitoring |
| User Satisfaction | ≥ 4/5 stars | User surveys |
| API Response Time | < 500ms | Backend monitoring |
| Concurrent User Support | 100+ | Load testing results |
| Patient Booking Completion Rate | ≥ 95% | Analytics tracking |

---

## 12. Development Roadmap & Phases

### Phase 1: Planning & Setup (Week 1-2)
- Finalize requirements and design
- Setup development environment
- Create data schema and database design
- Prepare dummy dataset

### Phase 2: Backend Development (Week 2-4)
- Setup Node.js/Express backend structure
- Implement authentication system
- Build queue management APIs
- Setup PostgreSQL database

### Phase 3: Frontend Development (Week 2-5)
- Design UI/UX in Figma
- Build patient portal interface
- Build admin dashboard interface
- Integrate with backend APIs

### Phase 4: ML Model Development (Week 2-4)
- Data exploration and analysis (EDA)
- Feature engineering
- Train wait time prediction model
- Wrap model in FastAPI/Flask

### Phase 5: Integration & Testing (Week 5-6)
- Integrate frontend, backend, and ML components
- Comprehensive testing (unit, integration, system)
- Bug fixes and optimization
- Load testing

### Phase 6: Deployment & Launch (Week 6-7)
- Deploy frontend to Vercel
- Deploy backend to Render
- Deploy ML API to cloud
- Monitor and support

---

## 13. Risk Management

### Identified Risks

| Risk | Probability | Impact | Mitigation Strategy |
|------|-------------|--------|---------------------|
| ML Model Accuracy Below Target | Medium | High | Early model evaluation, alternative algorithms |
| Database Performance Issues | Medium | High | Query optimization, indexing strategy, caching |
| Integration Delays | Medium | Medium | Early integration testing, clear API contracts |
| Deployment Issues | Low | High | Infrastructure documentation, rollback plan |
| Team Availability | Low | Medium | Clear task allocation, progress monitoring |
| Scope Creep | Medium | Medium | Strict scope management, MVP focus |

### Risk Mitigation Actions
1. **Daily standup meetings** to monitor progress and identify blockers early
2. **Regular integration testing** to catch issues before final integration
3. **Documentation** of all APIs and system components
4. **Backup plans** for critical functionalities
5. **Load testing** to validate system scalability

---

## 14. Constraints & Assumptions

### Constraints
- **MVP Focus:** Project limited to Minimum Viable Product (MVP) scope
- **Dummy Data:** Uses simulated dataset, not production hospital data
- **Mock Integration:** BPJS integration is simulation-based only
- **Development Timeline:** Limited to capstone project duration (6-8 weeks)

### Assumptions
- Hospital has basic IT infrastructure and internet connectivity
- Users (patients/staff) are comfortable with web interfaces
- Team has necessary technical skills in full-stack development, data science, and ML
- Dummy dataset accurately represents realistic hospital scenarios

---

## 15. Acceptance Criteria

The project is considered successful when:

✅ **Functional Completeness**
- All functional requirements (FR1-FR10) implemented and tested
- Patient portal fully functional for booking and queue tracking
- Admin dashboard provides real-time monitoring capabilities

✅ **Performance Standards**
- Page load times < 2 seconds
- API response times < 500ms under normal load
- System supports 100+ concurrent users

✅ **ML Model Quality**
- Wait time prediction MAE ≤ 15 minutes
- Model evaluation metrics meet or exceed targets

✅ **Quality Assurance**
- All critical and high-priority bugs fixed
- Code coverage ≥ 80% for backend services
- Security vulnerabilities resolved

✅ **Deployment & Accessibility**
- Frontend accessible via public Vercel URL
- Backend APIs functional and accessible
- Database properly configured and backed up

✅ **Documentation**
- API documentation complete
- System architecture documented
- Deployment guide provided

---

## 16. Glossary

| Term | Definition |
|------|-----------|
| **Queue** | Ordered list of patients waiting for service |
| **Wait Time** | Estimated duration a patient waits before service begins |
| **Service Time** | Duration of actual service/consultation |
| **Peak Hour** | Time period with highest number of patient arrivals |
| **Department** | Specialized service unit within the hospital (e.g., Cardiology, Pediatrics) |
| **Queue Number** | Unique identifier assigned to patient for tracking |
| **ML Model** | Trained artificial intelligence model for wait time prediction |
| **API** | Application Programming Interface for system integration |
| **MVP** | Minimum Viable Product with essential features only |

---

## Appendices
- **Flowcharts & System Diagrams**
## 1. Patient Booking Flow

```mermaid
flowchart TD
    A["Patient Visits Website"] --> B["Login/Register"]
    B --> C{User Authenticated?}
    C -->|No| B
    C -->|Yes| D["Browse Departments & Doctors"]
    D --> E["Select Department & Doctor"]
    E --> F["Choose Preferred Time Slot"]
    F --> G["ML Model Predicts Wait Time"]
    G --> H["Display Estimated Wait Time"]
    H --> I{Patient Confirms?}
    I -->|Cancel| D
    I -->|Confirm| J["Save Booking to Database"]
    J --> K["Generate Queue Number"]
    K --> L["Send Confirmation to Patient"]
    L --> M["Display Queue Tracking Page"]
    M --> N["Patient Monitors Queue Status"]
    N --> O["Patient Notified - Ready for Service"]
```

---

## 2. Queue Management & Wait Time Prediction Flow

```mermaid
flowchart TD
    A["New Patient Arrives"] --> B["System Fetches Queue Data"]
    B --> C["Retrieve Patient Profile & History"]
    C --> D["Get Doctor Schedule & Availability"]
    D --> E["Get Current Queue Status"]
    E --> F["Send Data to ML Model API"]
    F --> G["ML Model: Extract Features"]
    G --> H["ML Model: Make Prediction"]
    H --> I["Generate Wait Time Estimate"]
    I --> J["Evaluate Current Queue Load"]
    J --> K{Load Balanced?}
    K -->|High Load| L["Recommend Alternative Department"]
    K -->|Balanced| M["Assign to Booked Department"]
    L --> N{Patient Accepts Alternative?}
    N -->|Yes| O["Update Queue Assignment"]
    N -->|No| M
    M --> O
    O --> P["Update Queue Position"]
    P --> Q["Update Real-time Queue Display"]
    Q --> R["Patient Notified of Position"]
    R --> S{Service Started?}
    S -->|Yes| T["Mark Patient as In-Service"]
    S -->|No| U["Wait for Next Update"]
    U --> R
    T --> V["Log Service Time & Metrics"]
    V --> W["Update Database"]
```

---

## 3. Admin Dashboard Monitoring Flow

```mermaid
flowchart TD
    A["Admin Logs In"] --> B{Authentication}
    B -->|Failed| A
    B -->|Success| C["Access Admin Dashboard"]
    C --> D["Dashboard Loads Real-time Data"]
    D --> E["Fetch Active Queues from Database"]
    E --> F["Fetch Wait Time Predictions"]
    F --> G["Calculate Performance Metrics"]
    G --> H["Display Queue Status Cards"]
    H --> I["Display Analytics Graphs"]
    I --> J{Admin Action?}
    J -->|View Department Details| K["Show Queue for Selected Department"]
    J -->|View Doctor Schedule| L["Display Doctor Schedule & Availability"]
    J -->|View Analytics| M["Show Historical Data & Trends"]
    J -->|Manage Capacity| N["Adjust Department Capacity"]
    J -->|No Action| O["Dashboard Refreshes Every 5 Seconds"]
    K --> O
    L --> O
    M --> O
    N --> P["Update Database"]
    P --> O
    O --> Q{Admin Exits?}
    Q -->|No| J
    Q -->|Yes| R["End Session"]
```

---

## 4. System Architecture & Integration Flow

```mermaid
graph TB
    subgraph "Frontend Layer"
        PP["Patient Portal<br/>Next.js/React"]
        AD["Admin Dashboard<br/>Next.js/React"]
    end
    
    subgraph "API Gateway & Backend"
        BE["Node.js Express API<br/>- Auth Service<br/>- Queue Management<br/>- Data Processing"]
    end
    
    subgraph "Machine Learning Layer"
        ML["ML Model API<br/>FastAPI/Flask<br/>- Wait Time Prediction<br/>- Distribution Optimization"]
    end
    
    subgraph "Data Layer"
        DB["PostgreSQL Database<br/>- Users<br/>- Queues<br/>- Schedules<br/>- Logs"]
        CACHE["Cache Layer<br/>Redis Optional"]
    end
    
    subgraph "External Integration"
        BPJS["Mock BPJS API<br/>Insurance Verification"]
        EMAIL["Email Service<br/>Notifications"]
    end
    
    subgraph "Infrastructure & Deployment"
        VERCEL["Vercel<br/>Frontend Hosting"]
        RENDER["Render/Railway<br/>Backend Hosting"]
        SUPABASE["Supabase/Neon<br/>Database Hosting"]
    end
    
    PP -->|API Requests| BE
    AD -->|API Requests| BE
    BE -->|Query/Update| DB
    BE -->|Predict Wait Time| ML
    ML -->|Feature Data| DB
    BE -->|Verify Insurance| BPJS
    BE -->|Send Email| EMAIL
    DB -->|Cache| CACHE
    VERCEL -->|Hosts| PP
    VERCEL -->|Hosts| AD
    RENDER -->|Hosts| BE
    RENDER -->|Hosts| ML
    SUPABASE -->|Hosts| DB
    
    style PP fill:#e1f5ff
    style AD fill:#e1f5ff
    style BE fill:#fff3e0
    style ML fill:#f3e5f5
    style DB fill:#e8f5e9
    style CACHE fill:#fce4ec
    style BPJS fill:#fff9c4
    style EMAIL fill:#fff9c4
    style VERCEL fill:#c8e6c9
    style RENDER fill:#c8e6c9
    style SUPABASE fill:#c8e6c9
```

---

## 5. End-to-End User Journey Flow

```mermaid
flowchart TD
    A["Patient Opens App"] --> B["Login/Register"]
    B --> C["Home Page - Browse Departments"]
    C --> D["Select Department & Doctor"]
    D --> E["ML Model Calculates<br/>Wait Time Prediction"]
    E --> F["Show Estimated Wait Time<br/>& Peak Hour Info"]
    F --> G{Book Appointment?}
    G -->|No| C
    G -->|Yes| H["Choose Time Slot"]
    H --> I["Confirm Booking"]
    I --> J["Queue Number Assigned"]
    J --> K["Enter Queue Tracking Page"]
    K --> L["Real-time Updates:<br/>Position & Wait Time"]
    L --> M{Service Started?}
    M -->|No| N["Wait & Monitor"]
    N --> L
    M -->|Yes| O["Patient Called for Service"]
    O --> P["Receive Service"]
    P --> Q["Service Completed"]
    Q --> R["Get Receipt & Summary"]
    R --> S["Rate Experience"]
    S --> T["End Session"]
    
    style A fill:#e3f2fd
    style B fill:#e3f2fd
    style C fill:#e3f2fd
    style D fill:#fff3e0
    style E fill:#f3e5f5
    style F fill:#e8f5e9
    style G fill:#fce4ec
    style H fill:#fff3e0
    style I fill:#fff3e0
    style J fill:#e8f5e9
    style K fill:#e1f5ff
    style L fill:#e1f5ff
    style M fill:#fce4ec
    style N fill:#e1f5ff
    style O fill:#fff9c4
    style P fill:#c8e6c9
    style Q fill:#c8e6c9
    style R fill:#c8e6c9
    style S fill:#fce4ec
    style T fill:#ffccbc
```

---

## 6. Data Flow - Wait Time Prediction

```mermaid
flowchart LR
    A["Patient Data<br/>- ID<br/>- Department<br/>- Time"] -->|Extract| B["Feature Engineering"]
    C["Historical Data<br/>- Service Times<br/>- Peak Hours<br/>- Doctor Schedules"] -->|Extract| B
    D["Current Queue State<br/>- Queue Length<br/>- Avg Service Time<br/>- Load Factor"] -->|Extract| B
    
    B -->|Process Features| E["ML Model<br/>Regression/<br/>Time Series"]
    E -->|Predict| F["Wait Time<br/>Estimate"]
    F --> G["Display to User"]
    F -->|Log Prediction| H["Database"]
    H -->|Feedback Loop| E
    
    style A fill:#e3f2fd
    style C fill:#e3f2fd
    style D fill:#e3f2fd
    style B fill:#fff3e0
    style E fill:#f3e5f5
    style F fill:#e8f5e9
    style G fill:#c8e6c9
    style H fill:#ffccbc
```

---

## 7. System Deployment Flow

```mermaid
flowchart TD
    A["Development<br/>Local Environment"] --> B["Git Push to<br/>GitHub"]
    B --> C["CI/CD Pipeline<br/>GitHub Actions"]
    C --> D{Tests Pass?}
    D -->|No| E["Notify Developer<br/>Fix Issues"]
    E --> B
    D -->|Yes| F["Build Artifacts"]
    
    F --> G["Deploy Frontend<br/>to Vercel"]
    F --> H["Deploy Backend<br/>to Render"]
    F --> I["Deploy ML API<br/>to Render"]
    
    G --> J["Live Patient Portal<br/>https://app.example.com"]
    H --> K["Live Backend API<br/>https://api.example.com"]
    I --> L["Live ML API<br/>https://ml.example.com"]
    
    J --> M["Monitor Performance<br/>Sentry/LogRocket"]
    K --> M
    L --> M
    
    M --> N{Issues Detected?}
    N -->|Yes| O["Rollback or Hotfix"]
    O --> B
    N -->|No| P["Production Live ✓"]
    
    style A fill:#e3f2fd
    style B fill:#fff3e0
    style C fill:#fff3e0
    style D fill:#fce4ec
    style E fill:#ffccbc
    style F fill:#e8f5e9
    style G fill:#c8e6c9
    style H fill:#c8e6c9
    style I fill:#c8e6c9
    style J fill:#a5d6a7
    style K fill:#a5d6a7
    style L fill:#a5d6a7
    style M fill:#fff9c4
    style N fill:#fce4ec
    style O fill:#ffccbc
    style P fill:#81c784
```

---

## 8. API Request-Response Flow (Booking & Queue Tracking)

```mermaid
flowchart LR
    A["Patient<br/>Click Book"] --> B["Frontend App<br/>React/Next.js"]
    B -->|POST /api/booking/predict| C["Backend API<br/>Extract Features"]
    C -->|Query| D["Database<br/>Get Queue Data"]
    D -->|Data| C
    C -->|Feature Data| E["ML API<br/>Predict Wait Time"]
    E -->|Prediction| C
    C -->|Save Data| F["Save Booking<br/>Update Database"]
    F -->|Confirmation| C
    C -->|Response| G["Return Queue#<br/>& Estimated Time"]
    G -->|JSON| B
    B -->|Render UI| H["Queue Tracking<br/>Display on App"]
    H -->|Real-time Updates| A
    
    style A fill:#e3f2fd
    style B fill:#e3f2fd
    style C fill:#fff3e0
    style D fill:#e8f5e9
    style E fill:#f3e5f5
    style F fill:#e8f5e9
    style G fill:#c8e6c9
    style H fill:#a5d6a7
```

---

## Supplementary: Complete API Endpoint Reference

| Endpoint | Method | Purpose | Request | Response |
|----------|--------|---------|---------|----------|
| `/api/auth/login` | POST | Patient/Admin login | `{email, password}` | `{token, user}` |
| `/api/auth/register` | POST | New patient registration | `{name, email, password}` | `{token, user}` |
| `/api/departments` | GET | List all departments | - | `[{id, name, wait_time}]` |
| `/api/doctors` | GET | List doctors by department | `{dept_id}` | `[{id, name, specialty}]` |
| `/api/booking/predict` | POST | Predict wait time & book | `{dept_id, doctor_id, time}` | `{queue_num, wait_time}` |
| `/api/queue/status` | GET | Get queue position & status | `{queue_number}` | `{position, wait_time, status}` |
| `/api/queue/all` | GET | Admin: all active queues | - | `[{dept, position, count}]` |
| `/api/admin/metrics` | GET | Admin: performance metrics | - | `{avg_wait, throughput, load}` |
| `/api/admin/schedule` | PUT | Manage doctor schedules | `{doctor_id, schedule}` | `{success, updated}` |

---

## Legend

🟦 Blue = Frontend/User Interface  
🟧 Orange = API/Backend Processing  
🟪 Purple = Machine Learning  
🟩 Green = Database/Storage  
🟨 Yellow = External Services  
🟩 Light Green = Deployment/Production


- **Database Schema**
## ER Diagram

```mermaid
erDiagram
    USERS ||--o{ BOOKINGS : makes
    USERS ||--o{ QUEUE_HISTORY : tracks
    DEPARTMENTS ||--o{ DOCTORS : has
    DEPARTMENTS ||--o{ QUEUES : manages
    DOCTORS ||--o{ DOCTOR_SCHEDULES : works
    DOCTORS ||--o{ SERVICES : provides
    BOOKINGS ||--o{ QUEUES : creates
    QUEUES ||--o{ QUEUE_HISTORY : logs
    SERVICES ||--o{ QUEUE_HISTORY : records
    QUEUES ||--o{ PREDICTIONS : generates

    USERS {
        int user_id PK
        string email UK
        string password_hash
        string full_name
        string phone
        string role
        string gender
        date date_of_birth
        text address
        string bpjs_number
        datetime created_at
        datetime updated_at
    }

    DEPARTMENTS {
        int dept_id PK
        string dept_name UK
        text description
        int capacity
        int current_load
        float avg_service_time
        datetime updated_at
    }

    DOCTORS {
        int doctor_id PK
        int dept_id FK
        string full_name
        string license_number
        string specialization
        string phone
        text bio
        float avg_consultation_time
        boolean is_active
        datetime created_at
    }

    DOCTOR_SCHEDULES {
        int schedule_id PK
        int doctor_id FK
        date schedule_date
        time start_time
        time end_time
        int max_patients
        int current_patients
        string status
        datetime created_at
    }

    BOOKINGS {
        int booking_id PK
        int user_id FK
        int doctor_id FK
        int dept_id FK
        datetime booking_datetime
        string status
        text notes
        datetime created_at
        datetime updated_at
    }

    QUEUES {
        int queue_id PK
        int booking_id FK
        int dept_id FK
        int queue_number
        int position
        int total_in_queue
        string status
        datetime arrival_time
        datetime called_time
        datetime service_start_time
        datetime service_end_time
        datetime created_at
        datetime updated_at
    }

    SERVICES {
        int service_id PK
        int queue_id FK
        int doctor_id FK
        int dept_id FK
        datetime service_start
        datetime service_end
        int actual_service_time
        string diagnosis
        text notes
        string service_status
        datetime created_at
    }

    QUEUE_HISTORY {
        int history_id PK
        int queue_id FK
        int user_id FK
        int dept_id FK
        int queue_position
        int predicted_wait_time
        int actual_wait_time
        float prediction_accuracy
        string event_type
        datetime event_timestamp
    }

    PREDICTIONS {
        int prediction_id PK
        int queue_id FK
        int dept_id FK
        int predicted_wait_minutes
        float confidence_score
        string model_version
        datetime prediction_time
        datetime created_at
    }
```
- Design Document (Figma Designs) - *To be created*
- API Specification - *To be created*
- ML Model Documentation - *To be created*
- Deployment Guide - *To be created*

---

**Document Version:** 1.0  
**Last Updated:** April 2026  
**Next Review:** Upon completion of Phase 1

