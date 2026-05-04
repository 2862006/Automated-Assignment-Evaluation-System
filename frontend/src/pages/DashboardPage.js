import React, { useEffect, useState } from 'react';
import { getStats, getSubmissions } from '../utils/api';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import './DashboardPage.css';

const GRADE_COLORS = {
  'A+': '#43e97b', 'A': '#43e97b', 'B': '#6c63ff',
  'C': '#f7971e', 'D': '#ff9a44', 'F': '#ff6584',
};

export default function DashboardPage() {
  const [stats, setStats] = useState(null);
  const [submissions, setSubmissions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getStats(), getSubmissions()])
      .then(([s, sub]) => { setStats(s.data); setSubmissions(sub.data); })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading">Loading dashboard...</div>;

  const chartData = stats?.grade_distribution
    ? Object.entries(stats.grade_distribution).map(([k, v]) => ({ grade: k, count: v }))
    : [];

  return (
    <div className="dashboard-page">
      <div className="page-header">
        <h1>Dashboard</h1>
        <p className="subtitle">Overview of all graded submissions.</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card card">
          <span className="stat-label">Total Graded</span>
          <span className="stat-val">{stats?.total_submissions ?? 0}</span>
        </div>
        <div className="stat-card card">
          <span className="stat-label">Average Score</span>
          <span className="stat-val accent">{stats?.average_score ?? 0}%</span>
        </div>
        <div className="stat-card card">
          <span className="stat-label">Highest Score</span>
          <span className="stat-val success">{stats?.highest_score ?? 0}%</span>
        </div>
        <div className="stat-card card">
          <span className="stat-label">Lowest Score</span>
          <span className="stat-val warn">{stats?.lowest_score ?? 0}%</span>
        </div>
      </div>

      {chartData.length > 0 && (
        <div className="card chart-card">
          <h3 className="section-title">Grade Distribution</h3>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <XAxis dataKey="grade" stroke="#7878a0" tick={{ fontSize: 13 }} />
              <YAxis stroke="#7878a0" tick={{ fontSize: 12 }} allowDecimals={false} />
              <Tooltip
                contentStyle={{ background: '#12121f', border: '1px solid #2a2a45', borderRadius: 8, color: '#e8e8f0' }}
                cursor={{ fill: 'rgba(108,99,255,0.08)' }}
              />
              <Bar dataKey="count" radius={[6, 6, 0, 0]}>
                {chartData.map((entry, i) => (
                  <Cell key={i} fill={GRADE_COLORS[entry.grade] || '#6c63ff'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      <div className="card">
        <h3 className="section-title">Recent Submissions</h3>
        {submissions.length === 0 ? (
          <div className="empty">No submissions yet. Grade something first!</div>
        ) : (
          <div className="table-wrap">
            <table className="sub-table">
              <thead>
                <tr>
                  <th>ID</th><th>Student</th><th>Subject</th>
                  <th>Score</th><th>Grade</th><th>Time</th>
                </tr>
              </thead>
              <tbody>
                {submissions.map(s => (
                  <tr key={s.id}>
                    <td className="mono muted">#{s.id}</td>
                    <td>{s.student_name}</td>
                    <td><span className="chip">{s.subject}</span></td>
                    <td className="mono">{s.marks_obtained}/{s.max_marks} ({s.percentage}%)</td>
                    <td>
                      <span className="grade-chip" style={{ color: GRADE_COLORS[s.grade_letter] || '#fff', borderColor: GRADE_COLORS[s.grade_letter] || '#2a2a45' }}>
                        {s.grade_letter}
                      </span>
                    </td>
                    <td className="muted time">{s.timestamp}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
