# 📧 Email Intent & Urgency Detector

An AI-powered web application that automatically analyzes emails and detects their **intent**, **urgency level**, **sentiment**, and **suggested action** using Large Language Models — with full **Langfuse observability tracing**.

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
- 🔭 **Langfuse Tracing** — Full LLM observability with prompt, response, latency and token tracking

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
        ↓
Langfuse Dashboard (Tracing & Observability)
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
| Langfuse | LLM observability & tracing dashboard |

---

## 📁 Project Structure

```
email-intent-detector/
│
├── app.py              ← Streamlit Web UI
├── main.py             ← Core logic (connects everything)
├── model.py            ← LLM setup (Groq) + Langfuse handler
├── prompt.py           ← Prompt template design
├── email_parser.py     ← Pydantic output schema
├── requirements.txt    ← All Python dependencies
├── .env                ← API Keys — never push this!
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

### 3️⃣ Setup API Keys
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_SECRET_KEY=your_langfuse_secret_key
LANGFUSE_HOST=https://us.cloud.langfuse.com
```

Get your free keys:
- Groq API Key 👉 https://console.groq.com
- Langfuse Keys 👉 https://us.cloud.langfuse.com

### 4️⃣ Run the Application
```bash
streamlit run app.py
```

Open your browser at 👉 **http://localhost:8501**

---

## 🔭 Langfuse Tracing

This project includes full **LLM observability** using Langfuse. Every email analysis call is automatically traced and logged to your Langfuse dashboard.

### What Gets Tracked:

| Metric | Description |
|---|---|
| 📝 Input | The email text sent to LLM |
| 📊 Output | The structured JSON response |
| ⏱️ Latency | How long the LLM call took |
| 🔢 Tokens | Input + output token count |
| 🔗 Chain | Full LangChain pipeline trace |

### View Traces:
👉 **https://us.cloud.langfuse.com → Tracing → Traces**

---

## 🧪 Example Input & Output

**Input Email:**
```
Hi,

I've been waiting for the invoice for 3 weeks now.
Our accounts team is closing books tomorrow morning at 10 AM.
If I don't receive it tonight, payment will be delayed a full month.
Please send it IMMEDIATELY.

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
| `LANGFUSE_PUBLIC_KEY` | Your Langfuse public key |
| `LANGFUSE_SECRET_KEY` | Your Langfuse secret key |
| `LANGFUSE_HOST` | https://us.cloud.langfuse.com |

---

## 📦 Requirements

```txt
langchain
langchain-core
langchain-groq
pydantic
streamlit
python-dotenv
langfuse
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

> Built with ❤️ using LangChain + Groq LLaMA + Streamlit + Langfuse
