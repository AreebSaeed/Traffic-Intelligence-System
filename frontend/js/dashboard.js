// Home dashboard: stats cards, weather panel, traffic summary, map, search.

let dashboardMap = null;
const highlightRef = { layer: null };

async function loadStats() {
  try {
    const stats = await apiGet("/stats");
    document.getElementById("stat-roads").textContent = formatNumber(stats.total_roads);
    document.getElementById("stat-predictions").textContent = formatNumber(stats.predictions_today);
    document.getElementById("stat-speed").textContent = `${stats.average_speed} km/h`;

    drawDonut("traffic-donut", stats.traffic_distribution || {});
    renderLegend("traffic-legend", stats.traffic_distribution || {});
  } catch (error) {
    console.warn("Stats failed:", error);
  }
}

async function loadWeather() {
  try {
    const weather = await apiGet("/weather/current");
    document.getElementById("stat-weather").textContent = `${weather.temperature}\u00B0C`;
    document.getElementById("weather-temp").textContent = `${weather.temperature}\u00B0C`;
    document.getElementById("weather-humidity").textContent = `${weather.humidity}%`;
    document.getElementById("weather-rain").textContent = `${weather.rain} mm`;
    document.getElementById("weather-wind").textContent = `${weather.wind_speed} km/h`;
  } catch (error) {
    console.warn("Weather failed:", error);
  }
}

async function initDashboardMap() {
  dashboardMap = createMap("dashboard-map", 11);
  try {
    await drawRoads(dashboardMap, { limit: 500 });
  } catch (error) {
    console.warn("Road drawing failed:", error);
  }
}

function wireMapSearch() {
  const form = document.getElementById("map-search-form");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const query = document.getElementById("map-search-input").value.trim();
    if (!query) return;
    const road = await searchAndZoom(dashboardMap, query, highlightRef);
    if (!road) alert("No road found for that name.");
  });
}

function wireQuickPredict() {
  const form = document.getElementById("quick-search-form");
  const resultsBox = document.getElementById("quick-search-results");
  const resultPanel = document.getElementById("quick-predict-result");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const query = document.getElementById("quick-search-input").value.trim();
    if (!query) return;

    resultsBox.innerHTML = "<span class='muted'>Searching...</span>";
    try {
      const roads = await apiGet(`/roads/search?name=${encodeURIComponent(query)}&limit=6`);
      if (!roads.length) {
        resultsBox.innerHTML = "<span class='muted'>No roads found.</span>";
        return;
      }

      const seen = new Set();
      resultsBox.innerHTML = "";
      for (const road of roads) {
        if (seen.has(road.road_id)) continue;
        seen.add(road.road_id);

        const button = document.createElement("button");
        button.textContent = `${road.name} (#${road.road_id})`;
        button.addEventListener("click", () => predictQuick(road, resultPanel));
        resultsBox.appendChild(button);
      }
    } catch (error) {
      resultsBox.innerHTML = "<span class='error-text'>Search failed. Is the API running?</span>";
    }
  });
}

async function predictQuick(road, panel) {
  panel.classList.add("visible");
  panel.innerHTML = `<span class="muted">Predicting traffic for ${road.name}...</span>`;
  try {
    const result = await apiGet(`/predict/${road.road_id}`);
    const level = levelFromLabel(result.prediction);
    const cls = (level || "medium").toLowerCase();
    panel.innerHTML =
      `<div style="font-weight:700;margin-bottom:6px">${result.road_name}</div>` +
      `<span class="badge ${cls}">${LEVEL_EMOJI[level] || ""} ${result.prediction}</span>` +
      `<div class="muted" style="margin-top:8px">Confidence ${(result.confidence * 100).toFixed(1)}% &middot; ${result.updated_at}</div>`;
    loadStats();
  } catch (error) {
    panel.innerHTML = "<span class='error-text'>Prediction failed.</span>";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  loadStats();
  loadWeather();
  initDashboardMap();
  wireMapSearch();
  wireQuickPredict();
});
