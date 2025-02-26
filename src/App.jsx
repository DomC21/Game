import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';

// Pages
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import LevelView from './pages/LevelView';
import ChapterView from './pages/ChapterView';
import QuizView from './pages/QuizView';
import Onboarding from './pages/Onboarding';
import NotFound from './pages/NotFound';

// Protected route component
const ProtectedRoute = ({ children }) => {
  const { currentUser, loading } = useAuth();
  
  if (loading) {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>;
  }
  
  if (!currentUser) {
    return <Navigate to="/login" />;
  }
  
  return children;
};

function AppRoutes() {
  const { currentUser } = useAuth();
  
  return (
    <Routes>
      {/* Public routes */}
      <Route path="/login" element={currentUser ? <Navigate to="/dashboard" /> : <Login />} />
      <Route path="/register" element={currentUser ? <Navigate to="/dashboard" /> : <Register />} />
      
      {/* Protected routes */}
      <Route path="/dashboard" element={
        <ProtectedRoute>
          <Dashboard />
        </ProtectedRoute>
      } />
      <Route path="/onboarding" element={
        <ProtectedRoute>
          <Onboarding />
        </ProtectedRoute>
      } />
      <Route path="/levels/:levelId" element={
        <ProtectedRoute>
          <LevelView />
        </ProtectedRoute>
      } />
      <Route path="/chapters/:chapterId" element={
        <ProtectedRoute>
          <ChapterView />
        </ProtectedRoute>
      } />
      <Route path="/quizzes/:quizId" element={
        <ProtectedRoute>
          <QuizView />
        </ProtectedRoute>
      } />
      
      {/* Redirect root to dashboard or login */}
      <Route path="/" element={currentUser ? <Navigate to="/dashboard" /> : <Navigate to="/login" />} />
      
      {/* 404 route */}
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

function App() {
  return (
    <Router>
      <AuthProvider>
        <div className="min-h-screen bg-gray-50">
          <AppRoutes />
        </div>
      </AuthProvider>
    </Router>
  );
}

export default App;
