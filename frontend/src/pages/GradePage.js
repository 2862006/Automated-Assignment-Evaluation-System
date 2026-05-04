import React, { useState } from 'react';
import { gradeSubmission } from '../utils/api';
import GradeResult from '../components/GradeResult';
import './GradePage.css';

const SUBJECTS = ['math', 'science', 'english', 'history', 'coding', 'other'];

export default function GradePage() {
  const [form, setForm] = useState({
    student_name: '',
    subject: 'english',
    question: '',
    answer: '',
    max_marks: 10,
    rubric: '',
    is_coding: false,
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }));

  const handleSubjectChange = (val) => {
    set('subject', val);
    if (val === 'coding') set('is_coding', true);
    else set('is_coding', false);
  };

  const handleSubmit = async () => {
    if (!form.student_name || !form.question || !form.answer) {
      setError('Please fill in student name, question, and answer.');
      return;
    }
    setError('');
    setLoading(true);
    setResult(null);
    try {
      const { data } = await gradeSubmission({ ...form, max_marks: Number(form.max_marks) });
      setResult(data);
    } catch (e) {
      setError(e.response?.data?.detail || 'Grading failed. Check your API key and backend.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grade-page">
      <div className="page-header">
        <h1>Grade a Submission</h1>
        <p className="subtitle">Paste student's answer — AI will grade + check plagiarism instantly.</p>
      </div>

      <div className="grade-layout">
        <div className="form-card card">
          <div className="form-row">
            <div className="field">
              <label>Student Name</label>
              <input placeholder="e.g. Rahul Sharma" value={form.student_name}
                onChange={e => set('student_name', e.target.value)} />
            </div>
            <div className="field field-sm">
              <label>Subject</label>
              <select value={form.subject} onChange={e => handleSubjectChange(e.target.value)}>
                {SUBJECTS.map(s => <option key={s} value={s}>{s.charAt(0).toUpperCase() + s.slice(1)}</option>)}
              </select>
            </div>
            <div className="field field-sm">
              <label>Max Marks</label>
              <input type="number" min="1" max="100" value={form.max_marks}
                onChange={e => set('max_marks', e.target.value)} />
            </div>
          </div>

          <div className="coding-toggle">
            <label className="toggle-label">
              <input type="checkbox" checked={form.is_coding}
                onChange={e => set('is_coding', e.target.checked)} />
              <span className="toggle-track"><span className="toggle-thumb" /></span>
              <span>Code Submission <span className="optional">(evaluate as programming answer)</span></span>
            </label>
          </div>

          <div className="field">
            <label>{form.is_coding ? 'Problem Statement' : 'Question'}</label>
            <textarea rows={3} placeholder={form.is_coding ? 'Write a function to reverse a string...' : 'What is photosynthesis?'}
              value={form.question} onChange={e => set('question', e.target.value)} />
          </div>

          <div className="field">
            <label>{form.is_coding ? "Student's Code" : "Student's Answer"}</label>
            <textarea rows={6}
              placeholder={form.is_coding ? 'def reverse_string(s):\n    return s[::-1]' : 'Paste the student\'s written answer here...'}
              value={form.answer} onChange={e => set('answer', e.target.value)}
              style={form.is_coding ? { fontFamily: 'var(--mono)', fontSize: '13px' } : {}} />
          </div>

          <div className="field">
            <label>Rubric <span className="optional">(optional)</span></label>
            <textarea rows={2} placeholder="e.g. 3 marks for definition, 4 for process, 3 for examples"
              value={form.rubric} onChange={e => set('rubric', e.target.value)} />
          </div>

          {error && <div className="error-msg">{error}</div>}

          <button className="grade-btn" onClick={handleSubmit} disabled={loading}>
            {loading ? <span className="spinner" /> : '◈'} {loading ? 'Grading...' : 'Grade with AI'}
          </button>
        </div>

        {result && <GradeResult data={result} />}
      </div>
    </div>
  );
}

