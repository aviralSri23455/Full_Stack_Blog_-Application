@echo off
echo 🚀 Starting deployment process...

REM Backend deployment
echo 📦 Setting up backend...
cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call .\venv\Scripts\Activate.ps1

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Run migrations
echo Running database migrations...
python manage.py migrate

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput

cd ..

REM Frontend deployment
echo 🎨 Setting up frontend...
cd frontend

REM Install dependencies
echo Installing Node.js dependencies...
npm install

REM Build for production
echo Building frontend for production...
npm run build

cd ..

echo ✅ Deployment completed successfully!
echo.
echo Next steps:
echo 1. Configure your web server (IIS/nginx)
echo 2. Set up SSL certificates
echo 3. Configure environment variables
echo 4. Start the Django server with: python manage.py runserver
echo 5. Serve the frontend build files from frontend/dist/

pause
