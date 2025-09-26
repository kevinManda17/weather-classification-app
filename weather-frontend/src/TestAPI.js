import React from 'react';
import axios from 'axios';

const TestAPI = () => {
  const testConnection = async () => {
    try {
      const response = await axios.get('http://172.20.10.5:8000/api/');
      console.log('Réponse:', response);
    } catch (error) {
      console.error('Erreur complète:', error);
      console.error('Status:', error.response?.status);
      console.error('Data:', error.response?.data);
    }
  };

  return (
    <div>
      <button onClick={testConnection}>Tester la connexion API</button>
    </div>
  );
};

export default TestAPI;