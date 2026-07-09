// Lightweight canvas charts (no external dependency).

function drawDonut(canvasId, data) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;

  const ctx = canvas.getContext("2d");
  const size = canvas.width;
  const center = size / 2;
  const outer = size / 2 - 6;
  const inner = outer * 0.62;

  ctx.clearRect(0, 0, size, size);

  const entries = Object.entries(data).filter(([, count]) => count > 0);
  const total = entries.reduce((sum, [, count]) => sum + count, 0);

  if (!total) {
    ctx.fillStyle = "#2b3d63";
    ctx.beginPath();
    ctx.arc(center, center, outer, 0, Math.PI * 2);
    ctx.arc(center, center, inner, 0, Math.PI * 2, true);
    ctx.fill();
    ctx.fillStyle = "#93a3c4";
    ctx.font = "12px Segoe UI";
    ctx.textAlign = "center";
    ctx.fillText("No data", center, center + 4);
    return;
  }

  let angle = -Math.PI / 2;
  for (const [level, count] of entries) {
    const slice = (count / total) * Math.PI * 2;
    ctx.beginPath();
    ctx.fillStyle = LEVEL_COLORS[level] || "#5d7290";
    ctx.moveTo(center, center);
    ctx.arc(center, center, outer, angle, angle + slice);
    ctx.closePath();
    ctx.fill();
    angle += slice;
  }

  // Punch the donut hole
  ctx.globalCompositeOperation = "destination-out";
  ctx.beginPath();
  ctx.arc(center, center, inner, 0, Math.PI * 2);
  ctx.fill();
  ctx.globalCompositeOperation = "source-over";

  ctx.fillStyle = "#e8edf7";
  ctx.font = "700 20px Segoe UI";
  ctx.textAlign = "center";
  ctx.fillText(formatNumber(total), center, center + 2);
  ctx.fillStyle = "#93a3c4";
  ctx.font = "11px Segoe UI";
  ctx.fillText("predictions", center, center + 18);
}

function renderLegend(elementId, data) {
  const element = document.getElementById(elementId);
  if (!element) return;

  const total = Object.values(data).reduce((sum, count) => sum + count, 0) || 1;
  element.innerHTML = ["Low", "Medium", "High"]
    .map((level) => {
      const count = data[level] || 0;
      const percent = Math.round((count / total) * 100);
      return (
        `<div><span class="dot" style="background:${LEVEL_COLORS[level]}"></span>` +
        `${LEVEL_EMOJI[level]} ${level} &middot; ${formatNumber(count)} (${percent}%)</div>`
      );
    })
    .join("");
}
