import React, { useState, useEffect } from 'react';

// NOTE: Ensure this URL matches your backend's running address and port
const API_URL = import.meta.env.VITE_API_URL; 

const ConnectionTest = () => {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // API calling logic runs in the useEffect hook
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`${API_URL}/`);
        
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status} ${response.statusText}`);
        }
        
        const result = await response.json();
        
        setData(result);
        
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  // --- Render Logic ---
  if (isLoading) {
    return <div className="card">Connecting to API...</div>;
  }

  if (error) {
    return <div className="card error">Connection Failed: {error}. Make sure FastAPI CORSMiddleware, if any, is configured correctly.</div>;
  }
  
  if (data) {
    return (
      <div className="card success">
        <h2>✅ Connection Successful!</h2>
        <p>Backend response received:</p>
        <pre>{JSON.stringify(data, null, 2)}</pre>
      </div>
    );
  }

  return <div className="card">An unknown error occurred.</div>;
};

export default ConnectionTest;
