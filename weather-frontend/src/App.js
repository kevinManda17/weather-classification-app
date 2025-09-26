// src/App.js
import React, { useState } from 'react';
import './App.css';
import ImageClassification from './components/ImageClassification';
import TabularClassification from './components/TabularClassification';

function App() {
  const [activeTab, setActiveTab] = useState('image');

  return (
    <div className="App">
      <header className="App-header">
        <h1>Analyse Météo Intelligente</h1>
      </header>
      <div className="tabs">
        <button 
          className={activeTab === 'image' ? 'active' : ''} 
          onClick={() => setActiveTab('image')}
        >
          Classification d'Image
        </button>
        <button 
          className={activeTab === 'tabular' ? 'active' : ''} 
          onClick={() => setActiveTab('tabular')}
        >
          Données Tabulaires
        </button>
      </div>
      <main>
        {activeTab === 'image' && <ImageClassification />}
        {activeTab === 'tabular' && <TabularClassification />}
      </main>
    </div>
  );
}

export default App;