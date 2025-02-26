import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

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
      // Mock levels data
      const mockLevels = [
        {
          id: 1,
          level_number: 1,
          title: "Foundations of Investing",
          description: "Learn the basic terminology, asset types, and fundamental concepts",
          required_points: 0,
          is_locked: false,
          chapters: [
            {
              id: 1,
              title: "Introduction to Investing",
              description: "Understanding the basics of investing and why it matters",
              content: "Introduction to investing content...",
              quiz_id: 1
            },
            {
              id: 2,
              title: "Asset Classes",
              description: "Exploring different types of investments: stocks, bonds, ETFs, and more",
              content: "Asset classes content...",
              quiz_id: 2
            },
            {
              id: 3,
              title: "Risk and Return",
              description: "Understanding the relationship between risk and potential returns",
              content: "Risk and return content...",
              quiz_id: 3
            }
          ]
        },
        {
          id: 2,
          level_number: 2,
          title: "Trading Psychology",
          description: "Master emotional discipline, risk appetite, and trading mindset",
          required_points: 100,
          is_locked: false,
          chapters: [
            {
              id: 4,
              title: "Emotional Discipline",
              description: "Learning to control emotions during market volatility",
              content: "Emotional discipline content...",
              quiz_id: 4
            },
            {
              id: 5,
              title: "Cognitive Biases",
              description: "Recognizing and overcoming common cognitive biases in trading",
              content: "Cognitive biases content...",
              quiz_id: 5
            }
          ]
        },
        {
          id: 3,
          level_number: 3,
          title: "Technical Analysis Basics",
          description: "Learn chart reading, support/resistance, and trend lines",
          required_points: 250,
          is_locked: true,
          chapters: []
        }
      ];
      
      return mockLevels;
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
