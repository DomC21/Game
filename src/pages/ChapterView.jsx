import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { contentAPI } from '../services/api';
import { Button } from '../components/ui-js/button';
import { Card, CardContent, CardFooter, CardHeader } from '../components/ui-js/card';
import { ChevronLeft, ChevronRight, BookOpen } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

const ChapterView = () => {
  const { chapterId } = useParams();
  const { token } = useAuth();
  const navigate = useNavigate();
  const [chapter, setChapter] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchChapter = async () => {
      try {
        setIsLoading(true);
        const data = await contentAPI.getChapter(token, chapterId);
        setChapter(data);
      } catch (err) {
        console.error('Error fetching chapter:', err);
        setError('Failed to load chapter content. Please try again.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchChapter();
  }, [token, chapterId]);

  const handleTakeQuiz = () => {
    if (chapter && chapter.quizzes && chapter.quizzes.length > 0) {
      navigate(`/quizzes/${chapter.quizzes[0].id}`);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p>Loading chapter content...</p>
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

  if (!chapter) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen p-4">
        <p>Chapter not found.</p>
        <Link to="/dashboard">
          <Button className="mt-4">Return to Dashboard</Button>
        </Link>
      </div>
    );
  }

  const hasQuiz = chapter.quizzes && chapter.quizzes.length > 0;

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      {/* Header */}
      <header className="mb-6">
        <Link to={`/levels/${chapter.level_id}`}>
          <Button variant="ghost" className="mb-2">
            <ChevronLeft className="mr-2 h-4 w-4" />
            Back to Level
          </Button>
        </Link>
        <h1 className="text-2xl font-bold">{chapter.title}</h1>
      </header>

      {/* Chapter Content */}
      <Card className="mb-6">
        <CardContent className="pt-6">
          <div className="prose max-w-none">
            <ReactMarkdown>{chapter.content}</ReactMarkdown>
          </div>
        </CardContent>
        <CardFooter className="flex justify-between">
          <Link to={`/levels/${chapter.level_id}`}>
            <Button variant="outline">
              <ChevronLeft className="mr-2 h-4 w-4" />
              Back to Level
            </Button>
          </Link>
          {hasQuiz && (
            <Button onClick={handleTakeQuiz}>
              Take Quiz
              <ChevronRight className="ml-2 h-4 w-4" />
            </Button>
          )}
        </CardFooter>
      </Card>
    </div>
  );
};

export default ChapterView;
