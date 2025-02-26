import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { authAPI } from '../services/api';
import { Button } from '../components/ui-js/button';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '../components/ui-js/card';
import { ChevronLeft, ChevronRight } from 'lucide-react';

const Onboarding = () => {
  const { token } = useAuth();
  const navigate = useNavigate();
  const [tutorial, setTutorial] = useState(null);
  const [currentStep, setCurrentStep] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchOnboarding = async () => {
      try {
        setIsLoading(true);
        const data = await authAPI.getOnboarding(token);
        setTutorial(data);
      } catch (err) {
        console.error('Error fetching onboarding tutorial:', err);
        setError('Failed to load onboarding tutorial. Please try again.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchOnboarding();
  }, [token]);

  const handleNext = () => {
    if (currentStep < tutorial.steps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      // Last step, redirect to dashboard
      navigate('/dashboard');
    }
  };

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSkip = () => {
    navigate('/dashboard');
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p>Loading onboarding tutorial...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen p-4">
        <p className="text-red-500">{error}</p>
        <Button onClick={() => navigate('/dashboard')} className="mt-4">
          Skip Onboarding
        </Button>
      </div>
    );
  }

  if (!tutorial) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen p-4">
        <p>No onboarding tutorial available.</p>
        <Button onClick={() => navigate('/dashboard')} className="mt-4">
          Go to Dashboard
        </Button>
      </div>
    );
  }

  const currentTutorialStep = tutorial.steps[currentStep];
  const isLastStep = currentStep === tutorial.steps.length - 1;

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50 p-4">
      <Card className="w-full max-w-2xl">
        <CardHeader>
          <CardTitle className="text-2xl text-center">{tutorial.title}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex justify-between items-center text-sm text-gray-500">
            <span>Step {currentStep + 1} of {tutorial.steps.length}</span>
            <Button variant="ghost" size="sm" onClick={handleSkip}>
              Skip Tutorial
            </Button>
          </div>
          
          <div className="py-6">
            <h3 className="text-xl font-semibold mb-2">{currentTutorialStep.title}</h3>
            <p className="text-gray-700">{currentTutorialStep.content}</p>
          </div>
          
          <div className="w-full bg-gray-200 h-1 rounded-full overflow-hidden">
            <div 
              className="bg-blue-600 h-1" 
              style={{ width: `${((currentStep + 1) / tutorial.steps.length) * 100}%` }}
            ></div>
          </div>
        </CardContent>
        <CardFooter className="flex justify-between">
          <Button 
            variant="outline" 
            onClick={handlePrevious}
            disabled={currentStep === 0}
          >
            <ChevronLeft className="mr-2 h-4 w-4" />
            Previous
          </Button>
          <Button onClick={handleNext}>
            {isLastStep ? 'Get Started' : 'Next'}
            {!isLastStep && <ChevronRight className="ml-2 h-4 w-4" />}
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
};

export default Onboarding;
