import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const codespace = process.env.REACT_APP_CODESPACE_NAME || 'localhost:8000';
    const apiUrl = `https://${codespace}-8000.app.github.dev/api/workouts/`;
    
    console.log('Fetching workouts from:', apiUrl);
    
    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log('Workouts data:', data);
        // Handle both paginated and plain array responses
        setWorkouts(Array.isArray(data) ? data : (data.results || []));
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching workouts:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="container mt-4"><p>Loading workouts...</p></div>;
  if (error) return <div className="container mt-4"><p className="text-danger">Error: {error}</p></div>;

  return (
    <div className="container mt-4">
      <h2>Workouts</h2>
      <div className="row">
        {workouts.map((workout) => (
          <div key={workout._id} className="col-md-4 mb-4">
            <div className="card h-100">
              <div className="card-body">
                <h5 className="card-title">{workout.name}</h5>
                <h6 className="card-subtitle mb-2 text-muted">
                  <span className={`badge ${workout.difficulty_level === 'Advanced' ? 'bg-danger' : workout.difficulty_level === 'Intermediate' ? 'bg-warning' : 'bg-success'}`}>
                    {workout.difficulty_level}
                  </span>
                </h6>
                <p className="card-text">{workout.description}</p>
                <ul className="list-group list-group-flush">
                  <li className="list-group-item">Duration: {workout.duration} minutes</li>
                  <li className="list-group-item">Type: {workout.exercise_type}</li>
                </ul>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Workouts;
