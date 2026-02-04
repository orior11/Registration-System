# Deployment Guide - Authentication API

Complete guide for deploying the authentication API to various environments.

## Table of Contents

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Azure Container Instances](#azure-container-instances)
4. [Azure App Service](#azure-app-service)
5. [Production Checklist](#production-checklist)

---

## Local Development

### Prerequisites

- Python 3.11+
- MongoDB Atlas account (or local MongoDB)
- pip package manager

### Setup Steps

1. **Clone and navigate to project**:
   ```bash
   cd "C:\Users\PinhasZ\Home Assignment\server-python"
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your actual credentials
   ```

5. **Generate JWT secret**:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   # Copy output to JWT_SECRET in .env
   ```

6. **Run the server**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

7. **Access the API**:
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs

---

## Docker Deployment

### Prerequisites

- Docker installed
- Docker Compose installed

### Using Docker Compose (Recommended)

1. **Configure environment**:
   ```bash
   # Ensure .env file exists with all required variables
   ```

2. **Build and run**:
   ```bash
   docker-compose up --build
   ```

3. **Run in background**:
   ```bash
   docker-compose up -d
   ```

4. **View logs**:
   ```bash
   docker-compose logs -f api
   ```

5. **Stop services**:
   ```bash
   docker-compose down
   ```

### Using Docker Directly

1. **Build image**:
   ```bash
   docker build -t auth-api:latest .
   ```

2. **Run container**:
   ```bash
   docker run -d \
     -p 8000:8000 \
     --name auth-api \
     --env-file .env \
     auth-api:latest
   ```

3. **View logs**:
   ```bash
   docker logs -f auth-api
   ```

4. **Stop and remove**:
   ```bash
   docker stop auth-api
   docker rm auth-api
   ```

---

## Azure Container Instances

### Prerequisites

- Azure CLI installed
- Azure subscription
- Azure account logged in: `az login`

### Automated Deployment (Recommended)

1. **Make script executable**:
   ```bash
   chmod +x azure-deploy.sh
   ```

2. **Set environment variables**:
   ```bash
   export MONGODB_URI="your-mongodb-uri"
   export JWT_SECRET="your-jwt-secret"
   export GOOGLE_CLIENT_ID="your-google-client-id"
   export GOOGLE_CLIENT_SECRET="your-google-client-secret"
   export FACEBOOK_APP_ID="your-facebook-app-id"
   export FACEBOOK_APP_SECRET="your-facebook-app-secret"
   ```

3. **Edit script configuration**:
   Open `azure-deploy.sh` and update:
   ```bash
   RESOURCE_GROUP="auth-api-rg"
   ACR_NAME="authapiregistry"  # Must be globally unique
   DNS_NAME_LABEL="my-auth-api"  # Must be globally unique
   ```

4. **Run deployment**:
   ```bash
   ./azure-deploy.sh
   ```

5. **Access your API**:
   ```
   http://my-auth-api.eastus.azurecontainer.io:8000
   ```

### Manual Deployment

#### Step 1: Create Resource Group

```bash
az group create \
  --name auth-api-rg \
  --location eastus
```

#### Step 2: Create Azure Container Registry

```bash
az acr create \
  --resource-group auth-api-rg \
  --name authapiregistry \
  --sku Basic \
  --admin-enabled true
```

#### Step 3: Build and Push Image

```bash
# Login to ACR
az acr login --name authapiregistry

# Build and push
az acr build \
  --registry authapiregistry \
  --image auth-api:latest \
  --file Dockerfile \
  .
```

#### Step 4: Deploy to Container Instances

```bash
az container create \
  --resource-group auth-api-rg \
  --name auth-api-container \
  --image authapiregistry.azurecr.io/auth-api:latest \
  --dns-name-label my-auth-api \
  --ports 8000 \
  --cpu 1 \
  --memory 1 \
  --environment-variables \
    JWT_ALGORITHM=HS256 \
    JWT_EXPIRATION_HOURS=24 \
    EMAIL_SERVICE=console \
  --secure-environment-variables \
    MONGODB_URI="$MONGODB_URI" \
    JWT_SECRET="$JWT_SECRET" \
  --restart-policy OnFailure
```

#### Step 5: Get Public URL

```bash
az container show \
  --resource-group auth-api-rg \
  --name auth-api-container \
  --query ipAddress.fqdn \
  --output tsv
```

### Managing the Deployment

**View logs**:
```bash
az container logs \
  --resource-group auth-api-rg \
  --name auth-api-container \
  --follow
```

**Restart container**:
```bash
az container restart \
  --resource-group auth-api-rg \
  --name auth-api-container
```

**Delete container**:
```bash
az container delete \
  --resource-group auth-api-rg \
  --name auth-api-container \
  --yes
```

**Update environment variables**:
```bash
# Delete and recreate with new variables
az container delete --resource-group auth-api-rg --name auth-api-container --yes
# Then run create command again with updated variables
```

---

## Azure App Service (Alternative)

### Deploy to Azure App Service

1. **Create App Service Plan**:
   ```bash
   az appservice plan create \
     --name auth-api-plan \
     --resource-group auth-api-rg \
     --sku B1 \
     --is-linux
   ```

2. **Create Web App**:
   ```bash
   az webapp create \
     --resource-group auth-api-rg \
     --plan auth-api-plan \
     --name my-auth-api-app \
     --deployment-container-image-name authapiregistry.azurecr.io/auth-api:latest
   ```

3. **Configure environment variables**:
   ```bash
   az webapp config appsettings set \
     --resource-group auth-api-rg \
     --name my-auth-api-app \
     --settings \
       MONGODB_URI="$MONGODB_URI" \
       JWT_SECRET="$JWT_SECRET" \
       JWT_ALGORITHM=HS256 \
       JWT_EXPIRATION_HOURS=24
   ```

4. **Enable HTTPS**:
   ```bash
   az webapp update \
     --resource-group auth-api-rg \
     --name my-auth-api-app \
     --https-only true
   ```

---

## Production Checklist

### Security

- [ ] Generate strong JWT_SECRET (32+ characters)
- [ ] Enable HTTPS/SSL
- [ ] Configure specific CORS origins (remove wildcard)
- [ ] Set up firewall rules
- [ ] Enable rate limiting
- [ ] Configure MongoDB IP whitelist
- [ ] Use secure environment variables
- [ ] Enable authentication on MongoDB
- [ ] Set up VPN or private networking
- [ ] Review and audit all endpoints

### Configuration

- [ ] Set EMAIL_SERVICE to 'azure' or 'sendgrid'
- [ ] Configure email sender domain
- [ ] Update FRONTEND_URL_WEB to production URL
- [ ] Update FRONTEND_URL_MOBILE to production URL
- [ ] Set appropriate JWT_EXPIRATION_HOURS
- [ ] Configure OAuth redirect URIs for production
- [ ] Set up custom domain
- [ ] Configure SSL certificates

### Monitoring

- [ ] Set up Azure Application Insights
- [ ] Configure logging
- [ ] Set up alerts for errors
- [ ] Monitor API performance
- [ ] Track usage metrics
- [ ] Set up uptime monitoring
- [ ] Configure backup strategy

### Testing

- [ ] Run all endpoint tests
- [ ] Test OAuth flows end-to-end
- [ ] Test password reset flow
- [ ] Load testing
- [ ] Security penetration testing
- [ ] Test CORS from production frontend
- [ ] Verify rate limiting works

### Documentation

- [ ] Update README with production URLs
- [ ] Document all environment variables
- [ ] Create runbook for common operations
- [ ] Document disaster recovery procedures
- [ ] Update API documentation with examples

---

## Environment Variables Reference

### Required

```env
MONGODB_URI=mongodb+srv://...           # MongoDB connection
JWT_SECRET=<secure-random-string>       # JWT signing key (CRITICAL!)
```

### Optional (Features)

```env
# OAuth - Google
GOOGLE_CLIENT_ID=<client-id>
GOOGLE_CLIENT_SECRET=<client-secret>
GOOGLE_REDIRECT_URI=https://your-domain.com/api/auth/google/callback

# OAuth - Facebook
FACEBOOK_APP_ID=<app-id>
FACEBOOK_APP_SECRET=<app-secret>
FACEBOOK_REDIRECT_URI=https://your-domain.com/api/auth/facebook/callback

# Email Service
EMAIL_SERVICE=azure                      # or 'sendgrid' or 'console'
AZURE_COMMUNICATION_CONNECTION_STRING=<connection-string>
FROM_EMAIL=noreply@yourdomain.com

# Frontend URLs
FRONTEND_URL_WEB=https://your-web-app.com
FRONTEND_URL_MOBILE=yourapp://auth
```

---

## Deployment Comparison

| Feature | Local Dev | Docker | ACI | App Service |
|---------|-----------|--------|-----|-------------|
| Setup Time | 5 min | 10 min | 20 min | 30 min |
| Cost | Free | Free | ~$15/mo | ~$13/mo |
| Scalability | No | No | Manual | Auto |
| HTTPS | No | No | Manual | Built-in |
| Custom Domain | No | No | Yes | Yes |
| Monitoring | No | Limited | Azure | Azure |
| Best For | Dev | Dev/Test | Production | Production |

---

## Post-Deployment Tasks

### 1. Update Frontend Configuration

Update your React web client:
```typescript
// web-client/src/config.ts
export const API_BASE_URL = 'https://my-auth-api.eastus.azurecontainer.io:8000';
```

Update your React Native mobile client:
```typescript
// mobile-app/config.ts
export const API_BASE_URL = 'https://my-auth-api.eastus.azurecontainer.io:8000';
```

### 2. Update OAuth Redirect URIs

In Google Cloud Console and Facebook Developer Portal:
- Add production callback URL
- Example: `https://my-auth-api.eastus.azurecontainer.io:8000/api/auth/google/callback`

### 3. Test Production Deployment

```bash
# Test health endpoint
curl https://my-auth-api.eastus.azurecontainer.io:8000/health

# Test registration
curl -X POST https://my-auth-api.eastus.azurecontainer.io:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com","password":"TestPass123"}'
```

### 4. Monitor and Maintain

- Check logs regularly
- Monitor error rates
- Review security alerts
- Update dependencies
- Backup database regularly

---

## Rollback Procedure

### Docker

```bash
# Stop current container
docker-compose down

# Revert code changes
git checkout previous-version

# Rebuild and restart
docker-compose up --build -d
```

### Azure Container Instances

```bash
# Deploy previous image version
az container create \
  --resource-group auth-api-rg \
  --name auth-api-container \
  --image authapiregistry.azurecr.io/auth-api:previous-tag \
  ...
```

---

## Support and Troubleshooting

### Common Issues

**Issue**: Container won't start
- **Solution**: Check logs with `az container logs`
- **Solution**: Verify all required environment variables are set

**Issue**: Cannot connect to MongoDB
- **Solution**: Check MONGODB_URI is correct
- **Solution**: Verify MongoDB network access (IP whitelist)

**Issue**: OAuth redirects fail
- **Solution**: Verify redirect URIs match exactly
- **Solution**: Check OAuth credentials are correct

**Issue**: High memory usage
- **Solution**: Increase container memory limit
- **Solution**: Optimize database queries

### Getting Help

1. Check server logs
2. Review API documentation at `/docs`
3. Test with Swagger UI
4. Check MongoDB connection
5. Verify environment variables

---

## Scaling Considerations

### Horizontal Scaling

For high traffic, consider:
- Azure Kubernetes Service (AKS)
- Multiple container instances behind load balancer
- Azure App Service with auto-scaling

### Performance Optimization

- Enable MongoDB indexes (already configured)
- Implement caching (Redis)
- Use connection pooling
- Optimize database queries
- Enable compression

### High Availability

- Deploy to multiple regions
- Set up health check monitoring
- Configure automatic restarts
- Implement database replication
- Set up backup and disaster recovery

---

## Cost Optimization

### Development

- Use `EMAIL_SERVICE=console` (free)
- Use MongoDB Atlas free tier
- Run locally (no Azure costs)

### Production

- Use Azure free tier when possible
- Monitor and set spending limits
- Use reserved instances for predictable workload
- Clean up unused resources
- Optimize container resource allocation

---

## Next Steps

1. ✅ Deploy to development environment
2. ✅ Test all endpoints
3. ⬜ Set up CI/CD pipeline
4. ⬜ Configure production OAuth
5. ⬜ Set up production email service
6. ⬜ Enable monitoring and alerts
7. ⬜ Perform security audit
8. ⬜ Load testing
9. ⬜ Deploy to production
10. ⬜ Update frontend to use production API
