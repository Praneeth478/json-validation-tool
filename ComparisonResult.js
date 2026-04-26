import React, { useState } from 'react';
import { 
  Plus, 
  Minus, 
  Edit3, 
  RotateCcw, 
  ChevronDown, 
  ChevronRight,
  CheckCircle,
  AlertTriangle
} from 'lucide-react';

const ComparisonResult = ({ result }) => {
  const [expandedSections, setExpandedSections] = useState({
    summary: true,
    differences: true,
  });

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const getChangeIcon = (changeType) => {
    switch (changeType) {
      case 'added':
        return <Plus className="change-icon added" size={16} />;
      case 'removed':
        return <Minus className="change-icon removed" size={16} />;
      case 'modified':
        return <Edit3 className="change-icon modified" size={16} />;
      case 'type_changed':
        return <RotateCcw className="change-icon type-changed" size={16} />;
      default:
        return <AlertTriangle className="change-icon unknown" size={16} />;
    }
  };

  const getChangeTypeLabel = (changeType) => {
    const labels = {
      added: 'Added',
      removed: 'Removed',
      modified: 'Modified',
      type_changed: 'Type Changed'
    };
    return labels[changeType] || 'Unknown';
  };

  const formatValue = (value) => {
    if (value === null) return 'null';
    if (value === undefined) return 'undefined';
    if (typeof value === 'string') return `"${value}"`;
    if (typeof value === 'object') return JSON.stringify(value, null, 2);
    return String(value);
  };

  const renderDifference = (diff, index) => (
    <div key={index} className={`difference-item ${diff.change_type}`}>
      <div className="difference-header">
        {getChangeIcon(diff.change_type)}
        <span className="change-type">{getChangeTypeLabel(diff.change_type)}</span>
        <span className="path">{diff.path}</span>
      </div>
      
      <div className="difference-content">
        {diff.change_type === 'added' && (
          <div className="value-change">
            <div className="value added">
              <span className="label">Added:</span>
              <pre className="value-text">{formatValue(diff.new_value)}</pre>
              <span className="type">({diff.new_type})</span>
            </div>
          </div>
        )}
        
        {diff.change_type === 'removed' && (
          <div className="value-change">
            <div className="value removed">
              <span className="label">Removed:</span>
              <pre className="value-text">{formatValue(diff.old_value)}</pre>
              <span className="type">({diff.old_type})</span>
            </div>
          </div>
        )}
        
        {(diff.change_type === 'modified' || diff.change_type === 'type_changed') && (
          <div className="value-change">
            <div className="value removed">
              <span className="label">Before:</span>
              <pre className="value-text">{formatValue(diff.old_value)}</pre>
              <span className="type">({diff.old_type})</span>
            </div>
            <div className="change-arrow">→</div>
            <div className="value added">
              <span className="label">After:</span>
              <pre className="value-text">{formatValue(diff.new_value)}</pre>
              <span className="type">({diff.new_type})</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );

  const renderSummaryCard = (label, count, type) => (
    <div className={`summary-card ${type}`}>
      <div className="summary-number">{count}</div>
      <div className="summary-label">{label}</div>
    </div>
  );

  return (
    <div className="comparison-result">
      <div className="result-header">
        <div className="result-status">
          {result.are_equal ? (
            <>
              <CheckCircle className="status-icon equal" size={24} />
              <h2 className="result-title">JSON objects are identical</h2>
            </>
          ) : (
            <>
              <AlertTriangle className="status-icon different" size={24} />
              <h2 className="result-title">
                Found {result.total_differences} difference{result.total_differences !== 1 ? 's' : ''}
              </h2>
            </>
          )}
        </div>
      </div>

      {!result.are_equal && (
        <>
          {/* Summary Section */}
          <div className="result-section">
            <button 
              className="section-header"
              onClick={() => toggleSection('summary')}
            >
              {expandedSections.summary ? <ChevronDown size={20} /> : <ChevronRight size={20} />}
              <h3>Summary</h3>
            </button>
            
            {expandedSections.summary && (
              <div className="summary-grid">
                {renderSummaryCard('Added', result.summary.added, 'added')}
                {renderSummaryCard('Removed', result.summary.removed, 'removed')}
                {renderSummaryCard('Modified', result.summary.modified, 'modified')}
                {renderSummaryCard('Type Changed', result.summary.type_changed, 'type-changed')}
              </div>
            )}
          </div>

          {/* Differences Section */}
          <div className="result-section">
            <button 
              className="section-header"
              onClick={() => toggleSection('differences')}
            >
              {expandedSections.differences ? <ChevronDown size={20} /> : <ChevronRight size={20} />}
              <h3>Detailed Differences</h3>
            </button>
            
            {expandedSections.differences && (
              <div className="differences-list">
                {result.differences.map((diff, index) => renderDifference(diff, index))}
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default ComparisonResult;