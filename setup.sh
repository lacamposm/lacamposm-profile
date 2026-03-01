#!/bin/bash
set -e

PROJECT_ID=$(gcloud config get-value project)
SERVICE_NAME="lacamposm-profile"
DOMAIN="www.lacamposm.com"

echo "Deploying to Cloud Run in project $PROJECT_ID..."

# Enable necessary APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# Submit cloud build
gcloud builds submit --config cloudbuild.yaml .

# You might need to verify domain ownership first before mapping
echo "Mapping domain $DOMAIN to Cloud Run service $SERVICE_NAME..."
gcloud beta run domain-mappings create --service $SERVICE_NAME --domain $DOMAIN --region us-central1 || \
echo "Domain mapping failed. Ensure domain is verified in Google Search Console and Cloud Run Domain Mappings."

echo "Setup and deployment complete."
