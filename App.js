import React, { useState, useEffect } from 'react';
import { Toaster, toast } from 'react-hot-toast';
import JsonInputSection from './components/JsonInputSection';
import ComparisonResult from './components/ComparisonResult';
import Header from './components/Header';
import ApiService from './apiService';
import './App.css';

function App() {
  const [json1, setJson1] = useState('');
  const [json2, setJson2] = useState('');
  const [comparisonResult, setComparisonResult] = useState(null);
  const [isComparing, setIsComparing] = useState(false);
  const [ignoreOrder, setIgnoreOrder] = useState(false);
  const [ignoreCase, setIgnoreCase] = useState(false);
  const [apiStatus, setApiStatus] = useState('checking');

  // Check API health on component mount
  useEffect(() => {
    checkApiHealth();
  }, []);

  const checkApiHealth = async () => {
    try {
      await ApiService.checkHealth();
      setApiStatus('connected');
      toast.success('Connected to JSON Comparator API');
    } catch (error) {
      setApiStatus('error');
      toast.error('Cannot connect to API. Please ensure the backend is running.');
    }
  };

  const handleCompare = async () => {
    if (!json1.trim() || !json2.trim()) {
      toast.error('Please provide both JSON inputs');
      return;
    }

    setIsComparing(true);
    setComparisonResult(null);

    try {
      // Try to parse JSON first to validate
      const parsedJson1 = JSON.parse(json1);
      const parsedJson2 = JSON.parse(json2);

      // Make API call
      const result = await ApiService.compareJSON(
        parsedJson1,
        parsedJson2,
        ignoreOrder,
        ignoreCase
      );

      setComparisonResult(result);
      
      if (result.are_equal) {
        toast.success('JSON objects are identical!');
      } else {
        toast.success(`Found ${result.total_differences} difference(s)`);
      }
    } catch (error) {
      console.error('Comparison error:', error);
      if (error.message.includes('Unexpected token')) {
        toast.error('Invalid JSON format. Please check your input.');
      } else {
        toast.error(error.message || 'Failed to compare JSON objects');
      }
    } finally {
      setIsComparing(false);
    }
  };

  const handleClear = () => {
    setJson1('');
    setJson2('');
    setComparisonResult(null);
    toast.success('Cleared all inputs');
  };

  const loadExample = () => {
    const example1 = {
      "user": {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30,
        "skills": ["Python", "JavaScript", "SQL"],
        "address": {
          "city": "New York",
          "zipcode": "10001"
        }
      }
    };

    const example2 = {
      "user": {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "age": 31,
        "skills": ["Python", "JavaScript", "SQL", "Go"],
        "address": {
          "city": "Boston",
          "zipcode": "02101",
          "state": "MA"
        }
      }
    };

    setJson1(JSON.stringify(example1, null, 2));
    setJson2(JSON.stringify(example2, null, 2));
    toast.success('Loaded example JSON objects');
  };

  return (
    <div className="app">
      <Toaster 
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#363636',
            color: '#fff',
          },
        }}
      />
      
      <Header 
        apiStatus={apiStatus}
        onRetryConnection={checkApiHealth}
      />

      <main className="main-content">
        <div className="comparison-controls">
          <div className="options">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={ignoreOrder}
                onChange={(e) => setIgnoreOrder(e.target.checked)}
              />
              Ignore array order
            </label>
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={ignoreCase}
                onChange={(e) => setIgnoreCase(e.target.checked)}
              />
              Ignore case
            </label>
          </div>

          <div className="action-buttons">
            <button 
              className="btn btn-secondary" 
              onClick={loadExample}
              disabled={isComparing}
            >
              Load Example
            </button>
            <button 
              className="btn btn-secondary" 
              onClick={handleClear}
              disabled={isComparing}
            >
              Clear All
            </button>
            <button 
              className="btn btn-primary" 
              onClick={handleCompare}
              disabled={isComparing || apiStatus !== 'connected'}
            >
              {isComparing ? 'Comparing...' : 'Compare JSON'}
            </button>
          </div>
        </div>

        <div className="input-section">
          <JsonInputSection
            label="JSON Object 1"
            value={json1}
            onChange={setJson1}
            placeholder="Paste your first JSON object here or upload a file..."
          />
          <div className="vs-divider">VS</div>
          <JsonInputSection
            label="JSON Object 2"
            value={json2}
            onChange={setJson2}
            placeholder="Paste your second JSON object here or upload a file..."
          />
        </div>

        {comparisonResult && (
          <ComparisonResult result={comparisonResult} />
        )}
      </main>
    </div>
  );
}

export default App;