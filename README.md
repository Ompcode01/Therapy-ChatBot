# 🧠 Therapy ChatBot for IGD & BDD Support

An AI-powered mental health support system designed to provide empathetic conversational assistance for individuals experiencing **Internet Gaming Disorder (IGD)** and **Body Dysmorphic Disorder (BDD)**.

---

## 🚀 Features

### 💬 1. Therapy Chat Interface

* AI-driven empathetic conversation
* Evidence-based responses (CBT-informed)
* Supports:

  * Gaming addiction behaviors (IGD)
  * Body image concerns (BDD)
* Includes mandatory safety disclaimer

---

### 🔑 2. Dynamic LLM Integration

* Supports:

  * Gemini API
  * Groq API
* Users can input API keys directly in the UI
* Backend dynamically switches provider based on key

---

### 📊 3. Health Metrics Dashboard

A simulated real-time monitoring dashboard displaying:

| Metric         | Range           |
| -------------- | --------------- |
| SpO2           | 95% – 100%      |
| Blood Pressure | 110/70 – 130/85 |
| Heart Rate     | 60 – 100 bpm    |
| Stress Level   | 1 – 10          |

* Generated using Python `random`
* Displayed using Streamlit components (`st.metric`, progress bars)

---

### 🎨 4. Therapeutic UI

* Clean, calming interface
* Streamlit-based frontend
* Multi-page or tab navigation:

  * Chat Page
  * Health Dashboard

---

## 🏗️ Project Structure

```
project/
│
├── main.py                # FastAPI backend entry point
├── frontend.py           # Streamlit UI
├── system.md             # LLM system prompt
├── README.md             # Project documentation
│
├── app/
│   ├── services/         # LLM integration & business logic
│   ├── core/             # Config, API keys, security
│   ├── schemas/          # Pydantic models
│   └── db/               # Database logic
│
├── requirements.txt
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <repo-url>
cd project
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Run Backend (FastAPI)

```bash
uvicorn main:app --reload
```

---

### 4. Run Frontend (Streamlit)

```bash
streamlit run frontend.py
```

---

## 🔐 API Key Usage

In the Streamlit sidebar:

* Paste either:

  * `GEMINI_API_KEY`
  * `GROQ_API_KEY`

### Backend Behavior:

* Detects which key is provided
* Routes request to corresponding LLM provider
* Applies therapy-focused system prompt (`system.md`)

---

## 🧩 Implementation Notes

### Backend (FastAPI)

* Accepts API key in request payload
* Passes key to LLM service layer
* Handles provider switching logic

### Frontend (Streamlit)

* Chat UI
* Sidebar for API key input
* Navigation for dashboard

### Services Layer

* Unified interface for:

  * Gemini
  * Groq
* Injects system prompt
* Returns formatted response

---

## ⚠️ Safety & Ethics

* Every AI response includes a disclaimer:

  > Not a substitute for professional medical advice
* Avoids diagnosis or medical claims
* Encourages professional help when needed

---

## 📦 Dependencies

Typical dependencies include:

* fastapi
* uvicorn
* streamlit
* pydantic
* google-generativeai
* groq
* python-dotenv

---

## 📈 Future Enhancements

* Real wearable device integration
* Persistent chat memory (DB)
* User authentication
* Advanced analytics dashboard

---

## 🤝 Contribution

Feel free to fork and improve:

* UI/UX enhancements
* Better therapy models
* Additional mental health domains

---

## 📜 License

MIT License (or specify as needed)

---

## 💡 Disclaimer

This project is intended for **supportive and educational purposes only** and does not replace professional mental health care.

---
