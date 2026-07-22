# 🚀 Cost-Aware AI IT Support Router

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![Next.js](https://img.shields.io/badge/Next.js-14-black)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![XGBoost](https://img.shields.io/badge/XGBoost-ML-orange)
![LangChain](https://img.shields.io/badge/LangChain-AI-success)
![LangSmith](https://img.shields.io/badge/LangSmith-Tracing-blueviolet)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)

A **production-inspired, cost-aware AI ticket routing system** that intelligently routes IT support requests using a hybrid AI architecture.

Instead of sending every ticket to an expensive Large Language Model, the system first uses a lightweight local **XGBoost classifier** for near-instant predictions. Only uncertain requests are escalated to **Google Gemini**, dramatically reducing inference cost while maintaining routing accuracy.

Beyond intelligent routing, the project demonstrates modern AI engineering practices including:

- 💰 FinOps (AI cost optimization)
- 🤖 Hybrid AI (Traditional ML + LLM)
- 👨‍💻 Human-in-the-Loop (HITL)
- 🔄 Dynamic model retraining
- 📊 AI observability with LangSmith
- 🔐 Role-Based Access Control (RBAC)
- 🐳 Dockerized full-stack deployment

The application includes dedicated dashboards for **Users, Department Agents, Administrators**, along with a **FinOps Dashboard** for monitoring AI performance, API costs, and routing analytics.

---

# 💡 Why this project?

Large Language Models are powerful—but they're also **slower and significantly more expensive** than traditional machine learning models.

This project explores a production-style hybrid AI approach where:

- Most tickets are classified using a fast local ML model.
- Only uncertain tickets are escalated to an LLM.
- Every LLM invocation is monitored for latency and cost.
- Human corrections continuously improve the routing model.

The result is an AI ticket router that is **cheaper, faster, observable, and continuously improving**.

---

# ✨ Key Features

- **Hybrid AI Routing Engine:** Uses `SentenceTransformers` + `XGBoost` for instant, **$0.00 cost routing**. If the ML model's confidence is below a configurable threshold, the request is automatically escalated to Google Gemini.
- **FinOps Dashboard:** Tracks total LLM API spend, estimated cost savings, ML autopilot success rate, latency comparisons, routing analytics, and model performance in real time.
- **Human-in-the-Loop (HITL):** Department agents can manually correct misrouted tickets, allowing the system to continuously improve through human feedback.
- **Dynamic Model Retraining:** Administrators can trigger a background retraining job that merges agent corrections with the original dataset, retrains the XGBoost model, and hot-swaps it into memory with **zero API downtime**.
- **Role-Based Access Control (RBAC):** Three user roles (Admin, Agent, Standard User) with dedicated dashboards and secure API endpoints.
- **AI Observability:** Integrated LangSmith tracing provides visibility into prompt execution, latency, token usage, and LLM behavior.
- **Full-Stack Dockerization:** Frontend, backend, and PostgreSQL database are fully containerized for one-command deployment.

---

# 🛠️ Architecture & Tech Stack

## Frontend

- Next.js 14
- React
- Tailwind CSS
- NextAuth (JWT Authentication)
- Lucide Icons

## Backend

- FastAPI
- Python
- SQLModel (SQLAlchemy)
- Pydantic

## Database

- PostgreSQL

## Machine Learning

- XGBoost
- SentenceTransformers (Hugging Face)
- Scikit-learn

## LLM & AI Observability

- Google Gemini 2.5 Flash
- LangChain
- LangSmith

## Infrastructure

- Docker
- Docker Compose

---

# 🧠 Hybrid AI Workflow

```text
User Ticket
      │
      ▼
Sentence Embedding
      │
      ▼
XGBoost Prediction
      │
      ▼
Confidence Score
      │
 ┌────┴──────────────┐
 │                   │
 │ Confidence ≥ 75%  │ Confidence < 75%
 ▼                   ▼
Route via ML     Gemini Flash
Cost: $0.00      via LangChain
Latency: ~60ms         │
                        ▼
               LangSmith Trace
                        │
                        ▼
             PostgreSQL Analytics
```

---

# ⚙️ How the Hybrid AI Engine Works

1. **Ticket Submission**
   - The user submits a subject and detailed description of an IT issue.

2. **Text Embedding**
   - A lightweight local SentenceTransformer model converts the ticket into a semantic vector embedding.

3. **Primary Prediction**
   - The XGBoost classifier predicts the appropriate department queue and returns a confidence score.

4. **Confidence Evaluation**

   - **Confidence ≥ 75%**
     - Ticket is routed using the local ML model.
     - **Estimated Cost:** `$0.00`
     - **Average Latency:** ~60 ms

   - **Confidence < 75%**
     - Ticket is automatically escalated to Google Gemini.
     - **Estimated Cost:** ~$0.002/request
     - **Average Latency:** ~1400 ms

5. **Analytics Logging**
   - Routing engine, confidence score, token usage, API cost, and latency are stored in PostgreSQL for FinOps analytics.

---

# 🔍 AI Observability

The project integrates **LangSmith** to trace and monitor every LLM invocation executed through LangChain.

Current observability includes:

- Prompt inspection
- Response inspection
- LLM latency monitoring
- Token usage tracking
- End-to-end execution traces
- Easier debugging of AI routing decisions

Since the primary router is the local XGBoost model, LangSmith is primarily used whenever the system falls back to Google Gemini.

---

# 📊 System Architecture

```text
                         User Ticket
                              │
                              ▼
               SentenceTransformer Embedding
                              │
                              ▼
                     XGBoost Classifier
                              │
                 ┌────────────┴────────────┐
                 │                         │
        Confidence ≥ 75%          Confidence < 75%
                 │                         │
                 ▼                         ▼
          Route via ML          Google Gemini Flash
          Cost: $0.00             via LangChain
          Latency: ~60ms                 │
                                         ▼
                                 LangSmith Tracing
                                         │
                                         ▼
                               PostgreSQL Analytics
                                         │
                                         ▼
                            FinOps Dashboard & Reports
```

---

# 🚀 Installation & Setup

## Prerequisites

- Docker
- Docker Compose
- Google Gemini API Key
- LangSmith API Key (optional, for AI tracing)

---

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/cost-aware-it-support-router.git
cd cost-aware-it-support-router
```

---

## 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
# ===========================
# Google Gemini
# ===========================

GOOGLE_API_KEY=your_google_api_key

# Cost Configuration
GEMINI_FLASH_COST_PER_1M=0.15

# ===========================
# LangSmith (Tracing)
# ===========================

LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=cost-aware-it-support-router

# ===========================
# PostgreSQL
# ===========================

POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=it_support_router
POSTGRES_HOST=localhost
POSTGRES_PORT=5433

# ===========================
# Backend
# ===========================

SECRET_KEY=your_secret_key
```

---

## 3. Build & Run

```bash
docker compose up --build -d
```

---

## 🌐 Access the Application

### Frontend

```
http://localhost:3000
```

### Backend API Documentation

```
http://localhost:8000/docs
```

---

# 📊 Dashboards

The application provides dedicated dashboards tailored to each user role.

## 👤 Standard User Dashboard

- Submit new IT support tickets
- Track ticket status
- View ticket history
- Receive routed department information

---

## 👨‍🔧 Department Agent Dashboard

- View assigned department tickets
- Correct incorrectly routed tickets
- Update ticket status
- Provide Human-in-the-Loop feedback

---

## 👑 Administrator Dashboard

- Manage Users
- Manage Department Agents
- Trigger AI retraining
- Monitor routing statistics
- View system activity

---

## 💰 FinOps Dashboard

Track the operational efficiency of the AI routing engine through real-time analytics:

- Total LLM API Spend
- Estimated Cost Savings
- ML vs LLM Routing Ratio
- Average ML Latency
- Average LLM Latency
- Autopilot Success Rate
- Routing Engine Distribution
- Token Usage Analytics

---

# 🎮 Usage Guide

## 1. Initial Administrator Login

On the first application startup, the backend automatically checks whether any users exist in the database.

If the database is empty, it seeds a default administrator account:

```text
Username: admin
Password: admin123
```

> **Note:** The admin account is created **only once** during the initial startup. If users already exist, the seeder is skipped.

After logging in as **admin**, you can:

- Create Department Agents
- Create Standard Users
- Manage the system
- Trigger AI model retraining
- Monitor the FinOps dashboard

---

## 2. Create Department Agents

Log into the frontend as **admin** with password **admin123**.

Navigate to:

```
Manage Users & Agents
```

Create department agents such as:

- IT Support
- Billing & Finance
- Human Resources
- Network Operations

---

## 3. Submit Tickets

Log in as a standard user and submit different support requests.

Examples:

- Password reset
- VPN not connecting
- Payroll issue
- Software installation
- Email not syncing

Observe how the router automatically selects the correct department.

---

## 4. Human-in-the-Loop Learning

Department agents review routed tickets.

If a ticket is incorrectly classified:

- Select the correct department.
- Save the correction.

The correction is automatically stored in PostgreSQL for future model retraining.

---

## 5. Retrain the AI Router

Log back in as **admin**.

Click:

```
Retrain AI Router
```

The backend automatically performs:

1. Load the original labeled dataset.
2. Retrieve all human corrections from PostgreSQL.
3. Merge corrections into the training dataset.
4. Retrain the XGBoost routing model.
5. Save the updated model.
6. Hot-swap the model into memory.
7. Continue serving requests without restarting the API.

This enables continuous learning with **zero downtime**.

---

# 🔄 Human-in-the-Loop Learning Pipeline

```text
Agent Reviews Ticket
          │
          ▼
Correct Department Selected
          │
          ▼
Correction Saved to PostgreSQL
          │
          ▼
Administrator Triggers Retraining
          │
          ▼
Merge Original Dataset
        +
Agent Corrections
          │
          ▼
Retrain XGBoost Model
          │
          ▼
Save New Model
          │
          ▼
Hot Swap into Memory
          │
          ▼
Improved Future Predictions
```

---

# 📂 Project Structure

```text
cost-aware-it-support-router/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── db/
│   │   ├── services/
│   │   ├── auth.py
│   │   ├── model_manager.py
│   │   └── main.py
│   │
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── app/
│   ├── public/
│   ├── Dockerfile
│   └── package.json
│
├── ml_pipeline/
│   ├── data/
│   ├── training/
│   ├── models/
│   └── artifacts/
│
├── docker-compose.yml
├── .env
└── README.md
```

---

# 📊 What Makes This Project Different?

Unlike traditional ticketing systems that rely entirely on LLMs, this project adopts a **hybrid AI architecture** that prioritizes speed, cost efficiency, and continuous learning.

Key engineering highlights include:

- ✅ Hybrid AI (Traditional ML + LLM)
- ✅ Cost-aware AI routing (FinOps)
- ✅ Human-in-the-Loop learning
- ✅ Dynamic model retraining
- ✅ Zero-downtime model updates
- ✅ LangSmith AI observability
- ✅ Role-Based Access Control (RBAC)
- ✅ Real-time FinOps analytics
- ✅ Dockerized full-stack deployment
- ✅ Production-inspired AI architecture

---

# 🔮 Future Enhancements

## 🧠 Out-of-Distribution (OOD) Detection

Introduce an absolute confidence threshold (for example **<40%**) to identify spam, irrelevant, or previously unseen ticket categories and automatically route them to a manual triage queue.

---

## 📚 Retrieval-Augmented Generation (RAG)

Integrate the routing engine with an internal knowledge base so users receive instant troubleshooting suggestions before their ticket is routed to a human agent.

---

## 📈 Explainable AI

Display confidence scores and feature importance to explain why the model selected a specific department.

---

## 📊 Advanced Monitoring

Integrate Prometheus and Grafana for infrastructure monitoring alongside LangSmith traces.

---

## 🤖 Multi-Model Routing

Experiment with multiple local ML models and dynamically choose the best routing strategy based on confidence and historical performance.

---

## 👨‍💻 Author

Built as a portfolio project demonstrating modern AI engineering concepts, including:

- Hybrid AI Systems
- Machine Learning
- Large Language Models
- FinOps
- Human-in-the-Loop Learning
- LangSmith Observability
- FastAPI
- Next.js
- PostgreSQL
- Docker
