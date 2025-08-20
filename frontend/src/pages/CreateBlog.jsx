import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { blogAPI } from '../services/api';
import './BlogForm.css';

const CreateBlog = () => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const navigate = useNavigate();

  const handleImageChange = (e) => {
    setImage(e.target.files[0]);
  };

  const validateContent = () => {
    const lines = content.split('\n').filter(line => line.trim() !== '');
    return lines.length >= 50;
  };

  const getLineCount = () => {
    return content.split('\n').filter(line => line.trim() !== '').length;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // Validate content length
    if (!validateContent()) {
      setError(`Content must have at least 50 lines. Currently has ${getLineCount()} lines.`);
      setLoading(false);
      return;
    }

    // Validate image
    if (!image) {
      setError('Image is required for blog creation.');
      setLoading(false);
      return;
    }

    const formData = new FormData();
    formData.append('title', title);
    formData.append('content', content);
    formData.append('image', image);

    try {
      await blogAPI.createBlog(formData);
      // Navigate to home page to see the new blog
      navigate('/', { replace: true });
    } catch (error) {
      setError(error.response?.data?.error || error.response?.data?.content?.[0] || error.response?.data?.image?.[0] || 'Failed to create blog. Please try again.');
      console.error('Error creating blog:', error.response ? error.response.data : error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="blog-form-container">
      <div className="blog-form">
        <h2>Create New Blog</h2>
        
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="title">Title *</label>
            <input
              type="text"
              id="title"
              name="title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
              disabled={loading}
              maxLength={200}
              placeholder="Enter a compelling blog title..."
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="image">Featured Image *</label>
            <input
              type="file"
              id="image"
              name="image"
              onChange={handleImageChange}
              disabled={loading}
              accept="image/*"
              required
            />
            <small className="field-hint">Upload a high-quality image for your blog post</small>
          </div>
          
          <div className="form-group">
            <label htmlFor="content">
              Content * 
              <span className={`line-counter ${getLineCount() >= 50 ? 'valid' : 'invalid'}`}>
                ({getLineCount()}/50 lines minimum)
              </span>
            </label>
            <textarea
              id="content"
              name="content"
              value={content}
              onChange={(e) => setContent(e.target.value)}
              required
              disabled={loading}
              rows={20}
              placeholder="Write your blog content here... (minimum 50 lines required)"
            />
            <small className="field-hint">
              Write engaging, detailed content. Each new line counts toward the 50-line minimum.
            </small>
          </div>
          
          <div className="form-actions">
            <button
              type="button"
              onClick={() => navigate('/')}
              className="cancel-btn"
              disabled={loading}
            >
              Cancel
            </button>
            <button 
              type="submit" 
              className="submit-btn" 
              disabled={loading || !validateContent() || !image}
            >
              {loading ? 'Creating...' : 'Create Blog'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreateBlog;
