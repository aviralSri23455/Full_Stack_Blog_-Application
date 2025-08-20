# GitHub Deployment Setup Guide

This guide explains how to set up your blog application for GitHub and handle environment variables securely.

## 🔒 Environment Variables and GitHub

### Why Environment Variables Matter

Environment variables contain sensitive information like:
- Database credentials
- Secret keys
- API keys
- AWS credentials

**NEVER commit these to GitHub!**

## 📁 File Structure for GitHub

### Files to Include in GitHub:
```
✅ All source code files
✅ .env.example (template file)
✅ requirements.txt
✅ package.json
✅ README.md
✅ DEPLOYMENT.md
✅ .gitignore
```

### Files to EXCLUDE from GitHub:
```
❌ .env (contains real secrets)
❌ db.sqlite3 (database file)
❌ media/ (uploaded files)
❌ node_modules/
❌ __pycache__/
❌ .vscode/
❌ logs/
```

## 🚀 GitHub Setup Steps

### 1. Prepare Repository

```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit initial version
git commit -m "Initial commit: Modern Blog Application"

# Add GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git push -u origin main
```

### 2. Environment Variables Strategy

#### For Local Development:
1. Copy `.env.example` to `.env`
2. Fill in your local values
3. `.env` is ignored by git (in .gitignore)

#### For Production Deployment:
1. Use `.env.example` as template
2. Create `.env` on production server
3. Fill with production values

### Example `.env` file structure:

**Local (.env):**
```env
SECRET_KEY=your-local-secret-key
DEBUG=True
MONGODB_URI=mongodb://localhost:27017/blog_local
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

**Production (.env):**
```env
SECRET_KEY=super-secure-production-key-min-50-characters-long
DEBUG=False
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/blog_prod
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
```

## 🔧 GitHub Actions (Optional CI/CD)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy Blog Application

on:
  push:
    branches: [ main ]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to EC2
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: ${{ secrets.EC2_HOST }}
        username: ubuntu
        key: ${{ secrets.EC2_SSH_KEY }}
        script: |
          cd /home/ubuntu/OMI
          git pull origin main
          cd backend
          source venv/bin/activate
          pip install -r requirements.txt
          python manage.py migrate
          python manage.py collectstatic --noinput
          sudo systemctl restart gunicorn
          sudo systemctl restart nginx

  deploy-frontend:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '20'
    
    - name: Install and Build
      run: |
        cd frontend
        npm ci
        echo "VITE_API_URL=${{ secrets.API_URL }}" > .env.production
        npm run build
    
    - name: Deploy to S3
      env:
        AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
        AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
      run: |
        cd frontend
        aws s3 sync dist/ s3://${{ secrets.S3_BUCKET }} --delete
        aws cloudfront create-invalidation --distribution-id ${{ secrets.CLOUDFRONT_ID }} --paths "/*"
```

### GitHub Secrets Setup:

1. Go to GitHub Repository → Settings → Secrets and Variables → Actions
2. Add these secrets:

```
EC2_HOST=your-ec2-ip-address
EC2_SSH_KEY=your-private-key-content
API_URL=https://your-api-domain.com/api
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
S3_BUCKET=your-frontend-bucket
CLOUDFRONT_ID=your-cloudfront-id
```

## 📝 Repository Best Practices

### 1. README.md Structure:
```markdown
# Project Title
## Features
## Tech Stack
## Installation
## Usage
## Deployment
## Contributing
```

### 2. Branch Strategy:
```
main        → Production-ready code
develop     → Development branch
feature/*   → Feature branches
hotfix/*    → Critical fixes
```

### 3. Commit Messages:
```
feat: add user authentication
fix: resolve CORS issue
docs: update deployment guide
style: improve blog card design
refactor: optimize API endpoints
```

### 4. Release Process:
```bash
# Create release branch
git checkout -b release/v1.0.0

# Update version numbers
# Test thoroughly

# Merge to main
git checkout main
git merge release/v1.0.0

# Tag release
git tag -a v1.0.0 -m "Version 1.0.0 - Initial release"
git push origin v1.0.0
```

## 🛡️ Security Checklist

### Before Pushing to GitHub:

- [ ] `.env` file is in `.gitignore`
- [ ] No hardcoded secrets in code
- [ ] `.env.example` contains only placeholder values
- [ ] Database files are ignored
- [ ] Media files are ignored
- [ ] All sensitive configs use environment variables

### Example of BAD code (don't do this):
```python
# ❌ BAD - Hardcoded secrets
SECRET_KEY = 'django-insecure-actual-secret-key'
MONGODB_URI = 'mongodb+srv://user:realpass@cluster.mongodb.net/'
```

### Example of GOOD code:
```python
# ✅ GOOD - Using environment variables
SECRET_KEY = config('SECRET_KEY')
MONGODB_URI = config('MONGODB_URI')
```

## 🔄 Deployment Workflow

### 1. Development:
```bash
# Work on feature
git checkout -b feature/new-feature
# Make changes
git add .
git commit -m "feat: add new feature"
git push origin feature/new-feature
# Create Pull Request
```

### 2. Production Deployment:
```bash
# After PR is merged to main
# SSH to production server
ssh ubuntu@your-server

# Update code
cd /home/ubuntu/OMI
git pull origin main

# Run deployment script
./deploy-backend.sh

# Update frontend
# Run from local machine
./deploy-frontend.sh
```

## 📊 Monitoring Deployment

### Check Deployment Status:
```bash
# Backend health
curl https://your-api-domain.com/api/

# Frontend health
curl https://your-frontend-domain.com

# Server status
systemctl status gunicorn
systemctl status nginx
```

### Logs Location:
```bash
# Application logs
tail -f /home/ubuntu/OMI/backend/logs/django.log

# Gunicorn logs
journalctl -u gunicorn.service -f

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

## 🚨 Emergency Procedures

### Rollback Deployment:
```bash
# Find last working commit
git log --oneline

# Rollback to specific commit
git checkout COMMIT_HASH
./deploy-backend.sh
```

### Database Backup:
```bash
# Backup SQLite
cp /home/ubuntu/OMI/backend/db.sqlite3 /home/ubuntu/backups/db_$(date +%Y%m%d_%H%M%S).sqlite3

# MongoDB backup (if needed)
mongodump --uri="your-mongodb-uri" --out=/home/ubuntu/backups/mongo_$(date +%Y%m%d_%H%M%S)
```

---

## 📋 Pre-Deployment Checklist

Before deploying to production:

- [ ] All environment variables configured
- [ ] .env.example updated with all required variables
- [ ] Database migrations tested
- [ ] Static files collection working
- [ ] CORS origins configured correctly
- [ ] SSL certificates ready
- [ ] Domain DNS configured
- [ ] Firewall rules set
- [ ] Backup strategy in place
- [ ] Monitoring tools configured
- [ ] Error logging enabled

Remember: **Test everything in a staging environment first!**
