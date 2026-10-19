// Single place for the backend URL. Override per environment with
// REACT_APP_API_URL (e.g. http://localhost:8000 for local development).
export const API_URL =
  process.env.REACT_APP_API_URL || 'https://lightweight-feedback-system-backend.onrender.com';
