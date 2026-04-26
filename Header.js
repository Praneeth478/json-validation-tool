import React from 'react';
import { RefreshCw, CheckCircle, XCircle, AlertCircle } from 'lucide-react';

const Header = ({ apiStatus, onRetryConnection }) => {
  const getStatusIcon = () => {
    switch (apiStatus) {
      case 'connected':
        return <CheckCircle className="status-icon connected" size={20} />;
      case 'error':
        return <XCircle className="status-icon error" size={20} />;
      default:
        return <AlertCircle className="status-icon checking" size={20} />;
    }
  };

  const getStatusText = () => {
    switch (apiStatus) {
      case 'connected':
        return 'API Connected';
      case 'error':
        return 'API Disconnected';
      default:
        return 'Checking API...';
    }
  };

  return (
    <header className="header">
      <div className="header-content">
        <div className="logo-section">
          <h1 className="logo">JSON Comparator</h1>
          <p className="tagline">Compare JSON objects and visualize differences</p>
        </div>
        
        <div className="status-section">
          <div className={`api-status ${apiStatus}`}>
            {getStatusIcon()}
            <span className="status-text">{getStatusText()}</span>
            {apiStatus === 'error' && (
              <button 
                className="retry-btn"
                onClick={onRetryConnection}
                title="Retry connection"
              >
                <RefreshCw size={16} />
              </button>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;