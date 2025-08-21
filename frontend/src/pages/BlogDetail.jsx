import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { blogAPI, getImageUrl } from '../services/api';
import { useAuth } from '../context/AuthContext';
import './BlogDetail.css';

const BlogDetail = () => {
  const [blog, setBlog] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [isEditing, setIsEditing] = useState(false);
  const [editForm, setEditForm] = useState({ title: '', content: '' });
  
  const { id } = useParams();
  const navigate = useNavigate();
  const { user, isAuthenticated } = useAuth();

  useEffect(() => {
    fetchBlog();
  }, [id]);

  const fetchBlog = async () => {
    try {
      setLoading(true);
      const response = await blogAPI.getBlog(id);
      setBlog(response.data);
      setEditForm({
        title: response.data.title,
        content: response.data.content,
      });
      setError('');
    } catch (error) {
      setError('Failed to fetch blog');
      console.error('Error fetching blog:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      const response = await blogAPI.updateBlog(id, editForm);
      setBlog(response.data);
      setIsEditing(false);
      setError('');
    } catch (error) {
      setError('Failed to update blog');
      console.error('Error updating blog:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this blog?')) {
      try {
        await blogAPI.deleteBlog(id);
        navigate('/my-blogs');
      } catch (error) {
        setError('Failed to delete blog');
        console.error('Error deleting blog:', error);
      }
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading) {
    return <div className="loading">Loading blog...</div>;
  }

  if (error && !blog) {
    return <div className="error-message">{error}</div>;
  }

  if (!blog) {
    return <div className="error-message">Blog not found</div>;
  }

  const isAuthor = isAuthenticated && user?.id === blog.author?.id;

  return (
    <div className="blog-detail">
      <div className="blog-detail-container">
        {error && <div className="error-message">{error}</div>}
      
      {isEditing ? (
        <div className="edit-form">
          <h2>Edit Blog</h2>
          <form onSubmit={handleEdit}>
            <div className="form-group">
              <label htmlFor="title">Title</label>
              <input
                type="text"
                id="title"
                value={editForm.title}
                onChange={(e) => setEditForm({ ...editForm, title: e.target.value })}
                required
                disabled={loading}
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="content">Content</label>
              <textarea
                id="content"
                value={editForm.content}
                onChange={(e) => setEditForm({ ...editForm, content: e.target.value })}
                required
                disabled={loading}
                rows={15}
              />
            </div>
            
            <div className="form-actions">
              <button
                type="button"
                onClick={() => setIsEditing(false)}
                className="cancel-btn"
                disabled={loading}
              >
                Cancel
              </button>
              <button type="submit" className="save-btn" disabled={loading}>
                {loading ? 'Saving...' : 'Save Changes'}
              </button>
            </div>
          </form>
        </div>
      ) : (
        <article className="blog-content">
          <header className="blog-header">
            <h1>{blog.title}</h1>
            <div className="blog-meta">
              <span className="author">By {blog.author?.username}</span>
              <span className="date">{formatDate(blog.created_at)}</span>
              {blog.updated_at !== blog.created_at && (
                <span className="updated">
                  (Updated: {formatDate(blog.updated_at)})
                </span>
              )}
            </div>
            
            {isAuthor && (
              <div className="blog-actions">
                <button
                  onClick={() => setIsEditing(true)}
                  className="edit-btn"
                >
                  Edit
                </button>
                <button
                  onClick={handleDelete}
                  className="delete-btn"
                >
                  Delete
                </button>
              </div>
            )}
          </header>
          
          {(blog.image_url || blog.image) && (
            <div className="blog-featured-image">
              <img src={blog.image_url || getImageUrl(blog.image)} alt={blog.title} />
            </div>
          )}
          
          <div className="blog-text">
            {blog.content.split('\n').map((paragraph, index) => (
              <p key={index}>{paragraph}</p>
            ))}
          </div>
        </article>
      )}
      </div>
    </div>
  );
};

export default BlogDetail;
