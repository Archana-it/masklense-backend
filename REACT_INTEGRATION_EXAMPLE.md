# React Frontend Integration Examples

## Setup API Client

```javascript
// src/api/client.js
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token refresh on 401
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      const refreshToken = localStorage.getItem('refreshToken');
      if (refreshToken) {
        try {
          const { data } = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
            refresh: refreshToken,
          });
          localStorage.setItem('accessToken', data.access);
          error.config.headers.Authorization = `Bearer ${data.access}`;
          return apiClient.request(error.config);
        } catch (refreshError) {
          localStorage.clear();
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

---

## Authentication Service

```javascript
// src/services/authService.js
import apiClient from '../api/client';

export const authService = {
  async register(email, fullName, password) {
    const { data } = await apiClient.post('/auth/register/', {
      email,
      full_name: fullName,
      password,
    });
    
    localStorage.setItem('accessToken', data.tokens.access);
    localStorage.setItem('refreshToken', data.tokens.refresh);
    localStorage.setItem('user', JSON.stringify(data.user));
    
    return data;
  },

  async login(email, password) {
    const { data } = await apiClient.post('/auth/login/', {
      email,
      password,
    });
    
    localStorage.setItem('accessToken', data.tokens.access);
    localStorage.setItem('refreshToken', data.tokens.refresh);
    localStorage.setItem('user', JSON.stringify(data.user));
    
    return data;
  },

  logout() {
    localStorage.clear();
    window.location.href = '/login';
  },

  getCurrentUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  },

  isAuthenticated() {
    return !!localStorage.getItem('accessToken');
  },
};
```

---

## Facial Analysis Service

```javascript
// src/services/analysisService.js
import apiClient from '../api/client';

export const analysisService = {
  async uploadImage(imageFile) {
    const formData = new FormData();
    formData.append('image', imageFile);
    
    const { data } = await apiClient.post('/analysis/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return data;
  },

  async getAllAnalyses() {
    const { data } = await apiClient.get('/analysis/list/');
    return data;
  },

  async getAnalysis(id) {
    const { data } = await apiClient.get(`/analysis/${id}/`);
    return data;
  },

  async getWeeklySummary() {
    const { data } = await apiClient.get('/summary/weekly/');
    return data;
  },

  async getSummaryHistory() {
    const { data } = await apiClient.get('/summary/history/');
    return data;
  },
};
```

---

## Register Component

```jsx
// src/components/Register.jsx
import React, { useState } from 'react';
import { authService } from '../services/authService';
import { useNavigate } from 'react-router-dom';

function Register() {
  const [formData, setFormData] = useState({
    email: '',
    fullName: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await authService.register(
        formData.email,
        formData.fullName,
        formData.password
      );
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.email?.[0] || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-container">
      <h2>Sign Up</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Full Name"
          value={formData.fullName}
          onChange={(e) => setFormData({ ...formData, fullName: e.target.value })}
          required
        />
        <input
          type="email"
          placeholder="Email"
          value={formData.email}
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={formData.password}
          onChange={(e) => setFormData({ ...formData, password: e.target.value })}
          required
          minLength={8}
        />
        {error && <p className="error">{error}</p>}
        <button type="submit" disabled={loading}>
          {loading ? 'Signing up...' : 'Sign Up'}
        </button>
      </form>
    </div>
  );
}

export default Register;
```

---

## Login Component

```jsx
// src/components/Login.jsx
import React, { useState } from 'react';
import { authService } from '../services/authService';
import { useNavigate } from 'react-router-dom';

function Login() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await authService.login(formData.email, formData.password);
      navigate('/dashboard');
    } catch (err) {
      setError('Invalid email or password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={formData.email}
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={formData.password}
          onChange={(e) => setFormData({ ...formData, password: e.target.value })}
          required
        />
        {error && <p className="error">{error}</p>}
        <button type="submit" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
    </div>
  );
}

export default Login;
```

---

## Image Capture & Upload Component

```jsx
// src/components/FacialAnalysis.jsx
import React, { useState, useRef } from 'react';
import { analysisService } from '../services/analysisService';

function FacialAnalysis() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [cameraActive, setCameraActive] = useState(false);

  // Start camera
  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { facingMode: 'user' } 
      });
      videoRef.current.srcObject = stream;
      setCameraActive(true);
    } catch (err) {
      setError('Camera access denied');
    }
  };

  // Capture image from camera
  const captureImage = () => {
    const canvas = canvasRef.current;
    const video = videoRef.current;
    
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    
    canvas.toBlob((blob) => {
      const file = new File([blob], 'captured-image.jpg', { type: 'image/jpeg' });
      setImage(file);
      setPreview(URL.createObjectURL(blob));
      
      // Stop camera
      video.srcObject.getTracks().forEach(track => track.stop());
      setCameraActive(false);
    }, 'image/jpeg');
  };

  // Handle file upload
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
      setPreview(URL.createObjectURL(file));
    }
  };

  // Upload and analyze
  const handleAnalyze = async () => {
    if (!image) return;
    
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const data = await analysisService.uploadImage(image);
      setResult(data);
    } catch (err) {
      setError('Analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="facial-analysis">
      <h2>Facial Analysis</h2>
      
      {/* Camera View */}
      {cameraActive && (
        <div className="camera-view">
          <video ref={videoRef} autoPlay playsInline />
          <button onClick={captureImage}>Capture</button>
        </div>
      )}
      
      <canvas ref={canvasRef} style={{ display: 'none' }} />
      
      {/* Controls */}
      {!cameraActive && !preview && (
        <div className="controls">
          <button onClick={startCamera}>Open Camera</button>
          <input 
            type="file" 
            accept="image/*" 
            onChange={handleFileChange}
          />
        </div>
      )}
      
      {/* Preview */}
      {preview && !result && (
        <div className="preview">
          <img src={preview} alt="Preview" />
          <button onClick={handleAnalyze} disabled={loading}>
            {loading ? 'Analyzing...' : 'Analyze'}
          </button>
          <button onClick={() => { setPreview(null); setImage(null); }}>
            Retake
          </button>
        </div>
      )}
      
      {/* Results */}
      {result && (
        <div className="results">
          <h3>Analysis Results</h3>
          <div className="score">
            Overall Score: {result.analysis_result.overall_score}/10
          </div>
          
          <div className="skin-health">
            <h4>Skin Health</h4>
            {Object.entries(result.analysis_result.skin_health).map(([key, value]) => (
              <div key={key} className="health-item">
                <span>{key.replace('_', ' ')}: </span>
                <span className={`level-${value}`}>{value}</span>
              </div>
            ))}
          </div>
          
          <div className="recommendations">
            <h4>Recommendations</h4>
            <ul>
              {result.analysis_result.recommendations.map((rec, idx) => (
                <li key={idx}>{rec}</li>
              ))}
            </ul>
          </div>
          
          <button onClick={() => { setResult(null); setPreview(null); setImage(null); }}>
            New Analysis
          </button>
        </div>
      )}
      
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default FacialAnalysis;
```

---

## Weekly Summary Component

```jsx
// src/components/WeeklySummary.jsx
import React, { useState, useEffect } from 'react';
import { analysisService } from '../services/analysisService';

function WeeklySummary() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSummary();
  }, []);

  const loadSummary = async () => {
    try {
      const data = await analysisService.getWeeklySummary();
      setSummary(data);
    } catch (err) {
      console.error('Failed to load summary', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (!summary) return <div>No data available</div>;

  return (
    <div className="weekly-summary">
      <h2>Weekly Summary</h2>
      <p className="date-range">
        {summary.week_start} to {summary.week_end}
      </p>
      
      {summary.summary_data.message ? (
        <p>{summary.summary_data.message}</p>
      ) : (
        <>
          <div className="stats">
            <div className="stat">
              <h3>{summary.total_analyses}</h3>
              <p>Total Scans</p>
            </div>
            <div className="stat">
              <h3>{summary.summary_data.average_score}</h3>
              <p>Average Score</p>
            </div>
            <div className="stat">
              <h3>{summary.summary_data.trend}</h3>
              <p>Trend</p>
            </div>
          </div>
          
          <div className="common-issues">
            <h3>Most Common Issues</h3>
            <ul>
              {Object.entries(summary.summary_data.most_common_issues).map(([issue, count]) => (
                <li key={issue}>{issue}: {count}</li>
              ))}
            </ul>
          </div>
        </>
      )}
    </div>
  );
}

export default WeeklySummary;
```

---

## Protected Route

```jsx
// src/components/ProtectedRoute.jsx
import React from 'react';
import { Navigate } from 'react-router-dom';
import { authService } from '../services/authService';

function ProtectedRoute({ children }) {
  if (!authService.isAuthenticated()) {
    return <Navigate to="/login" replace />;
  }
  
  return children;
}

export default ProtectedRoute;
```

---

## App Router Setup

```jsx
// src/App.jsx
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Register from './components/Register';
import Login from './components/Login';
import FacialAnalysis from './components/FacialAnalysis';
import WeeklySummary from './components/WeeklySummary';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route 
          path="/dashboard" 
          element={
            <ProtectedRoute>
              <FacialAnalysis />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/summary" 
          element={
            <ProtectedRoute>
              <WeeklySummary />
            </ProtectedRoute>
          } 
        />
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
```

---

## Install Required Packages

```bash
npm install axios react-router-dom
```

---

## Notes

- Update `API_BASE_URL` if your backend runs on a different port
- Add proper error handling and loading states
- Style components according to your design
- Add form validation
- Implement proper state management (Redux, Zustand, etc.) for larger apps
- Handle image compression before upload for better performance
