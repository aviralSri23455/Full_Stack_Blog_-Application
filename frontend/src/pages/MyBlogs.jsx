import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { blogAPI, getImageUrl } from '../services/api';
import './MyBlogs.css';

const MyBlogs = () => {
  const [blogs, setBlogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchMyBlogs(currentPage);
  }, [currentPage]);

  const fetchMyBlogs = async (page) => {
    try {
      setLoading(true);
      const response = await blogAPI.getMyBlogs(page, 10);
      setBlogs(response.data.results || []);
      setTotalPages(Math.ceil(response.data.count / 10));
      setError('');
    } catch (error) {
      setError('Failed to fetch your blogs');
      console.error('Error fetching my blogs:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (blogId) => {
    if (window.confirm('Are you sure you want to delete this blog?')) {
      try {
        await blogAPI.deleteBlog(blogId);
        setBlogs(blogs.filter(blog => blog.django_id !== blogId));
      } catch (error) {
        setError('Failed to delete blog');
        console.error('Error deleting blog:', error);
      }
    }
  };

  const handleTogglePublish = async (blogId, currentStatus) => {
    try {
      const response = await blogAPI.togglePublish(blogId);
      setBlogs(blogs.map(blog => 
        blog.django_id === blogId 
          ? { ...blog, is_published: response.data.is_published }
          : blog
      ));
    } catch (error) {
      setError('Failed to toggle publish status');
      console.error('Error toggling publish status:', error);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  if (loading) {
    return <div className="loading">Loading your blogs...</div>;
  }

  return (
    <div className="my-blogs">
      <div className="my-blogs-container">
        <div className="my-blogs-header">
          <h1>My Blogs</h1>
          <Link to="/create-blog" className="create-btn">
            Create New Blog
          </Link>
        </div>
        
        <div className="my-blogs-info">
          <p className="info-text">
            <strong>Note:</strong> Only <span className="status-published">Published</span> blogs appear on the home page. 
            <span className="status-draft">Draft</span> blogs are only visible to you.
          </p>
        </div>

        {error && <div className="error-message">{error}</div>}

        <div className="blogs-list">
        {blogs.length === 0 ? (
          <div className="no-blogs">
            <h3>You haven't created any blogs yet</h3>
            <p>Start writing your first blog post!</p>
            <Link to="/create-blog" className="create-first-btn">
              Create Your First Blog
            </Link>
          </div>
        ) : (
          blogs.map((blog) => (
            <div key={blog._id || blog.django_id} className="blog-item">
              {blog.image && (
                <div className="blog-image">
                  <img src={getImageUrl(blog.image)} alt={blog.title} />
                </div>
              )}
              <div className="blog-info">
                <h3 className="blog-title">
                  <Link to={`/blog/${blog.django_id}`}>{blog.title}</Link>
                </h3>
                <div className="blog-meta">
                  <span className="blog-date">
                    Created: {formatDate(blog.created_at)}
                  </span>
                  {blog.updated_at !== blog.created_at && (
                    <span className="blog-updated">
                      Updated: {formatDate(blog.updated_at)}
                    </span>
                  )}
                  <span className={`blog-status ${blog.is_published ? 'published' : 'draft'}`}>
                    {blog.is_published ? 'Published' : 'Draft'}
                  </span>
                </div>
                <div className="blog-preview">
                  {blog.content.substring(0, 150)}...
                </div>
              </div>
              
              <div className="blog-actions">
                <Link 
                  to={`/blog/${blog.django_id}`} 
                  className="view-btn"
                >
                  View
                </Link>
                <button
                  onClick={() => handleTogglePublish(blog.django_id, blog.is_published)}
                  className={`toggle-btn ${blog.is_published ? 'unpublish' : 'publish'}`}
                >
                  {blog.is_published ? 'Unpublish' : 'Publish'}
                </button>
                <button
                  onClick={() => handleDelete(blog.django_id)}
                  className="delete-btn"
                >
                  Delete
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      {totalPages > 1 && (
        <div className="pagination">
          <button
            onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
            disabled={currentPage === 1}
            className="pagination-btn"
          >
            Previous
          </button>
          
          <div className="pagination-info">
            Page {currentPage} of {totalPages}
          </div>
          
          <button
            onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
            disabled={currentPage === totalPages}
            className="pagination-btn"
          >
            Next
          </button>
        </div>
      )}
      </div>
    </div>
  );
};

export default MyBlogs;
