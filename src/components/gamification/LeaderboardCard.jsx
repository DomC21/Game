import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui-js/card';
import { Badge } from '../ui-js/badge';

const LeaderboardCard = ({ leaderboard, currentUserId }) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center">
          <span className="text-yellow-500 mr-2">🏆</span>
          Leaderboard
        </CardTitle>
        <CardDescription>See how you rank against other learners</CardDescription>
      </CardHeader>
      <CardContent>
        {leaderboard.length > 0 ? (
          <div className="rounded-lg border overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Rank</th>
                  <th scope="col" className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">User</th>
                  <th scope="col" className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Level</th>
                  <th scope="col" className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Points</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {leaderboard.slice(0, 10).map((user, index) => (
                  <tr key={user.id} className={user.id === currentUserId ? 'bg-blue-50' : ''}>
                    <td className="px-4 py-3 whitespace-nowrap">
                      <LeaderboardRank rank={index + 1} />
                    </td>
                    <td className="px-4 py-3 whitespace-nowrap text-sm">
                      <div className="flex items-center">
                        <span className="font-medium text-gray-900">{user.username}</span>
                        {user.id === currentUserId && (
                          <Badge className="ml-2 bg-blue-100 text-blue-800 text-xs">You</Badge>
                        )}
                      </div>
                    </td>
                    <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
                      <Badge variant="outline" className="bg-gray-50">
                        Level {user.current_level}
                      </Badge>
                    </td>
                    <td className="px-4 py-3 whitespace-nowrap text-sm">
                      <span className="font-medium text-gray-900">{user.total_points}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            No leaderboard data available yet.
          </div>
        )}
      </CardContent>
    </Card>
  );
};

// Helper component for rank display
const LeaderboardRank = ({ rank }) => {
  let badgeClass = "flex items-center justify-center w-8 h-8 rounded-full text-white font-bold";
  
  if (rank === 1) {
    badgeClass += " bg-yellow-500"; // Gold
  } else if (rank === 2) {
    badgeClass += " bg-gray-400"; // Silver
  } else if (rank === 3) {
    badgeClass += " bg-amber-700"; // Bronze
  } else {
    badgeClass += " bg-gray-200 text-gray-700"; // Others
  }
  
  return (
    <div className={badgeClass}>
      {rank}
    </div>
  );
};

export default LeaderboardCard;
