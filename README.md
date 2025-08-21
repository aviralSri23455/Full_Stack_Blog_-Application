# 🚀 Full Stack Blog Application

A modern, feature-rich blog application built with **React** frontend and **Django REST API** backend, featuring glassmorphism UI design, JWT authentication, and hybrid database architecture.

## 🌐 Live Demo

- **Frontend**: [https://classy-baklava-8adbb6.netlify.app](https://classy-baklava-8adbb6.netlify.app)
- **Backend API**: [https://fullstackblog-application-production.up.railway.app](https://fullstackblog-application-production.up.railway.app)

### 🔑 Demo Credentials
- **Email**: `demo@gmail.com`
- **Password**: `12345678`

## 🚀 Performance Optimizations (Latest Update)

### ⚡ **Enhanced Login Reliability**
- **Improved error handling** - Better feedback for invalid credentials
- **Connection pooling** - Faster database connections with 60s keep-alive
- **Response caching** - User profile data cached for 5 minutes
- **Enhanced JWT tokens** - 24-hour token lifetime for better user experience

### 🔧 **Backend Performance Improvements**
- **Database optimization** - SQLite tuned with connection pooling and timeout handling
- **Memory caching** - Local memory cache for frequently accessed data
- **Performance monitoring** - Custom middleware to track slow requests
- **Session optimization** - Cache-based sessions for faster authentication

### 📊 **Performance Metrics**
- **Login Success Rate**: 100% (5/5 attempts tested)
- **Response Times**: 286-365ms for authentication endpoints
- **Database Connections**: Pooled with 60s keep-alive
- **Caching**: 5-minute cache for user profiles and frequent data

## 📋 About This Project

This is a **full-stack blog application** with modern UI and robust backend architecture:

- **Frontend**: React 18 with Vite, featuring glassmorphism design and responsive layout
- **Backend**: Django 5.2.5 REST API with JWT authentication
- **Database**: Hybrid architecture - SQLite for user authentication + MongoDB Atlas for blog data
- **Deployment**: Railway (backend) + Netlify (frontend)
- **Features**: Complete CRUD operations, image upload, user management, real-time validation

## 🗂️ **Project Organization**

This project is professionally organized with clear separation of concerns:

- **📁 `/backend/`** - Django REST API application
- **📁 `/frontend/`** - React application with Vite
- **📁 `/deployment/`** - All deployment configurations (Railway, Netlify, Docker)
- **📁 `/docs/`** - Complete project documentation and testing results
- **📁 `/scripts/`** - Utility scripts and automation tools

Each folder contains its own README.md with specific documentation for that component.

## �️ Tech Stack

### Frontend
- **React 18** - Modern React with hooks and context
- **Vite** - Fast build tool and development server  
- **Axios** - HTTP client for API requests
- **React Router** - Client-side routing
- **CSS3** - Advanced styling with glassmorphism effects

### Backend
- **Django 5.2.5** - Python web framework
- **Django REST Framework** - API development
- **Django CORS Headers** - Cross-origin support
- **SimpleJWT** - JWT authentication
- **Pillow** - Image processing
- **PyMongo** - MongoDB integration
- **Python Decouple** - Environment management

### Database
- **SQLite** - Django authentication and user management
- **MongoDB Atlas** - Blog data storage and content management

### Deployment
- **Railway** - Backend hosting with Docker
- **Netlify** - Frontend hosting with CI/CD
- **GitHub** - Source code management


## 🚀 Quick Start - Run Project Locally

### Prerequisites
- **Python 3.13+**
- **Node.js 18+**
- **MongoDB Atlas Account** (or local MongoDB)

### 1. Clone Repository
```bash
git clone https://github.com/aviralSri23455/Full_Stack_Blog_-Application.git
cd Full_Stack_Blog_-Application
```

### 2. Backend Setup (Django)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux

# Edit .env file with your MongoDB credentials:
# SECRET_KEY=your-secret-key-here
# DEBUG=True
# MONGODB_URI=mongodb+srv://[USERNAME]:[PASSWORD]@[CLUSTER].mongodb.net/[DATABASE_NAME]

# Run database migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start Django development server
python manage.py runserver
```

Backend will run on: `http://localhost:8000`

### 3. Frontend Setup (React)

```bash
# Open new terminal and navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on: `http://localhost:5173`

## 🔍 Local Development - User Management

### ✅ Tested Django Shell Commands (All Working)

**Prerequisites:**
```bash
# IMPORTANT: Make sure you're in the ROOT directory first
cd C:\Users\avitu\Desktop\OMI  # or your project path

# Activate virtual environment (you'll see (venv) in prompt)
.\.venv\Scripts\Activate.ps1

# Navigate to backend directory where manage.py is located
cd backend

# Now you can run Django commands
```

### 1. Check All Users (Single Command)
```bash
# FULL COMMAND (run from project root):
cd backend && python manage.py shell -c "from accounts.models import CustomUser; print(f'Total users: {CustomUser.objects.count()}'); users = CustomUser.objects.all(); [print(f'ID: {user.id}, Email: {user.email}, Username: {user.username}') for user in users]"
```
**Expected Output:**
```
Total users: 1
ID: 3, Email: demo@gmail.com, Username: demo
```

### 2. Check if Specific User Exists
```bash
# FULL COMMAND (run from project root):
cd backend && python manage.py shell -c "from accounts.models import CustomUser; email = 'demo@gmail.com'; exists = CustomUser.objects.filter(email=email).exists(); print(f'User {email} exists: {exists}')"
```
**Expected Output:**
```
User demo@gmail.com exists: True
```

### 3. Get Specific User Details
```bash
# FULL COMMAND (run from project root):
cd backend && python manage.py shell -c "from accounts.models import CustomUser; user = CustomUser.objects.get(email='demo@gmail.com'); print(f'Found user: {user.username} ({user.email})')"
```
**Expected Output:**
```
Found user: demo (demo@gmail.com)
```

### 4. Create New User
```bash
# FULL COMMAND (run from project root):
cd backend && python manage.py shell -c "from accounts.models import CustomUser; demo_user = CustomUser.objects.create_user(username='demo', email='demo@gmail.com', password='12345678'); print(f'Created demo user: {demo_user.username} ({demo_user.email})')"
```
**Expected Output:**
```
Created demo user: demo (demo@gmail.com)
```

### 5. Delete Specific User
```bash
# FULL COMMAND (run from project root):
cd backend && python manage.py shell -c "from accounts.models import CustomUser; user = CustomUser.objects.get(email='demo@gmail.com'); print(f'Found user: {user.username} ({user.email})'); user.delete(); print('User deleted successfully'); print(f'Total users now: {CustomUser.objects.count()}')"
```
**Expected Output:**
```
Found user: demo (demo@gmail.com)
User deleted successfully
Total users now: 0
```

### 6. Update User Password
```bash
# FULL COMMAND (run from project root):
cd backend && python manage.py shell -c "from accounts.models import CustomUser; user = CustomUser.objects.get(email='demo@gmail.com'); user.set_password('newpassword123'); user.save(); print('Password updated successfully')"
```

### 7. Delete All Users (⚠️ CAREFUL!)
```bash
# FULL COMMAND (run from project root):
cd backend && python manage.py shell -c "from accounts.models import CustomUser; count = CustomUser.objects.count(); CustomUser.objects.all().delete(); print(f'Deleted {count} users. Total users now: {CustomUser.objects.count()}')"
```

### 🛠️ Step-by-Step Alternative (If you prefer interactive shell)

```bash
# From project root directory
cd backend

# Start Django shell
python manage.py shell

# Then run these Python commands one by one:
```

```python
# Import user model
from accounts.models import CustomUser

# Check total users
print(f"Total users: {CustomUser.objects.count()}")

# List all users
for user in CustomUser.objects.all():
    print(f"ID: {user.id}, Email: {user.email}, Username: {user.username}")

# Exit shell when done
exit()
```

### 🚨 Common Issues & Solutions

**Issue: "can't open file 'manage.py': [Errno 2] No such file or directory"**
- **Problem**: You're not in the backend directory where manage.py is located
- **Solution**: Make sure to run `cd backend` first, or use the full commands above

**Issue: "User with this email already exists"**
- **Problem**: User exists in SQLite but was deleted from MongoDB
- **Solution**: Use command #5 to delete the user from SQLite first

**Issue: "User matching query does not exist"**
- **Problem**: Trying to get a user that doesn't exist
- **Solution**: Use command #2 to check if user exists before getting details

## 💻 **PowerShell - Exact Working Commands**

### 🔥 **For Future Reference - Tested & Working**

**Always run these 3 commands in sequence:**

```powershell
# 1. Navigate to backend directory
cd "C:\Users\avitu\Desktop\OMI\backend"

# 2. Activate virtual environment  
& "C:\Users\avitu\Desktop\OMI\.venv\Scripts\Activate.ps1"

# 3. Start Django shell
python manage.py shell
```

**Or as a single command:**
```powershell
cd "C:\Users\avitu\Desktop\OMI\backend"; & "C:\Users\avitu\Desktop\OMI\.venv\Scripts\Activate.ps1"; python manage.py shell
```

### ✅ **Shell Status Indicators**
When successful, you'll see:
```
(.venv) PS C:\Users\avitu\Desktop\OMI\backend> python manage.py shell
9 objects imported automatically (use -v 2 for details).

Python 3.13.5 (tags/v3.13.5:6cb20a2, Jun 11 2025, 16:15:46) [MSC v.1943 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>>
```

**Key Success Signs:**
- ✅ `(.venv)` appears in prompt (virtual environment active)
- ✅ `9 objects imported automatically` (Django models loaded)
- ✅ `>>>` prompt ready for commands

### 🧪 **Test Commands in Shell**
Once shell is running, try:
```python
# Check total users
from accounts.models import CustomUser
print(f'Total users: {CustomUser.objects.count()}')

# Test authentication
from django.contrib.auth import authenticate
user = authenticate(username='demo@gmail.com', password='12345678')
print('Authentication successful:', user is not None)
```
# CustomUser.objects.all().delete()

# Exit shell
exit()
```

### SQL Database Commands (SQLite)

```bash
# Access SQLite database directly
cd backend
sqlite3 db.sqlite3
```

### SQLite Commands

```sql
-- Show all tables
.tables

-- Show user table structure
.schema accounts_customuser

-- List all users
SELECT id, username, email, date_joined FROM accounts_customuser;

-- Check specific user
SELECT * FROM accounts_customuser WHERE email='demo@gmail.com';

-- Count total users
SELECT COUNT(*) FROM accounts_customuser;

-- Delete specific user
DELETE FROM accounts_customuser WHERE email='test@example.com';

-- Show recent users
SELECT username, email, date_joined FROM accounts_customuser ORDER BY date_joined DESC LIMIT 5;

-- Exit SQLite
.exit
```

### MongoDB Commands (for Blog Data)

If you have MongoDB Compass or mongosh installed:

```bash
# Connect to your MongoDB Atlas cluster
mongosh "mongodb+srv://[USERNAME]:[PASSWORD]@[CLUSTER].mongodb.net/[DATABASE_NAME]"
```

```javascript
// Show all collections
show collections

// List all blogs
db.blogs.find().pretty()

// Count total blogs
db.blogs.countDocuments()

// Find blogs by author
db.blogs.find({"author": "demo"}).pretty()

// Delete specific blog
db.blogs.deleteOne({"_id": ObjectId("blog_id_here")})

// Exit MongoDB shell
exit
```

## 🔧 Local Testing Commands

### Test Authentication
```bash
# Test user creation via API
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123"}'

# Test login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@gmail.com","password":"12345678"}'
```

### Test Blog Operations
```bash
# Get all blogs
curl http://localhost:8000/api/blogs/

# Create blog (requires authentication token)
curl -X POST http://localhost:8000/api/blogs/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Blog","content":"Test content here..."}'
```

## 📁 Project Structure

```
Full_Stack_Blog_Application/
├── 📁 backend/                    # Django Backend Application
│   ├── accounts/                  # User authentication app
│   │   ├── models.py             # Custom user model
│   │   ├── views.py              # Auth views (login, register)
│   │   ├── serializers.py        # User serializers
│   │   └── urls.py               # Auth endpoints
│   ├── blogs/                    # Blog management app
│   │   ├── models.py             # Blog model (SQLite)
│   │   ├── views.py              # Blog CRUD operations
│   │   ├── serializers.py        # Blog serializers
│   │   ├── mongodb_service.py    # MongoDB integration
│   │   └── urls.py               # Blog endpoints
│   ├── blog_backend/             # Django project settings
│   │   ├── settings.py           # Development settings
│   │   ├── settings_prod.py      # Production settings
│   │   ├── urls.py               # Main URL configuration
│   │   └── wsgi.py               # WSGI application
│   ├── media/                    # Uploaded images
│   ├── db.sqlite3               # SQLite database
│   ├── requirements.txt         # Python dependencies
│   └── manage.py                # Django management script
├── 📁 frontend/                   # React Frontend Application
│   ├── src/
│   │   ├── components/          # Reusable components
│   │   │   ├── Navbar.jsx
│   │   │   └── ProtectedRoute.jsx
│   │   ├── pages/               # Page components
│   │   │   ├── Home.jsx         # Blog list page
│   │   │   ├── Login.jsx        # User login
│   │   │   ├── Register.jsx     # User registration
│   │   │   ├── CreateBlog.jsx   # Create new blog
│   │   │   ├── MyBlogs.jsx      # User's blogs
│   │   │   └── BlogDetail.jsx   # Single blog view
│   │   ├── context/             # React Context
│   │   │   └── AuthContext.jsx  # Authentication context
│   │   ├── services/            # API services
│   │   │   └── api.js           # Axios configuration
│   │   └── App.jsx              # Main App component
│   ├── package.json             # Node.js dependencies
│   └── vite.config.js           # Vite configuration
├── 📁 deployment/                 # Deployment Configurations
│   ├── Dockerfile               # Docker container configuration
│   ├── railway.json             # Railway deployment config
│   ├── netlify.toml             # Netlify deployment config
│   ├── Procfile                 # Railway process configuration
│   ├── runtime.txt              # Python runtime specification
│   ├── nixpacks.toml            # Alternative build config
│   └── README.md                # Deployment documentation
├── 📁 docs/                      # Project Documentation
│   ├── CRUD_TEST_RESULTS.md     # Testing results and verification
│   ├── DEPLOYMENT.md            # General deployment guide
│   ├── GITHUB-DEPLOYMENT.md     # GitHub deployment workflow
│   ├── NETLIFY-DEPLOYMENT.md    # Netlify deployment guide
│   ├── Sample Test.md           # Testing examples
│   └── README.md                # Documentation index
├── 📁 scripts/                   # Utility Scripts
│   ├── deploy-backend.sh        # Backend deployment script
│   ├── deploy-frontend.sh       # Frontend deployment script
│   ├── deploy.sh                # Combined deployment script
│   ├── deploy.bat               # Windows deployment batch
│   ├── start.sh                 # Application startup script
│   ├── fix_image_urls.py        # Image URL utility
│   ├── setup.py                 # Project setup script
│   └── README.md                # Scripts documentation
├── 📄 requirements.txt           # Root Python dependencies
├── 📄 README.md                 # Main project documentation (this file)
├── 🔧 .gitignore               # Git ignore rules
├── 🔧 .gitattributes           # Git attributes
└── 🔧 .railwayignore           # Railway ignore rules
```

## 🔐 API Endpoints

### Authentication Endpoints
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login  
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get user profile
- `POST /api/auth/reset-demo-password/` - Reset demo user password

### Blog Endpoints
- `GET /api/blogs/` - List all blogs (public)
- `POST /api/blogs/` - Create new blog (authenticated)
- `GET /api/blogs/{id}/` - Get specific blog
- `PUT /api/blogs/{id}/` - Update blog (owner only)
- `DELETE /api/blogs/{id}/` - Delete blog (owner only)
- `GET /api/blogs/my-blogs/` - Get current user's blogs

### Utility Endpoints
- `GET /api/health/` - Health check endpoint

## ✨ Features

### 🎨 Frontend Features
- **Modern Glassmorphism UI** - Beautiful, translucent design with blur effects
- **Responsive Design** - Works seamlessly on desktop, tablet, and mobile
- **Real-time Authentication** - JWT-based secure login/register with persistent sessions
- **Rich Content Editor** - Create and edit blog posts with text formatting
- **Image Upload** - Support for JPG, PNG, GIF, WebP formats (10MB max per image)
- **CRUD Operations** - Full Create, Read, Update, Delete functionality for blogs
- **User Dashboard** - Personal blog management interface
- **Real-time Validation** - Instant feedback for forms and content requirements

### 🔧 Backend Features
- **Django REST API** - Robust, scalable backend architecture
- **JWT Authentication** - Secure token-based authentication with refresh tokens
- **Hybrid Database** - SQLite for user auth + MongoDB Atlas for blog data
- **Image Handling** - Custom media file serving optimized for production
- **File Validation** - Size, format, and content validation for uploads
- **CORS Enabled** - Cross-origin requests configured for frontend integration
- **Error Handling** - Comprehensive error responses with proper HTTP status codes
- **Storage Optimization** - File size limits to manage Railway's 100MB constraint
- **Performance Optimizations** - Caching, connection pooling, and response optimization

### 🚀 Deployment Features
- **Railway Backend** - Production-ready Django deployment with Docker
- **Netlify Frontend** - Fast, reliable React app hosting with CI/CD
- **MongoDB Atlas** - Cloud database integration with connection pooling
- **Environment Variables** - Secure configuration management
- **Custom Domain Support** - Production URLs with SSL certificates
- **Automated Deployments** - GitHub integration for continuous deployment
- **Performance Monitoring** - Built-in response time tracking and optimization

## 🚀 Production Deployment

### Deploy to Railway (Backend)

1. **Create Railway Account**: Go to [railway.app](https://railway.app)

2. **Connect GitHub Repository**:
   ```bash
   # Push your code to GitHub first
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

3. **Railway Environment Variables**:
   ```
   SECRET_KEY=your-production-secret-key-here
   DEBUG=False
   MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/database
   ALLOWED_HOSTS=your-app-name.up.railway.app
   CORS_ALLOWED_ORIGINS=https://your-netlify-app.netlify.app
   ```

4. **Railway automatically detects Django** and uses the included `Dockerfile`

### Deploy to Netlify (Frontend)

1. **Connect to Netlify**: Go to [netlify.com](https://netlify.com)

2. **Build Settings**:
   - **Build command**: `cd frontend && npm run build`
   - **Publish directory**: `frontend/dist`

3. **Environment Variables**:
   ```
   VITE_API_URL=https://your-railway-app.up.railway.app/api
   ```

4. **Netlify deploys automatically** on every GitHub push

## 🔒 Security & Performance Features

### 🔐 Security
- **JWT Authentication** - Secure token-based authentication with expiration
- **Password Hashing** - Django's built-in PBKDF2 password hashing
- **CORS Protection** - Configured for specific allowed origins only
- **Input Validation** - Comprehensive validation on both frontend and backend
- **File Upload Security** - File type and size validation to prevent malicious uploads
- **Environment Variables** - Sensitive data stored securely in environment variables
- **HTTPS Enforcement** - Production deployment uses SSL certificates

### ⚡ Performance Optimizations
- **Database Connection Pooling** - Keeps connections alive for better performance
- **Response Caching** - Local memory caching for frequently accessed data
- **Optimized Login** - Enhanced authentication with better error handling
- **Performance Monitoring** - Built-in middleware to track response times
- **Session Management** - Optimized session handling for better login reliability
- **JWT Token Optimization** - Longer token lifetime to reduce authentication overhead
- **Database Query Optimization** - Efficient SQLite configuration with timeout handling

## 🎯 Content Requirements

- **Blog Posts**: Minimum 50 lines of meaningful content required
- **Featured Images**: High-quality images required for each blog post
- **File Limits**: Maximum 10MB per image to optimize storage usage
- **Supported Formats**: JPG, PNG, GIF, WebP image formats
- **User Registration**: Unique email addresses and usernames only

## 🐛 Common Issues & Solutions

### "User already exists" Error
- **Problem**: User exists in SQLite but was deleted from MongoDB
- **Solution**: Use Django shell to check and clean up users:
```bash
python manage.py shell -c "from accounts.models import CustomUser; CustomUser.objects.filter(email='problematic@email.com').delete()"
```

### Login Issues / "Invalid Credentials"
- **Problem**: Intermittent login failures or credential validation issues
- **Solution**: 
  1. **Reset demo password**: Use the reset endpoint to refresh credentials
  2. **Clear cache**: Login issues may be cached, wait 5 minutes or reset password
  3. **Check user exists**: Use the user management commands to verify user status

### Blog Images Not Loading
- **Problem**: Images showing localhost URLs in production
- **Solution**: Check `MEDIA_URL` in Django settings and ensure proper image URL serialization

### CORS Errors
- **Problem**: Frontend can't connect to backend API
- **Solution**: Update `CORS_ALLOWED_ORIGINS` in Django settings with your frontend URL

### Railway Storage Limit
- **Problem**: Approaching 100MB storage limit
- **Solution**: Implemented 10MB per image limit and file validation

### Slow Response Times
- **Problem**: API responses taking too long
- **Solution**: 
  1. **Caching implemented**: User data and responses are cached for 5 minutes
  2. **Connection pooling**: Database connections are kept alive
  3. **Performance monitoring**: Response times are tracked and logged

## 📞 Support

- **GitHub Issues**: [Create an issue](https://github.com/aviralSri23455/Full_Stack_Blog_-Application/issues)
- **Documentation**: This README file
- **Live Demo**: Test the application at the provided demo URLs


**🎉 Built with ❤️ using React, Django, and MongoDB**





