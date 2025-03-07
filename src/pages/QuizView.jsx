import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useGamification } from '../contexts/GamificationContext';
import { contentAPI } from '../services/api';
import { Button } from '../components/ui-js/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '../components/ui-js/card';
import { RadioGroup, RadioGroupItem } from '../components/ui-js/radio-group';
import { Label } from '../components/ui-js/label';
import { Alert, AlertDescription, AlertTitle } from '../components/ui-js/alert';
import { Progress } from '../components/ui-js/progress';
import { Badge } from '../components/ui-js/badge';
import { ChevronLeft, CheckCircle, XCircle, Award, Trophy, Clock, AlertTriangle, ArrowRight } from 'lucide-react';

// Quiz components
import QuestionFeedback from '../components/quiz/QuestionFeedback';
import PatternRecognition from '../components/quiz/PatternRecognition';
import ScenarioChallenge from '../components/quiz/ScenarioChallenge';
import BossFightIntro from '../components/quiz/BossFightIntro';
import QuizResultCard from '../components/gamification/QuizResultCard';

const QuizView = () => {
  const { quizId } = useParams();
  const { token, refreshUser } = useAuth();
  const { refreshGamificationData } = useGamification();
  const navigate = useNavigate();
  const [quiz, setQuiz] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [answerFeedback, setAnswerFeedback] = useState({});
  const [showFeedback, setShowFeedback] = useState(false);
  const [quizSubmitted, setQuizSubmitted] = useState(false);
  const [quizResult, setQuizResult] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showBossFightIntro, setShowBossFightIntro] = useState(false);
  const [timeRemaining, setTimeRemaining] = useState(null);
  const [timerActive, setTimerActive] = useState(false);

  useEffect(() => {
    const fetchQuiz = async () => {
      try {
        setIsLoading(true);
        const data = await contentAPI.getQuiz(token, quizId);
        setQuiz(data);
        
        // If it's a boss fight quiz, show the intro first
        if (data.quiz_type === "boss_fight") {
          setShowBossFightIntro(true);
        }
        
        // If the quiz has a time limit, set up the timer
        if (data.time_limit_seconds) {
          setTimeRemaining(data.time_limit_seconds);
        }
      } catch (err) {
        console.error('Error fetching quiz:', err);
        setError('Failed to load quiz. Please try again.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchQuiz();
  }, [token, quizId]);
  
  // Timer effect for timed quizzes
  useEffect(() => {
    let timer;
    if (timerActive && timeRemaining !== null && timeRemaining > 0) {
      timer = setInterval(() => {
        setTimeRemaining(prev => {
          if (prev <= 1) {
            clearInterval(timer);
            handleSubmitQuiz(); // Auto-submit when time runs out
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }
    
    return () => {
      if (timer) clearInterval(timer);
    };
  }, [timerActive, timeRemaining]);

  const handleAnswerSelect = (questionId, optionId) => {
    setSelectedAnswers({
      ...selectedAnswers,
      [questionId]: optionId,
    });
    
    // For immediate feedback quizzes, show feedback right away
    if (quiz.show_immediate_feedback) {
      const question = quiz.questions.find(q => q.id === questionId);
      const selectedOption = question.options.find(o => o.id === optionId);
      
      setAnswerFeedback({
        ...answerFeedback,
        [questionId]: {
          isCorrect: selectedOption.is_correct,
          explanation: selectedOption.explanation || question.explanation,
          points: selectedOption.is_correct ? question.points : 0
        }
      });
      
      setShowFeedback(true);
    }
  };

  const handleNextQuestion = () => {
    if (currentQuestion < quiz.questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
      setShowFeedback(false);
    }
  };

  const handlePreviousQuestion = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
      setShowFeedback(false);
    }
  };
  
  const startQuiz = () => {
    setShowBossFightIntro(false);
    
    // Start the timer if it's a timed quiz
    if (timeRemaining !== null) {
      setTimerActive(true);
    }
  };
  
  const handlePatternAnswer = (isCorrect, questionId) => {
    const question = quiz.questions.find(q => q.id === questionId);
    
    setSelectedAnswers({
      ...selectedAnswers,
      [questionId]: isCorrect ? 1 : 0, // 1 for correct, 0 for incorrect
    });
    
    setAnswerFeedback({
      ...answerFeedback,
      [questionId]: {
        isCorrect,
        explanation: question.explanation,
        points: isCorrect ? question.points : 0
      }
    });
  };
  
  const handleScenarioAnswer = (isCorrect, questionId) => {
    const question = quiz.questions.find(q => q.id === questionId);
    
    setSelectedAnswers({
      ...selectedAnswers,
      [questionId]: isCorrect ? 1 : 0, // 1 for correct, 0 for incorrect
    });
    
    setAnswerFeedback({
      ...answerFeedback,
      [questionId]: {
        isCorrect,
        explanation: question.explanation,
        points: isCorrect ? question.points : 0
      }
    });
  };

  const handleSubmitQuiz = async () => {
    try {
      setIsLoading(true);
      
      // Stop the timer if it's active
      if (timerActive) {
        setTimerActive(false);
      }
      
      const result = await contentAPI.submitQuiz(token, quizId, selectedAnswers);
      setQuizResult(result);
      setQuizSubmitted(true);
      
      // Refresh user data to update points, level, etc.
      await refreshUser();
      
      // Refresh gamification data to update achievements, etc.
      refreshGamificationData();
    } catch (err) {
      console.error('Error submitting quiz:', err);
      setError('Failed to submit quiz. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const isQuestionAnswered = (questionId) => {
    return selectedAnswers[questionId] !== undefined;
  };

  const allQuestionsAnswered = () => {
    if (!quiz || !quiz.questions) return false;
    return quiz.questions.every(q => isQuestionAnswered(q.id));
  };

  if (isLoading && !quiz) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p>Loading quiz...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen p-4">
        <p className="text-red-500">{error}</p>
        <Link to="/dashboard">
          <Button className="mt-4">Return to Dashboard</Button>
        </Link>
      </div>
    );
  }

  if (!quiz) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen p-4">
        <p>Quiz not found.</p>
        <Link to="/dashboard">
          <Button className="mt-4">Return to Dashboard</Button>
        </Link>
      </div>
    );
  }

  // If quiz is submitted, show results
  if (quizSubmitted && quizResult) {
    return (
      <div className="min-h-screen bg-gray-50 p-4">
        <header className="mb-6">
          <Link to={`/chapters/${quiz.chapter_id}`}>
            <Button variant="ghost" className="mb-2">
              <ChevronLeft className="mr-2 h-4 w-4" />
              Back to Chapter
            </Button>
          </Link>
          <h1 className="text-2xl font-bold">{quiz.title} - Results</h1>
        </header>

        <QuizResultCard 
          result={quizResult} 
          onContinue={() => navigate('/dashboard')} 
        />
        
        {/* Show detailed question feedback */}
        <div className="mt-8">
          <Card>
            <CardHeader>
              <CardTitle>Question Review</CardTitle>
              <CardDescription>Review your answers and learn from your mistakes</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {quiz.questions.map((question, index) => {
                const userAnswer = selectedAnswers[question.id];
                const correctOption = question.options.find(o => o.is_correct);
                const selectedOption = question.options.find(o => o.id === userAnswer);
                const isCorrect = selectedOption?.is_correct || false;
                
                return (
                  <div key={question.id} className="border-b pb-4 last:border-b-0 last:pb-0">
                    <div className="flex items-start">
                      <div className={`flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center mr-2 ${
                        isCorrect ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'
                      }`}>
                        {isCorrect ? (
                          <CheckCircle className="h-4 w-4" />
                        ) : (
                          <XCircle className="h-4 w-4" />
                        )}
                      </div>
                      <div>
                        <h3 className="font-medium">Question {index + 1}: {question.question_text}</h3>
                        <div className="mt-2 text-sm">
                          <p className="text-gray-600">Your answer: {selectedOption?.option_text || 'Not answered'}</p>
                          {!isCorrect && (
                            <p className="text-green-600 mt-1">Correct answer: {correctOption?.option_text}</p>
                          )}
                        </div>
                        {question.explanation && (
                          <div className="mt-2 p-3 bg-gray-50 rounded-md text-sm text-gray-700">
                            <p className="font-medium">Explanation:</p>
                            <p>{question.explanation}</p>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                );
              })}
            </CardContent>
            <CardFooter className="flex justify-center">
              <Link to="/dashboard">
                <Button>
                  Return to Dashboard
                </Button>
              </Link>
            </CardFooter>
          </Card>
        </div>
      </div>
    );
  }
  
  // Show boss fight intro
  if (showBossFightIntro && quiz) {
    return (
      <div className="min-h-screen bg-gray-50 p-4 flex items-center justify-center">
        <BossFightIntro 
          title={quiz.title}
          description={quiz.description}
          requiredScore={quiz.passing_score || 80}
          totalQuestions={quiz.questions.length}
          onStart={startQuiz}
        />
      </div>
    );
  }

  // If quiz is not submitted, show quiz questions
  const question = quiz.questions[currentQuestion];
  const progress = ((currentQuestion + 1) / quiz.questions.length) * 100;
  const feedback = answerFeedback[question.id];

  // Format time remaining for display
  const formatTimeRemaining = () => {
    if (!timeRemaining) return null;
    const minutes = Math.floor(timeRemaining / 60);
    const seconds = timeRemaining % 60;
    return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
  };

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <header className="mb-6">
        <Link to={`/chapters/${quiz.chapter_id}`}>
          <Button variant="ghost" className="mb-2">
            <ChevronLeft className="mr-2 h-4 w-4" />
            Back to Chapter
          </Button>
        </Link>
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold">{quiz.title}</h1>
          <div className="flex items-center space-x-2">
            {timeRemaining !== null && (
              <div className={`flex items-center px-3 py-1 rounded-full ${
                timeRemaining < 30 ? 'bg-red-100 text-red-700' : 'bg-blue-100 text-blue-700'
              }`}>
                <Clock className="h-4 w-4 mr-1" />
                <span className="font-medium">{formatTimeRemaining()}</span>
              </div>
            )}
            {quiz.quiz_type === "boss_fight" && (
              <Badge variant="destructive">Boss Fight</Badge>
            )}
          </div>
        </div>
        <p className="text-gray-600">{quiz.description}</p>
      </header>

      <Card className="mb-6">
        <CardHeader>
          <div className="flex justify-between items-center">
            <CardTitle>Question {currentQuestion + 1} of {quiz.questions.length}</CardTitle>
            <span className="text-sm text-gray-500">
              {quiz.quiz_type === "boss_fight" 
                ? "You need 80% to pass this boss fight!" 
                : question.points ? `Points: ${question.points}` : `Points: ${quiz.points_reward}`}
            </span>
          </div>
          <Progress value={progress} className="h-2" />
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Show feedback if available */}
          {showFeedback && feedback && (
            <QuestionFeedback 
              isCorrect={feedback.isCorrect} 
              explanation={feedback.explanation} 
              points={feedback.points} 
            />
          )}
          
          {/* Render different question types */}
          {question.question_type === 'pattern_recognition' ? (
            <PatternRecognition 
              pattern={question.pattern_image || question.pattern_text}
              options={question.options.map(o => o.option_text)}
              correctAnswer={question.options.find(o => o.is_correct)?.option_text}
              onAnswer={(isCorrect) => handlePatternAnswer(isCorrect, question.id)}
            />
          ) : question.question_type === 'scenario' ? (
            <ScenarioChallenge 
              scenario={question.question_text}
              options={question.options.map(o => o.option_text)}
              correctOption={question.options.find(o => o.is_correct)?.option_text}
              explanation={question.explanation}
              onAnswer={(isCorrect) => handleScenarioAnswer(isCorrect, question.id)}
            />
          ) : (
            <div>
              <h3 className="text-lg font-medium mb-4">{question.question_text}</h3>
              
              <RadioGroup 
                value={selectedAnswers[question.id]?.toString()} 
                onValueChange={(value) => handleAnswerSelect(question.id, parseInt(value))}
                disabled={showFeedback && feedback}
              >
                <div className="space-y-3">
                  {question.options.map(option => (
                    <div 
                      key={option.id} 
                      className={`flex items-center space-x-2 p-3 rounded-lg transition-colors ${
                        showFeedback && selectedAnswers[question.id] === option.id
                          ? option.is_correct
                            ? 'bg-green-50 border border-green-200'
                            : 'bg-red-50 border border-red-200'
                          : 'hover:bg-gray-50'
                      }`}
                    >
                      <RadioGroupItem 
                        value={option.id.toString()} 
                        id={`option-${option.id}`} 
                        disabled={showFeedback && feedback}
                      />
                      <Label 
                        htmlFor={`option-${option.id}`} 
                        className="flex-grow cursor-pointer"
                      >
                        {option.option_text}
                      </Label>
                      {showFeedback && selectedAnswers[question.id] === option.id && (
                        option.is_correct 
                          ? <CheckCircle className="h-5 w-5 text-green-600" /> 
                          : <XCircle className="h-5 w-5 text-red-600" />
                      )}
                    </div>
                  ))}
                </div>
              </RadioGroup>
            </div>
          )}
        </CardContent>
        <CardFooter className="flex justify-between">
          <Button 
            variant="outline" 
            onClick={handlePreviousQuestion}
            disabled={currentQuestion === 0}
          >
            Previous
          </Button>
          
          {showFeedback && feedback ? (
            <Button 
              onClick={handleNextQuestion}
              disabled={currentQuestion >= quiz.questions.length - 1}
            >
              {currentQuestion >= quiz.questions.length - 1 ? 'Finish' : 'Next'}
              {currentQuestion < quiz.questions.length - 1 && (
                <ArrowRight className="ml-2 h-4 w-4" />
              )}
            </Button>
          ) : currentQuestion < quiz.questions.length - 1 ? (
            <Button 
              onClick={handleNextQuestion}
              disabled={!isQuestionAnswered(question.id)}
            >
              Next
            </Button>
          ) : (
            <Button 
              onClick={handleSubmitQuiz}
              disabled={!allQuestionsAnswered()}
              className="bg-green-600 hover:bg-green-700"
            >
              Submit Quiz
            </Button>
          )}
        </CardFooter>
      </Card>

      <div className="flex justify-between items-center">
        <div className="flex space-x-1">
          {quiz.questions.map((_, index) => (
            <button
              key={index}
              className={`w-3 h-3 rounded-full ${
                index === currentQuestion
                  ? 'bg-blue-600'
                  : isQuestionAnswered(quiz.questions[index].id)
                  ? 'bg-green-500'
                  : 'bg-gray-300'
              }`}
              onClick={() => setCurrentQuestion(index)}
              aria-label={`Go to question ${index + 1}`}
            />
          ))}
        </div>
        
        {allQuestionsAnswered() && currentQuestion !== quiz.questions.length - 1 && (
          <Button onClick={handleSubmitQuiz} className="bg-green-600 hover:bg-green-700">
            Submit Quiz
          </Button>
        )}
      </div>
    </div>
  );
};

export default QuizView;
