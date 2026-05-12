# Portfolio Django API - React Frontend Integration Guide

## Django Backend Overview

This Django project serves as a complete portfolio backend API with the following features:

### 🛠️ Technology Stack
- **Django 5.2.2** - Web framework
- **Django REST Framework** - API development
- **JWT Authentication** - Token-based authentication
- **CKEditor 5** - Rich text content management
- **Swagger/OpenAPI** - API documentation
- **CORS** - Cross-origin resource sharing enabled
- **SQLite** - Database (PostgreSQL configuration available)

### 📊 Data Models

#### UserProfile (Custom User Model)
- Extends Django's AbstractUser
- Fields: first_name, last_name, avatar, bio (CKEditor), location, github, linkedin, website

#### Skill
- Fields: name, percentage, icon

#### Project
- Fields: title, description (CKEditor), image, cover_image, project_url, created_at

#### BlogPost
- Fields: title, content (CKEditor), created_at, updated_at, cover_image, is_published, tag, read_time, slug

#### BlogContent
- Fields: content (CKEditor), blog_post (FK), created_at

#### Experience
- Fields: job_title, company, start_date, end_date, description (CKEditor)

#### Education
- Fields: school, degree, teacher, start_date, end_date, description (CKEditor)

#### Message
- Fields: name, email, subject, message, created_at, read_at

#### PageViewLog
- Fields: project (FK), ip_address, timestamp

### 🚀 API Endpoints

#### Authentication
- `POST /token/` - Get JWT token
- `POST /token/refresh/` - Refresh JWT token

#### Users
- `GET /users/` - List users

#### Skills
- `GET /skills/` - List skills
- `POST /skill/create/` - Create skill
- `GET /skill/{id}/` - Get skill detail
- `PUT /skill/{id}/` - Update skill
- `DELETE /skill/{id}/` - Delete skill

#### Projects
- `GET /projects/` - List projects
- `POST /project/create/` - Create project
- `GET /project/{id}/` - Get project detail
- `PUT /project/{id}/` - Update project
- `DELETE /project/{id}/` - Delete project

#### Blog Posts
- `GET /blogs/` - List blog posts
- `POST /blog/create/` - Create blog post
- `GET /blog/{slug}/` - Get blog post detail
- `PUT /blog/{slug}/update/` - Update blog post
- `DELETE /blog/{slug}/delete/` - Delete blog post

#### Blog Contents
- `GET /blog-contents/` - List blog contents
- `POST /blog-content/create/` - Create blog content
- `GET /blog-content/{id}/` - Get blog content detail

#### Experiences
- `GET /experiences/` - List experiences
- `POST /experience/create/` - Create experience
- `GET /experience/{id}/` - Get experience detail
- `PUT /experience/{id}/` - Update experience
- `DELETE /experience/{id}/` - Delete experience

#### Educations
- `GET /educations/` - List educations
- `POST /education/create/` - Create education
- `GET /education/{id}/` - Get education detail
- `PUT /education/{id}/` - Update education
- `DELETE /education/{id}/` - Delete education

#### Messages
- `GET /messages/` - List messages
- `POST /message/create/` - Create message
- `GET /message/{id}/` - Get message detail

#### Page Views
- `POST /page-view/create/` - Log page view
- `GET /page-views/` - List page views

#### Documentation
- `GET /` - Swagger UI documentation

---

## 🎯 React Frontend Implementation Guide

### 📋 Prerequisites
- Node.js (v16 or higher)
- npm or yarn
- Basic knowledge of React and modern JavaScript

### 🚀 Setup Instructions

#### 1. Create React App
```bash
npx create-react-app portfolio-frontend
cd portfolio-frontend
```

#### 2. Install Required Dependencies
```bash
# Core dependencies
npm install axios react-router-dom @reduxjs/toolkit react-redux

# UI/Styling
npm install @mui/material @emotion/react @emotion/styled @mui/icons-material
# OR
npm install tailwindcss

# Additional utilities
npm install react-hook-form @hookform/resolvers yup
npm install react-query
npm install date-fns
npm install react-markdown
npm install react-helmet
```

#### 3. Project Structure
```
src/
├── components/
│   ├── common/
│   │   ├── Header.jsx
│   │   ├── Footer.jsx
│   │   ├── Loading.jsx
│   │   └── ErrorBoundary.jsx
│   ├── layout/
│   │   ├── Layout.jsx
│   │   └── Navigation.jsx
│   ├── sections/
│   │   ├── Hero.jsx
│   │   ├── About.jsx
│   │   ├── Skills.jsx
│   │   ├── Projects.jsx
│   │   ├── Experience.jsx
│   │   ├── Education.jsx
│   │   ├── Blog.jsx
│   │   └── Contact.jsx
│   └── ui/
│       ├── Button.jsx
│       ├── Card.jsx
│       ├── Modal.jsx
│       └── Form.jsx
├── pages/
│   ├── Home.jsx
│   ├── About.jsx
│   ├── Projects.jsx
│   ├── Blog.jsx
│   ├── BlogDetail.jsx
│   └── Contact.jsx
├── hooks/
│   ├── useAuth.js
│   ├── useApi.js
│   └── useLocalStorage.js
├── services/
│   ├── api.js
│   ├── auth.js
│   └── storage.js
├── store/
│   ├── index.js
│   ├── authSlice.js
│   ├── portfolioSlice.js
│   └── blogSlice.js
├── utils/
│   ├── constants.js
│   ├── helpers.js
│   └── validators.js
├── styles/
│   ├── globals.css
│   └── components.css
└── App.jsx
```

### 🔧 Configuration

#### 1. Environment Variables (.env)
```env
REACT_APP_API_BASE_URL=http://localhost:8000
REACT_APP_MEDIA_URL=http://localhost:8000/media/
```

#### 2. API Service Configuration
```javascript
// src/services/api.js
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_BASE_URL}/token/refresh/`, {
          refresh: refreshToken
        });
        
        const { access } = response.data;
        localStorage.setItem('access_token', access);
        
        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
      }
    }
    
    return Promise.reject(error);
  }
);

export default api;
```

### 🎨 Component Examples

#### 1. Projects Component
```javascript
// src/components/sections/Projects.jsx
import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchProjects } from '../store/portfolioSlice';
import Card from '../ui/Card';

const Projects = () => {
  const dispatch = useDispatch();
  const { projects, loading, error } = useSelector(state => state.portfolio);

  useEffect(() => {
    dispatch(fetchProjects());
  }, [dispatch]);

  if (loading) return <div>Loading projects...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <section id="projects" className="py-20">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-bold text-center mb-12">My Projects</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map(project => (
            <Card key={project.id} project={project} />
          ))}
        </div>
      </div>
    </section>
  );
};

export default Projects;
```

#### 2. Blog Component
```javascript
// src/components/sections/Blog.jsx
import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchBlogPosts } from '../store/blogSlice';
import { Link } from 'react-router-dom';

const Blog = () => {
  const dispatch = useDispatch();
  const { posts, loading, error } = useSelector(state => state.blog);

  useEffect(() => {
    dispatch(fetchBlogPosts());
  }, [dispatch]);

  if (loading) return <div>Loading blog posts...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <section id="blog" className="py-20 bg-gray-50">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-bold text-center mb-12">Latest Blog Posts</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {posts.map(post => (
            <article key={post.id} className="bg-white rounded-lg shadow-md overflow-hidden">
              {post.cover_image && (
                <img 
                  src={`${process.env.REACT_APP_MEDIA_URL}${post.cover_image}`}
                  alt={post.title}
                  className="w-full h-48 object-cover"
                />
              )}
              <div className="p-6">
                <div className="flex items-center mb-2">
                  <span className="text-sm text-gray-500">{post.tag}</span>
                  <span className="text-sm text-gray-500 ml-auto">{post.read_time} min read</span>
                </div>
                <h3 className="text-xl font-semibold mb-2">{post.title}</h3>
                <div 
                  className="text-gray-600 mb-4 line-clamp-3"
                  dangerouslySetInnerHTML={{ __html: post.content }}
                />
                <Link 
                  to={`/blog/${post.slug}`}
                  className="text-blue-600 hover:text-blue-800 font-medium"
                >
                  Read More →
                </Link>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Blog;
```

### 📱 Redux Store Setup

#### 1. Portfolio Slice
```javascript
// src/store/portfolioSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import api from '../services/api';

// Async thunks
export const fetchProjects = createAsyncThunk(
  'portfolio/fetchProjects',
  async () => {
    const response = await api.get('/projects/');
    return response.data;
  }
);

export const fetchSkills = createAsyncThunk(
  'portfolio/fetchSkills',
  async () => {
    const response = await api.get('/skills/');
    return response.data;
  }
);

export const fetchExperiences = createAsyncThunk(
  'portfolio/fetchExperiences',
  async () => {
    const response = await api.get('/experiences/');
    return response.data;
  }
);

export const fetchEducations = createAsyncThunk(
  'portfolio/fetchEducations',
  async () => {
    const response = await api.get('/educations/');
    return response.data;
  }
);

export const fetchUserProfile = createAsyncThunk(
  'portfolio/fetchUserProfile',
  async () => {
    const response = await api.get('/users/');
    return response.data[0]; // Assuming first user is the portfolio owner
  }
);

const portfolioSlice = createSlice({
  name: 'portfolio',
  initialState: {
    projects: [],
    skills: [],
    experiences: [],
    educations: [],
    userProfile: null,
    loading: false,
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      // Projects
      .addCase(fetchProjects.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchProjects.fulfilled, (state, action) => {
        state.loading = false;
        state.projects = action.payload;
      })
      .addCase(fetchProjects.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })
      // Skills
      .addCase(fetchSkills.fulfilled, (state, action) => {
        state.skills = action.payload;
      })
      // Experiences
      .addCase(fetchExperiences.fulfilled, (state, action) => {
        state.experiences = action.payload;
      })
      // Educations
      .addCase(fetchEducations.fulfilled, (state, action) => {
        state.educations = action.payload;
      })
      // User Profile
      .addCase(fetchUserProfile.fulfilled, (state, action) => {
        state.userProfile = action.payload;
      });
  },
});

export default portfolioSlice.reducer;
```

### 🎯 Key Features to Implement

#### 1. Responsive Design
- Mobile-first approach
- Breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px)
- Use CSS Grid and Flexbox for layouts

#### 2. Performance Optimization
- Code splitting with React.lazy()
- Image optimization with lazy loading
- Memoization with React.memo()
- Virtual scrolling for large lists

#### 3. SEO Optimization
- Meta tags with react-helmet
- Structured data (JSON-LD)
- Open Graph tags
- Semantic HTML5 elements

#### 4. Accessibility
- ARIA labels
- Keyboard navigation
- Screen reader support
- Color contrast compliance

#### 5. Contact Form
```javascript
// src/components/sections/Contact.jsx
import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import api from '../../services/api';

const Contact = () => {
  const { register, handleSubmit, formState: { errors }, reset } = useForm();
  const [status, setStatus] = useState('');

  const onSubmit = async (data) => {
    try {
      setStatus('sending');
      await api.post('/message/create/', data);
      setStatus('success');
      reset();
    } catch (error) {
      setStatus('error');
    }
  };

  return (
    <section id="contact" className="py-20">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-bold text-center mb-12">Get In Touch</h2>
        <form onSubmit={handleSubmit(onSubmit)} className="max-w-lg mx-auto">
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Name
            </label>
            <input
              {...register('name', { required: 'Name is required' })}
              className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
            />
            {errors.name && <p className="text-red-500 text-xs mt-1">{errors.name.message}</p>}
          </div>
          
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Email
            </label>
            <input
              type="email"
              {...register('email', { required: 'Email is required' })}
              className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
            />
            {errors.email && <p className="text-red-500 text-xs mt-1">{errors.email.message}</p>}
          </div>
          
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Subject
            </label>
            <input
              {...register('subject', { required: 'Subject is required' })}
              className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
            />
            {errors.subject && <p className="text-red-500 text-xs mt-1">{errors.subject.message}</p>}
          </div>
          
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Message
            </label>
            <textarea
              {...register('message', { required: 'Message is required' })}
              rows="4"
              className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
            />
            {errors.message && <p className="text-red-500 text-xs mt-1">{errors.message.message}</p>}
          </div>
          
          <button
            type="submit"
            disabled={status === 'sending'}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:bg-gray-400"
          >
            {status === 'sending' ? 'Sending...' : 'Send Message'}
          </button>
          
          {status === 'success' && (
            <p className="text-green-600 text-center mt-4">Message sent successfully!</p>
          )}
          {status === 'error' && (
            <p className="text-red-600 text-center mt-4">Error sending message. Please try again.</p>
          )}
        </form>
      </div>
    </section>
  );
};

export default Contact;
```

### 🚀 Deployment

#### 1. Build for Production
```bash
npm run build
```

#### 2. Deploy Options
- **Netlify**: Drag and drop the build folder
- **Vercel**: Connect GitHub repository
- **AWS S3 + CloudFront**: Static hosting
- **GitHub Pages**: Free hosting for static sites

#### 3. Environment Variables for Production
```env
REACT_APP_API_BASE_URL=https://your-django-api.com
REACT_APP_MEDIA_URL=https://your-django-api.com/media/
```

### 📝 Additional Considerations

#### 1. Error Handling
- Global error boundary
- API error handling
- User feedback for errors

#### 2. Loading States
- Skeleton loaders
- Spinners
- Progress indicators

#### 3. Caching
- React Query for API caching
- Service worker for offline support
- Browser caching strategies

#### 4. Analytics
- Google Analytics integration
- Page view tracking (use existing PageViewLog API)

#### 5. Testing
- Jest for unit tests
- React Testing Library for component tests
- Cypress for E2E tests

---

## 🎯 Development Workflow

1. **Start Django Backend**: `python manage.py runserver`
2. **Start React Frontend**: `npm start`
3. **API Documentation**: Visit `http://localhost:8000/` for Swagger UI
4. **Admin Panel**: Visit `http://localhost:8000/admin/`

## 📚 Resources

- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [React Documentation](https://reactjs.org/)
- [Redux Toolkit Documentation](https://redux-toolkit.js.org/)
- [Material-UI Documentation](https://mui.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)

---

Bu README sizning Django portfolio backend'ingiz to'liq tahlili va React frontend yaratish uchun kerak bo'lgan barcha ma'lumotlarni o'z ichiga oladi. Cloudda ishlash uchun bu qo'llanma sizga to'liq yordam beradi.
