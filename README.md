# 🚀 Full-Stack AI Authentication Platform

> A production-ready, enterprise-grade authentication system with FastAPI backend, React frontend, MongoDB database, and Google OAuth integration.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/react-18.2+-61dafb.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/typescript-5.0+-3178c6.svg)](https://www.typescriptlang.org/)

---

## ✨ Features

### 🔐 Authentication & Security
- **JWT Authentication** - Secure token-based auth with 24-hour expiration
- **Google OAuth 2.0** - Social login integration with token verification
- **Email/Password Registration** - Traditional signup with strong validation
- **Password Reset Flow** - 6-digit code via email with 15-minute expiry
- **Rate Limiting** - Protection against brute force attacks (5 attempts/min)
- **bcrypt Password Hashing** - Industry-standard security (12 salt rounds)

### 🌐 Multi-Platform Support
- **Web Application** - Modern React SPA with Tailwind CSS
- **Mobile App** - React Native app with Expo
- **RESTful API** - Well-documented FastAPI backend

### 🛠️ Developer Experience
- **Auto-Generated API Docs** - Swagger UI and ReDoc
- **Docker Support** - Containerized deployment ready
- **Azure Deployment** - One-command cloud deployment scripts
- **Type Safety** - TypeScript frontend, Pydantic backend
- **Hot Reload** - Development mode with auto-refresh

### 💼 Production Ready
- **MongoDB Integration** - Scalable NoSQL database with Motor async driver
- **CORS Configured** - Cross-origin support for web and mobile
- **Environment Variables** - Secure configuration management
- **Comprehensive Error Handling** - User-friendly error messages
- **Structured Logging** - Easy debugging and monitoring

---

## 🏗️ Tech Stack

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python web framework
- **[MongoDB](https://www.mongodb.com/)** - NoSQL database (Motor async driver)
- **[Pydantic](https://docs.pydantic.dev/)** - Data validation and settings
- **[JWT](https://jwt.io/)** - JSON Web Tokens (python-jose)
- **[bcrypt](https://github.com/pyca/bcrypt/)** - Password hashing
- **[Authlib](https://authlib.org/)** - OAuth 2.0 implementation
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI server

### Frontend
- **[React 18](https://react.dev/)** - UI library
- **[TypeScript](https://www.typescriptlang.org/)** - Type safety
- **[Vite](https://vitejs.dev/)** - Build tool & dev server
- **[Tailwind CSS](https://tailwindcss.com/)** - Utility-first CSS framework
- **[React Router](https://reactrouter.com/)** - Client-side routing
- **[@react-oauth/google](https://www.npmjs.com/package/@react-oauth/google)** - Google OAuth

### DevOps
- **[Docker](https://www.docker.com/)** - Containerization
- **[Azure Container Instances](https://azure.microsoft.com/products/container-instances/)** - Cloud deployment

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** ([Download](https://www.python.org/downloads/))
- **Node.js 18+** ([Download](https://nodejs.org/))
- **MongoDB Atlas Account** (or local MongoDB) ([Sign up](https://www.mongodb.com/cloud/atlas))
- **Git** ([Download](https://git-scm.com/downloads))

### One-Command Startup

```bash
# Clone the repository
git clone https://github.com/orior11/fullstack-ai.git
cd fullstack-ai

# Run both servers
python run_app.py
```

This will automatically:
1. ✅ Install Python dependencies
2. ✅ Install Node.js dependencies
3. ✅ Start FastAPI backend on `http://localhost:8000`
4. ✅ Start React frontend on `http://localhost:5173`
5. ✅ Open your browser automatically

---

## 📦 Manual Setup

### Backend Setup

```bash
# Navigate to backend directory
cd server-python

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your MongoDB URI and credentials

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Backend will be available at:**
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Frontend Setup

```bash
# Navigate to frontend directory
cd web-client

# Install dependencies
npm install

# Configure environment variables
cp .env.example .env
# Edit .env with your Google OAuth Client ID

# Run the development server
npm run dev
```

**Frontend will be available at:** http://localhost:5173

---

## 🔧 Configuration

### Environment Variables

#### Backend (`.env` in `server-python/`)

```env
# MongoDB Configuration
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/database
DATABASE_NAME=HomeAssignment
COLLECTION_NAME=users

# JWT Configuration
JWT_SECRET=your-super-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback

# Facebook OAuth (Optional)
FACEBOOK_APP_ID=your-facebook-app-id
FACEBOOK_APP_SECRET=your-facebook-app-secret
FACEBOOK_REDIRECT_URI=http://localhost:8000/api/auth/facebook/callback

# Email Service (for password reset)
EMAIL_SERVICE=console  # Options: console, azure, sendgrid
FROM_EMAIL=noreply@yourdomain.com

# Frontend URLs
FRONTEND_URL_WEB=http://localhost:5173
FRONTEND_URL_MOBILE=exp://localhost:19000
```

#### Frontend (`.env` in `web-client/`)

```env
# Google OAuth Configuration
VITE_GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
```

### Generate JWT Secret

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 📚 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/register` | Register new user | ❌ |
| POST | `/api/login` | Login with email/password | ❌ |
| POST | `/api/auth/google` | Google OAuth (token-based) | ❌ |
| GET | `/api/auth/google` | Google OAuth (redirect-based) | ❌ |
| GET | `/api/auth/google/callback` | Google OAuth callback | ❌ |
| GET | `/api/me` | Get current user info | ✅ |

### Password Reset Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/password-reset/request` | Request reset code |
| POST | `/api/password-reset/verify` | Verify reset code |
| POST | `/api/password-reset/complete` | Complete password reset |

### Health & Documentation

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/docs` | Swagger UI |
| GET | `/redoc` | ReDoc documentation |

---

## 🧪 API Usage Examples

### Register a New User

```bash
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

### Get Current User (Protected)

```bash
curl http://localhost:8000/api/me \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Request Password Reset

```bash
curl -X POST http://localhost:8000/api/password-reset/request \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com"}'
```

---

## 🗄️ Database Schema

### User Collection

```javascript
{
  _id: ObjectId,
  name: String,
  email: String (unique, indexed),
  password_hash: String (optional for OAuth users),
  social_provider: String ("google" | "facebook" | null),
  social_provider_id: String (optional, indexed),
  picture_url: String (optional),
  created_at: DateTime,
  last_login: DateTime (optional),
  is_verified: Boolean,
  reset_code: String (optional),
  reset_code_expires: DateTime (optional)
}
```

---

## 🐳 Docker Deployment

### Using Docker Compose

```bash
cd server-python
docker-compose up --build
```

This will:
- Build the FastAPI container
- Start the server on port 8000
- Connect to your MongoDB instance

### Manual Docker Build

```bash
cd server-python
docker build -t fullstack-ai-backend .
docker run -p 8000:8000 --env-file .env fullstack-ai-backend
```

---

## ☁️ Azure Deployment

### Deploy to Azure Container Instances

```bash
cd server-python
./azure-deploy.sh
```

The script will:
1. Build the Docker image
2. Push to Azure Container Registry
3. Deploy to Azure Container Instances
4. Set up environment variables
5. Configure networking

See [DEPLOYMENT_GUIDE.md](./server-python/DEPLOYMENT_GUIDE.md) for detailed instructions.

---

## 📱 Mobile App

A React Native mobile application is included in the `mobile-app/` directory with Expo.

### Setup & Run

```bash
cd mobile-app
npm install
npm start
```

Scan the QR code with the Expo Go app on your phone.

---

## 📁 Project Structure

```
fullstack-ai/
├── server-python/              # FastAPI Backend
│   ├── app/
│   │   ├── auth/              # Authentication logic
│   │   │   ├── jwt_handler.py # JWT operations
│   │   │   ├── oauth.py       # OAuth providers
│   │   │   └── password.py    # Password hashing
│   │   ├── routes/            # API routes
│   │   │   ├── auth.py        # Auth endpoints
│   │   │   └── password_reset.py
│   │   ├── services/          # Business logic
│   │   │   ├── user_service.py
│   │   │   └── email_service.py
│   │   ├── config.py          # Configuration
│   │   ├── database.py        # MongoDB connection
│   │   ├── models.py          # Pydantic models
│   │   └── main.py            # FastAPI app
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│   └── .env.example
├── web-client/                 # React Frontend
│   ├── src/
│   │   ├── App.tsx            # Main app component
│   │   ├── LoginPage.tsx      # Login page
│   │   ├── RegistrationPage.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.cjs
│   └── .env.example
├── mobile-app/                 # React Native App
│   ├── App.tsx
│   └── package.json
├── server-nodejs/              # Optional Node.js Service
│   └── (OpenAI integration)
├── run_app.py                  # One-command startup
├── README.md
├── LICENSE
└── .gitignore
```

---

## 🔒 Security Features

- ✅ **JWT Authentication** - Secure tokens with 24-hour expiration
- ✅ **Password Hashing** - bcrypt with 12 salt rounds
- ✅ **Rate Limiting** - Prevents brute force attacks
- ✅ **CORS Protection** - Configured allowed origins
- ✅ **Input Validation** - Pydantic validates all inputs
- ✅ **Password Requirements** - Min 8 chars, uppercase, lowercase, digit
- ✅ **OAuth 2.0** - Secure social authentication with Google
- ✅ **Environment Variables** - Secrets not hardcoded
- ✅ **HTTPS Ready** - SSL/TLS support for production

---

## 🧪 Testing

### Backend Tests

```bash
cd server-python
pytest
```

### Frontend Tests

```bash
cd web-client
npm test
```

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🐛 Troubleshooting

### Common Issues

#### MongoDB Connection Error
```
[ERROR] Failed to connect to MongoDB
```
**Solution:** Check your `MONGODB_URI` in `.env`. Ensure your IP is whitelisted in MongoDB Atlas.

#### Port Already in Use
```
Address already in use: 8000
```
**Solution:** Kill the process or change the port.

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

#### Google OAuth Error
```
The given origin is not allowed
```
**Solution:** Add `http://localhost:5173` to Authorized JavaScript origins in Google Cloud Console.

#### Module Not Found
```
ModuleNotFoundError: No module named 'app'
```
**Solution:** Ensure virtual environment is activated and in correct directory.

---

## 📞 Support & Documentation

### Additional Documentation

- **[API Testing Guide](./server-python/API_TESTING_GUIDE.md)** - 40+ API test examples
- **[Deployment Guide](./server-python/DEPLOYMENT_GUIDE.md)** - Azure deployment instructions
- **[Backend README](./server-python/README.md)** - Backend-specific documentation

### Useful Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [MongoDB Documentation](https://www.mongodb.com/docs/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

---

## 🎯 Roadmap

- [ ] Add unit and integration tests
- [ ] Implement refresh tokens
- [ ] Add two-factor authentication (2FA)
- [ ] Create admin dashboard
- [ ] Add user profile management
- [ ] Implement email verification flow
- [ ] Add more OAuth providers (GitHub, LinkedIn)
- [ ] Create API rate limiting dashboard
- [ ] Add WebSocket support for real-time features

---

## 📊 Project Stats

- **Total Files:** 40+
- **Lines of Code:** 5,000+
- **API Endpoints:** 10+
- **Technologies:** 15+
- **Test Coverage:** Growing

---

**Made with ❤️ for the developer community**

For questions or support, please open an issue on GitHub.

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=orior11/fullstack-ai&type=Date)](https://star-history.com/#orior11/fullstack-ai&Date)

