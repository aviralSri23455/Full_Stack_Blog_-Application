#!/usr/bin/env python
"""
Script to clean all users and blogs from both Django and MongoDB databases
"""
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_backend.settings')
django.setup()

from accounts.models import CustomUser
from blogs.models import Blog
from blogs.mongodb_service import MongoDBService

def clean_databases():
    print("=== CLEANING DATABASES ===")
    
    # Clean Django SQLite database
    user_count = CustomUser.objects.count()
    blog_count = Blog.objects.count()
    
    print(f"Django - Users before deletion: {user_count}")
    print(f"Django - Blogs before deletion: {blog_count}")
    
    if user_count > 0:
        CustomUser.objects.all().delete()
        print("✅ Django users deleted")
    
    if blog_count > 0:
        Blog.objects.all().delete()
        print("✅ Django blogs deleted")
    
    # Clean MongoDB
    try:
        db = MongoDBService()
        
        # Count ALL MongoDB documents (not just published ones)
        mongo_blogs = db.db.blogs.count_documents({}) if db.db is not None else 0
        mongo_users = db.db.users.count_documents({}) if db.db is not None else 0
        
        print(f"MongoDB - Users before deletion: {mongo_users}")
        print(f"MongoDB - Blogs before deletion: {mongo_blogs}")
        
        # Delete from MongoDB
        if mongo_users > 0:
            user_result = db.db.users.delete_many({})
            print(f"✅ MongoDB users deleted: {user_result.deleted_count}")
        
        if mongo_blogs > 0:
            # Try multiple approaches to delete blogs
            blog_result = db.db.blogs.delete_many({})
            print(f"✅ MongoDB blogs delete_many result: {blog_result.deleted_count}")
            
            # Try dropping the collection
            db.db.blogs.drop()
            print("✅ MongoDB blogs collection dropped")
            
            # Recreate empty collection
            db.db.create_collection('blogs')
            print("✅ MongoDB blogs collection recreated")
        
        # Final verification using direct count (not get_all_blogs)
        print("\n=== FINAL STATUS ===")
        print(f"Django Users remaining: {CustomUser.objects.count()}")
        print(f"Django Blogs remaining: {Blog.objects.count()}")
        print(f"MongoDB Users remaining: {db.db.users.count_documents({}) if db.db is not None else 0}")
        print(f"MongoDB Blogs remaining: {db.db.blogs.count_documents({}) if db.db is not None else 0}")
        print("=== DATABASES CLEANED ===")
        
    except Exception as e:
        print(f"MongoDB Error: {e}")

if __name__ == "__main__":
    clean_databases()
