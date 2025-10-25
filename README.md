# 🌾 Project Samarth — Agricultural Intelligence System

An intelligent Q&A system that integrates heterogeneous agricultural and climate data from data.gov.in to provide accurate, cited, data-driven insights for policy recommendations.



## 📊 Data Sources

### 1. Ministry of Agriculture & Farmers Welfare
- **Dataset**: District-wise Crop Production Statistics
- **Coverage**: 31 States & UTs, 5 major crops
- **Key Fields**: 
  - `state_name`, `district_name`, `crop`
  - `crop_year`, `production_` (tonnes)
  - `area_` (hectares)

### 2. India Meteorological Department (IMD)
- **Dataset**: Daily District-wise Rainfall Data
- **Coverage**: All districts, multi-year historical records
- **Key Fields**:
  - `State`, `District`, `Year`
  - `Rainfall` (mm), `Date`

---

## 🔄 Example Data Flow

**Query**: *"Compare rainfall in Kerala and Tamil Nadu for last 5 years and show top 3 crops"*

📝 User Query
↓
🔍 Classification & Entity Extraction

Type: Comparative Analysis

States: [Kerala, Tamil Nadu]

Years: [2020-2024]

Top N: 3
↓
📡 Parallel API Calls

Fetch Kerala rainfall (2020-2024)

Fetch Tamil Nadu rainfall (2020-2024)

Fetch crop data for both states
↓
🔀 Data Integration

Aggregate rainfall by year

Rank crops by production

Add source citations
↓
📊 Response Generation

Kerala: 2,845 mm (avg)
📌 Source: IMD Dataset

Tamil Nadu: 1,234 mm (avg)
📌 Source: IMD Dataset

Top 3 Crops per state
📌 Source: Agriculture Dataset

text

---

## 🎯 Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Pattern-based Query Classification** | Fast, interpretable, no ML training needed |
| **Real-time API Integration** | Always fresh data, no cache staleness |
| **Automatic Source Citation** | Every claim traceable to origin dataset |
| **Schema Normalization** | Handles heterogeneous data structures |
| **Pagination Strategy** | Overcomes API 1000-record limit |

---

## ⚙️ Technical Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **UI** | Streamlit | Fast prototyping, Python-native |
| **Processing** | Pandas | Industry-standard data operations |
| **API Client** | Requests | Reliable HTTP communication |
| **NLP** | Regex | Lightweight entity extraction |

---

## 📈 Performance Metrics

- **Accuracy**: 100% (no predictions, only sourced facts)
- **Traceability**: Every data point cited
- **Response Time**: 2-5 seconds per query
- **Data Freshness**: Real-time (no caching)

---

## 🔍 Supported Query Types

✅ **Comparative Analysis** - Multi-state/crop comparisons  
✅ **District-Level Analysis** - Highest/lowest production  
✅ **Trend Analysis** - Multi-year patterns with correlation  
✅ **Policy Recommendations** - Data-backed arguments  
✅ **Top-N Rankings** - Most produced crops by volume  
✅ **Simple Queries** - Single-dimension lookups  

---

## 🚀 Sample Queries

"Compare rainfall in Kerala and Tamil Nadu for last 5 years and show top 3 crops"

"District with highest rice production in Punjab vs lowest in Bihar"

"Analyze wheat production trend in Punjab over last decade"

"Policy to promote rice over wheat in Maharashtra based on last 5 years"

"What are the top 5 most produced crops in Punjab?"

text

---

## 🔒 Core Values

- **Accuracy & Traceability**: Every claim sourced and cited
- **Data Sovereignty**: Can be deployed in secure, private environments
- **Real-time Integration**: No stale data
- **Simplicity**: Interpretable, maintainable architecture

---

## 📦 Project Structure

project-samarth/
├── app.py # Streamlit UI
├── query_engine.py # Query processing & classification
├── data_fetch.py # API integration layer
├── requirements.txt # Python dependencies
└── README.md # This file

text

---

## 🛠️ Installation & Usage

Install dependencies
pip install -r requirements.txt

Run the application
streamlit run app.py

text

---

## 📝 License

Built for accurate, traceable, data-driven policy decisions using public government data from data.gov.in.

---

*Project Samarth - Agricultural Intelligence System*
