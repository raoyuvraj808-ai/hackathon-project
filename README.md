# CampusBuddy 🎓

**CampusBuddy** is an AI-powered college survival assistant designed to help college students navigate campus life, facilities, academic deadlines, and everyday survival tips with ease.

Built for hackathons and rapid iteration, CampusBuddy pairs a friendly **Streamlit** user interface with local **Ollama** LLM integration, configured for a **Gemma 4** model.

---

## 📁 Project Structure

```text
Campus Buddy/
│
├── app.py              # Main Streamlit web application & UI logic
├── campus_data.json    # Structured demonstration data for campus resources & FAQs
├── requirements.txt    # Project dependencies (Streamlit, Requests)
└── README.md           # Documentation, setup guide, and project overview
```

---

## 📄 File Descriptions

| File | Purpose |
| :--- | :--- |
| **`app.py`** | Main entry point for the Streamlit application. Provides a clean student-facing dashboard with tabs for facilities, FAQs, emergency contacts, and an AI chat interface prepared for Ollama integration. Includes a sidebar to configure the Ollama endpoint and specify a custom model tag (such as Gemma 4). |
| **`campus_data.json`** | Demonstration dataset containing realistic, fictional college information for Pinecrest University (operating hours, emergency services, academic calendar, Wi-Fi setup, ID policies, tutoring). |
| **`requirements.txt`** | Minimal Python package dependencies (`streamlit` and `requests`) required to run the web interface and query the local Ollama API. |
| **`README.md`** | Clear reference guide with setup instructions, configuration details, and architecture overview. |

---

## 🚀 Getting Started

### 1. Prerequisites
- **Python**: 3.9 or newer installed on your machine.
- **Ollama**: Installed and running locally (default: `http://localhost:11434`). Download from [ollama.com](https://ollama.com) if you haven't already.

### 2. Set Up a Virtual Environment (Recommended)

In your terminal or PowerShell inside the project directory:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

*(Note: Install dependencies when you are ready to test/run the application.)*

```bash
pip install -r requirements.txt
```

### 4. Configure Your Local Model in Ollama

1. Start Ollama on your system:
   ```bash
   ollama serve
   ```
2. Pull your chosen model. When Gemma 4 is available or installed in your local Ollama environment, note its model tag.
3. Open the CampusBuddy sidebar in the web app, check your Ollama connection, and enter your model tag into the **Ollama Model Tag** field.

### 5. Run the Application

```bash
streamlit run app.py
```

Open your browser to `http://localhost:8501` to view CampusBuddy.

---

## 🛠️ Next Implementation Steps

We will build out the application features iteratively:
1. **Ollama Integration**: Connect the user question interface directly to the local Ollama `/api/generate` or `/api/chat` endpoint.
2. **Context-Aware Grounding (RAG/Prompt Injection)**: Inject relevant campus data from `campus_data.json` into the model prompt to produce accurate, hallucination-free survival answers.
3. **Conversational Memory**: Enable multi-turn chat history so students can ask follow-up questions.

