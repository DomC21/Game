/**
 * API service for communicating with the backend
 */

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Helper function for handling API responses
const handleResponse = async (response) => {
  if (!response.ok) {
    const error = await response.json().catch(() => ({
      detail: 'An unexpected error occurred'
    }));
    throw new Error(error.detail || 'An unexpected error occurred');
  }
  return response.json();
};

// Auth API calls
export const authAPI = {
  register: async (userData) => {
    const response = await fetch(`${API_URL}/api/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });
    return handleResponse(response);
  },

  login: async (credentials) => {
    const formData = new URLSearchParams();
    formData.append('username', credentials.email);
    formData.append('password', credentials.password);

    const response = await fetch(`${API_URL}/api/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData,
    });
    return handleResponse(response);
  },

  getProfile: async (token) => {
    const response = await fetch(`${API_URL}/api/auth/me`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return handleResponse(response);
  },

  getOnboarding: async (token) => {
    const response = await fetch(`${API_URL}/api/auth/onboarding`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return handleResponse(response);
  },
};

// Content API calls
export const contentAPI = {
  getLevels: async (token) => {
    const response = await fetch(`${API_URL}/api/levels`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return handleResponse(response);
  },

  getLevel: async (token, levelId) => {
    const response = await fetch(`${API_URL}/api/levels/${levelId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return handleResponse(response);
  },

  getChapter: async (token, chapterId) => {
    const response = await fetch(`${API_URL}/api/chapters/${chapterId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return handleResponse(response);
  },

  getQuiz: async (token, quizId) => {
    const response = await fetch(`${API_URL}/api/quizzes/${quizId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return handleResponse(response);
  },

  submitQuiz: async (token, quizId, answers) => {
    const response = await fetch(`${API_URL}/api/quizzes/${quizId}/submit`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        quiz_id: quizId,
        answers: answers,
      }),
    });
    return handleResponse(response);
  },
};

// User progress API calls
export const progressAPI = {
  getUserProgress: async (token) => {
    const response = await fetch(`${API_URL}/api/users/progress`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return handleResponse(response);
  },

  updateProgress: async (token, levelId, isCompleted) => {
    const response = await fetch(`${API_URL}/api/users/progress/${levelId}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        level_id: levelId,
        is_completed: isCompleted,
      }),
    });
    return handleResponse(response);
  },

  getAchievements: async (token) => {
    const response = await fetch(`${API_URL}/api/achievements`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return handleResponse(response);
  },

  getUserAchievements: async (token) => {
    const response = await fetch(`${API_URL}/api/users/achievements`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return handleResponse(response);
  },

  getQuizAttempts: async (token) => {
    const response = await fetch(`${API_URL}/api/users/quiz-attempts`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return handleResponse(response);
  },
  
  getUserStreak: async (token) => {
    const response = await fetch(`${API_URL}/api/users/streak`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return handleResponse(response);
  },
  
  getNextLevelRequirements: async (token) => {
    const response = await fetch(`${API_URL}/api/users/next-level`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return handleResponse(response);
  },
  
  getUserStats: async (token) => {
    const response = await fetch(`${API_URL}/api/users/stats`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return handleResponse(response);
  },
  
  getProgressHistory: async (token) => {
    const response = await fetch(`${API_URL}/api/users/progress-history`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return handleResponse(response);
  },
};

// Leaderboard API calls
export const leaderboardAPI = {
  getLeaderboard: async () => {
    const response = await fetch(`${API_URL}/api/leaderboard`);
    return handleResponse(response);
  },
};
