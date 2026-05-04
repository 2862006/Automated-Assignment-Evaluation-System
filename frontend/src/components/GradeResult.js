import React from 'react';
import './GradeResult.css';

const GRADE_COLORS = {
  'A+': '#43e97b', 'A': '#43e97b', 'B': '#6c63ff',
  'C': '#f7971e', 'D': '#ff9a44', 'F': '#ff6584',
};

const RISK_COLORS = { Low: '#43e97b', Medium: '#f7971e', High: '#ff6584' };

function PlagiarismBadge({ data }) {
  const color = RISK_COLORS[data.risk_level] || '#7878a0';
  return (
    <div className="plagiarism-box" style={{ borderColor: color }}>
      <div className="plag-header">
        <span className="plag-title">🔍 Plagiarism Check</span>
        <span className="plag-verdict" style={{ color }}>{data.verdict}</span>
      </div>
      <div className="plag-row">
        <div className="plag-score-wrap">
          <div className="plag-bar-bg">
            <div className="plag-bar-fill" style={{ width: `${data.similarity_percentage}%`, background: color }} />
          </div>
          <span className="plag-pct" style={{ color }}>{data.similarity_percentage}% similarity</span>
        </div>
        <span className="plag-risk" style={{ color, borderColor: color }}>{data.risk_level} Risk</span>
      </div>
      {data.matched_with && (
        <p className="plag-match">⚠ High similarity with: <strong>{data.matched_with}</strong></p>
      )}
    </div>
  );
}

export default function GradeResult({ data }) {
  const color = GRADE_COLORS[data.grade_letter] || '#6c63ff';

  return (
    <div className="result-card card">
      <div className="result-header">
        <div>
          <h2>{data.student_name}</h2>
          <span className="subject-tag">{data.subject}</span>
        </div>
        <div className="grade-badge" style={{ borderColor: color, color }}>
          {data.grade_letter}
        </div>
      </div>

      <div className="score-row">
        <div className="score-item">
          <span className="score-label">Marks</span>
          <span className="score-val">{data.marks_obtained} / {data.max_marks}</span>
        </div>
        <div className="score-item">
          <span className="score-label">Percentage</span>
          <span className="score-val" style={{ color }}>{data.percentage}%</span>
        </div>
        <div className="progress-bar-wrap">
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${data.percentage}%`, background: color }} />
          </div>
        </div>
      </div>

      {data.plagiarism && <PlagiarismBadge data={data.plagiarism} />}

      <div className="feedback-section">
        <h3>Overall Feedback</h3>
        <p className="overall-feedback">{data.overall_feedback}</p>
      </div>

      <div className="two-col">
        <div className="strengths-box">
          <h4>✓ Strengths</h4>
          <ul>{data.strengths.map((s, i) => <li key={i}>{s}</li>)}</ul>
        </div>
        <div className="improvements-box">
          <h4>↑ Improvements</h4>
          <ul>{data.improvements.map((s, i) => <li key={i}>{s}</li>)}</ul>
        </div>
      </div>

      {data.detailed_feedback?.length > 0 && (
        <div className="detailed-section">
          <h3>Detailed Feedback</h3>
          {data.detailed_feedback.map((fb, i) => (
            <div className="fb-item" key={i}>
              <div className="fb-category">{fb.category}</div>
              <p className="fb-comment">{fb.comment}</p>
              <p className="fb-suggestion">💡 {fb.suggestion}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

