import axios from 'axios';

// Base API configuration
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://your-api-domain.com'  // Replace with your production URL
  : 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API service class
export class ApiService {
  /**
   * Compare two JSON objects
   * @param {Object} json1 - First JSON object
   * @param {Object} json2 - Second JSON object
   * @param {boolean} ignoreOrder - Ignore order in arrays
   * @param {boolean} ignoreCase - Ignore case in strings
   * @returns {Promise<Object>} Comparison result
   */
  static async compareJSON(json1, json2, ignoreOrder = false, ignoreCase = false) {
    try {
      const response = await api.post('/compare', {
        json1,
        json2,
        ignore_order: ignoreOrder,
        ignore_case: ignoreCase,
      });
      return response.data;
    } catch (error) {
      console.error('API Error:', error);
      if (error.response?.data?.detail) {
        throw new Error(error.response.data.detail);
      }
      throw new Error('Failed to compare JSON objects');
    }
  }

  /**
   * Compare JSON from text strings
   * @param {string} jsonText1 - First JSON as string
   * @param {string} jsonText2 - Second JSON as string
   * @param {boolean} ignoreOrder - Ignore order in arrays
   * @param {boolean} ignoreCase - Ignore case in strings
   * @returns {Promise<Object>} Comparison result
   */
  static async compareJSONText(jsonText1, jsonText2, ignoreOrder = false, ignoreCase = false) {
    try {
      const response = await api.post('/compare-text', {
        json_text1: jsonText1,
        json_text2: jsonText2,
        ignore_order: ignoreOrder,
        ignore_case: ignoreCase,
      });
      return response.data;
    } catch (error) {
      console.error('API Error:', error);
      if (error.response?.data?.detail) {
        throw new Error(error.response.data.detail);
      }
      throw new Error('Failed to compare JSON text');
    }
  }

  /**
   * Check API health
   * @returns {Promise<Object>} Health status
   */
  static async checkHealth() {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      console.error('Health check failed:', error);
      throw new Error('API is not accessible');
    }
  }
}

export default ApiService;