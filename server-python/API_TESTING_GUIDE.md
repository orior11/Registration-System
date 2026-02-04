# API Testing Guide

Complete guide for testing all authentication API endpoints with example requests and expected responses.

## Setup

### Prerequisites

- Server running at `http://localhost:8000`
- MongoDB connected
- (Optional) OAuth credentials configured
- (Optional) Email service configured

### Tools

- **cURL** - Command-line HTTP client
- **Postman** - GUI API testing tool
- **HTTPie** - User-friendly HTTP client
- **Swagger UI** - http://localhost:8000/docs (built-in)

## Test Workflow

### 1. Health Check

Verify the server is running:

```bash
curl http://localhost:8000/health
```

Expected Response:
```json
{
  "status": "ok",
  "database": "connected"
}
```

### 2. User Registration

#### Test Case: Valid Registration

```bash
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "password": "SecurePass123"
  }'
```

Expected Response (200):
```json
{
  "success": true,
  "message": "User registered successfully",
  "welcome_message": "Welcome to our platform!"
}
```

#### Test Case: Duplicate Email

```bash
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "email": "john.doe@example.com",
    "password": "AnotherPass456"
  }'
```

Expected Response (400):
```json
{
  "detail": "Email already registered"
}
```

#### Test Case: Weak Password

```bash
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "weak"
  }'
```

Expected Response (422):
```json
{
  "detail": [
    {
      "type": "value_error",
      "msg": "Password must contain at least one uppercase letter",
      "ctx": {...}
    }
  ]
}
```

### 3. User Login

#### Test Case: Successful Login

```bash
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "SecurePass123"
  }'
```

Expected Response (200):
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "name": "John Doe",
    "email": "john.doe@example.com",
    "social_provider": null
  }
}
```

#### Test Case: Invalid Password

```bash
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "WrongPassword"
  }'
```

Expected Response (401):
```json
{
  "detail": "Incorrect email or password"
}
```

#### Test Case: User Not Found

```bash
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "nonexistent@example.com",
    "password": "AnyPassword123"
  }'
```

Expected Response (401):
```json
{
  "detail": "Incorrect email or password"
}
```

### 4. Get Current User (Protected Route)

First, login and save the token:

```bash
TOKEN=$(curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john.doe@example.com","password":"SecurePass123"}' \
  | jq -r '.access_token')
```

Then use the token:

```bash
curl -X GET http://localhost:8000/api/me \
  -H "Authorization: Bearer $TOKEN"
```

Expected Response (200):
```json
{
  "id": "507f1f77bcf86cd799439011",
  "name": "John Doe",
  "email": "john.doe@example.com",
  "social_provider": null,
  "created_at": "2026-02-02T18:30:00",
  "last_login": "2026-02-02T19:15:00"
}
```

#### Test Case: Invalid Token

```bash
curl -X GET http://localhost:8000/api/me \
  -H "Authorization: Bearer invalid_token"
```

Expected Response (401):
```json
{
  "detail": "Could not validate credentials"
}
```

### 5. OAuth Social Login

#### Google OAuth

**Step 1**: Initiate OAuth (open in browser)
```
http://localhost:8000/api/auth/google
```

This will redirect to Google's consent screen.

**Step 2**: After approval, Google redirects to callback:
```
http://localhost:8000/api/auth/google/callback?code=...
```

Server will:
- Exchange code for token
- Get user info from Google
- Create/login user
- Redirect to frontend with JWT token:
```
http://localhost:5173?token=eyJ0eXAiOiJKV1QiLCJhbGc...
```

#### Facebook OAuth

**Step 1**: Initiate OAuth (open in browser)
```
http://localhost:8000/api/auth/facebook
```

Same flow as Google.

### 6. Password Reset Flow

#### Step 1: Request Reset Code

```bash
curl -X POST http://localhost:8000/api/password-reset/request \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com"
  }'
```

Expected Response (200):
```json
{
  "success": true,
  "message": "Reset code sent to your email"
}
```

**Note**: Check console output for the 6-digit code if using `EMAIL_SERVICE=console`

#### Step 2: Verify Reset Code

```bash
curl -X POST http://localhost:8000/api/password-reset/verify \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "code": "123456"
  }'
```

Expected Response (200):
```json
{
  "success": true,
  "message": "Reset code verified successfully"
}
```

#### Test Case: Invalid Code

```bash
curl -X POST http://localhost:8000/api/password-reset/verify \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "code": "999999"
  }'
```

Expected Response (400):
```json
{
  "detail": "Invalid reset code"
}
```

#### Step 3: Complete Password Reset

```bash
curl -X POST http://localhost:8000/api/password-reset/complete \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "code": "123456",
    "new_password": "NewSecurePass789"
  }'
```

Expected Response (200):
```json
{
  "success": true,
  "message": "Password reset successfully"
}
```

#### Test Case: Expired Code

Wait 16 minutes after requesting code, then:

```bash
curl -X POST http://localhost:8000/api/password-reset/complete \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "code": "123456",
    "new_password": "NewPassword123"
  }'
```

Expected Response (400):
```json
{
  "detail": "Reset code has expired. Please request a new one"
}
```

## Postman Collection

### Import into Postman

Create a new collection with these requests:

1. **Health Check**
   - Method: GET
   - URL: `{{base_url}}/health`

2. **Register**
   - Method: POST
   - URL: `{{base_url}}/api/register`
   - Body (JSON):
     ```json
     {
       "name": "{{$randomFullName}}",
       "email": "{{$randomEmail}}",
       "password": "TestPass123"
     }
     ```

3. **Login**
   - Method: POST
   - URL: `{{base_url}}/api/login`
   - Body (JSON):
     ```json
     {
       "email": "john.doe@example.com",
       "password": "SecurePass123"
     }
     ```
   - Tests (extract token):
     ```javascript
     pm.test("Login successful", function() {
       pm.response.to.have.status(200);
       var jsonData = pm.response.json();
       pm.environment.set("token", jsonData.access_token);
     });
     ```

4. **Get Current User**
   - Method: GET
   - URL: `{{base_url}}/api/me`
   - Headers:
     - Authorization: `Bearer {{token}}`

5. **Request Password Reset**
   - Method: POST
   - URL: `{{base_url}}/api/password-reset/request`
   - Body (JSON):
     ```json
     {
       "email": "john.doe@example.com"
     }
     ```

### Environment Variables

Set in Postman:
- `base_url`: `http://localhost:8000`
- `token`: (auto-filled by login test)

## HTTPie Examples

More readable alternative to cURL:

### Register
```bash
http POST localhost:8000/api/register \
  name="John Doe" \
  email="john@example.com" \
  password="SecurePass123"
```

### Login
```bash
http POST localhost:8000/api/login \
  email="john@example.com" \
  password="SecurePass123"
```

### Get Current User
```bash
http GET localhost:8000/api/me \
  Authorization:"Bearer YOUR_TOKEN_HERE"
```

## Rate Limiting Tests

### Test Login Rate Limit (5 attempts/minute)

```bash
for i in {1..6}; do
  echo "Attempt $i:"
  curl -X POST http://localhost:8000/api/login \
    -H "Content-Type: application/json" \
    -d '{"email":"test@example.com","password":"wrong"}' \
    -w "\nStatus: %{http_code}\n\n"
  sleep 1
done
```

Expected:
- Attempts 1-5: Return 401 (Unauthorized)
- Attempt 6: Return 429 (Too Many Requests)

## Integration Testing Scenarios

### Scenario 1: New User Full Flow

```bash
# 1. Register
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice Smith","email":"alice@example.com","password":"AlicePass123"}'

# 2. Login
TOKEN=$(curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"AlicePass123"}' \
  | jq -r '.access_token')

# 3. Get user info
curl -X GET http://localhost:8000/api/me \
  -H "Authorization: Bearer $TOKEN"
```

### Scenario 2: Password Reset Flow

```bash
# 1. Request reset
curl -X POST http://localhost:8000/api/password-reset/request \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com"}'

# 2. Check console for code (if EMAIL_SERVICE=console)
# CODE=123456

# 3. Verify code
curl -X POST http://localhost:8000/api/password-reset/verify \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","code":"123456"}'

# 4. Complete reset
curl -X POST http://localhost:8000/api/password-reset/complete \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","code":"123456","new_password":"NewAlicePass456"}'

# 5. Login with new password
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"NewAlicePass456"}'
```

### Scenario 3: OAuth Social Login

1. Open browser: `http://localhost:8000/api/auth/google`
2. Sign in with Google account
3. Approve permissions
4. Redirected to: `http://localhost:5173?token=...`
5. Extract token from URL
6. Use token to access protected endpoints

## Performance Testing

### Load Testing with Apache Bench

```bash
# Install Apache Bench
# Ubuntu: sudo apt-get install apache2-utils
# macOS: already installed

# Test login endpoint
ab -n 100 -c 10 -p login.json -T application/json \
  http://localhost:8000/api/login

# login.json content:
# {"email":"john@example.com","password":"SecurePass123"}
```

### Load Testing with wrk

```bash
# Install wrk: https://github.com/wg/wrk

# Test health endpoint
wrk -t4 -c100 -d30s http://localhost:8000/health

# Test with POST request
wrk -t4 -c100 -d30s -s post.lua http://localhost:8000/api/login

# post.lua:
# wrk.method = "POST"
# wrk.headers["Content-Type"] = "application/json"
# wrk.body = '{"email":"john@example.com","password":"SecurePass123"}'
```

## Security Testing

### Test 1: SQL Injection Attempt

```bash
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "' OR '1'='1"
  }'
```

Expected: Should fail validation (Pydantic prevents injection)

### Test 2: JWT Token Tampering

```bash
# Get valid token
TOKEN="eyJ0eXAiOiJKV1QiLCJhbGc..."

# Tamper with token (change a character)
TAMPERED_TOKEN="${TOKEN:0:50}X${TOKEN:51}"

# Try to use tampered token
curl -X GET http://localhost:8000/api/me \
  -H "Authorization: Bearer $TAMPERED_TOKEN"
```

Expected Response (401):
```json
{
  "detail": "Could not validate credentials"
}
```

### Test 3: CORS Validation

```bash
# Request from unauthorized origin
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -H "Origin: http://malicious-site.com" \
  -d '{"email":"john@example.com","password":"SecurePass123"}'
```

Check response headers - should not include `Access-Control-Allow-Origin: http://malicious-site.com`

## Python Testing Script

Create `test_api.py`:

```python
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    print("✅ Health check passed")

def test_register():
    data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "TestPass123"
    }
    response = requests.post(f"{BASE_URL}/api/register", json=data)
    assert response.status_code == 200
    print("✅ Registration passed")
    return response.json()

def test_login():
    data = {
        "email": "test@example.com",
        "password": "TestPass123"
    }
    response = requests.post(f"{BASE_URL}/api/login", json=data)
    assert response.status_code == 200
    result = response.json()
    assert "access_token" in result
    print("✅ Login passed")
    return result["access_token"]

def test_get_current_user(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/me", headers=headers)
    assert response.status_code == 200
    print("✅ Get current user passed")
    return response.json()

def test_password_reset():
    # Step 1: Request reset
    response = requests.post(
        f"{BASE_URL}/api/password-reset/request",
        json={"email": "test@example.com"}
    )
    assert response.status_code == 200
    print("✅ Password reset request passed")
    
    # Note: Code will be in console output if EMAIL_SERVICE=console
    # For automated testing, you'd need to mock the email service
    
if __name__ == "__main__":
    print("Starting API tests...\n")
    test_health()
    test_register()
    token = test_login()
    test_get_current_user(token)
    test_password_reset()
    print("\n🎉 All tests passed!")
```

Run tests:
```bash
python test_api.py
```

## Browser Testing

### Using Swagger UI

1. Open http://localhost:8000/docs
2. Click on any endpoint to expand
3. Click "Try it out"
4. Fill in parameters
5. Click "Execute"
6. View response

### OAuth Testing in Browser

1. **Google**:
   - Navigate to: `http://localhost:8000/api/auth/google`
   - Sign in with Google
   - Check redirect URL contains token

2. **Facebook**:
   - Navigate to: `http://localhost:8000/api/auth/facebook`
   - Sign in with Facebook
   - Check redirect URL contains token

## Automated Test Suite (pytest)

Create `tests/test_auth.py`:

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_register():
    response = client.post("/api/register", json={
        "name": "Test User",
        "email": "pytest@example.com",
        "password": "PyTest123"
    })
    assert response.status_code == 200
    assert response.json()["success"] == True

def test_login():
    # First register
    client.post("/api/register", json={
        "name": "Login Test",
        "email": "login@example.com",
        "password": "LoginPass123"
    })
    
    # Then login
    response = client.post("/api/login", json={
        "email": "login@example.com",
        "password": "LoginPass123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_invalid_login():
    response = client.post("/api/login", json={
        "email": "wrong@example.com",
        "password": "WrongPass123"
    })
    assert response.status_code == 401
```

Run tests:
```bash
pytest tests/
```

## Monitoring & Logs

### View Server Logs

```bash
# Docker
docker logs -f auth-api

# Docker Compose
docker-compose logs -f api

# Azure Container Instances
az container logs \
  --resource-group auth-api-rg \
  --name auth-api-container \
  --follow
```

### Check Request/Response Details

Add logging to see all requests:

```bash
# Run server with debug logging
uvicorn app.main:app --reload --log-level debug
```

## Troubleshooting Test Failures

### Registration Fails

- Check MongoDB connection
- Verify email format is valid
- Ensure password meets requirements
- Check for duplicate email

### Login Fails

- Verify user was registered successfully
- Check password matches exactly
- Ensure MongoDB is accessible

### OAuth Fails

- Verify OAuth credentials in `.env`
- Check redirect URIs match exactly
- Ensure callback URL is accessible
- For local testing, use http://localhost:8000 (not 127.0.0.1)

### Password Reset Fails

- Check email service is configured
- Verify user exists
- Ensure reset code hasn't expired (15 min)
- Check console output for reset code

### Protected Routes Fail

- Verify JWT token is valid
- Check Authorization header format: `Bearer <token>`
- Ensure token hasn't expired (24 hours)

## Test Checklist

- [ ] Server starts without errors
- [ ] Health endpoint returns OK
- [ ] Registration with valid data succeeds
- [ ] Registration with duplicate email fails
- [ ] Registration with weak password fails
- [ ] Login with valid credentials succeeds
- [ ] Login with invalid credentials fails
- [ ] Protected route works with valid token
- [ ] Protected route fails without token
- [ ] Protected route fails with invalid token
- [ ] Google OAuth flow works (if configured)
- [ ] Facebook OAuth flow works (if configured)
- [ ] Password reset request succeeds
- [ ] Password reset code verification works
- [ ] Password reset completion succeeds
- [ ] Expired reset code is rejected
- [ ] Invalid reset code is rejected
- [ ] Rate limiting triggers after 5 attempts
- [ ] CORS allows authorized origins
- [ ] Swagger UI is accessible

## Next Steps

1. **Implement Unit Tests** - Test individual functions
2. **Add Integration Tests** - Test full workflows
3. **Set Up CI/CD** - Automated testing on push
4. **Add Monitoring** - Azure Application Insights
5. **Performance Testing** - Load and stress tests
6. **Security Audit** - OWASP top 10 checks
