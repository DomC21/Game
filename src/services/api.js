import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_URL || 'https://app-yinpjyoy.fly.dev';

// Create axios instance with default config
const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests if available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Authentication API
export const authAPI = {
  login: async (credentials) => {
    try {
      // Convert credentials to FormData for OAuth2 compatibility
      const formData = new FormData();
      formData.append('username', credentials.email); // OAuth2 expects 'username' field
      formData.append('password', credentials.password);
      
      const response = await api.post('/api/auth/login', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      console.error('Login API error:', error);
      throw error;
    }
  },
  
  register: async (userData) => {
    try {
      // Ensure userData matches the expected schema on the backend
      const userDataFormatted = {
        email: userData.email,
        username: userData.username,
        password: userData.password
      };
      
      const response = await api.post('/api/auth/register', userDataFormatted, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      return response.data;
    } catch (error) {
      console.error('Register API error:', error);
      throw error;
    }
  },
  
  getProfile: async (token) => {
    try {
      const response = await api.get('/api/auth/me');
      return response.data;
    } catch (error) {
      console.error('Get profile API error:', error);
      throw error;
    }
  },
};

// Progress tracking API
export const progressAPI = {
  getUserProgress: async () => {
    try {
      const response = await api.get('/api/users/progress');
      return response.data;
    } catch (error) {
      console.error('Get user progress API error:', error);
      throw error;
    }
  },
  
  getUserAchievements: async () => {
    try {
      const response = await api.get('/api/users/achievements');
      return response.data;
    } catch (error) {
      console.error('Get user achievements API error:', error);
      throw error;
    }
  },
  
  getQuizAttempts: async () => {
    try {
      const response = await api.get('/api/users/quiz-attempts');
      return response.data;
    } catch (error) {
      console.error('Get quiz attempts API error:', error);
      throw error;
    }
  },
  
  submitQuizAttempt: async (quizId, answers) => {
    try {
      const response = await api.post(`/api/quizzes/${quizId}/submit`, { answers });
      return response.data;
    } catch (error) {
      console.error('Submit quiz attempt API error:', error);
      throw error;
    }
  },
};

// Content API
export const contentAPI = {
  getLevels: async () => {
    try {
      const response = await api.get('/api/levels');
      return response.data;
    } catch (error) {
      console.error('Get levels API error:', error);
      throw error;
    }
  },
  
  getLevel: async (levelId) => {
    try {
      const response = await api.get(`/api/levels/${levelId}`);
      return response.data;
    } catch (error) {
      console.error('Get level API error:', error);
      throw error;
    }
  },
  
  getChapter: async (chapterId) => {
    try {
      const response = await api.get(`/api/chapters/${chapterId}`);
      return response.data;
    } catch (error) {
      console.error('Get chapter API error:', error);
      throw error;
    }
  },
  
  getQuiz: async (quizId) => {
    try {
      const response = await api.get(`/api/quizzes/${quizId}`);
      return response.data;
    } catch (error) {
      console.error('Get quiz API error:', error);
      throw error;
    }
  },
};

// Leaderboard API
export const leaderboardAPI = {
  getLeaderboard: async () => {
    try {
      const response = await api.get('/api/leaderboard');
      return response.data;
    } catch (error) {
      console.error('Get leaderboard API error:', error);
      throw error;
    }
  },
};

// Onboarding API
export const onboardingAPI = {
  getOnboardingSteps: async () => {
    try {
      const response = await api.get('/api/auth/onboarding');
      return response.data;
    } catch (error) {
      console.error('Get onboarding steps API error:', error);
      throw error;
    }
  },
  
  completeOnboarding: async () => {
    try {
      const response = await api.post('/api/auth/onboarding/complete');
      return response.data;
    } catch (error) {
      console.error('Complete onboarding API error:', error);
      throw error;
    }
  },
};
