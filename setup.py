from setuptools import setup, find_packages

setup(
    name="blog-backend",
    version="1.0.0",
    description="Django Blog Backend API",
    packages=find_packages(where="backend"),
    package_dir={"": "backend"},
    python_requires=">=3.11",
    install_requires=[
        "django>=5.2.5",
        "djangorestframework>=3.14.0",
        "djangorestframework-simplejwt>=5.3.0",
        "django-cors-headers>=4.3.0",
        "python-decouple>=3.8",
        "pymongo>=4.5.0",
        "Pillow>=10.0.0",
        "gunicorn>=21.2.0",
        "boto3>=1.28.0",
        "django-storages>=1.14.0",
        "psycopg2-binary>=2.9.7",
        "whitenoise>=6.5.0",
        "django-environ>=0.11.0",
    ],
)
