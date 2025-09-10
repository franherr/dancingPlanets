function updateCanvasVisibility() {
  for (let i = 0; i < 4; ++i) {
    const checked = document.getElementById('toggle' + i).checked;
    const cell = document.getElementById('corresp' + i).parentElement;
    cell.style.display = checked ? '' : 'none';
  }
}
// Helper: drawKnotStrands (for torus knots)
function drawKnotStrands(a, b, color, ctx) {
  ctx.save();
  ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
  const w = ctx.canvas.width, h = ctx.canvas.height;
  ctx.strokeStyle = color;
  ctx.lineWidth = 1.2;
  ctx.globalAlpha = 0.8;
  // Draw the torus square
  ctx.strokeRect(w * 0.1, h * 0.1, w * 0.8, h * 0.8);
  // Draw strands
  for (let k = 0; k <= Math.max(Math.abs(a), Math.abs(b)); k++) {
    let x0, y0, x1, y1;
    if (a >= b) {
      x0 = w * (0.1 + 0.8 * (k / Math.abs(b)));
      y0 = h * 0.1;
      x1 = x0;
      y1 = h * 0.9;
    } else {
      x0 = w * 0.1;
      y0 = h * (0.1 + 0.8 * (k / Math.abs(a)));
      x1 = w * 0.9;
      y1 = y0;
    }
    ctx.beginPath();
    ctx.moveTo(x0, y0);
    ctx.lineTo(x1, y1);
    ctx.stroke();
  }
  ctx.restore();
}

// Helper: sampleKnot (draws points on torus knot)
function sampleKnot(a, b, m, color, ctx) {
  ctx.save();
  const w = ctx.canvas.width, h = ctx.canvas.height;
  ctx.fillStyle = color;
  for (let k = 0; k < m; k++) {
    const x = w * (0.1 + 0.8 * ((a * (k / m)) % 1));
    const y = h * (0.1 + 0.8 * ((b * (k / m)) % 1));
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
  const cx = ctx.canvas.width / 2, cy = ctx.canvas.height / 2, scale = Math.min(cx, cy) * 0.16; // further reduced scale for more zoom out
  ctx.translate(cx, cy);
  ctx.beginPath();
  let first = true;
  for (let t = 0; t <= range; t += 0.1) {
    const x = scale * (a * Math.cos(t) + b * Math.cos((a / b) * t));
    const y = scale * (a * Math.sin(t) + b * Math.sin((a / b) * t));
    if (first) { ctx.moveTo(x, y); first = false; }
    else { ctx.lineTo(x, y); }
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
