import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://fullstackblog-application-production.up.railway.app/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
            refresh: refreshToken,
          });

          const { access } = response.data;
          localStorage.setItem('access_token', access);

          originalRequest.headers.Authorization = `Bearer ${access}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (userData) => api.post('/auth/register/', userData),
  login: (credentials) => api.post('/auth/login/', credentials),
  logout: (refreshToken) => api.post('/auth/logout/', { refresh: refreshToken }),
  getProfile: () => api.get('/auth/profile/'),
};

// Blog API
export const blogAPI = {
  getBlogs: (page = 1, pageSize = 10) => 
    api.get(`/blogs/?page=${page}&page_size=${pageSize}`),
  getBlog: (id) => api.get(`/blogs/${id}/`),
  createBlog: (blogData) => api.post('/blogs/', blogData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }),
  updateBlog: (id, blogData) => api.put(`/blogs/${id}/`, blogData),
  deleteBlog: (id) => api.delete(`/blogs/${id}/`),
  getMyBlogs: (page = 1, pageSize = 10) => 
    api.get(`/blogs/my-blogs/?page=${page}&page_size=${pageSize}`),
  togglePublish: (id) => api.patch(`/blogs/${id}/toggle-publish/`),
};

// Utility function to get full image URL
export const getImageUrl = (imagePath) => {
  if (!imagePath) return null;
  // If it's already a full URL, return as is
  if (imagePath.startsWith('http')) return imagePath;
  // If it starts with /media, build the full URL
  if (imagePath.startsWith('/media')) {
    return `http://localhost:8000${imagePath}`;
  }
  // If it's just the filename, build the full URL
  return `http://localhost:8000/media/${imagePath}`;
};

export default api;
