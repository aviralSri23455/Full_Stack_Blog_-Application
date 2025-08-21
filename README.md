# 🚀 Full Stack Blog Application

A modern blog application built with **React** frontend and **Django REST API** backend, featuring glassmorphism UI design, JWT authentication, and hybrid database architecture.

## 🌐 Live Demo

- **Frontend**: [https://665e2cd37e84b418a5ca85e8--wonderful-melba-ea4e8b.netlify.app](https://665e2cd37e84b418a5ca85e8--wonderful-melba-ea4e8b.netlify.app)
- **Backend API**: [https://fullstackblog-application-production.up.railway.app](https://fullstackblog-application-production.up.railway.app)

### 🔑 Demo Credentials
- **Email**: `demo@gmail.com`
- **Password**: `12345678`

## 🛠️ Tech Stack

### Frontend
- **React 18** with Vite
- **Axios** for API requests
- **React Router** for routing
- **CSS3** with glassmorphism design

### Backend
- **Django 5.2.5** with REST Framework
- **JWT Authentication** (SimpleJWT)
- **Pillow** for image processing
- **PyMongo** for MongoDB integration

### Database
- **SQLite** - User authentication
- **MongoDB Atlas** - Blog data storage

### Deployment
- **Railway** - Backend hosting
- **Netlify** - Frontend hosting
- **GitHub** - Source code management

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Node.js 18+
- MongoDB Atlas account

### 1. Clone Repository
```bash
git clone https://github.com/aviralSri23455/Full_Stack_Blog_-Application.git
cd Full_Stack_Blog_-Application
```

### 2. Backend Setup
```bash
cd backend

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate    # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file with:
# SECRET_KEY=your-secret-key
# DEBUG=True
# MONGODB_URI=your-mongodb-connection-string

# Run migrations and start server
python manage.py migrate
python manage.py runserver
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## 📁 Project Structure

```
├── backend/
│   ├── accounts/          # User authentication
│   ├── blogs/            # Blog management
│   ├── blog_backend/     # Django settings
│   └── media/           # Uploaded images
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/      # Page components
│   │   ├── context/    # Auth context
│   │   └── services/   # API services
│   └── package.json
└── README.md
```

## 🔐 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `GET /api/auth/profile/` - Get user profile

### Blogs
- `GET /api/blogs/` - List all blogs
- `POST /api/blogs/` - Create blog (authenticated)
- `GET /api/blogs/{id}/` - Get specific blog
- `PUT /api/blogs/{id}/` - Update blog (owner only)
- `DELETE /api/blogs/{id}/` - Delete blog (owner only)
- `GET /api/blogs/my-blogs/` - Get user's blogs

## ✨ Features

- **Modern Glassmorphism UI** with responsive design
- **JWT Authentication** with secure login/register
- **CRUD Operations** for blog management
- **Image Upload** support (10MB max)
- **Hybrid Database** architecture
- **Real-time Validation** and error handling
- **Production Ready** deployment configuration

## 🔧 Local User Management

### Django Shell Commands
```bash
cd backend
python manage.py shell
```

```python
# Check users
from accounts.models import CustomUser
print(f"Total users: {CustomUser.objects.count()}")

# List all users
for user in CustomUser.objects.all():
    print(f"ID: {user.id}, Email: {user.email}")

# Delete user if needed
CustomUser.objects.filter(email='user@example.com').delete()

exit()
```

## 🚀 Deployment

### Railway (Backend)
1. Connect GitHub repository
2. Set environment variables:
   ```
   SECRET_KEY=production-secret-key
   DEBUG=False
   MONGODB_URI=your-mongodb-atlas-uri
   ALLOWED_HOSTS=your-railway-domain.up.railway.app
   CORS_ALLOWED_ORIGINS=https://your-netlify-app.netlify.app
   ```

### Netlify (Frontend)
1. Connect GitHub repository
2. Build settings:
   - **Build command**: `cd frontend && npm run build`
   - **Publish directory**: `frontend/dist`
3. Environment variable:
   - `VITE_API_URL=https://your-railway-app.up.railway.app/api`

## 📄 License

MIT License - Open source project

---

**Built with ❤️ using React, Django, and MongoDB**
