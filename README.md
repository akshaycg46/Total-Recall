---

# TotalRecall 🧠

**TotalRecall** is an AI-powered personal memory assistant. It allows you to record thoughts or information via speech, stores them as high-dimensional vector embeddings, and enables semantic retrieval so you can "recall" details later just by asking.

---

## 🚀 Features

* **Voice-to-Memory:** Capture notes hands-free using Google Speech Recognition.
* **Semantic Search:** Uses `BAAI/bge-small-en-v1.5` embeddings to find the *meaning* of your query, not just keywords.
* **Vector Storage:** Powered by PostgreSQL and the `pgvector` extension for efficient similarity searching.
* **Local & Cloud LLM Support:** Integration with local models (via GPT4All or LocalAI) and OpenAI's GPT models.
* **Text-to-Speech:** Responds to your queries vocally, creating a conversational loop.

---

## 🛠️ Architecture

The application is split into two primary workflows:

1. **Ingestion (`main.py`):** Microphone Input → Speech-to-Text → Embedding Generation → PostgreSQL.
2. **Recall (`recall.py`):** Microphone Input → Embedding Generation → Vector Similarity Search (`pgvector`) → Context Retrieval → LLM Response → Text-to-Speech.

---

## 📋 Prerequisites

* **Python 3.8+**
* **PostgreSQL** with the [pgvector](https://github.com/pgvector/pgvector) extension installed.
* **FFmpeg** (required for some audio processing).
* **PortAudio** (for `PyAudio` / `speech_recognition`).

---

## 🔧 Setup & Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/totalrecall.git
cd totalrecall

```


2. **Install dependencies:**
```bash
pip install sqlalchemy psycopg2-binary pgvector sentence-transformers openai speechrecognition gpt4all torch

```


3. **Database Configuration:**
Ensure your PostgreSQL server is running and create the extension:
```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE test (id SERIAL PRIMARY KEY, content TEXT, embedding VECTOR(384));

```


*Update the database credentials in `db.py` and `genemb.py`.*

---

## 🖥️ Usage

### 1. Store a Memory

Run the ingestion script and speak clearly into your microphone.

```bash
python main.py

```

*Example: "I put my car keys in the top drawer of the hallway cabinet."*

### 2. Recall a Memory

Run the recall script to ask a question.

```bash
python recall.py

```

*Example: "Where did I leave my keys?"*
*Response: "The closest match found is: I put my car keys in the top drawer of the hallway cabinet."*

---

## 📂 File Structure

| File | Purpose |
| --- | --- |
| `main.py` | Entry point for recording and saving new voice memories. |
| `recall.py` | Entry point for querying the system via voice. |
| `genemb.py` | Logic for generating embeddings using `SentenceTransformers`. |
| `p2.py` | Core similarity search logic using SQLAlchemy and `pgvector`. |
| `llm.py` | Interface for interacting with local or OpenAI LLMs. |
| `dao.py` | Raw SQL access methods for database operations. |
| `db.py` | SQLAlchemy models and schema definitions. |

---

## 🛡️ Note on API Keys

* **Local:** The system is configured to look for a local LLM at `http://localhost:4891/v1` in `llm.py`.
* **OpenAI:** If using GPT-3.5/4, ensure your API key is correctly set in `processor.py` and `p1.py`.
