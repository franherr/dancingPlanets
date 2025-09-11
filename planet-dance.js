function updateCanvasVisibility() {
  for (let i = 0; i < 4; ++i) {
    const checked = document.getElementById('toggle' + i).checked;
    const cell = document.getElementById('corresp' + i).parentElement;
    cell.style.display = checked ? '' : 'none';
  }
}

function drawKnotStrands(a, b, color, ctx) {
  ctx.save();
  //ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);

  const w = ctx.canvas.width;
  const h = ctx.canvas.height;

  ctx.lineWidth = 1.2;
  ctx.globalAlpha = 0.8;

  ctx.strokeStyle = 'black';
  // Draw the unit square
  const px = x => w * (0.1 + 0.8 * x);
  const py = y => h * (0.1 + 0.8 * (1 - y));  // Flip Y for canvas

  ctx.strokeRect(px(0), py(1), px(1) - px(0), py(0) - py(1));

  const slope = b / a;

 const drawLine = (x0, y0) => {
  const slope = b / a;
  const points = [];

  const addPoint = (x, y) => {
    // Check if already included (avoid duplicate corner points)
    for (const p of points) {
      if (Math.abs(p.x - x) < 1e-10 && Math.abs(p.y - y) < 1e-10) return;
    }
    if (x >= 0 && x <= 1 && y >= 0 && y <= 1) {
      points.push({ x, y });
    }
  };

  // Intersections with all 4 sides
  addPoint(0, slope * (0 - x0) + y0);       // Left
  addPoint(1, slope * (1 - x0) + y0);       // Right

  if (slope !== 0) {
    addPoint((0 - y0) / slope + x0, 0);     // Bottom
    addPoint((1 - y0) / slope + x0, 1);     // Top
  }

  if (points.length >= 2) {
    const [p1, p2] = points;
    ctx.beginPath();
    ctx.moveTo(px(p1.x), py(p1.y));
    ctx.lineTo(px(p2.x), py(p2.y));
    ctx.stroke();
  }
};

  ctx.strokeStyle = color;
  // Vertical edges: x = 0 and x = 1
  for (let k = 0; k <= Math.max(Math.abs(a), Math.abs(b)); k++) {
    const x = k / Math.abs(b);
    const y = k / Math.abs(a);
    if (x <= 1) {
      drawLine(x, 0);  // bottom edge
      drawLine(x, 1);  // top edge
    }
    if (y <= 1) {
      drawLine(0, y);  // left edge
      drawLine(1, y);  // right edge
    }
  }

  ctx.restore();
}

// Helper: sampleKnot (draws points on torus knot)
function sampleKnot(a, b, m, color, ctx) {
  ctx.save();
  const w = ctx.canvas.width, h = ctx.canvas.height;
  const px = x => w * (0.1 + 0.8 * x);
  const py = y => h * (0.1 + 0.8 * (1 - y));  // Flip Y for canvas
  ctx.fillStyle = color;
  for (let k = 0; k < m; k++) {
    const x = px((a * (k / m)) % 1);
    const y = py((b * (k / m)) % 1);
    ctx.beginPath();
    ctx.arc(x, y, 2, 0, 2 * Math.PI);
    ctx.fill();
  }
  ctx.restore();
}

// Port of drawCorrespondence
function drawCorrespondence(alpha, beta, mult) {
  const d = gcd(alpha, beta);
  const a = alpha / d;
  const b = beta / d;
  const sam = Math.abs(alpha * mult - beta);
  // 0: Planet Dance (upper left)
  const ctx0 = document.getElementById('corresp0').getContext('2d');
  planetDance(a, b, ctx0);
  // 1: Linear Loops on Torus (upper right)
  const ctx1 = document.getElementById('corresp1').getContext('2d');
  ctx1.clearRect(0, 0, ctx1.canvas.width, ctx1.canvas.height);
  drawKnotStrands(a, b, COLORS[0], ctx1);
  drawKnotStrands(1, mult, COLORS[2], ctx1);
  sampleKnot(1, mult, sam, '#000', ctx1);
  // 2: Epicycloid (lower right)
  const ctx2 = document.getElementById('corresp2').getContext('2d');
  plotEpicycloid(ctx2, a, b, PERIOD);
  // 3: Modular Multiplication Table (lower left)
  const ctx3 = document.getElementById('corresp3').getContext('2d');
  drawMMT(sam, mult, ctx3);
}
// Generate chords for modular multiplication table
function generateModChords(mod, mult) {
  // This is equivalent to generatePlanetDanceChords(1, mult, mod)
  const chords = [];
  for (let i = 0; i < mod; i++) {
    chords.push([
      (2 * Math.PI * i) / mod,
      (2 * Math.PI * (mult * i % mod)) / mod
    ]);
  }
  return chords;
}

function drawMMT(m, a, ctx) {
  drawChords(ctx, generateModChords(m, a), false, true);
}
// planet-dance.js
// Port of danceAndEpicycloid from Python to JavaScript for browser canvas

const PERIOD = 20 * Math.PI;
const COLORS = ['#227c9d', '#17c3b2', '#c67b35', '#a877ba', '#ffcb77', '#47865b', '#fe6d73'];

function gcd(a, b) {
  a = Math.abs(a); b = Math.abs(b);
  while (b) { [a, b] = [b, a % b]; }
  return a;
}

function generatePlanetDanceChords(a, b, m) {
  const chords = [];
  for (let i = 0; i < m; i++) {
    chords.push([
      (2 * Math.PI * a * i) / m,
      (2 * Math.PI * b * i) / m
    ]);
  }
  return chords;
}

function drawChords(ctx, chords, extended = false, circle = true) {
  ctx.save();
  ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
  const cx = ctx.canvas.width / 2, cy = ctx.canvas.height / 2, r = Math.min(cx, cy) * 0.9;
  ctx.translate(cx, cy);
  ctx.lineWidth = 0.7;
  ctx.globalAlpha = chords.length > 800 ? 0.05 : 1;
  if (circle) {
    ctx.beginPath();
    ctx.arc(0, 0, r, 0, 2 * Math.PI);
    ctx.strokeStyle = '#222';
    ctx.lineWidth = 1;
    ctx.globalAlpha = 0.5;
    ctx.stroke();
    ctx.globalAlpha = chords.length > 800 ? 0.05 : 1;
  }
  ctx.strokeStyle = '#222';
  for (const [a1, a2] of chords) {
    if (Math.abs(((a1 / (2 * Math.PI)) % 1) - ((a2 / (2 * Math.PI)) % 1)) > 1e-8) {
      ctx.beginPath();
      ctx.moveTo(r * Math.cos(a1), r * Math.sin(a1));
      ctx.lineTo(r * Math.cos(a2), r * Math.sin(a2));
      ctx.stroke();
    }
  }
  ctx.restore();
}

function plotEpicycloid(ctx, a, b, range) {
  ctx.save();
  ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
  const w = ctx.canvas.width;
  const h = ctx.canvas.height;
  // Center and scale
  const cx = w / 2;
  const cy = h / 2;
  const scale = 0.4 * Math.min(w, h);  // adjust zoom here
  ctx.beginPath();
  let first = true;
  const sample = Math.min(Math.abs(a/b), Math.abs(b/a));
  for (let t = 0; t <= range; t += 0.1*sample) {
    const x = (1/(a+b)) * (a * Math.cos(b*t) + b * Math.cos(a* t));
    const y = (1/(a+b)) * (a * Math.sin(b*t) + b * Math.sin(a * t));

    const canvasX = cx + scale * x;
    const canvasY = cy - scale * y; // Flip Y so positive is up
    if (first) {
      ctx.moveTo(canvasX, canvasY);
      first = false;
    } else {
      ctx.lineTo(canvasX, canvasY);
    }
  }
  ctx.strokeStyle = COLORS[3];
  ctx.lineWidth = 2;
  ctx.globalAlpha = 0.9;
  ctx.stroke();
  ctx.restore();
}

function planetDance(a, b, ctx) {
  const extended = a * b < 0;
  drawChords(ctx, generatePlanetDanceChords(a, b, 3000), extended, true);
}

function danceAndEpicycloid(alpha, beta) {
  const d = gcd(alpha, beta);
  const a = alpha / d;
  const b = beta / d;
  const ctx1 = document.getElementById('planetDance').getContext('2d');
  const ctx2 = document.getElementById('epicycloid').getContext('2d');
  planetDance(a, b, ctx1);
  plotEpicycloid(ctx2, a, b, PERIOD);
}

// Example usage:

function updateSamDisplay(alpha, beta, mult) {
  const sam = Math.abs(alpha * mult - beta);
  document.getElementById('samValue').textContent = sam;
  return sam;
}

function getInputsAndDraw() {
  const alpha = parseInt(document.getElementById('alphaInput').value, 10);
  const beta = parseInt(document.getElementById('betaInput').value, 10);
  const mult = parseInt(document.getElementById('multInput').value, 10);
  updateSamDisplay(alpha, beta, mult);
  drawCorrespondence(alpha, beta, mult);
}

document.addEventListener('DOMContentLoaded', () => {
  // Set initial sam value and draw
  getInputsAndDraw();
  // Add event listeners for parameters
  document.getElementById('alphaInput').addEventListener('input', getInputsAndDraw);
  document.getElementById('betaInput').addEventListener('input', getInputsAndDraw);
  document.getElementById('multInput').addEventListener('input', getInputsAndDraw);
  // Add event listeners for checkboxes
  for (let i = 0; i < 4; ++i) {
    document.getElementById('toggle' + i).addEventListener('change', updateCanvasVisibility);
  }
  updateCanvasVisibility();
});
