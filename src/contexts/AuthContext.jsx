import React, { createContext, useState, useEffect, useContext } from 'react';
import { authAPI } from '../services/api';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // If we have a token, fetch the user profile
    if (token) {
      fetchUserProfile();
    } else {
      setLoading(false);
    }
  }, [token]);

  const fetchUserProfile = async () => {
    try {
      setLoading(true);
      const userData = await authAPI.getProfile(token);
      setCurrentUser(userData);
      setError(null);
    } catch (err) {
      console.error('Error fetching user profile:', err);
      setError(err.message);
      // If there's an error (like an expired token), log the user out
      logout();
    } finally {
      setLoading(false);
    }
  };

  const login = async (credentials) => {
    try {
      setLoading(true);
      const data = await authAPI.login(credentials);
      const { access_token } = data;
      
      // Save token to localStorage and state
      localStorage.setItem('token', access_token);
      setToken(access_token);
      
      // Fetch user profile with the new token
      try {
        await fetchUserProfile();
      } catch (profileErr) {
        console.error('Error fetching profile after login:', profileErr);
        // Continue with login success even if profile fetch fails
      }
      
      return { success: true };
    } catch (err) {
      console.error('Login error:', err);
      setError(err.response?.data?.detail || err.message || 'Login failed');
      return { success: false, error: err.response?.data?.detail || err.message || 'Login failed' };
    } finally {
      setLoading(false);
    }
  };

  const register = async (userData) => {
    try {
      setLoading(true);
      await authAPI.register(userData);
      
      // After registration, log the user in
      return login({
        email: userData.email,
        password: userData.password,
      });
    } catch (err) {
      console.error('Registration error:', err);
      setError(err.message);
      return { success: false, error: err.message };
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setCurrentUser(null);
  };

  const value = {
    currentUser,
    token,
    loading,
    error,
    login,
    register,
    logout,
    refreshUser: fetchUserProfile,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
