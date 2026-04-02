# 🤖 AI Chat Bot (FastAPI + Gemini)

A simple AI chatbot API built using **FastAPI** and **Google Gemini (LangChain)**.
It supports conversation handling and can be integrated with any frontend.
(ReadMe Generated with AI)
---

## 🚀 Features

* FastAPI backend
* Gemini LLM integration
* Supports multiple API keys (rotation)
* Simple `/chat` endpoint
* Easy to extend with memory / agents

---

## 📦 Installation

```bash
pip install -r requirements.txt
```

---

## ⚙️ Environment Setup

Create a `.env` file in the root directory and add:

```env
GOOGLE_API_KEY=your_google_api_key_here
mongoString=your_mongodb_connection_string
```

Example:

```env
GOOGLE_API_KEY=AIza7c-8sk
mongoString=mongodb+sr...
```

---

## ▶️ Run the server

```bash
fastapi run main.py
```

Server will start at:

```
http://localhost:8000
```

---

## 📡 API Usage

### Endpoint:

```
POST /chat
```

### Request:

```json
{
  "message": "Hello",
  "session_id": "user1"
}
```

### Response:

```json
{
  "response": "Hi! How can I help you?"
}
```

---

## 🧪 Test API

Open:

```
http://localhost:8000/docs
```

---

## ⚙️ Tech Stack

* FastAPI
* LangChain
* Google Gemini API

---

## 📁 Project Structure

```
.
├── main.py
├── agent.py
├── tools/
├── requirements.txt
└── README.md
```

---

## 🔐 Notes

* Never commit your `.env` file
* Add `.env` to `.gitignore`
* Rotate API keys if exposed

---

## 💡 Future Improvements

* Add chat history (memory)
* Add authentication
* Deploy on cloud (AWS / Railway / Vercel)

---
