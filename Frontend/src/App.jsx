import { useState } from 'react';
import './App.css';

function App() {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleClassify = async (e) => {
    e.preventDefault();
    if (!text.trim()) return;

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await fetch('http://localhost:3000/api/classify', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      });

      const data = await response.json();

      if (response.ok) {
        setResult(data.prediction);
      } else {
        setError(data.error || 'Failed to classify email.');
      }
    } catch (err) {
      setError('Cannot connect to the server. Make sure the Node.js backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="glass-panel">
        <header>
          <h1>Secure<span>Mail</span></h1>
          <p>Advanced AI Spam Classification</p>
        </header>

        <form onSubmit={handleClassify} className="input-section">
          <textarea
            placeholder="Paste the email content here..."
            value={text}
            onChange={(e) => setText(e.target.value)}
            disabled={loading}
          />
          
          <button type="submit" disabled={loading || !text.trim()} className={loading ? 'loading' : ''}>
            {loading ? 'Analyzing...' : 'Classify Email'}
          </button>
        </form>

        {error && (
          <div className="error-message">
            <span className="icon">⚠️</span> {error}
          </div>
        )}

        {result && (
          <div className={`result-card ${result.replace(' ', '-')}`}>
            <h2>{result === 'spam' ? '🚨 Spam Detected' : '✅ Safe Email'}</h2>
            <p>Our AI model classified this message as <strong>{result.toUpperCase()}</strong>.</p>
          </div>
        )}
      </div>
      
      {/* Background decoration */}
      <div className="blob blob-1"></div>
      <div className="blob blob-2"></div>
    </div>
  );
}

export default App;
