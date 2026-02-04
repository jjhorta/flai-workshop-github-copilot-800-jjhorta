import React, { useState, useEffect } from 'react';

function Teams() {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const codespace = process.env.REACT_APP_CODESPACE_NAME || 'localhost:8000';
    const apiUrl = `https://${codespace}-8000.app.github.dev/api/teams/`;
    
    console.log('Fetching teams from:', apiUrl);
    
    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log('Teams data:', data);
        // Handle both paginated and plain array responses
        setTeams(Array.isArray(data) ? data : (data.results || []));
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching teams:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) return (
    <div className="container mt-4 loading-spinner">
      <div className="spinner-border text-primary" role="status">
        <span className="visually-hidden">Loading...</span>
      </div>
      <p className="mt-3">Loading teams...</p>
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
      <h2 className="mb-4">Teams</h2>
      {teams.length === 0 ? (
        <div className="alert alert-info" role="alert">
          No teams found. Create a team and start competing!
        </div>
      ) : (
        <div className="row">
          {teams.map((team) => (
            <div key={team._id} className="col-md-6 col-lg-4 mb-4">
              <div className="card shadow-sm">
                <div className="card-header bg-primary text-white">
                  <h5 className="card-title mb-0 text-white">{team.name}</h5>
                </div>
                <div className="card-body">
                  <p className="card-text">{team.description}</p>
                </div>
                <div className="card-footer text-muted">
                  <small><i className="bi bi-calendar"></i> Created: {new Date(team.created_at).toLocaleDateString()}</small>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Teams;
