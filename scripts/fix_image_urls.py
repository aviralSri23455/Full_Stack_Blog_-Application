"""
MongoDB URL Fix Script
Run this locally to update existing blog image URLs from localhost to Railway production URLs
"""

import os
from pymongo import MongoClient
from urllib.parse import quote_plus

# MongoDB connection (use your actual credentials)
username = "teamproject440"
password = quote_plus("yWr7BNo8QSc3F0lT")
cluster = "cluster20.hi6xiaz.mongodb.net"
database_name = "myDatabase"

# MongoDB URI
mongo_uri = f"mongodb+srv://{username}:{password}@{cluster}/{database_name}?retryWrites=true&w=majority&appName=Cluster20"

# Railway production URL
railway_url = "https://fullstackblog-application-production.up.railway.app"

def fix_image_urls():
    try:
        # Connect to MongoDB
        client = MongoClient(mongo_uri)
        db = client[database_name]
        
        # Get blogs collection
        blogs_collection = db.blogs_blog
        
        # Find all blogs with localhost image URLs
        blogs_with_localhost = blogs_collection.find({
            "image": {"$regex": "http://localhost:8000/media/"}
        })
        
        updated_count = 0
        for blog in blogs_with_localhost:
            old_url = blog["image"]
            # Replace localhost:8000 with Railway URL
            new_url = old_url.replace("http://localhost:8000", railway_url)
            
            # Update the blog
            result = blogs_collection.update_one(
                {"_id": blog["_id"]},
                {"$set": {"image": new_url}}
            )
            
            if result.modified_count > 0:
                updated_count += 1
                print(f"Updated blog '{blog.get('title', 'Unknown')}': {old_url} -> {new_url}")
        
        print(f"\nTotal blogs updated: {updated_count}")
        client.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_image_urls()
