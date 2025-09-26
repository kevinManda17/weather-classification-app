// src/components/ImageClassification.js
import React, { useState } from 'react';
import axios from 'axios';

const ImageClassification = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedImage(file);
      setPreviewUrl(URL.createObjectURL(file));
      setPrediction(null);
      setError('');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedImage) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('image', selectedImage);

    try {
      const response = await axios.post('http://172.20.10.5:8000/predict/image/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setPrediction(response.data);
      setError('');
    } catch (err) {
      setError(err.response?.data?.error || 'Une erreur est survenue');
      setPrediction(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="classification-container">
      <h2>Classification d'Image Météo</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="image-upload">Choisir une image :</label>
          <input
            type="file"
            id="image-upload"
            accept="image/*"
            onChange={handleImageChange}
          />
        </div>
        {previewUrl && (
          <div className="image-preview">
            <img src={previewUrl} alt="Preview" />
          </div>
        )}
        <button type="submit" disabled={!selectedImage || loading}>
          {loading ? 'Traitement...' : 'Prédire'}
        </button>
      </form>

      {error && <div className="error">{error}</div>}

      {prediction && (
        <div className="result">
          <h3>Résultat :</h3>
          <p><strong>Prédiction :</strong> {prediction.prediction}</p>
          <p><strong>Confiance :</strong> {(prediction.confidence * 100).toFixed(2)}%</p>
          <div>
            <strong>Conseils :</strong>
            <ul>
              {Object.entries(prediction.advice).map(([key, value]) => (
                <li key={key}><strong>{key} :</strong> {value}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default ImageClassification;