// Manual prediction form: builds a request for POST /predict-manual.

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("prediction-form");
  const resultPanel = document.getElementById("prediction-result");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const payload = {
      road_type: document.getElementById("input-road-type").value,
      length: parseFloat(document.getElementById("input-length").value) || 0,
      lanes: parseFloat(document.getElementById("input-lanes").value) || 0,
      maxspeed: parseFloat(document.getElementById("input-speed").value) || 0,
      temperature: parseFloat(document.getElementById("input-temperature").value) || 0,
      humidity: parseFloat(document.getElementById("input-humidity").value) || 0,
      rain: parseFloat(document.getElementById("input-rain").value) || 0,
      hour: parseInt(document.getElementById("input-hour").value, 10) || 0,
    };

    resultPanel.classList.add("visible");
    resultPanel.innerHTML = "<span class='muted'>Running the model...</span>";

    try {
      const result = await apiPost("/predict-manual", payload);
      const level = result.prediction;
      const cls = (level || "medium").toLowerCase();
      const percent = (result.confidence * 100).toFixed(1);

      resultPanel.innerHTML =
        `<div class="result-emoji">${LEVEL_EMOJI[level] || ""}</div>` +
        `<div class="result-label ${cls}">${result.label}</div>` +
        `<div class="confidence-track"><div class="confidence-fill ${cls}" style="width:${percent}%"></div></div>` +
        `<div class="muted">Model confidence: ${percent}%</div>`;
    } catch (error) {
      resultPanel.innerHTML =
        "<span class='error-text'>Prediction failed. Make sure the backend is running on port 8000.</span>";
    }
  });
});
