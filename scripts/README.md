# 🛠️ Scripts and Utilities

This folder contains utility scripts and automation tools for the project.

## 📁 Files in this folder:

### 🚀 **Deployment Scripts**
- **`deploy-backend.sh`** - Backend deployment automation script
- **`deploy-frontend.sh`** - Frontend deployment automation script
- **`deploy.sh`** - Combined deployment script for both backend and frontend
- **`deploy.bat`** - Windows batch file for deployment
- **`start.sh`** - Application startup script

### 🔧 **Utility Scripts**
- **`fix_image_urls.py`** - Python utility to fix image URL issues in production
- **`setup.py`** - Project setup and initialization script

## 🎯 **Script Purposes**

### 🌐 **Deployment Automation**
- **Cross-platform**: Both shell scripts (Linux/macOS) and batch files (Windows)
- **Automated workflows**: Streamline deployment processes
- **Error handling**: Built-in error checking and validation

### 🛠️ **Maintenance Tools**
- **Image URL fixes**: Resolve production image serving issues
- **Setup automation**: Initialize project environments
- **Startup helpers**: Quick application launching

## ⚠️ **Usage Notes**

### 🔒 **Safety First**
- Review scripts before running in production
- Test in development environment first
- Some scripts may require environment variables

### 🎮 **How to Use**
```bash
# Make scripts executable (Linux/macOS)
chmod +x *.sh

# Run deployment scripts
./deploy.sh                # Combined deployment
./deploy-backend.sh        # Backend only
./deploy-frontend.sh       # Frontend only

# Windows users
deploy.bat                 # Use batch file

# Utility scripts
python fix_image_urls.py   # Fix image URL issues
python setup.py           # Project setup
```

## 🔄 **Maintenance**
- Scripts are kept separate from source code for better organization
- Easy to modify and maintain without affecting application code
- Version controlled for change tracking

---
*These scripts help automate common tasks and maintain the application efficiently.*
