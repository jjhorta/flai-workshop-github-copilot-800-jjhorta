import React, { useState, useEffect } from 'react';

function Activities() {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const codespace = process.env.REACT_APP_CODESPACE_NAME || 'localhost:8000';
    const apiUrl = `https://${codespace}-8000.app.github.dev/api/activities/`;
    
    console.log('Fetching activities from:', apiUrl);
    
    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log('Activities data:', data);
        // Handle both paginated and plain array responses
        setActivities(Array.isArray(data) ? data : (data.results || []));
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching activities:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) return (
    <div className="container mt-4 loading-spinner">
      <div className="spinner-border text-primary" role="status">
        <span className="visually-hidden">Loading...</span>
      </div>
      <p className="mt-3">Loading activities...</p>
    </div>
  );
  
  if (error) return (
    <div className="container mt-4">
      <div className="alert alert-danger" role="alert">
        <h4 className="alert-heading">Error!</h4>
        <p>{error}</p>
      </div>
    </div>
  );

  return (
    <div className="container mt-4">
      <h2 className="mb-4">Activities</h2>
      <div className="table-responsive">
        <table className="table table-striped table-hover">
        <thead>
          <tr>
            <th>Activity Type</th>
            <th>User ID</th>
            <th>Duration (min)</th>
            <th>Distance (km)</th>
            <th>Calories</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {activities.map((activity) => (
            <tr key={activity._id}>
              <td>{activity.activity_type}</td>
              <td>{activity.user_id}</td>
              <td>{activity.duration}</td>
              <td>{activity.distance ? activity.distance.toFixed(2) : 'N/A'}</td>
              <td>{activity.calories}</td>
              <td>{new Date(activity.date).toLocaleDateString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
      </div>
      {activities.length === 0 && (
        <div className="alert alert-info" role="alert">
          No activities found. Start tracking your fitness journey!
        </div>
      )}
    </div>
  );
}

export default Activities;
