import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { blogAPI, getImageUrl } from '../services/api';
import './Home.css';

const Home = () => {
  const [blogs, setBlogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [error, setError] = useState('');
  const location = useLocation();

  useEffect(() => {
    fetchBlogs(currentPage);
  }, [currentPage]);

  // Refresh data when location changes (navigation to home)
  useEffect(() => {
    if (location.pathname === '/') {
      fetchBlogs(1); // Always fetch first page when navigating to home
      setCurrentPage(1);
    }
  }, [location.pathname]);

  const fetchBlogs = async (page) => {
    try {
      setLoading(true);
      const response = await blogAPI.getBlogs(page, 10);
      setBlogs(response.data.results || []);
      setTotalPages(Math.ceil(response.data.count / 10));
      setError('');
    } catch (error) {
      setError('Failed to fetch blogs');
      console.error('Error fetching blogs:', error);
    } finally {
      setLoading(false);
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
    return <div className="loading">Loading blogs...</div>;
  }

  return (
    <div className="home">
      <div className="home-container">
        <div className="home-header">
          <h1>Latest Blogs</h1>
          <p>Discover amazing stories from our community</p>
        </div>

        {error && <div className="error-message">{error}</div>}

        <div className="blogs-grid">
        {blogs.length === 0 ? (
          <div className="no-blogs">
            <h3>No blogs found</h3>
            <p>Be the first to create a blog post!</p>
          </div>
        ) : (
          blogs.map((blog) => (
            <div key={blog._id || blog.django_id || blog.id} className="blog-card">
              {(blog.image) && (
                <div className="blog-image">
                  <img src={getImageUrl(blog.image)} alt={blog.title} />
                </div>
              )}
              <div className="blog-content">
                <h3 className="blog-title">
                  <Link to={`/blog/${blog.django_id || blog.id}`}>{blog.title}</Link>
                </h3>
                <div className="blog-meta">
                  <span className="blog-author">
                    By {blog.author_username || blog.author?.username}
                  </span>
                  <span className="blog-date">{formatDate(blog.created_at)}</span>
                </div>
                <div className="blog-preview">
                  {blog.content_preview || blog.content.substring(0, 200) + '...'}
                </div>
                <Link to={`/blog/${blog.django_id || blog.id}`} className="read-more">
                  Read More
                </Link>
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

export default Home;
