import pymongo
from django.conf import settings
from datetime import datetime
import json
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)


class MongoDBService:
    def __init__(self):
        try:
            self.client = pymongo.MongoClient(settings.MONGODB_URI)
            self.db = self.client[settings.MONGODB_NAME]
            self.users_collection = self.db.users
            self.blogs_collection = self.db.blogs
            # Test connection
            self.client.admin.command('ping')
            logger.info("MongoDB connection successful")
        except Exception as e:
            logger.error(f"MongoDB connection failed: {e}")
            self.client = None
            self.db = None

    def save_user(self, user_data):
        """Save user data to MongoDB"""
        if self.db is None:
            logger.warning("MongoDB not available, skipping user save")
            return
            
        try:
            user_doc = {
                'django_id': user_data['id'],
                'username': user_data['username'],
                'email': user_data['email'],
                'created_at': user_data['created_at'],
                'updated_at': user_data['updated_at']
            }
            
            # Check if user already exists
            existing_user = self.users_collection.find_one({'django_id': user_data['id']})
            if existing_user:
                self.users_collection.update_one(
                    {'django_id': user_data['id']},
                    {'$set': user_doc}
                )
            else:
                self.users_collection.insert_one(user_doc)
        except Exception as e:
            logger.error(f"Error saving user to MongoDB: {e}")

    def save_blog(self, blog_data):
        """Save blog data to MongoDB"""
        if self.db is None:
            logger.warning("MongoDB not available, skipping blog save")
            return
            
        try:
            blog_doc = {
                'django_id': blog_data['id'],
                'title': blog_data['title'],
                'content': blog_data['content'],
                'image': blog_data.get('image', ''),
                'author_id': blog_data['author_id'],
                'author_email': blog_data['author_email'],
                'author_username': blog_data['author_username'],
                'created_at': blog_data['created_at'],
                'updated_at': blog_data['updated_at'],
                'is_published': blog_data['is_published']
            }
            
            # Check if blog already exists
            existing_blog = self.blogs_collection.find_one({'django_id': blog_data['id']})
            if existing_blog:
                self.blogs_collection.update_one(
                    {'django_id': blog_data['id']},
                    {'$set': blog_doc}
                )
            else:
                self.blogs_collection.insert_one(blog_doc)
        except Exception as e:
            logger.error(f"Error saving blog to MongoDB: {e}")

    def delete_blog(self, blog_id):
        """Delete blog from MongoDB"""
        if self.db is None:
            logger.warning("MongoDB not available, skipping blog delete")
            return
            
        try:
            self.blogs_collection.delete_one({'django_id': blog_id})
        except Exception as e:
            logger.error(f"Error deleting blog from MongoDB: {e}")

    def _convert_objectid_to_string(self, doc):
        """Convert ObjectId fields to strings for JSON serialization"""
        if isinstance(doc, dict):
            for key, value in doc.items():
                if isinstance(value, ObjectId):
                    doc[key] = str(value)
                elif isinstance(value, dict):
                    doc[key] = self._convert_objectid_to_string(value)
                elif isinstance(value, list):
                    doc[key] = [self._convert_objectid_to_string(item) if isinstance(item, dict) else str(item) if isinstance(item, ObjectId) else item for item in value]
        return doc

    def get_all_blogs(self, page=1, page_size=10):
        """Get all published blogs from MongoDB with pagination"""
        if self.db is None:
            logger.warning("MongoDB not available, returning empty results")
            return {
                'blogs': [],
                'total': 0,
                'page': page,
                'page_size': page_size,
                'total_pages': 0
            }
            
        try:
            skip = (page - 1) * page_size
            blogs = list(self.blogs_collection.find(
                {'is_published': True}
            ).sort('created_at', -1).skip(skip).limit(page_size))
            
            # Convert ObjectIds to strings
            blogs = [self._convert_objectid_to_string(blog) for blog in blogs]
            
            total = self.blogs_collection.count_documents({'is_published': True})
            
            return {
                'blogs': blogs,
                'total': total,
                'page': page,
                'page_size': page_size,
                'total_pages': (total + page_size - 1) // page_size
            }
        except Exception as e:
            logger.error(f"Error fetching blogs from MongoDB: {e}")
            return {
                'blogs': [],
                'total': 0,
                'page': page,
                'page_size': page_size,
                'total_pages': 0
            }

    def get_blog_by_id(self, blog_id):
        """Get a specific blog by Django ID"""
        if self.db is None:
            return None
            
        try:
            blog = self.blogs_collection.find_one({'django_id': blog_id})
            if blog:
                blog = self._convert_objectid_to_string(blog)
            return blog
        except Exception as e:
            logger.error(f"Error fetching blog from MongoDB: {e}")
            return None

    def get_user_blogs(self, user_id, page=1, page_size=10):
        """Get blogs by user from MongoDB"""
        if self.db is None:
            logger.warning("MongoDB not available, returning empty results")
            return {
                'blogs': [],
                'total': 0,
                'page': page,
                'page_size': page_size,
                'total_pages': 0
            }
            
        try:
            skip = (page - 1) * page_size
            blogs = list(self.blogs_collection.find(
                {'author_id': user_id}
            ).sort('created_at', -1).skip(skip).limit(page_size))
            
            # Convert ObjectIds to strings
            blogs = [self._convert_objectid_to_string(blog) for blog in blogs]
            
            total = self.blogs_collection.count_documents({'author_id': user_id})
            
            return {
                'blogs': blogs,
                'total': total,
                'page': page,
                'page_size': page_size,
                'total_pages': (total + page_size - 1) // page_size
            }
        except Exception as e:
            logger.error(f"Error fetching user blogs from MongoDB: {e}")
            return {
                'blogs': [],
                'total': 0,
                'page': page,
                'page_size': page_size,
                'total_pages': 0
            }


# Global instance
mongodb_service = MongoDBService()
