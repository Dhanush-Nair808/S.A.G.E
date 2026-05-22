# S.A.G.E - Support And Guidance Expert

**S.A.G.E** is a full-stack AI-powered customer support system that intelligently classifies support tickets, analyzes sentiment, generates professional responses, and continuously improves through user feedback.

It combines **Machine Learning**, **Sentiment Analysis**, **Policy-aware LLM responses (RAG)**, and a clean user interface for both customers and support teams.

---

## ✨ Features

- **Ticket Classification**: Automatically categorizes reviews into `account_access`, `billing`, `bug_report`, `refund_request`, `shipping_delivery`, etc.
- **Sentiment Analysis**: Detects Positive/Negative sentiment using transformer models.
- **Policy-Grounded AI Responses**: Uses RAG (Retrieval-Augmented Generation) to retrieve relevant company policy sections and generate accurate replies via Mistral AI.
- **Closed-Loop Feedback**: Users can rate responses → model automatically retrains on new data.
- **Interactive Chatbot**: Real-time conversational support.
- **Analytics Dashboard**: Live statistics on reviews, satisfaction, and category distribution.
- **User Authentication**: Secure registration and login system.
- **Modern UI**: Clean, Amazon-inspired Streamlit frontend.

---

## 🏗️ How It Works

1. **Submit Review** → User writes a support ticket/review.
2. **ML Processing** → Scikit-learn pipelines classify category and analyze sentiment.
3. **RAG Retrieval** → Relevant sections from company policy documents are fetched.
4. **Response Generation** → Mistral LLM generates a professional, policy-aligned reply.
5. **Feedback Loop** → User rates the response → system retrains the classification model.
6. **Analytics & History** → All activity is logged and visualized.

---

## 🛠 Tech Stack

| Component          | Technology                                      |
|--------------------|-------------------------------------------------|
| Backend            | FastAPI, SQLAlchemy, SQLite                     |
| Frontend           | Streamlit                                       |
| ML Classification  | scikit-learn (Logistic Regression, SVM, NB)     |
| Sentiment Analysis | Hugging Face Transformers                       |
| RAG / LLM          | LangChain, ChromaDB, Mistral AI                 |
| Vector Embeddings  | Sentence-Transformers                           |
| Authentication     | JWT + bcrypt                                    |
| Others             | Joblib, Pandas, Plotly                          |

---

## 📁 Project Structure

```bash
S.A.G.E/
├── backend/
│   ├── main.py                 # FastAPI endpoints
│   ├── ml/                     # ML models & inference
│   ├── rag/                    # RAG ingestion & retrieval
│   ├── services/               # Business logic
│   └── database/               # Models & DB setup
├── frontend/
│   └── app.py                  # Streamlit UI
├── docs/                       # Company policy PDFs
├── backend/ml/models/          # Trained models (large files)
├── backend/chroma_db/          # Vector database
├── data/                       # SQLite database
├── ML_SAGE_Modified.ipynb      # Model training notebook
├── requirements.txt
├── run_app.ps1
└── .env
```

🚀 Quick Start
1. Clone the Repository
Bashgit clone <your-repo-url>
cd S.A.G.E
2. Setup Environment
Bashpython -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
3. Environment Variables
Create a .env file in the root:
envMISTRAL_API_KEY=your_mistral_api_key_here
MISTRAL_MODEL=mistral-small-latest
4. Prepare ML Models (Important)
Since model files are too large for GitHub:

Open ML_SAGE_Modified.ipynb
Run all cells from top to bottom
This will train the models and save them to backend/ml/models/

Alternatively, you can run the final export cells manually.
5. Setup RAG (Company Policy Knowledge)
Bash# Place your policy PDFs in the docs/ folder
# Then run:
python backend/rag/ingest.py
6. Initialize Database
Bashpython -c "from backend.database.init_db import *; print('DB initialized')"

▶️ Running the Application
Recommended (One-click)
PowerShell./run_app.ps1
This starts both backend and frontend and opens the browser.
Manual Start
Bash# Terminal 1 - Backend
uvicorn backend.main:app --reload --port 8000

# Terminal 2 - Frontend
streamlit run frontend/app.py

🔄 Updating the System

Add new policies: Put PDFs in docs/ → re-run ingest.py
Improve classification: Submit feedback in the app → model retrains automatically
Retrain manually: Use the notebook or call retraining endpoint


📊 Key Directories (Add to .gitignore)
gitignorevenv/
.env
__pycache__/
backend/ml/models/
backend/chroma_db/
*.db

🤝 Contributing
Contributions are welcome! You can help with:

Adding more ML models
Improving RAG retrieval quality
Enhancing the UI/UX
Adding new features (notifications, multi-language, etc.)


S.A.G.E — Making customer support Smarter, Accurate, Grounded, and Efficient.

This version gives equal weight to ML classification, sentiment analysis, RAG, feedback loop, UI, and deployment aspects.
