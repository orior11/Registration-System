#!/bin/bash

# Azure Container Instances Deployment Script
# This script builds, pushes, and deploys the authentication API to Azure

set -e  # Exit on any error

# Configuration - Update these values
RESOURCE_GROUP="auth-api-rg"
LOCATION="eastus"
ACR_NAME="authapiregistry"
IMAGE_NAME="auth-api"
IMAGE_TAG="latest"
CONTAINER_NAME="auth-api-container"
DNS_NAME_LABEL="my-auth-api"

echo "🚀 Starting Azure deployment..."

# Step 1: Create Resource Group (if it doesn't exist)
echo "📦 Creating resource group..."
az group create --name $RESOURCE_GROUP --location $LOCATION || echo "Resource group already exists"

# Step 2: Create Azure Container Registry (if it doesn't exist)
echo "🏗️  Creating Azure Container Registry..."
az acr create \
  --resource-group $RESOURCE_GROUP \
  --name $ACR_NAME \
  --sku Basic \
  || echo "ACR already exists"

# Step 3: Enable admin access on ACR
echo "🔑 Enabling admin access on ACR..."
az acr update --name $ACR_NAME --admin-enabled true

# Step 4: Get ACR credentials
echo "🔐 Getting ACR credentials..."
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query username -o tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query passwords[0].value -o tsv)
ACR_SERVER=$(az acr show --name $ACR_NAME --query loginServer -o tsv)

echo "ACR Server: $ACR_SERVER"

# Step 5: Build and push image to ACR
echo "🏗️  Building and pushing Docker image to ACR..."
az acr build \
  --registry $ACR_NAME \
  --image $IMAGE_NAME:$IMAGE_TAG \
  --file Dockerfile \
  .

# Step 6: Deploy to Azure Container Instances
echo "🚢 Deploying to Azure Container Instances..."
az container create \
  --resource-group $RESOURCE_GROUP \
  --name $CONTAINER_NAME \
  --image $ACR_SERVER/$IMAGE_NAME:$IMAGE_TAG \
  --registry-login-server $ACR_SERVER \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --dns-name-label $DNS_NAME_LABEL \
  --ports 8000 \
  --cpu 1 \
  --memory 1 \
  --environment-variables \
    JWT_ALGORITHM=HS256 \
    JWT_EXPIRATION_HOURS=24 \
    EMAIL_SERVICE=console \
    FRONTEND_URL_WEB=https://${DNS_NAME_LABEL}.${LOCATION}.azurecontainer.io \
  --secure-environment-variables \
    MONGODB_URI=$MONGODB_URI \
    JWT_SECRET=$JWT_SECRET \
    GOOGLE_CLIENT_ID=$GOOGLE_CLIENT_ID \
    GOOGLE_CLIENT_SECRET=$GOOGLE_CLIENT_SECRET \
    FACEBOOK_APP_ID=$FACEBOOK_APP_ID \
    FACEBOOK_APP_SECRET=$FACEBOOK_APP_SECRET \
  --restart-policy OnFailure

# Step 7: Get the FQDN
echo "✅ Deployment complete!"
FQDN=$(az container show \
  --resource-group $RESOURCE_GROUP \
  --name $CONTAINER_NAME \
  --query ipAddress.fqdn \
  --output tsv)

echo ""
echo "======================================"
echo "🎉 Deployment Successful!"
echo "======================================"
echo "API URL: http://${FQDN}:8000"
echo "API Docs: http://${FQDN}:8000/docs"
echo "Health Check: http://${FQDN}:8000/health"
echo "======================================"
echo ""
echo "To view logs:"
echo "az container logs --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME"
echo ""
echo "To delete the container:"
echo "az container delete --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME --yes"
