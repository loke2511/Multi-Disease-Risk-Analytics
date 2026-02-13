# 📊 System Flowcharts

## 1. User Journey Flow

```mermaid
flowchart TD
    Start([User Visits Platform]) --> CheckAuth{Logged In?}
    CheckAuth -->|No| Register[Register/Login]
    Register --> Dashboard
    CheckAuth -->|Yes| Dashboard[View Dashboard]
    
    Dashboard --> SelectDisease[Select Disease for Prediction]
    SelectDisease --> FillForm[Fill Symptom Form<br/>Age, symptoms, lifestyle]
    FillForm --> Submit[Submit Form]
    
    Submit --> AIProcess[AI Analyzes Symptoms<br/>Using ML Model]
    AIProcess --> Result[View Risk Assessment<br/>Probability + Recommendations]
    
    Result --> Decision{What Next?}
    Decision -->|Download Report| PDF[Generate PDF Report]
    Decision -->|View History| History[View Past Predictions]
    Decision -->|Analytics| Analytics[View Trends Dashboard]
    Decision -->|New Prediction| SelectDisease
    
    PDF --> End([User Gets Report])
    History --> End
    Analytics --> End
```

---

## 2. System Architecture Flow

```mermaid
flowchart LR
    User([User Browser]) -->|HTTP Request| Frontend[Frontend Layer<br/>HTML/CSS/JS]
    
    Frontend -->|Form Data| Backend[Flask Backend<br/>Routes + Controllers]
    
    Backend --> Auth[Authentication<br/>Flask-Login]
    Backend --> Prediction[Prediction Service<br/>ML Models]
    Backend --> PDFGen[PDF Generator<br/>ReportLab]
    
    Auth --> DB[(SQLite Database<br/>Users + History)]
    Prediction --> Models[ML Models<br/>Random Forest<br/>15 Diseases]
    Prediction --> DB
    PDFGen --> Reports[PDF Reports]
    
    Backend -->|JSON Response| Frontend
    Frontend -->|Display| User
```

---

## 3. ML Prediction Flow

```mermaid
flowchart TD
    Input[User Inputs Symptoms] --> Preprocess[Data Preprocessing<br/>Normalize, Scale, Encode]
    Preprocess --> LoadModel[Load Trained ML Model<br/>Random Forest]
    
    LoadModel --> Predict[Model Makes Prediction<br/>Risk Probability 0-100%]
    Predict --> RiskCalc{Calculate Risk Level}
    
    RiskCalc -->|0-40%| Low[Low Risk<br/>Green Badge]
    RiskCalc -->|40-70%| Medium[Medium Risk<br/>Orange Badge]
    RiskCalc -->|70-100%| High[High Risk<br/>Red Badge]
    
    Low --> Recommend[Generate Recommendations]
    Medium --> Recommend
    High --> Recommend
    
    Recommend --> Save[Save to Database<br/>User History]
    Save --> Display[Display Results to User<br/>Gauge + Advice + Tests]
```

---

## 4. Data Flow Diagram

```mermaid
flowchart TB
    subgraph Input Layer
        A1[User Registration Data]
        A2[Symptom Inputs]
        A3[Lifestyle Data]
    end
    
    subgraph Processing Layer
        B1[Authentication Module]
        B2[ML Prediction Engine]
        B3[Analytics Engine]
        B4[PDF Generator]
    end
    
    subgraph Data Layer
        C1[(User Table)]
        C2[(Prediction Table)]
        C3[ML Model Files]
        C4[Generated PDFs]
    end
    
    subgraph Output Layer
        D1[Risk Dashboard]
        D2[PDF Reports]
        D3[Analytics Charts]
        D4[Prediction History]
    end
    
    A1 --> B1 --> C1
    A2 --> B2 --> C2
    A3 --> B2
    B2 --> C3
    
    C1 --> D1
    C2 --> D1
    C2 --> B4 --> C4 --> D2
    C2 --> B3 --> D3
    C2 --> D4
```

---

## 5. Complete System Workflow

```mermaid
flowchart TD
    Start([System Start]) --> Init[Initialize Flask App]
    Init --> LoadDB[Connect to SQLite Database]
    LoadDB --> LoadModels[Load ML Models into Memory]
    
    LoadModels --> Ready{Server Running<br/>localhost:5000}
    
    Ready -->|User Request| Route{Request Type?}
    
    Route -->|/register| RegRoute[Registration Route]
    Route -->|/login| LoginRoute[Login Route]
    Route -->|/predict| PredRoute[Prediction Route]
    Route -->|/analytics| AnalRoute[Analytics Route]
    Route -->|/download| PDFRoute[PDF Download Route]
    
    RegRoute --> ValidateReg{Valid Data?}
    ValidateReg -->|Yes| CreateUser[Create User in DB]
    ValidateReg -->|No| Error1[Show Error]
    CreateUser --> Success1[Redirect to Dashboard]
    
    LoginRoute --> AuthCheck{Valid Credentials?}
    AuthCheck -->|Yes| CreateSession[Create Session]
    AuthCheck -->|No| Error2[Show Login Error]
    CreateSession --> Success2[Redirect to Dashboard]
    
    PredRoute --> GetForm[Get Symptom Form]
    GetForm --> UserFills[User Fills Form]
    UserFills --> ValidateInput{Valid Input?}
    ValidateInput -->|No| Error3[Show Validation Error]
    ValidateInput -->|Yes| CallML[Call ML Prediction Service]
    
    CallML --> Preprocess[Preprocess Input]
    Preprocess --> RunModel[Run Random Forest Model]
    RunModel --> GetProba[Get Probability Score]
    GetProba --> CalcRisk[Calculate Risk Level]
    CalcRisk --> SaveDB[Save Prediction to Database]
    SaveDB --> ShowResult[Display Result Page]
    
    AnalRoute --> FetchHistory[Fetch User's Predictions]
    FetchHistory --> GenerateCharts[Generate Analytics Charts]
    GenerateCharts --> ShowAnalytics[Display Analytics Dashboard]
    
    PDFRoute --> FetchPred[Fetch Prediction by ID]
    FetchPred --> GenPDF[Generate PDF with ReportLab]
    GenPDF --> SendFile[Send PDF File to User]
    
    ShowResult --> End([User Receives Output])
    ShowAnalytics --> End
    SendFile --> End
    Success1 --> End
    Success2 --> End
    Error1 --> End
    Error2 --> End
    Error3 --> End
```

---

## 6. Database Schema Flow

```mermaid
erDiagram
    USER ||--o{ PREDICTION : makes
    USER {
        int id PK
        string username
        string email
        string password_hash
        datetime created_at
    }
    PREDICTION {
        int id PK
        int user_id FK
        string disease_type
        float risk_probability
        string risk_level
        json input_features
        datetime created_at
    }
```

---

## Legend

- **🟢 Green** = Low Risk (0-40%)
- **🟠 Orange** = Medium Risk (40-70%)
- **🔴 Red** = High Risk (70-100%)

---

## How to Use This Document

1. **For Presentation**: Screenshot these flowcharts and add to your PPT
2. **On GitHub**: These Mermaid diagrams render automatically on GitHub
3. **For Viva**: Explain each flowchart to demonstrate system understanding

