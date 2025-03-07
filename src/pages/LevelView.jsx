import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { contentAPI } from '../services/api';
import { Button } from '../components/ui-js/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '../components/ui-js/card';
import { Badge } from '../components/ui-js/badge';
import { ChevronLeft, BookOpen, CheckCircle, List } from 'lucide-react';

const LevelView = () => {
  const { levelId } = useParams();
  const { token } = useAuth();
  const [level, setLevel] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Function to extract and render subsections from chapter content
  const renderSubsections = (content) => {
    // Use regex to extract subsections from the Markdown content
    const subsectionRegex = /## (.*?)(?=\n## |\n# |\n$)/gs;
    const subsections = content.match(subsectionRegex) || [];
    
    if (subsections.length === 0) return null;
    
    return (
      <div className="mt-4 space-y-2">
        <h3 className="text-lg font-medium flex items-center">
          <List className="mr-2 h-4 w-4" />
          Subsections:
        </h3>
        <ul className="list-disc pl-5">
          {subsections.map((subsection, index) => {
            const title = subsection.match(/## (.*?)(?=\n|$)/)?.[1] || `Subsection ${index + 1}`;
            return (
              <li key={index} className="text-gray-700">
                {title}
              </li>
            );
          })}
        </ul>
      </div>
    );
  };

  useEffect(() => {
    const fetchLevel = async () => {
      try {
        setIsLoading(true);
        const data = await contentAPI.getLevel(token, levelId);
        setLevel(data);
      } catch (err) {
        console.error('Error fetching level:', err);
        setError('Failed to load level content. Please try again.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchLevel();
  }, [token, levelId]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p>Loading level content...</p>
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

  if (!level) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen p-4">
        <p>Level not found.</p>
        <Link to="/dashboard">
          <Button className="mt-4">Return to Dashboard</Button>
        </Link>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      {/* Header */}
      <header className="mb-6">
        <Link to="/dashboard">
          <Button variant="ghost" className="mb-2">
            <ChevronLeft className="mr-2 h-4 w-4" />
            Back to Dashboard
          </Button>
        </Link>
        <h1 className="text-2xl font-bold">Level {level.level_number}: {level.title}</h1>
        <p className="text-gray-600">{level.description}</p>
      </header>

      {/* Chapters List */}
      <div className="space-y-4">
        <h2 className="text-xl font-semibold mb-2">Chapters</h2>
        
        {level.chapters && level.chapters.length > 0 ? (
          level.chapters.map((chapter, index) => (
            <Card key={chapter.id}>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <span className="bg-gray-200 text-gray-700 rounded-full w-6 h-6 flex items-center justify-center mr-2 text-sm">
                    {index + 1}
                  </span>
                  {chapter.title}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="line-clamp-2">
                  {chapter.content.substring(0, 150)}...
                </CardDescription>
                
                {/* Extract and display subsections */}
                {renderSubsections(chapter.content)}
              </CardContent>
              <CardFooter className="flex justify-between">
                <Link to={`/chapters/${chapter.id}`}>
                  <Button>
                    <BookOpen className="mr-2 h-4 w-4" />
                    Read Chapter
                  </Button>
                </Link>
                {chapter.quizzes && chapter.quizzes.length > 0 && (
                  <Link to={`/quizzes/${chapter.quizzes[0].id}`}>
                    <Button variant="outline">
                      Take Quiz
                    </Button>
                  </Link>
                )}
              </CardFooter>
            </Card>
          ))
        ) : (
          <p className="text-gray-500">No chapters available for this level.</p>
        )}
      </div>
    </div>
  );
};

export default LevelView;
