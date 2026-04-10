# 📧 Email Intent & Urgency Detector

An AI-powered web application that automatically analyzes emails and detects their **intent**, **urgency level**, **sentiment**, and **suggested action** using Large Language Models.

---

## 🎯 Project Overview

In real workplaces, people receive hundreds of emails daily. Reading each one to figure out what the sender wants and how urgent it is wastes a lot of time. This AI tool does that **instantly and automatically.**

You simply paste any email into the app — the AI reads it and gives you a complete structured analysis within seconds.

---

## ✨ Features

- 🔍 **Intent Detection** — Finds the purpose of the email (complaint, request, follow-up, inquiry, appreciation, etc.)
- 🚨 **Urgency Classification** — Labels urgency as Low / Medium / High / Critical
- 📝 **Email Summary** — Gives a clear 1-2 line summary of the email
- ✅ **Action Suggestion** — Suggests exactly what the recipient should do next
- 😤 **Sentiment Detection** — Detects the tone (Polite, Neutral, Frustrated, Angry, Positive, Negative)
- 📊 **Structured JSON Output** — Clean structured output using Pydantic models
- 🎨 **Beautiful UI** — Dark themed colorful Streamlit interface
- 💡 **Sample Emails** — 8 built-in sample emails to test instantly

---

## 🏗️ System Architecture

```
User Input (Email Text)
        ↓
Prompt Template (prompt.py)
        ↓
LLM — Groq LLaMA 3.1 (model.py)
        ↓
Pydantic Output Parser (email_parser.py)
        ↓
Structured Result (main.py)
        ↓
Streamlit Web UI (app.py)
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.10+ | Core programming language |
| LangChain | LLM orchestration framework |
| Groq API (LLaMA 3.1) | Free & fast LLM inference |
| Pydantic v2 | Structured output schema & validation |
| Streamlit | Interactive web UI |
| python-dotenv | Secure environment variable management |

---

## 📁 Project Structure

```
email-intent-detector/
│
├── app.py              ← Streamlit Web UI
├── main.py             ← Core logic (connects everything)
├── model.py            ← LLM setup (Groq)
├── prompt.py           ← Prompt template design
├── email_parser.py     ← Pydantic output schema
├── requirements.txt    ← All Python dependencies
├── .env                ← API Key — never push this!
├── .env.example        ← API Key placeholder template
└── .gitignore          ← Git ignore rules
```

---

## ⚙️ Setup & Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/pokalabalaji113-jpg/email-intent-detector.git
cd email-intent-detector
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Setup API Key
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
```
Get your free Groq API key at 👉 https://console.groq.com

### 4️⃣ Run the Application
```bash
streamlit run app.py
```

Open your browser at 👉 **http://localhost:8501**

---

## 🧪 Example Input & Output

**Input Email:**
```
Hi,

I've been waiting for the invoice for 3 weeks now.
Our accounts team is closing books tomorrow morning at 10 AM.
If I don't receive it tonight, payment will be delayed by another full month.
This is completely unacceptable. Please send it IMMEDIATELY.

Regards,
John Carter
```

**Output:**
```json
{
  "intent": "Invoice Request",
  "urgency": "Critical",
  "summary": "Client urgently needs invoice before accounts closing tomorrow morning.",
  "suggested_action": "Send invoice immediately and confirm receipt via reply email.",
  "sentiment": "Frustrated"
}
```

---

## 🔐 Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API key from https://console.groq.com |

---

## 📦 Requirements

```txt
langchain>=0.3.0
langchain-core>=0.3.0
langchain-groq>=0.2.0
pydantic>=2.0.0
streamlit>=1.30.0
python-dotenv>=1.0.0
```

---

## 🚀 Live Demo

👉 **Deployed App:** [Email Intent & Urgency Detector](https://email-intent-detector.streamlit.app)

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

**Balaji Pokala**

[![GitHub](https://img.shields.io/badge/GitHub-pokalabalaji113--jpg-black?logo=github)](https://github.com/pokalabalaji113-jpg)

---

> Built with ❤️ using LangChain + Groq LLaMA + Streamlit