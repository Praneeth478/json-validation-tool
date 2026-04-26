# JSON Comparator Frontend

A modern React frontend for the JSON Comparator API that provides an intuitive interface for comparing JSON objects and visualizing differences.

## Features

- **Dual Input Methods**: Paste JSON directly or upload JSON files
- **Drag & Drop**: Drag JSON files directly into input areas  
- **Real-time Validation**: Instant JSON syntax validation
- **Visual Diff Display**: Color-coded differences with detailed breakdown
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Dark Mode**: Automatic dark/light mode based on system preference
- **Format Helper**: Auto-format JSON for better readability

## Screenshots

### Main Interface
- Split-pane JSON input with upload capability
- Real-time validation indicators
- Comparison options (ignore order, ignore case)

### Results Display
- Summary statistics with color-coded counts
- Detailed differences with path indicators
- Collapsible sections for better organization
- Type-specific icons for different change types

## Getting Started

### Prerequisites
- Node.js (v14 or higher)
- npm or yarn
- JSON Comparator API running on `http://localhost:8000`

### Installation

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

4. **Open your browser:**
   ```
   http://localhost:3000
   ```

### Production Build

```bash
npm run build
```

This creates a `build` folder with optimized production files.

## API Integration

The frontend automatically connects to the JSON Comparator API at:
- Development: `http://localhost:8000`
- Production: Configure `API_BASE_URL` in `src/apiService.js`

## Usage Guide

### Comparing JSON Objects

1. **Input Methods:**
   - **Text Input**: Paste JSON directly into the text areas
   - **File Upload**: Click "Upload" button to select JSON files
   - **Drag & Drop**: Drag JSON files directly into input areas

2. **Validation:**
   - Green checkmark: Valid JSON
   - Red X: Invalid JSON format
   - Auto-formatting available for valid JSON

3. **Comparison Options:**
   - **Ignore Array Order**: Treats `[1,2,3]` and `[3,2,1]` as equal
   - **Ignore Case**: Case-insensitive string comparison

4. **Running Comparison:**
   - Click "Compare JSON" to analyze differences
   - Results show summary and detailed breakdown

### Understanding Results

#### Summary Section
- **Added**: New fields/values in second JSON
- **Removed**: Fields/values missing in second JSON  
- **Modified**: Changed values
- **Type Changed**: Data type changes (e.g., string → number)

#### Detailed Differences
- **Path**: JSON path to changed field (e.g., `user.address.city`)
- **Change Type**: Icon and label indicating type of change
- **Before/After**: Original and new values with data types

### Tips & Tricks

1. **Load Example**: Click "Load Example" to see sample JSON comparison
2. **Format JSON**: Use "Format" button to pretty-print JSON
3. **Clear All**: Quick way to reset both input areas
4. **File Validation**: Only `.json` files are accepted for upload
5. **Large Files**: Comparison handles moderately large JSON objects efficiently

## Architecture

```
src/
├── components/
│   ├── Header.js              # Top navigation with API status
│   ├── JsonInputSection.js    # JSON input with file upload
│   └── ComparisonResult.js    # Results display component
├── apiService.js              # API communication layer  
├── App.js                     # Main application component
├── App.css                    # Comprehensive styling
└── index.js                   # React app bootstrap
```

### Key Components

- **Header**: Shows API connection status with retry functionality
- **JsonInputSection**: Handles text input, file upload, drag & drop, and validation
- **ComparisonResult**: Displays differences with collapsible sections and color coding
- **ApiService**: Manages all API communications with error handling

## Styling

- **CSS Grid/Flexbox**: Modern responsive layout
- **CSS Variables**: Consistent color scheme and theming
- **Mobile-First**: Responsive design for all screen sizes
- **Dark Mode**: Automatic system preference detection
- **Animations**: Smooth transitions and hover effects

## Error Handling

- **Network Errors**: Connection status indicator and retry functionality
- **JSON Validation**: Real-time syntax checking with visual feedback
- **API Errors**: User-friendly error messages with toast notifications
- **File Upload**: Validation for file type and content

## Performance

- **Lazy Loading**: Components load as needed
- **Debounced Validation**: Efficient real-time JSON checking
- **Optimized Renders**: React.memo and proper key usage
- **Code Splitting**: Automatic bundle optimization

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers

## Troubleshooting

### API Connection Issues
1. Ensure the FastAPI backend is running on `http://localhost:8000`
2. Check browser console for network errors
3. Use the "Retry" button in the header
4. Verify CORS settings if accessing from different domain

### JSON Validation Issues
1. Use online JSON validators to check syntax
2. Check for trailing commas (not allowed in JSON)
3. Ensure proper quote usage (double quotes only)
4. Use the "Format" button to identify issues

### Upload Issues
1. Ensure files have `.json` extension
2. Check file content is valid JSON
3. Verify file size (large files may take time)
4. Try copy-paste as alternative to upload

## Development

### Available Scripts
- `npm start`: Development server with hot reload
- `npm build`: Production build
- `npm test`: Run test suite
- `npm eject`: Eject from Create React App (irreversible)

### Environment Variables
Create `.env` file for custom configuration:
```
REACT_APP_API_BASE_URL=http://localhost:8000
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License
This project is part of the JSON Comparator suite and follows the same licensing terms.