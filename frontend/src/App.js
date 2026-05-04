import React, { useState } from 'react';
import GradePage from './pages/GradePage';
import DashboardPage from './pages/DashboardPage';
import './App.css';

export default function App() {
  const [page, setPage] = useState('grade');

  return (
    <div className="app">
      <header className="header">
        <div className="header-inner">
          <div className="logo">
            <span className="logo-icon">◈</span>
            <span className="logo-text">Grade<em>AI</em></span>
          </div>
          <nav className="nav">
            <button
              className={`nav-btn ${page === 'grade' ? 'active' : ''}`}
              onClick={() => setPage('grade')}
            >Grade</button>
            <button
              className={`nav-btn ${page === 'dashboard' ? 'active' : ''}`}
              onClick={() => setPage('dashboard')}
            >Dashboard</button>
          </nav>
        </div>
      </header>
      <main className="main">
        {page === 'grade' ? <GradePage /> : <DashboardPage />}
      </main>
    </div>
  );
}
