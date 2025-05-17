# Deployment Guide

This guide explains how to deploy the Slate EV Truck API to various hosting platforms.

## Current Deployments

### Documentation Site

The documentation for this project is currently deployed on Netlify:

- **Live URL**: [https://cool-baklava-79da84.netlify.app/](https://cool-baklava-79da84.netlify.app/)
- **Deploy Status**: [![Netlify Status](https://api.netlify.com/api/v1/badges/9a67d4ca-a675-4c4b-ace4-26453b4bc15d/deploy-status)](https://app.netlify.com/sites/cool-baklava-79da84/deploys)

## Deployment Options

Here are the top options for deploying your FastAPI application, ordered by ease of use:

## 1. Netlify (Used for This Documentation)

This documentation site is deployed on Netlify. For the API itself, you'd want to use one of the options below.

## 2. Railway.app (Recommended for the API)

[Railway.app](https://railway.app/) offers the simplest deployment process with a generous free tier:

1. Go to [Railway.app](https://railway.app/) and sign up with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Add environment variables:
   ```
   DATABASE_URL=sqlite:///./slate.db
   ENVIRONMENT=production
   ```
5. Railway will automatically:
   - Detect your Python application
   - Set up the build configuration
   - Deploy your application
   - Provide you with a URL

**Free Tier Includes:**

- 500 hours of runtime per month
- 1GB of storage
- Automatic HTTPS
- Continuous deployment from GitHub
- Built-in monitoring

## 3. Render.com

[Render](https://render.com/) provides a simple deployment process with a free tier:

1. Sign up at [Render.com](https://render.com/)
2. Connect your GitHub repository
3. Create a new Web Service
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Environment Variables:
     ```
     DATABASE_URL=sqlite:///./slate.db
     ENVIRONMENT=production
     ```

**Free Tier Includes:**

- 750 hours of runtime per month
- Automatic HTTPS
- Continuous deployment
- Custom domains

## 4. PythonAnywhere

[PythonAnywhere](https://www.pythonanywhere.com/) is great for Python applications:

1. Sign up for a free account
2. Go to Web tab and create a new web app
3. Choose "FastAPI" as your framework
4. Upload your code or clone from GitHub
5. Configure your virtual environment and requirements

**Free Tier Includes:**

- 512MB of storage
- HTTPS support
- Custom domains
- Basic monitoring

## 5. Fly.io

[Fly.io](https://fly.io/) offers a generous free tier with global deployment:

1. Install Fly CLI:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```
2. Sign up and login:
   ```bash
   fly auth signup
   fly auth login
   ```
3. Create a `fly.toml`:
   ```bash
   fly launch
   ```
4. Deploy:
   ```bash
   fly deploy
   ```

**Free Tier Includes:**

- 3 shared-cpu VMs
- 3GB persistent volume storage
- 160GB outbound data transfer
- Global edge network

## Production Deployment Checklist

Before deploying to production, ensure you:

### 1. Environment Variables

Set up environment variables:

- `DATABASE_URL`: Use a proper production database URL
- `ENVIRONMENT=production`: To enable production settings
- Any other API keys or secrets

### 2. Database Configuration

- Consider using a managed database service:
  - PostgreSQL on Railway, Render, or AWS RDS
  - MySQL/MariaDB on various platforms
- Set up database migrations
- Configure database connection pooling
- Set up backups

### 3. Security Measures

- Enable CORS with proper settings
- Set up proper authentication if needed
- Ensure HTTPS is enabled
- Configure rate limiting
- Set up monitoring for security events

### 4. Performance Optimization

- Configure proper number of workers
- Set up caching if needed
- Optimize database queries
- Consider using a CDN

### 5. Monitoring and Logging

- Set up application monitoring
- Configure error tracking (Sentry, etc.)
- Set up logging
- Configure performance monitoring

## Netlify Deployment for Documentation

This documentation is deployed to Netlify using the following configuration:

1. The `netlify.toml` file in the `docs/` directory:

```toml
[build]
  base = "docs/"
  command = "pip install -r requirements.txt && mkdocs build"
  publish = "site"

[build.environment]
  PYTHON_VERSION = "3.11"
  PIP_DISABLE_PIP_VERSION_CHECK = "1"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

2. The `requirements.txt` file in the `docs/` directory:

```
mkdocs==1.5.3
mkdocs-material==9.4.7
markdown==3.5.1
mkdocs-autorefs==0.5.0
mkdocstrings==0.22.0
mkdocstrings-python==1.7.3
pymdown-extensions==10.3.1
```

3. Steps to deploy your own documentation:

   - Fork or clone this repository
   - Sign up for Netlify and connect your GitHub repository
   - Configure the build settings:
     - Base directory: `docs/`
     - Build command: `pip install -r requirements.txt && mkdocs build`
     - Publish directory: `site/`
   - Click "Deploy site"
   - Optionally configure a custom domain
