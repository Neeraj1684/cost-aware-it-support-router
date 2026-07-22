# 🚀 Cost-Aware IT Support Router

An enterprise-grade, cost-aware AI ticketing system that intelligently routes IT support requests. It utilizes a hybrid AI architecture—employing a fast, free local Machine Learning model (XGBoost) as the primary router, and seamlessly falling back to a Large Language Model (Gemini) only when necessary.

By tracking API costs, latency, and agent corrections, this system demonstrates advanced **FinOps**, **Human-in-the-Loop (HITL)** active learning, and dynamic model retraining.

---

## ✨ Key Features

- **Hybrid AI Routing Engine:** Uses `SentenceTransformers` + `XGBoost` for instant, **$0.00 cost routing**. If the ML model's confidence is below a configurable threshold, it escalates to a Large Language Model for zero-shot classification.
- **FinOps Dashboard:** Tracks total LLM API spend, estimated cost savings, ML autopilot success rate, latency comparisons, and routing analytics in real time.
- **Human-in-the-Loop (HITL) Retraining:** Department agents can manually correct misrouted tickets. An admin can trigger background retraining that merges corrections with the original dataset, retrains the XGBoost model, and hot-swaps it into memory with **zero API downtime**.
- **Role-Based Access Control (RBAC):** Three user roles (Admin, Agent, Standard User) with dedicated dashboards and secure API endpoints.
- **Full-Stack Dockerization:** Frontend, backend, and PostgreSQL database are fully containerized for one-command deployment.

---

## 🛠️ Architecture & Tech Stack

### Frontend
- Next.js 14
- React
- Tailwind CSS
- NextAuth (JWT Authentication)
- Lucide Icons

### Backend
- FastAPI
- Python
- SQLModel (SQLAlchemy)
- Pydantic

### Database
- PostgreSQL

### Machine Learning
- XGBoost
- Scikit-learn
- SentenceTransformers (Hugging Face)

### LLM Integration
- LangChain
- LiteLLM
- Google Gemini Pro

### Infrastructure
- Docker
- Docker Compose

---

## 🧠 How the Hybrid AI Engine Works

1. **Ticket Submission**
   - The user submits a subject and description for an IT issue.

2. **Text Embedding**
   - The backend generates a vector embedding using a lightweight local NLP model.

3. **Primary Prediction**
   - The XGBoost classifier predicts the target department and outputs a confidence score.

4. **Decision Logic**
   - **Confidence ≥ 75%**
     - Ticket is routed using the local ML model.
     - **Cost:** `$0.00`
     - **Latency:** ~60 ms

   - **Confidence < 75%**
     - Ticket is escalated to the Gemini LLM.
     - **Cost:** ~$0.002/request
     - **Latency:** ~1400 ms

5. **Analytics Logging**
   - Routing engine, confidence, token usage, API cost, and latency are logged to PostgreSQL for the FinOps dashboard.

---

## 🚀 Installation & Setup

### Prerequisites

- Docker
- Docker Compose
- Google Gemini API Key

---

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/cost-aware-it-support-router.git
cd cost-aware-it-support-router
```

---

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@db:5432/it_support_router
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=it_support_router

# NextAuth
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your_super_secret_key_here

# LLM API
GEMINI_API_KEY=your_gemini_api_key_here
```

---

### 3. Build & Run

```bash
docker compose up --build -d
```

---

### Access the Application

**Frontend**

```
http://localhost:3000
```

**Backend API Docs**

```
http://localhost:8000/docs
```

---

## 🎮 Usage Guide

### 1. Bootstrap the Admin

Open the FastAPI Swagger UI:

```
http://localhost:8000/docs
```

Use the endpoint:

```
POST /api/v1/auth/register
```

Create an account with the username:

```
luffy
```

> **Note:** The username `luffy` is hardcoded as the master administrator.

---

### 2. Create Department Agents

1. Log into the frontend as **luffy**.
2. Open **Manage Users & Agents**.
3. Create department agents (for example, **Billing & Finance**).

---

### 3. Generate Tickets

Log in as a standard user and submit various IT support tickets.

---

### 4. Trigger Human-in-the-Loop Learning

#### Agent

- Review assigned tickets.
- Correct any misrouted ticket using the department dropdown.

#### Admin

- Log back in as **luffy**.
- Click **Retrain AI Router**.

The backend will:

- Merge agent corrections
- Retrain the XGBoost model
- Replace the in-memory model
- Continue serving requests without downtime

---

## 📊 What Makes This Project Different?

- ✅ Hybrid AI (ML + LLM)
- ✅ Cost-aware routing (FinOps)
- ✅ Human-in-the-loop feedback system
- ✅ Active learning & dynamic retraining
- ✅ Zero-downtime model updates
- ✅ Enterprise RBAC
- ✅ Real-time analytics dashboard
- ✅ Dockerized full-stack deployment

---

## 🔮 Future Enhancements

### Out-of-Distribution (OOD) Detection

Implement an absolute confidence threshold (e.g., **<40%**) to detect spam, irrelevant requests, or unknown issue types and automatically route them to a manual triage queue.

### Retrieval-Augmented Generation (RAG)

Connect the routing engine to an internal knowledge base so users receive instant troubleshooting suggestions before the ticket is routed to a human agent.

---

## 📄 License

This project is licensed under the MIT License.

---

## ⭐ If you found this project interesting...

Consider giving it a **⭐ on GitHub**!