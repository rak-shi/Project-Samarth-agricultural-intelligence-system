# 🌾 Project Samarth — System Architecture

## Three-Layer Architecture

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ USER INTERFACE LAYER 
┃ (Streamlit) ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ 📝 Natural Language Query Input ┃
┃ 📊 Interactive Results Display ┃
┃ 🔗 Source Citation Rendering ┃
┃ 📈 Progress Indicators & Metrics ┃
┗━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
│
▼
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ QUERY ENGINE (Intelligence Layer) ┃
┃ (query_engine.py) ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ 🔍 Query Classification ┃
┃ ├─ Comparative Analysis ┃
┃ ├─ District-Level Analysis ┃
┃ ├─ Trend Analysis ┃
┃ ├─ Policy Recommendation ┃
┃ └─ Simple Lookup ┃
┃ 🧩 Entity Extraction ┃
┃ ├─ States (31 recognized) ┃
┃ ├─ Crops (rice, wheat, maize, sugarcane, cotton) ┃
┃ ├─ Years/Time Ranges ┃
┃ └─ Numeric Parameters (top N, last M years) ┃
┃ 🔀 Data Integration ┃
┃ ├─ Multi-source data merging ┃
┃ ├─ Temporal alignment ┃
┃ ├─ Schema normalization ┃
┃ └─ Aggregation & correlation ┃
┃ 📌 Citation Management ┃
┃ └─ Automatic source attribution ┃
┗━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
│
▼
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ DATA ACCESS LAYER (API Integration) ┃
┃ (data_fetch.py) ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ ┌────────────────────────────┐ ┌────────────────────────┐┃
┃ │ MINISTRY OF AGRICULTURE │ │ INDIA METEOROLOGICAL │┃
┃ │ & FARMERS WELFARE │ │ DEPARTMENT (IMD) │┃
┃ │ 🌾 Crop Production Data │ │ 🌧️ Rainfall Data │┃
┃ │ - State/District-wise │ │ - Daily district data │┃
┃ │ - 5 major crops │ │ - Multi-year coverage │┃
┃ │ - Area & Production │ │ - Historical records │┃
┃ │ - Yearly aggregation │ │ - Millimeter precision │┃
┃ │ 📊 Schema: │ │ 📊 Schema: │┃
┃ │ state_name │ │ State │┃
┃ │ district_name │ │ District │┃
┃ │ crop │ │ Year │┃
┃ │ crop_year │ │ Rainfall (mm) │┃
┃ │ production_ (tonnes) │ │ Date │┃
┃ │ area_ (hectares) │ │ │┃
┃ └────────────────────────────┘ └────────────────────────┘┃
┃ 🔄 API Features: ┃
┃ - Pagination (1000 records/request) ┃
┃ - Error handling & timeouts ┃
┃ - Real-time data (no caching) ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

text

---

## Example Data Flow

**Query**: *Compare rainfall in Kerala and Tamil Nadu for last 5 years and show top 3 crops*

📝 USER INPUT
|
▼
🔍 Query Classification & Entity Extraction

Type: Comparative Analysis + Top Crops

States: Kerala, Tamil Nadu

Years: 2020-2024

Top N: 3
|
▼
📡 Data Fetch (parallel API calls)

IMD rainfall for both states

Crop data for both states
|
▼
🔀 Data Integration

Aggregate rainfall

Rank crops by production

Add source citations
|
▼
📊 Output Display

Average rainfall with citation

Top crops per state with citation

text

---

## Key Design Principles

- **Pattern-based query classification:** Fast, interpretable, and flexible
- **Entity extraction:** Extracts states, crops, years, and numeric parameters from varied natural language queries
- **Real-time API integration:** Always fresh data; no caching complications
- **Pagination strategy:** Handles data.gov.in’s 1000 record/request limit automatically
- **Schema normalization:** Handles different column names and data formats
- **Automatic source citation:** Every result references its originating dataset

---

## Performance Highlights

- **Accuracy:** 100% (no predictions, only sourced facts)
- **Traceability:** Every claim is cited
- **Speed:** 2–5 seconds per query

---

## Example Technologies Used

| Layer      | Technology   | Why?                           |
|------------|-------------|--------------------------------|
| UI         | Streamlit   | Fast prototyping, interactive  |
| Engine     | Pandas      | Industry-standard data ops     |
| API Client | Requests    | Robust HTTP library            |
| NLP        | Regex       | Lightweight, interpretable     |

---

## Core Query Types Supported

- Comparative analysis (state/state, crop/crop)
- District-level comparisons (highest/lowest)
- Multiyear trend analysis with correlation
- Policy recommendation synthesis
- Top-N rankings
- Simple queries

---

*Built for accuracy, traceability, and real-time integration using public government data.*

