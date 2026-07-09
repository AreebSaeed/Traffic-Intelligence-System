// Shared API helpers for the Traffic Intelligence frontend.

const API_BASE = "http://127.0.0.1:8000";

const LEVEL_COLORS = {
  Low: "#2ecc71",
  Medium: "#f5b041",
  High: "#e74c3c",
};

const LEVEL_EMOJI = {
  Low: "\u{1F7E2}",
  Medium: "\u{1F7E1}",
  High: "\u{1F534}",
};

async function apiGet(path) {
  const response = await fetch(`${API_BASE}${path}`);
  if (!response.ok) {
    throw new Error(`GET ${path} failed (${response.status})`);
  }
  return response.json();
}

async function apiPost(path, body) {
  const response = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!response.ok) {
    throw new Error(`POST ${path} failed (${response.status})`);
  }
  return response.json();
}

function parseGeometry(geometryText) {
  if (!geometryText) return null;
  try {
    return JSON.parse(geometryText);
  } catch {
    return null;
  }
}

function levelFromLabel(label) {
  if (!label) return null;
  const text = String(label);
  if (text.includes("High")) return "High";
  if (text.includes("Medium")) return "Medium";
  if (text.includes("Low")) return "Low";
  return null;
}

function formatNumber(value) {
  return Number(value).toLocaleString("en-US");
}
