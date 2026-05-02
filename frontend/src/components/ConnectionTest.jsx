import React, { useState, useEffect } from 'react';

// NOTE: Ensure this URL matches your backend's running address and port
const API_URL = import.meta.env.VITE_API_URL; 

const ConnectionTest = () => {
  const [data, setData] = useState(null);
  const [promptData, setPromptData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isPromptLoading, setIsPromptLoading] = useState(false);
  const [error, setError] = useState(null);
  const [promptError, setPromptError] = useState(null);

  // Basic API connection test
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

  // Test prompt builder endpoint
  const testPromptBuilder = async () => {
    setIsPromptLoading(true);
    setPromptError(null);
    
    try {
      const response = await fetch(`${API_URL}/user-submissions/api/prompt-builder`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          idea: 'Create a task management application with user authentication and real-time updates',
          stack: ['React', 'FastAPI', 'MongoDB', 'Socket.io']
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`HTTP error! Status: ${response.status} - ${errorData.detail || response.statusText}`);
      }
      
      const result = await response.json();
      setPromptData(result);
      
    } catch (err) {
      setPromptError(err.message);
    } finally {
      setIsPromptLoading(false);
    }
  };

  // --- Render Logic ---
  if (isLoading) {
    return <div className="card">Connecting to API...</div>;
  }

  if (error) {
    return (
      <div className="card">
        <h3>Connection Failed: {error}</h3>
        <p>Make sure FastAPI CORSMiddleware is configured correctly.</p>
      </div>
    );
  }
  
  return (
    <div className="card">
      <div style={{ marginBottom: '20px' }}>
        <h2>✅ Basic Connection Successful!</h2>
        <p>Server Status: {data?.status || 'Unknown'}</p>
        <p>Service: {data?.service || 'Unknown'}</p>
      </div>

      <div style={{ marginBottom: '20px' }}>
        <h3>🔧 Prompt Builder Service Test</h3>
        <button 
          onClick={testPromptBuilder}
          disabled={isPromptLoading}
          style={{
            padding: '10px 20px',
            backgroundColor: isPromptLoading ? '#ccc' : '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: isPromptLoading ? 'not-allowed' : 'pointer'
          }}
        >
          {isPromptLoading ? 'Testing...' : 'Test Prompt Builder Endpoint'}
        </button>
      </div>

      {isPromptLoading && (
        <div className="card">
          <p>Testing prompt builder endpoint...</p>
        </div>
      )}

      {promptError && (
        <div className="card error">
          <h4>❌ Prompt Builder Test Failed</h4>
          <p>{promptError}</p>
        </div>
      )}

      {promptData && (
        <div className="card success">
          <h4>✅ Prompt Builder Test Successful!</h4>
          <p><strong>Status:</strong> {promptData.success ? 'Success' : 'Failed'}</p>
          <p><strong>Message:</strong> {promptData.message}</p>
          <details style={{ marginTop: '10px' }}>
            <summary style={{ cursor: 'pointer', fontWeight: 'bold' }}>View Generated Prompt</summary>
            <div style={{ 
              marginTop: '10px', 
              padding: '10px', 
              backgroundColor: '#f8f9fa', 
              borderRadius: '4px',
              fontSize: '12px',
              maxHeight: '200px',
              overflow: 'auto',
              whiteSpace: 'pre-wrap'
            }}>
              {promptData.prompt}
            </div>
          </details>
        </div>
      )}
    </div>
  );
};

export default ConnectionTest;
