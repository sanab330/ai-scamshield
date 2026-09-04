/**
 * API Service for AI ScamShield.
 * Communicates with the local FastAPI backend daemon.
 */

const API_BASE = '/api';

export async function scanMessage(text) {
  const response = await fetch(`${API_BASE}/scan/message`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({ detail: 'Scan request failed' }));
    throw new Error(err.detail || 'Failed to analyze message');
  }
  return response.json();
}

export async function scanUrl(url) {
  const response = await fetch(`${API_BASE}/scan/url`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url }),
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({ detail: 'URL scan failed' }));
    throw new Error(err.detail || 'Failed to inspect URL');
  }
  return response.json();
}

export async function scanConversation(conversationText) {
  const response = await fetch(`${API_BASE}/scan/conversation`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ conversation_text: conversationText }),
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({ detail: 'Conversation scan failed' }));
    throw new Error(err.detail || 'Failed to analyze conversation');
  }
  return response.json();
}

export async function scanPayment(paymentData) {
  const response = await fetch(`${API_BASE}/scan/payment`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(paymentData),
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({ detail: 'Payment scan failed' }));
    throw new Error(err.detail || 'Failed to analyze payment risk');
  }
  return response.json();
}

export async function scanProfile(profileData) {
  const response = await fetch(`${API_BASE}/scan/profile`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(profileData),
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({ detail: 'Profile scan failed' }));
    throw new Error(err.detail || 'Failed to analyze profile');
  }
  return response.json();
}

export async function getDashboardStats() {
  const response = await fetch(`${API_BASE}/stats/dashboard`);
  if (!response.ok) {
    throw new Error('Failed to fetch dashboard statistics');
  }
  return response.json();
}

export async function getHistory(limit = 50) {
  const response = await fetch(`${API_BASE}/history?limit=${limit}`);
  if (!response.ok) {
    throw new Error('Failed to fetch scan history');
  }
  return response.json();
}

export async function clearHistory() {
  const response = await fetch(`${API_BASE}/history`, {
    method: 'DELETE',
  });
  if (!response.ok) {
    throw new Error('Failed to clear history');
  }
  return response.json();
}

export async function sendFeedback(scanId, feedbackType, notes = '') {
  const response = await fetch(`${API_BASE}/feedback`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      scan_id: scanId,
      feedback_type: feedbackType,
      notes,
    }),
  });
  if (!response.ok) {
    throw new Error('Failed to submit feedback');
  }
  return response.json();
}
