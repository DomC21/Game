import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { contentAPI } from '../services/api';
import { Button } from '../components/ui-js/button';
import { Card, CardContent, CardFooter, CardHeader } from '../components/ui-js/card';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '../components/ui-js/tabs';
import { ChevronLeft, ChevronRight, BookOpen, List } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

const ChapterView = () => {
  const { chapterId } = useParams();
  const { token } = useAuth();
  const navigate = useNavigate();
  const [chapter, setChapter] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [subsections, setSubsections] = useState([]);
  const [activeTab, setActiveTab] = useState("full-content");
  
  // Function to extract subsections from chapter content
  const extractSubsections = (content) => {
    const subsectionRegex = /## (.*?)(?=\n## |\n# |\n$)/gs;
    const matches = content.match(subsectionRegex) || [];
    
    return matches.map((subsection, index) => {
      const title = subsection.match(/## (.*?)(?=\n|$)/)?.[1] || `Subsection ${index + 1}`;
      const content = subsection.replace(/## .*?\n/, '').trim();
      return { id: `subsection-${index}`, title, content };
    });
  };

  useEffect(() => {
    const fetchChapter = async () => {
      try {
        setIsLoading(true);
        const data = await contentAPI.getChapter(token, chapterId);
        setChapter(data);
        
        // Extract subsections from chapter content
        if (data && data.content) {
          const extractedSubsections = extractSubsections(data.content);
          setSubsections(extractedSubsections);
        }
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

      {/* Chapter Content with Tabs */}
      <Card className="mb-6">
        <CardContent className="pt-6">
          <Tabs defaultValue="full-content" value={activeTab} onValueChange={setActiveTab} className="mb-6">
            <TabsList>
              <TabsTrigger value="full-content">Full Content</TabsTrigger>
              {subsections.map((subsection) => (
                <TabsTrigger key={subsection.id} value={subsection.id}>
                  {subsection.title}
                </TabsTrigger>
              ))}
            </TabsList>
            
            <TabsContent value="full-content" className="mt-4">
              <div className="prose max-w-none">
                <ReactMarkdown>{chapter.content}</ReactMarkdown>
              </div>
            </TabsContent>
            
            {subsections.map((subsection) => (
              <TabsContent key={subsection.id} value={subsection.id} className="mt-4">
                <div className="prose max-w-none">
                  <h2>{subsection.title}</h2>
                  <ReactMarkdown>{subsection.content}</ReactMarkdown>
                </div>
              </TabsContent>
            ))}
          </Tabs>
          
          {/* Subsections List for Mobile/Small Screens */}
          <div className="md:hidden mt-6">
            <h3 className="text-lg font-medium flex items-center mb-2">
              <List className="mr-2 h-4 w-4" />
              Subsections:
            </h3>
            <ul className="list-disc pl-5 space-y-2">
              {subsections.map((subsection) => (
                <li key={subsection.id} className="text-gray-700">
                  <button 
                    className="text-left hover:text-blue-600 focus:outline-none focus:text-blue-600"
                    onClick={() => setActiveTab(subsection.id)}
                  >
                    {subsection.title}
                  </button>
                </li>
              ))}
            </ul>
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
