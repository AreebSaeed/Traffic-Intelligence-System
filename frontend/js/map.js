// Leaflet map helpers: draw roads colored by prediction, search & zoom.

const KARACHI_CENTER = [24.8607, 67.0011];

function createMap(elementId, zoom = 11) {
  const map = L.map(elementId, { zoomControl: true }).setView(KARACHI_CENTER, zoom);
  L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
    attribution: '&copy; OpenStreetMap contributors &copy; CARTO',
    maxZoom: 19,
  }).addTo(map);
  return map;
}

async function loadPredictionLookup(limit = 1000) {
  const lookup = {};
  try {
    const history = await apiGet(`/predictions/history?limit=${limit}`);
    for (const row of history) {
      if (!(row.road_id in lookup)) {
        lookup[row.road_id] = row.prediction;
      }
    }
  } catch (error) {
    console.warn("Could not load prediction history:", error);
  }
  return lookup;
}

function roadStyle(level) {
  return {
    color: LEVEL_COLORS[level] || "#5d7290",
    weight: level ? 3.5 : 2,
    opacity: level ? 0.95 : 0.55,
  };
}

function buildPopupHtml(road, level) {
  const color = LEVEL_COLORS[level] || "#5d7290";
  const badge = level
    ? `<span class="popup-badge" style="background:${color}22;color:${color}">` +
      `${LEVEL_EMOJI[level] || ""} ${level} Traffic</span>`
    : `<span class="popup-badge" style="background:#5d729022;color:#93a3c4">No prediction yet</span>`;

  return (
    `<div class="popup-title">${road.name}</div>` +
    `<div class="muted">Type: ${road.road_type || "n/a"} &middot; ID: ${road.road_id}</div>` +
    badge +
    `<br><button class="popup-btn" onclick="predictRoadFromPopup(${road.road_id}, this)">Predict now</button>`
  );
}

async function predictRoadFromPopup(roadId, button) {
  button.disabled = true;
  button.textContent = "Predicting...";
  try {
    const result = await apiGet(`/predict/${roadId}`);
    const level = levelFromLabel(result.prediction);
    const color = LEVEL_COLORS[level] || "#5d7290";
    button.outerHTML =
      `<span class="popup-badge" style="background:${color}22;color:${color}">` +
      `${LEVEL_EMOJI[level] || ""} ${result.prediction} (${Math.round(result.confidence * 100)}%)</span>`;
    if (window._roadLayers && window._roadLayers[roadId]) {
      window._roadLayers[roadId].setStyle(roadStyle(level));
    }
  } catch (error) {
    button.textContent = "Failed - retry";
    button.disabled = false;
  }
}

async function drawRoads(map, { limit = 600 } = {}) {
  const [roads, predictions] = await Promise.all([
    apiGet(`/roads?limit=${limit}`),
    loadPredictionLookup(),
  ]);

  window._roadLayers = window._roadLayers || {};
  const group = L.featureGroup();

  for (const road of roads) {
    const geometry = parseGeometry(road.geometry);
    if (!geometry) continue;

    const level = predictions[road.road_id] || null;
    const layer = L.geoJSON(geometry, { style: roadStyle(level) });
    layer.bindPopup(buildPopupHtml(road, level));
    layer.addTo(group);
    window._roadLayers[road.road_id] = layer;
  }

  group.addTo(map);
  return { roadCount: roads.length, predictions };
}

async function searchAndZoom(map, name, highlightLayerRef) {
  const results = await apiGet(`/roads/search?name=${encodeURIComponent(name)}&limit=10`);
  if (!results.length) return null;

  const road = results[0];
  const geometry = parseGeometry(road.geometry);
  if (!geometry) return road;

  if (highlightLayerRef.layer) {
    map.removeLayer(highlightLayerRef.layer);
  }

  const highlight = L.geoJSON(geometry, {
    style: { color: "#38bdf8", weight: 6, opacity: 1 },
  }).addTo(map);
  highlight.bindPopup(buildPopupHtml(road, null)).openPopup();
  highlightLayerRef.layer = highlight;

  map.fitBounds(highlight.getBounds(), { maxZoom: 16, padding: [40, 40] });
  return road;
}
