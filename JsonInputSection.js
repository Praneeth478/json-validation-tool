import React, { useRef, useState } from 'react';
import { Upload, FileText, Check, X } from 'lucide-react';
import { toast } from 'react-hot-toast';

const JsonInputSection = ({ label, value, onChange, placeholder }) => {
  const fileInputRef = useRef(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const [fileName, setFileName] = useState('');

  const handleFileUpload = (file) => {
    if (!file) return;

    // Accept JSON files, text files, and other common text file extensions
    const validTypes = ['application/json', 'text/plain', 'text/json'];
    const validExtensions = ['.json', '.txt', '.text'];
    
    const hasValidType = validTypes.includes(file.type);
    const hasValidExtension = validExtensions.some(ext => file.name.toLowerCase().endsWith(ext));
    
    if (!hasValidType && !hasValidExtension) {
      toast.error('Please upload a JSON file (.json) or text file (.txt) containing JSON');
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const content = e.target.result;
        // Validate JSON content
        JSON.parse(content);
        onChange(content);
        setFileName(file.name);
        toast.success(`Loaded ${file.name}`);
      } catch (error) {
        toast.error('File content is not valid JSON. Please check the JSON syntax.');
      }
    };
    reader.readAsText(file);
  };

  const handleFileInputChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      handleFileUpload(file);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    
    const file = e.dataTransfer.files[0];
    if (file) {
      handleFileUpload(file);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleTextChange = (e) => {
    onChange(e.target.value);
    if (fileName) {
      setFileName(''); // Clear filename when text is manually edited
    }
  };

  const formatJson = () => {
    try {
      const parsed = JSON.parse(value);
      const formatted = JSON.stringify(parsed, null, 2);
      onChange(formatted);
      toast.success('JSON formatted');
    } catch (error) {
      toast.error('Invalid JSON format');
    }
  };

  const clearInput = () => {
    onChange('');
    setFileName('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const isValidJson = () => {
    if (!value.trim()) return null;
    try {
      JSON.parse(value);
      return true;
    } catch {
      return false;
    }
  };

  const validationStatus = isValidJson();

  return (
    <div className="json-input-section">
      <div className="input-header">
        <label className="input-label">{label}</label>
        <div className="input-actions">
          {fileName && (
            <div className="file-indicator">
              <FileText size={16} />
              <span>{fileName}</span>
            </div>
          )}
          
          {validationStatus !== null && (
            <div className={`validation-indicator ${validationStatus ? 'valid' : 'invalid'}`}>
              {validationStatus ? (
                <><Check size={16} /> Valid JSON</>
              ) : (
                <><X size={16} /> Invalid JSON</>
              )}
            </div>
          )}

          <button
            className="btn btn-sm btn-secondary"
            onClick={() => fileInputRef.current?.click()}
            title="Upload JSON file"
          >
            <Upload size={16} />
            Upload
          </button>
          
          {value && (
            <>
              <button
                className="btn btn-sm btn-secondary"
                onClick={formatJson}
                title="Format JSON"
              >
                Format
              </button>
              <button
                className="btn btn-sm btn-secondary"
                onClick={clearInput}
                title="Clear input"
              >
                <X size={16} />
              </button>
            </>
          )}
        </div>
      </div>

      <div 
        className={`input-container ${isDragOver ? 'drag-over' : ''}`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
      >
        <textarea
          className={`json-textarea ${validationStatus === false ? 'invalid' : ''}`}
          value={value}
          onChange={handleTextChange}
          placeholder={placeholder}
          rows={15}
          spellCheck={false}
        />
        
        {isDragOver && (
          <div className="drop-overlay">
            <Upload size={48} />
            <p>Drop JSON or text file here</p>
          </div>
        )}

        <input
          ref={fileInputRef}
          type="file"
          accept=".json,.txt,.text,application/json,text/plain"
          onChange={handleFileInputChange}
          style={{ display: 'none' }}
        />
      </div>
    </div>
  );
};

export default JsonInputSection;