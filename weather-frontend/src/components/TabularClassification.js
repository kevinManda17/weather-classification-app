// src/components/TabularClassification.js
import React, { useState } from 'react';
import axios from 'axios';

const TabularClassification = () => {
  const [formData, setFormData] = useState({
    wind_speed: 10.0,
    precipitation: 50.0,
    temperature: 25.0,
    humidity: 70.0,
    pressure: 1013.0,
    solar_radiation: 1, // 0: Faible, 1: Modéré, 2: Élevé
    cloud_cover: 50.0,
    visibility: 10.0,
    dew_point: 10.0,
    uv_index: 5.0
  });
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: parseFloat(e.target.value)
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await axios.post('http://172.20.10.5:8000/predict/tabular/', formData);
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
      <h2>Classification par Données Tabulaires</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Vitesse du vent (km/h) :</label>
          <input
            type="number"
            name="wind_speed"
            value={formData.wind_speed}
            onChange={handleChange}
            min="0"
            max="200"
            step="0.1"
          />
        </div>
        <div className="form-group">
          <label>Précipitation (%) :</label>
          <input
            type="number"
            name="precipitation"
            value={formData.precipitation}
            onChange={handleChange}
            min="0"
            max="100"
            step="0.1"
          />
        </div>
        <div className="form-group">
          <label>Température (°C) :</label>
          <input
            type="number"
            name="temperature"
            value={formData.temperature}
            onChange={handleChange}
            min="-50"
            max="60"
            step="0.1"
          />
        </div>
        <div className="form-group">
          <label>Humidité (%) :</label>
          <input
            type="number"
            name="humidity"
            value={formData.humidity}
            onChange={handleChange}
            min="0"
            max="100"
            step="0.1"
          />
        </div>
        <div className="form-group">
          <label>Pression (hPa) :</label>
          <input
            type="number"
            name="pressure"
            value={formData.pressure}
            onChange={handleChange}
            min="800"
            max="1100"
            step="0.1"
          />
        </div>
        <div className="form-group">
          <label>Rayonnement solaire :</label>
          <select name="solar_radiation" value={formData.solar_radiation} onChange={handleChange}>
            <option value={0}>Faible</option>
            <option value={1}>Modéré</option>
            <option value={2}>Élevé</option>
          </select>
        </div>
        <div className="form-group">
          <label>Couverture nuageuse (%) :</label>
          <input
            type="number"
            name="cloud_cover"
            value={formData.cloud_cover}
            onChange={handleChange}
            min="0"
            max="100"
            step="0.1"
          />
        </div>
        <div className="form-group">
          <label>Visibilité (km) :</label>
          <input
            type="number"
            name="visibility"
            value={formData.visibility}
            onChange={handleChange}
            min="0"
            max="50"
            step="0.1"
          />
        </div>
        <div className="form-group">
          <label>Point de rosée (°C) :</label>
          <input
            type="number"
            name="dew_point"
            value={formData.dew_point}
            onChange={handleChange}
            min="-30"
            max="30"
            step="0.1"
          />
        </div>
        <div className="form-group">
          <label>Indice UV :</label>
          <input
            type="number"
            name="uv_index"
            value={formData.uv_index}
            onChange={handleChange}
            min="0"
            max="12"
            step="0.1"
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Traitement...' : 'Prédire'}
        </button>
      </form>

      {error && <div className="error">{error}</div>}

      {prediction && (
        <div className="result">
          <h3>Résultat :</h3>
          <p><strong>Prédiction :</strong> {prediction.prediction}</p>
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

export default TabularClassification;