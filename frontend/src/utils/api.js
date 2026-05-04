import axios from 'axios';

const API = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1',
});

export const gradeSubmission = (data) => API.post('/grade', data);
export const getSubmissions = () => API.get('/submissions');
export const getStats = () => API.get('/stats');
export const healthCheck = () => API.get('/health');

export default API;
