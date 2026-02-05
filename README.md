
```markdown:readme.md
# 🚀 Full-Stack AI Authentication Platform

A professional, end-to-end authentication system featuring a **FastAPI** backend, **React** web client, and **React Native** mobile app. Integrated with **MongoDB**, **Google OAuth**, and **Azure** deployment scripts.

---

## 📺 Demo & Preview
https://youtu.be/tgonLSCvH3w

---

## ⚡ Quick Start (One Command)
Run the entire ecosystem (Backend + Frontend) with a single script:
```bash
python run_app.py

```

---

## 🛠️ Manual Setup

### 🐍 Backend (FastAPI)

```bash
cd server-python
python -m venv venv
# Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

```

### ⚛️ Frontend (React + Vite)

```bash
cd web-client
npm install
npm run dev

```

---

## 📚 API Documentation

| Method | Endpoint | Description | Auth Required |
| --- | --- | --- | --- |
| `POST` | `/api/register` | Register new user | ❌ |
| `POST` | `/api/login` | Login with email/password | ❌ |
| `POST` | `/api/auth/google` | Google OAuth | ❌ |
| `GET` | `/api/me` | Get current user info | ✅ |

---

## 🔒 Security Features

* **JWT Authentication** (24h expiration)
* **Password Hashing** with `bcrypt`
* **OAuth 2.0** Google Integration
* **Input Validation** via `Pydantic`

---

## 📂 Project Structure

```text
fullstack-ai/
├── server-python/      # FastAPI Backend
├── web-client/         # React Frontend
├── mobile-app/         # React Native (Expo)
└── run_app.py          # Startup Script
