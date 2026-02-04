# Authentication API

A robust, secure authentication server built with Python FastAPI, MongoDB, and Azure-ready deployment.

## Features

- ✅ **User Registration** - Email/password with bcrypt hashing
- ✅ **User Login** - JWT token-based authentication
- ✅ **OAuth Social Login** - Google and Facebook integration
- ✅ **Password Reset** - Email-based 6-digit code verification
- ✅ **Rate Limiting** - Protection against brute force attacks
- ✅ **CORS Configured** - Ready for React Web and React Native mobile
- ✅ **API Documentation** - Auto-generated Swagger UI
- ✅ **Docker Ready** - Containerized deployment
- ✅ **Azure Deployment** - Scripts for Azure Container Instances

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Required environment variables:
- `MONGODB_URI` - MongoDB connection string
- `JWT_SECRET` - Secret key for JWT tokens (generate with `python -c "import secrets; print(secrets.token_urlsafe(32))"`)
- OAuth credentials (optional, for social login)
- Email service credentials (optional, for password reset)

### 3. Run the Server

```bash
# Development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/register` | Register new user |
| POST | `/api/login` | Login with email/password |
| GET | `/api/me` | Get current user (requires auth) |

### OAuth Social Login

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/auth/google` | Initiate Google OAuth |
| GET | `/api/auth/google/callback` | Google OAuth callback |
| GET | `/api/auth/facebook` | Initiate Facebook OAuth |
| GET | `/api/auth/facebook/callback` | Facebook OAuth callback |

### Password Reset

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/password-reset/request` | Request reset code |
| POST | `/api/password-reset/verify` | Verify reset code |
| POST | `/api/password-reset/complete` | Complete password reset |

### Health & Documentation

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/docs` | Swagger UI documentation |
| GET | `/redoc` | ReDoc documentation |

## Usage Examples

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

Response:
```json
{
  "success": true,
  "message": "User registered successfully",
  "welcome_message": "Welcome to our platform!"
}
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

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "name": "John Doe",
    "email": "john@example.com",
    "social_provider": null
  }
}
```

### Get Current User (Protected Route)

```bash
curl -X GET http://localhost:8000/api/me \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Request Password Reset

```bash
curl -X POST http://localhost:8000/api/password-reset/request \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com"
  }'
```

### Complete Password Reset

```bash
curl -X POST http://localhost:8000/api/password-reset/complete \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "code": "123456",
    "new_password": "NewSecurePass456"
  }'
```

## Docker Deployment

### Build and Run with Docker Compose

```bash
docker-compose up --build
```

### Build Docker Image

```bash
docker build -t auth-api .
```

### Run Docker Container

```bash
docker run -d \
  -p 8000:8000 \
  --env-file .env \
  --name auth-api \
  auth-api
```

## Azure Deployment

### Prerequisites

- Azure CLI installed and configured
- Azure subscription
- Azure Container Registry (or create one)

### Deploy to Azure Container Instances

```bash
# Make script executable
chmod +x azure-deploy.sh

# Set environment variables
export MONGODB_URI="your-mongodb-uri"
export JWT_SECRET="your-jwt-secret"
export GOOGLE_CLIENT_ID="your-google-client-id"
export GOOGLE_CLIENT_SECRET="your-google-client-secret"

# Run deployment script
./azure-deploy.sh
```

The script will:
1. Create Azure resources (Resource Group, Container Registry)
2. Build and push Docker image to ACR
3. Deploy to Azure Container Instances
4. Output the public URL

## OAuth Setup

### Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URI: `http://localhost:8000/api/auth/google/callback`
6. Add credentials to `.env`:
   ```
   GOOGLE_CLIENT_ID=your-client-id
   GOOGLE_CLIENT_SECRET=your-client-secret
   ```

### Facebook OAuth

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app
3. Add Facebook Login product
4. Set Valid OAuth Redirect URIs: `http://localhost:8000/api/auth/facebook/callback`
5. Add credentials to `.env`:
   ```
   FACEBOOK_APP_ID=your-app-id
   FACEBOOK_APP_SECRET=your-app-secret
   ```

## Email Service Setup

### Console (Development)

Default mode - prints emails to console. No setup needed.

### Azure Communication Services

1. Create Azure Communication Services resource
2. Get connection string
3. Add to `.env`:
   ```
   EMAIL_SERVICE=azure
   AZURE_COMMUNICATION_CONNECTION_STRING=your-connection-string
   FROM_EMAIL=noreply@yourdomain.com
   ```

### SendGrid

1. Sign up at [SendGrid](https://sendgrid.com/)
2. Create API key
3. Add to `.env`:
   ```
   EMAIL_SERVICE=sendgrid
   SENDGRID_API_KEY=your-api-key
   FROM_EMAIL=noreply@yourdomain.com
   ```

## Security Features

- **Password Hashing**: bcrypt with 12 salt rounds
- **JWT Tokens**: Secure tokens with 24-hour expiration
- **Rate Limiting**: 5 attempts per minute on login endpoint
- **CORS**: Configured for specific origins only
- **Input Validation**: Pydantic models with strict validation
- **Password Requirements**:
  - Minimum 8 characters
  - At least 1 uppercase letter
  - At least 1 lowercase letter
  - At least 1 digit

## Frontend Integration

### Web Client (React)

```typescript
// Login
const response = await fetch('http://localhost:8000/api/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password })
});
const data = await response.json();
localStorage.setItem('token', data.access_token);

// Protected API call
const userResponse = await fetch('http://localhost:8000/api/me', {
  headers: { 'Authorization': `Bearer ${token}` }
});
```

### Mobile Client (React Native)

```typescript
import AsyncStorage from '@react-native-async-storage/async-storage';

// Login
const response = await fetch('http://localhost:8000/api/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password })
});
const data = await response.json();
await AsyncStorage.setItem('token', data.access_token);

// Protected API call
const token = await AsyncStorage.getItem('token');
const userResponse = await fetch('http://localhost:8000/api/me', {
  headers: { 'Authorization': `Bearer ${token}` }
});
```

## Project Structure

```
server-python/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app & routes
│   ├── models.py               # Pydantic models
│   ├── database.py             # MongoDB connection
│   ├── config.py               # Configuration
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── jwt_handler.py      # JWT operations
│   │   ├── oauth.py            # OAuth providers
│   │   └── password.py         # Password hashing
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py             # Auth endpoints
│   │   └── password_reset.py   # Password reset endpoints
│   └── services/
│       ├── __init__.py
│       ├── email_service.py    # Email sending
│       └── user_service.py     # User operations
├── .env                        # Environment variables
├── .env.example                # Example environment file
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose configuration
├── azure-deploy.sh             # Azure deployment script
└── README.md                   # This file
```

## Development

### Install Development Dependencies

```bash
pip install -r requirements.txt
```

### Run Tests (Future Enhancement)

```bash
pytest
```

### Code Formatting

```bash
black app/
isort app/
```

### Type Checking

```bash
mypy app/
```

## Troubleshooting

### MongoDB Connection Issues

- Verify `MONGODB_URI` in `.env`
- Check MongoDB Atlas IP whitelist (allow your IP or 0.0.0.0/0 for testing)
- Ensure database user has read/write permissions

### OAuth Not Working

- Verify OAuth credentials in `.env`
- Check redirect URIs match exactly in OAuth provider settings
- For local development, use `http://localhost:8000` (not 127.0.0.1)

### Email Not Sending

- Check EMAIL_SERVICE is set correctly
- Verify email service credentials
- In development, use `EMAIL_SERVICE=console` to print to console

### CORS Errors

- Add your frontend URL to CORS origins in `app/main.py`
- Ensure credentials are included in frontend requests

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Open an issue on GitHub
- Check the `/docs` endpoint for API documentation
- Review logs: `docker logs auth-api` (if using Docker)

## Roadmap

- [ ] Unit tests
- [ ] Integration tests
- [ ] Refresh tokens
- [ ] Email verification
- [ ] Two-factor authentication (2FA)
- [ ] Account deletion
- [ ] User roles and permissions
- [ ] Activity logging
- [ ] API versioning
