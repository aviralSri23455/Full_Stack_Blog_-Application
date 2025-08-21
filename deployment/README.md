# 🚀 Deployment Configuration

This folder contains all deployment configuration files for the Full Stack Blog Application.

## 📁 Files in this folder:

### 🐳 **Docker Configuration**
- **`Dockerfile`** - Docker container configuration for Railway backend deployment
- **`railway.json`** - Railway platform-specific configuration
- **`runtime.txt`** - Python runtime version specification

### 🌐 **Frontend Deployment**
- **`netlify.toml`** - Netlify deployment configuration for React frontend
- **`nixpacks.toml`** - Alternative build configuration (not currently used)

### 📦 **Build Configuration**
- **`Procfile`** - Process file for Railway deployment (defines how to run the app)

## ⚠️ **Important Notes:**

### 🔒 **Do Not Modify These Files**
These files are critical for deployment and any changes could break:
- Railway backend deployment
- Netlify frontend deployment
- Production environment configurations

### 🏗️ **Current Deployment Setup**
- **Backend**: Railway uses `Dockerfile` and `railway.json`
- **Frontend**: Netlify uses `netlify.toml` and `package.json` build commands
- **Build Process**: Fully automated via GitHub integration

## 🔧 **Active Configurations**

### Railway Backend
```json
// railway.json - Railway deployment configuration
{
  "build": {
    "builder": "dockerfile"
  },
  "deploy": {
    "numReplicas": 1
  }
}
```

### Netlify Frontend
```toml
# netlify.toml - Netlify deployment configuration
[build]
  command = "cd frontend && npm install && npm run build"
  publish = "frontend/dist"

[build.environment]
  NODE_VERSION = "18"
```

## 🚀 **Live Deployments**
- **Backend**: https://fullstackblog-application-production.up.railway.app
- **Frontend**: https://665e2cd37e84b418a5ca85e8--wonderful-melba-ea4e8b.netlify.app

---
*This folder keeps all deployment configurations organized and separate from source code.*
